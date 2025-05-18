package main

import (
	"Trashed/Trashed/gameLogic"
	"Trashed/Trashed/proto"
	"context"
	"fmt"
	"log"
	"math/rand"
	"net"
	"sync"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/reflection"
)

type server struct {
	proto.UnimplementedGameServiceServer
	mu    sync.Mutex
	games map[string]game
}

type game struct {
	Data *proto.GameData
	SubscribedInputStreams map[string]proto.GameService_JoinInputUpdatesServer 
	states *proto.GameState
	LatestInputs map[string]*proto.Input // Store latest input per player
}

func NewServer() *server {
	return &server{
		games: make(map[string]game),
	}
}

const (
	// Define the colors available for players
	Red    = "red"
	Green  = "green"
	Blue   = "blue"
	Yellow = "yellow"
)


func generateGameCode() string {
	rand.Seed(time.Now().UnixNano())
	const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	code := make([]byte, 6)
	for i := range code {
		code[i] = charset[rand.Intn(len(charset))]
	}


	//!!!!!!!!!!!!!!!!!!!!
	code = []byte("2")
	return string(code)
}

func (s *server) CreateGame(ctx context.Context, in *proto.Empty) (*proto.GameCode, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Generar un código único para la partida
	gameCode := generateGameCode()
	s.games[gameCode] = game{
		Data: &proto.GameData{
			Code:    gameCode,
			Players: []*proto.PlayerData{},
			Started: false,
		},
		SubscribedInputStreams: make(map[string]proto.GameService_JoinInputUpdatesServer),
	}

	log.Printf("Game created with code: %s", gameCode)
	return &proto.GameCode{Code: gameCode}, nil
}


func (s *server) JoinGame(in *proto.PlayerData, stream proto.GameService_JoinGameServer) error {
	gameCode := in.GameCode

	// Verificar si la partida existe
	s.mu.Lock()
	game, exists := s.games[gameCode]
	if !exists {
		s.mu.Unlock()
		log.Printf("Partida no encontrada: %s", gameCode)
		return fmt.Errorf("partida no encontrada")
	}

	//search for a color that is not used
	usedColors := make(map[string]bool)

	for _, player := range game.Data.Players {
		usedColors[player.Color] = true
	}

	availableColors := []string{Red, Green, Blue, Yellow}
	
	var selectedColor string
	
	for _, color := range availableColors {
		if !usedColors[color] {
			selectedColor = color
			break
		}
	}

	// Agregar el jugador a la partida
	player := &proto.PlayerData{
		PlayerUuid: in.PlayerUuid,
		Username:   in.Username,
		Color:      selectedColor,
		Slot:       int32(len(game.Data.Players)),
		GameCode:   gameCode,
	}
	game.Data.Players = append(game.Data.Players, player)
	s.mu.Unlock()

	log.Printf("Nuevo jugador agregado: %s, username: %s, slot: %d", player.PlayerUuid, player.Username, player.Slot)

	// Enviar actualizaciones de la lista de jugadores conectados
	for {
		s.mu.Lock()
		gameData := &proto.GameData{
			Code:    gameCode,
			Players: game.Data.Players,
			Started: game.Data.Started,
		}
		s.mu.Unlock()

		if err := stream.Send(gameData); err != nil {
			log.Printf("Error enviando datos de la partida: %v", err)
			return err
		}	

		time.Sleep(1 * time.Second) // Enviar actualizaciones cada segundo
	}
}


