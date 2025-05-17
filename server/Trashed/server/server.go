package main

import (
	"Trashed/Trashed/proto"
	"context"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net"
	"sync"
	"time"

	"google.golang.org/grpc"
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






func (s *server) JoinInputUpdates(stream proto.GameService_JoinInputUpdatesServer) (error) {
	//manejar datos de entrada
	for{
		in,err := stream.Recv()


		//manage errors
		if err == io.EOF {
			log.Println("Stream closed by client")
			return nil
		}

		if err != nil {
			log.Printf("Error receiving input: %v", err)
			return err
		}


		// Check if the game exists
		s.mu.Lock()
		game, exists := s.games[in.Code]
		if !exists {
			s.mu.Unlock()
			log.Printf("Game not found: %s", in.Code)
			return fmt.Errorf("game not found")
		}

		//if exist, verify if the user is in the subscriber list 
				
		// Add the subscriber if not already present
		if _, ok := game.SubscribedInputStreams[in.Player.PlayerUuid]; !ok {
			game.SubscribedInputStreams[in.Player.PlayerUuid] = stream
			log.Printf("Added subscriber: %s", in.Player.PlayerUuid)
		}

		s.mu.Unlock()

		log.Printf("Received input in game %s, for player %s: %v", in.Code, in.Player.PlayerUuid, in.Input)

		for playerUUID, sub_stream := range game.SubscribedInputStreams {
			// playerUUID is the key (string)
			// stream is the value (proto.GameService_JoinInputUpdatesServer)
			log.Printf("sending to subscriber: %s", playerUUID)
			sub_stream.Send(in)
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
