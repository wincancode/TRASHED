package main

import (
	pb "Trashed/proto"
	"log"
	"net"
	"sync"

	"google.golang.org/grpc"
)

type server struct{
	pb.UnimplementedGameServiceServer
}

const (
	// Define the colors available for players
	Red    = "red"
	Green  = "green"
	Blue   = "blue"
	Yellow = "yellow"
)

var  (
	players []*pb.PlayerData
	JoinUpdatesChanels [] chan *pb.PlayerData
	joinUpdatesChanel = make(chan *pb.PlayerData, 1)
) 


func addPlayer(in *pb.PlayerData) {
	// Add the player to the list of clients
	for i:= range players {
		if players[i].PlayerUuid == in.PlayerUuid {
			log.Printf("Player %s already exists", in.PlayerUuid)
			return
		}
	}

	//add color and slot
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

func (s *server) JoinGame(in *pb.PlayerData, stream pb.GameService_JoinGameServer) error {
	var mu sync.Mutex


	
	// Add the player to the list of clients
	mu.Lock()
	addPlayer(in)
	//create a new channel for the player
	joinUpdatesChanel := make(chan *pb.PlayerData, 1)
	JoinUpdatesChanels = append(JoinUpdatesChanels, joinUpdatesChanel)
	mu.Unlock()




	mu.Lock()
	// Send the player data to all clients
	for _,subscriber := range JoinUpdatesChanels {
		subscriber <- in
	}
	mu.Unlock()





	for {
        select {
        case player := <-joinUpdatesChanel:
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
	pb.RegisterGameServiceServer(s, &server{})

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