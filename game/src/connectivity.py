
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
        
def connect_to_server(player_id, player_name, game_code, update_players_callback):
    """Connect to the server and handle the JoinGame response."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        try:
            # Llamar a JoinGame y manejar la respuesta en streaming
            print(f"Enviando datos al servidor: player_id={player_id}, player_name={player_name}, game_code={game_code}")
            responses = stub.JoinGame(service_pb2.PlayerData(
                player_uuid=player_id,
                username=player_name,
                game_code=game_code,
            ))
            for response in responses:
                print(f"Received response: {response}")
                # Pasar la lista de jugadores al callback
                update_players_callback(response.players)
        except grpc.RpcError as e:
            print(f"Stream closed with error: {e}")