
import threading
from time import time
import grpc
import player
import server.service_pb2 as service_pb2
import server.service_pb2_grpc as service_pb2_grpc

DIRECTION = "localhost:50051"


def request_game_code_from_server():
    """Request a game code from the server."""
    with grpc.insecure_channel(DIRECTION) as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        try:
            response = stub.CreateGame(service_pb2.Empty())
            return response.code
        except grpc.RpcError as e:
            print(f"Failed to create game: {e}")
            return None
        
 #!!!!!!!_?! DELETE< JUST TEST
def get_input_updates(stream,channel):
    for message in stream:
        print(message)


def connect_to_server(player_id, player_name, game_code, update_players_callback):
    """Connect to the server and handle the JoinGame response."""
    with grpc.insecure_channel(DIRECTION) as channel:
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
                update_players_callback(response.players, response.started)

                # #prevent creating multiple connections
                if (response.started):                    
                    return
        except grpc.RpcError as e:
            print(f"Stream closed with error: {e}")


def request_start_game(game_code):
    with grpc.insecure_channel(DIRECTION) as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        try:
            response = stub.StartGame(service_pb2.GameCode(code=game_code))
            return response
        except grpc.RpcError as e:
            print(f"Failed to start game: {e}")
            return False

def join_input_updates(stub, code, player_uuid):
    def request_messages():
        while True:
            # Yield messages to send to the server
            yield service_pb2.PlayerState(
               code=code,
               player=service_pb2.PlayerData(player_uuid=player_uuid),
               input=service_pb2.Input(move=False)  # or your actual input data
            )
            time.sleep(1)  # Example: send every second

    responses = stub.JoinInputUpdates(request_messages())
    for response in responses:
        print("Received from server:", response)

