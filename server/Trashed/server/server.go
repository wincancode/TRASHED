package main

import (
	"Trashed/proto"
	"context"
	"fmt"
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
	gameCode := in.GameCode

	// Verificar si la partida existe
	s.mu.Lock()
	game, exists := s.games[gameCode]
	if !exists {
		s.mu.Unlock()
		log.Printf("Partida no encontrada: %s", gameCode)
		return fmt.Errorf("Partida no encontrada")
	}

	// Agregar el jugador a la partida
	player := &proto.PlayerData{
		PlayerUuid: in.PlayerUuid,
		Username:   in.Username,
		Color:      "green",
		Slot:       int32(len(game.Players)),
		GameCode:   gameCode,
	}
	game.Players = append(game.Players, player)
	s.mu.Unlock()

	log.Printf("Nuevo jugador agregado: %s, username: %s, slot: %d", player.PlayerUuid, player.Username, player.Slot)

	// Enviar actualizaciones de la lista de jugadores conectados
	for {
		s.mu.Lock()
		gameData := &proto.GameData{
			Code:    gameCode,
			Players: game.Players,
		}
		s.mu.Unlock()

		if err := stream.Send(gameData); err != nil {
			log.Printf("Error enviando datos de la partida: %v", err)
			return err
		}

		time.Sleep(1 * time.Second) // Enviar actualizaciones cada segundo
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
