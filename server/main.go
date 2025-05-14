package main

import (
	"log"
	"sync"

	pb "grpc-server-project/proto"
	"net"

	"google.golang.org/grpc"
)

type server struct {
    pb.UnimplementedGreeterServer
}

var clients []pb.Greeter_ChatServer

// Chat implements the bidirectional streaming for live chat
func (s *server) Chat(stream pb.Greeter_ChatServer) error {
    log.Println("Chat started")
    var mu sync.Mutex

    for {
        // Receive a message from the client
        in, err := stream.Recv()
        if err != nil {
            log.Printf("Error receiving message: %v", err)
            return err
        }

		// Add the client to the list of clients
		mu.Lock()
		// Check if the client is already in the list
		var found bool
		for _, client := range clients {
			if client == stream {
				found = true
				break				
			}	
		}
		if !found {
			clients = append(clients, stream)
			log.Printf("New client added: %s", in.Sender)
		}
		mu.Unlock()


        log.Printf("Received from %s: %s", in.Sender, in.Message)

        // Send a the message back to all clients except the sender
        mu.Lock()
		
		// Send the message to all clients
		for _, client := range clients {
			if client != stream {
				err := client.Send(&pb.Greeting{
					Sender:  in.Sender,
					Message: in.Message,
				})
				if err != nil {
					log.Printf("Error sending message to %s: %v", in.Sender, err)
			}
		}}
        mu.Unlock()

    
    }
}



func main() {
    listener, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("Failed to listen: %v", err)
    }

    grpcServer := grpc.NewServer()
    pb.RegisterGreeterServer(grpcServer, &server{})

    log.Println("Server is listening on port 50051")

    if err := grpcServer.Serve(listener); err != nil {
        log.Fatalf("Failed to serve: %v", err)
    }
}