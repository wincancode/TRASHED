
import grpc
import server.service_pb2 as service_pb2
import server.service_pb2_grpc as service_pb2_grpc



def request_game_code_from_server():
    """Request a game code from the server."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        try:
            response = stub.CreateGame(service_pb2.Empty())
            return response.code
        except grpc.RpcError as e:
            print(f"Failed to create game: {e}")
            return None