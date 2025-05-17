
from encodings.punycode import T
import threading
import time
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
                    print("Game started, closing connection.")
                    channel.close()    
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


def generate_player_states(player_uuid):
    for i in range(1000000000000000000000000):
        yield service_pb2.PlayerState(
            code="GAME123",
            player=service_pb2.PlayerData(player_uuid=player_uuid, username=f"user"),
            timestamp=123456789 + i,
            input=service_pb2.Input(move=True)
        )

        # Simulate some delay
        time.sleep(1)

def join_input_updates(code, player_uuid):
    channel = grpc.insecure_channel(DIRECTION)
    stub = service_pb2_grpc.GameServiceStub(channel)

    metadata = [
        ('game_code', code),
        ('player_uuid', player_uuid)
    ]

    responses = stub.JoinInputUpdates(generate_player_states(player_uuid), metadata=metadata)
    for response in responses:
        print("Received:", response)
