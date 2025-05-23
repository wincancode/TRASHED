from encodings.punycode import T
import threading
import time
import grpc
import player
import server.service_pb2 as service_pb2
import server.service_pb2_grpc as service_pb2_grpc

DIRECTION = "192.168.169.148:50051"


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
    try:
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
                    # Pasar la lista de jugadores al callback
                    update_players_callback(response.players, response.started)

                    # #prevent creating multiple connections
                    if response.started:        
                        print("Game started, closing connection.")
                        return  # Do not close the channel here, let the context manager handle it
            except grpc.RpcError as e:
                print(f"Stream closed with error: {e}")
                # If the error is 'partida no encontrada', treat as graceful disconnect
                if hasattr(e, 'details') and e.details() == 'partida no encontrada':
                    update_players_callback([], False)
                else:
                    update_players_callback([], False)
    except Exception as e:
        print(f"Connection error: {e}")
        update_players_callback([], False)


def request_start_game(game_code):
    with grpc.insecure_channel(DIRECTION) as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        try:
            response = stub.StartGame(service_pb2.GameCode(code=game_code))
            return response
        except grpc.RpcError as e:
            print(f"Failed to start game: {e}")
            return False



def join_game_state_updates(code, player_uuid, obtain_input_callback,player_input_iterator):
    channel = grpc.insecure_channel(DIRECTION)
    stub = service_pb2_grpc.GameServiceStub(channel)

    metadata = [
        ('game_code', code),
        ('player_uuid', player_uuid)
    ]

    responses = stub.JoinInputUpdates(player_input_iterator(), metadata=metadata)
    for response in responses:
        obtain_input_callback(response)
