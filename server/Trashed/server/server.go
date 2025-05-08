package main

import (
	"Trashed/proto"
	"context"
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
	games map[string]*proto.GameData
}

func NewServer() *server {
	return &server{
		games: make(map[string]*proto.GameData),
	}
}

const (
	// Define the colors available for players
	Red    = "red"
	Green  = "green"
	Blue   = "blue"
	Yellow = "yellow"
)

var (
	players             []*proto.PlayerData
	JoinUpdatesChannels []chan *proto.PlayerData
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
	s.games[gameCode] = &proto.GameData{
		Code:    gameCode,
		Players: []*proto.PlayerData{},
	}

	log.Printf("Game created with code: %s", gameCode)
	return &proto.GameCode{Code: gameCode}, nil
}

func addPlayer(in *proto.PlayerData) {
	// Add the player to the list of clients
	for i := range players {
		if players[i].PlayerUuid == in.PlayerUuid {
			log.Printf("Player %s already exists", in.PlayerUuid)
			return
		}
	}

	// Add color and slot
	players = append(players, in)

	in.Slot = int32(len(players) - 1)

	switch len(players) % 3 {
	case 0:
		in.Color = Red
	case 1:
		in.Color = Green
	case 2:
		in.Color = Blue
	}

	log.Printf("New player added: %s, color %s, slot %d", in.PlayerUuid, in.Color, in.Slot)
}

func (s *server) JoinGame(in *proto.PlayerData, stream proto.GameService_JoinGameServer) error {
	var mu sync.Mutex

	// Add the player to the list of clients
	mu.Lock()
	addPlayer(in)
	// Create a new channel for the player
	joinUpdatesChannel := make(chan *proto.PlayerData, 1)
	JoinUpdatesChannels = append(JoinUpdatesChannels, joinUpdatesChannel)
	mu.Unlock()

	mu.Lock()
	// Send the player data to all clients
	for _, subscriber := range JoinUpdatesChannels {
		subscriber <- in
	}
	mu.Unlock()

	for {
		select {
		case player := <-joinUpdatesChannel:
			// Send the player data to the client
			err := stream.Send(player)
			if err != nil {
				log.Printf("Error sending player data to %s: %v", in.PlayerUuid, err)
				return err
			}
		default:
			// Optionally, send a heartbeat or perform other checks
			err := stream.Context().Err()
			if err != nil {
				log.Printf("Connection lost for player %s: %v", in.PlayerUuid, err)
				return err
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