func (s *server) StartGame(ctx context.Context, in *proto.GameCode) (*proto.BoolMessage,error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	gameCode := in.Code
	game, exists := s.games[gameCode]
	if !exists {
		log.Printf("Partida no encontrada: %s", gameCode)
		return &proto.BoolMessage{Value: false}, fmt.Errorf("partida no encontrada")
	}

	//inicializar estados del juego
	PlayerStates := make(map[string]*proto.PlayerState)
	for _, player := range game.Data.Players {
		PlayerStates[player.PlayerUuid] = &proto.PlayerState{
			Code: gameCode,
			PlayerUuid: player.PlayerUuid,
			Timestamp: time.Now().Unix(),
			Position: &proto.Position{
				X: 800/2,
				Y: 600/2,
				Angle: 360,
				SpeedX: 0,
				SpeedY: 0,
				AccelerationX: 0,
				AccelerationY: 0,
			},
		}
	}
	game.states = &proto.GameState{
		PlayerStates: PlayerStates,
	}
	// Initialize LatestInputs map
	game.LatestInputs = make(map[string]*proto.Input)
	s.games[gameCode] = game

	// Marcar la partida como iniciada
	game.Data.Started = true

	// Start the fixed-tick game loop
	go s.runGameLoop(gameCode)

	log.Printf("Partida iniciada: %s", gameCode)
	return &proto.BoolMessage{Value: true}, nil;
}

// Fixed-tick game loop for each game
func (s *server) runGameLoop(gameCode string) {
	ticker := time.NewTicker(time.Second / 60) // 60 FPS
	defer ticker.Stop()
	var lastTick = time.Now()
	for {
		<-ticker.C
		deltaTime := time.Since(lastTick).Seconds()
		lastTick = time.Now()
		s.mu.Lock()
		game, exists := s.games[gameCode]
		if !exists || !game.Data.Started {
			s.mu.Unlock()
			return
		}
		for playerID, playerState := range game.states.PlayerStates {
			input := game.LatestInputs[playerID]
			if input == nil {
				input = &proto.Input{} // default input if none received
			}
			position := playerState.Position
			new_state := gameLogic.UpdateShipPosition(position, input, deltaTime)
			playerState.Position = new_state
			playerState.Timestamp = time.Now().Unix()
		}
		// Broadcast updated state to all subscribed players
		for _, subStream := range game.SubscribedInputStreams {
			err := subStream.Send(game.states)
			if err != nil {
				log.Printf("Error sending state to player: %v", err)
			}
		}
		s.games[gameCode] = game
		s.mu.Unlock()
	}
}




func (s *server) JoinInputUpdates(stream proto.GameService_JoinInputUpdatesServer) error {
	md,ok := metadata.FromIncomingContext(stream.Context())
	if !ok {
		return fmt.Errorf("metadata not found")
	}
	gameCode := md.Get("game_code")
	playerUuid := md.Get("player_uuid")
	if len(playerUuid) == 0 {
		return fmt.Errorf("player uuid not found")
	}
	if len(gameCode) == 0 {
		return fmt.Errorf("game code not found")
	}
	gameCodeStr := gameCode[0]
	playerUuidStr := playerUuid[0]
	log.Printf("Player UUID: %s, Game Code: %s", playerUuidStr, gameCodeStr)
	// Subscribe the player to input updates
	s.mu.Lock()
	game, exists := s.games[gameCodeStr]
	if !exists {
		s.mu.Unlock()
		log.Printf("Partida no encontrada: %s", gameCodeStr)
		return fmt.Errorf("partida no encontrada")
	}
	if _, exists := game.SubscribedInputStreams[playerUuidStr]; exists {
		s.mu.Unlock()
		log.Printf("Player already subscribed: %s", playerUuidStr)
		return fmt.Errorf("player already subscribed")
	}
	game.SubscribedInputStreams[playerUuidStr] = stream
	s.games[gameCodeStr] = game
	s.mu.Unlock()
	log.Printf("Player subscribed to input updates: %s", playerUuidStr)
	// Only store latest input per player
	for {
		in, err := stream.Recv()
		if err != nil {
			return err
		}
		s.mu.Lock()
		game, exists := s.games[gameCodeStr]
		if exists {
			game.LatestInputs[in.PlayerUuid] = in.Input
			s.games[gameCodeStr] = game
		}
		s.mu.Unlock()
	}
}


func main() {
	// Create a new gRPC server
	s := grpc.NewServer()
	proto.RegisterGameServiceServer(s, NewServer())

	reflection.Register(s)

	// Listen on port 50051
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	log.Println("Server is running on port 50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
