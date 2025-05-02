import grpc
import service_pb2
import service_pb2_grpc

def run():

    #read the id and name of the player from the command line
    player_id = input("Enter your player ID: ")
    player_name = input("Enter your player name: ")


    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        # Call JoinGame and handle the streaming response
        responses = stub.JoinGame(service_pb2.PlayerData(
            player_uuid=player_id,
            timestamp=1234567890,
            username=player_name,
        ))
        try:
            for response in responses:
                print(f"Received update: {response}")
        except grpc.RpcError as e:
            print(f"Stream closed with error: {e}")

if __name__ == "__main__":
    run()