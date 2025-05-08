import grpc
import pygame
from connectivity import request_game_code_from_server
import server.service_pb2 as service_pb2
import server.service_pb2_grpc as service_pb2_grpc
import settings as stt
import sys
import random
import os


screen_width, screen_height = stt.GAME_WIDTH, stt.GAME_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

def connect_to_server(player_id, player_name):
    """Connect to the server and handle the JoinGame response."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        try:
            # Call JoinGame and handle the streaming response
            responses = stub.JoinGame(service_pb2.PlayerData(
                player_uuid=player_id,
                timestamp=1234567890,  # Replace with actual timestamp if needed
                username=player_name,
            ))
            for response in responses:
                print(f"Received update: {response}")
        except grpc.RpcError as e:
            print(f"Stream closed with error: {e}")

def send_game_state_to_server(game_code, ships):
    """Send the created game state to the server."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.GameServiceStub(channel)
        try:
            # Create a PlayerState for each ship and send it to the server
            for ship_color in ships:
                player_state = service_pb2.PlayerState(
                    player_uuid=f"{game_code}_{ship_color}",
                    timestamp=1234567890,  # Replace with actual timestamp if needed
                    posX=0,  # Initial position X
                    posY=0,  # Initial position Y
                    angle=0  # Initial angle
                )
                response = stub.SendState(player_state)
                print(f"Server response: {response}")
        except grpc.RpcError as e:
            print(f"Failed to send game state: {e}")


def draw_button(screen, text, x, y, width, height, font, color, hover_color, mouse_pos, click):
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click:
            return True
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surface = font.render(text, True, stt.WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return False

def show_start_screen():
    font_title = pygame.font.Font(None, 74)
    font_button = pygame.font.Font(None, 50)

    title_text = font_title.render("Titulo del Juego", True, stt.WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

    button_width, button_height = 300, 60
    button_spacing = 20
    button_x = (screen_width - button_width) // 2
    button_y = screen_height // 2

    while True:
        screen.fill(stt.BLACK)

        # Draw title
        screen.blit(title_text, title_rect)

        # Get mouse position and click state
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        # Draw buttons
        create_game = draw_button(screen, "Crear partida", button_x, button_y + button_height + button_spacing, button_width, button_height, font_button, stt.BLACK, stt.BLUE, mouse_pos, click)
        join_game = draw_button(screen, "Unirse a partida", button_x, button_y, button_width, button_height, font_button, stt.BLACK, stt.BLUE, mouse_pos, click)

        if join_game:
            print("Unirse a partida seleccionado")
            return "join"
        if create_game:
            print("Crear partida seleccionado")
            return "create"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def show_create_game_screen():
    font_title = pygame.font.Font(None, 74)
    font_code = pygame.font.Font(None, 50)

    # Generar un código de partida aleatorio
    game_code = request_game_code_from_server()

    # Arreglo de naves (máximo 3)
    ships = ["red", "blue"]  # Colores de las naves

    # Cargar imágenes de las naves
    ship_images = {
        "red": pygame.image.load(stt.SHIP_DEFAULT_SPRITE),
        "blue": pygame.image.load(stt.SHIP_DEFAULT_SPRITE),
        "green": pygame.image.load(stt.SHIP_DEFAULT_SPRITE)
    }

    # Escalar imágenes de las naves
    for color in ship_images:
        ship_images[color] = pygame.transform.scale(ship_images[color], (50, 50))

    while True:
        screen.fill(stt.BLACK)

        # Dibujar el título
        title_text = font_title.render("Crear Partida", True, stt.WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_text, title_rect)

        # Dibujar el código de partida
        code_text = font_code.render(f"Código de partida: {game_code}", True, stt.WHITE)
        code_rect = code_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(code_text, code_rect)

        # Dibujar las naves con separaciones
        start_x = screen_width // 2 - 100
        y_position = screen_height // 2 + 20
        for i in range(3):  # Siempre iterar hasta 3 para mostrar divisores
            x_position = start_x + i * 100
            if i < len(ships):
                color = ships[i]
                screen.blit(ship_images[color], (x_position, y_position))

            # Dibujar separadores
            if i < 2:  # Mostrar separadores entre las posiciones
                separator_text = font_code.render("/", True, stt.WHITE)
                separator_rect = separator_text.get_rect(center=(x_position + 75, y_position + 25))
                screen.blit(separator_text, separator_rect)

        # Dibujar botón de "Empezar partida"
        button_width, button_height = 200, 50
        button_x = screen_width - button_width - 20
        button_y = screen_height - button_height - 20
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, stt.BLUE, button_rect)

        button_text = font_code.render("Empezar", True, stt.WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        # Detectar clic en el botón
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if button_rect.collidepoint(mouse_pos) and click:
            print("Partida iniciada")
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


def show_join_game_screen():
    font = pygame.font.Font(None, 50)
    input_box_id = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 60, 300, 50)
    input_box_name = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50)
    button_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 80, 200, 50)

    color_inactive = stt.BLUE
    color_active = stt.WHITE
    color_button = stt.GREEN
    active_id = False
    active_name = False
    player_id = ""
    player_name = ""

    while True:
        screen.fill(stt.BLACK)

        pygame.draw.rect(screen, color_active if active_id else color_inactive, input_box_id, 2)
        pygame.draw.rect(screen, color_active if active_name else color_inactive, input_box_name, 2)
        pygame.draw.rect(screen, color_button, button_box)

        # Render text
        id_text = font.render(player_id, True, stt.WHITE)
        name_text = font.render(player_name, True, stt.WHITE)
        button_text = font.render("Join Game", True, stt.WHITE)

        screen.blit(id_text, (input_box_id.x + 10, input_box_id.y + 10))
        screen.blit(name_text, (input_box_name.x + 10, input_box_name.y + 10))
        screen.blit(button_text, (button_box.x + 50, button_box.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_id.collidepoint(event.pos):
                    active_id = True
                    active_name = False
                elif input_box_name.collidepoint(event.pos):
                    active_name = True
                    active_id = False
                elif button_box.collidepoint(event.pos):
                    # Connect to the server
                    if player_id and player_name:
                        connect_to_server(player_id, player_name)
                    else:
                        print("Player ID and Name are required!")
                    return
                else:
                    active_id = False
                    active_name = False
            if event.type == pygame.KEYDOWN:
                if active_id:
                    if event.key == pygame.K_BACKSPACE:
                        player_id = player_id[:-1]
                    else:
                        player_id += event.unicode
                elif active_name:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        clock.tick(30)