package main

import (
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

	// Agregar el jugador a la partida
	player := &proto.PlayerData{
		PlayerUuid: in.PlayerUuid,
		Username:   in.Username,
		Color:      "green",
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

	// Marcar la partida como iniciada
	game.Data.Started = true
	
	log.Printf("Partida iniciada: %s", gameCode)
	return &proto.BoolMessage{Value: true}, nil;
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


	s.mu.Lock()
	game, exists := s.games[gameCodeStr]

	if !exists {
		s.mu.Unlock()
		log.Printf("Partida no encontrada: %s", gameCodeStr)
		return fmt.Errorf("partida no encontrada")
	}

	// Check if the player is already subscribed
	if _, exists := game.SubscribedInputStreams[playerUuidStr]; exists {
		s.mu.Unlock()
		log.Printf("Player already subscribed: %s", playerUuidStr)
		return fmt.Errorf("player already subscribed")
	}

	// Subscribe the player to input updates
	game.SubscribedInputStreams[playerUuidStr] = stream
	s.mu.Unlock()
	log.Printf("Player subscribed to input updates: %s", playerUuidStr)

	for {
        in, err := stream.Recv()
        if err != nil {
            return err
        }
        log.Printf("Received: %v", in)
        // Echo back the input to all subscribed players
        for _, subStream := range game.SubscribedInputStreams {
			err := subStream.Send(in)
			if err != nil {
				log.Printf("Error sending input to player: %v", err)
			}
		}

		
				


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
