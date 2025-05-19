import grpc
import pygame
from connectivity import request_game_code_from_server, connect_to_server, request_start_game
from background import create_background_asteroids, update_and_draw_asteroids
import server.service_pb2 as service_pb2
import server.service_pb2_grpc as service_pb2_grpc
import settings as stt
import sys
import threading
from crt import draw_crt_effect



screen_width, screen_height = stt.GAME_WIDTH, stt.GAME_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

def show_main_menu(screen):
    """Muestra el menú principal con asteroides moviéndose en el fondo."""
    pygame.init()
    clock = pygame.time.Clock()

    # Configuración de fuentes
    font_title = pygame.font.Font(None, 100)
    font_message = pygame.font.Font(None, 50)

    # Texto del título y mensaje
    title_text = font_title.render("Space Z", True, stt.WHITE)
    title_rect = title_text.get_rect(center=(stt.GAME_WIDTH // 2, stt.GAME_HEIGHT // 3))

    message_text = font_message.render("Presiona Enter para Continuar", True, stt.WHITE)
    message_rect = message_text.get_rect(center=(stt.GAME_WIDTH // 2, stt.GAME_HEIGHT // 2))

    # Crear asteroides para el fondo
    asteroids = create_background_asteroids(15)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar Enter para continuar
                    running = False

        # Limpiar pantalla
        screen.fill(stt.BLACK)

        # Actualizar y dibujar asteroides
        delta_time = clock.tick(stt.GAME_FPS) / 1000.0  # Convertir a segundos
        update_and_draw_asteroids(asteroids, screen, delta_time)

        # Dibujar texto
        screen.blit(title_text, title_rect)
        screen.blit(message_text, message_rect)
        draw_crt_effect(screen)
        pygame.display.flip()

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

    title_text = font_title.render("Space Z", True, stt.WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

    button_width, button_height = 300, 60
    button_spacing = 20
    button_x = (screen_width - button_width) // 2
    button_y = screen_height // 2

    asteroids = create_background_asteroids(15)

    while True:
        screen.fill(stt.BLACK)

        delta_time = clock.tick(stt.GAME_FPS) / 1000.0
        update_and_draw_asteroids(asteroids, screen, delta_time)

        # Draw title
        screen.blit(title_text, title_rect)

        # Get mouse position and click state
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        # Draw buttons
        create_game = draw_button(
            screen, "Crear partida",
            button_x, button_y + button_height + button_spacing,
            button_width, button_height, font_button,
            stt.BLACK, stt.BLUE, mouse_pos, click
        )
        join_game = draw_button(
            screen, "Unirse a partida",
            button_x, button_y,
            button_width, button_height, font_button,
            stt.BLACK, stt.BLUE, mouse_pos, click
        )
        tutorial = draw_button(
            screen, "Tutorial",
            button_x, button_y + 2 * (button_height + button_spacing),
            button_width, button_height, font_button,
            stt.BLACK, stt.BLUE, mouse_pos, click
        )

        # Only return if the mouse was released after a click (prevents accidental double triggers)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if join_game and join_game:  # Button was pressed and mouse released
                    print("Unirse a partida seleccionado")
                    return "join"
                if create_game and create_game:
                    print("Crear partida seleccionado")
                    return "create"
                if tutorial and tutorial:
                    print("Tutorial seleccionado")
                    return "tutorial"

        draw_crt_effect(screen)
        pygame.display.flip()
        clock.tick(60)

def show_create_game_screen():
    # Mostrar pantalla para ingresar datos del jugador
    player_id, player_name = show_player_data_screen()

    # Si el usuario presionó "Regresar", salir de la función
    if player_id is None and player_name is None:
        return "back", '', '', []

    # Solicitar el código de partida al servidor
    game_code = request_game_code_from_server()
    if not game_code:
        print("Error al crear la partida.")
        from menu import show_disconnected_screen, show_main_menu
        show_disconnected_screen(screen)
        show_main_menu(screen)
        return "back", '', '', []

    # Mostrar pantalla de espera
    online_players = show_waiting_screen(game_code, player_id, player_name)
    return '',player_id, game_code, online_players

def show_join_game_screen():
    font = pygame.font.Font(None, 50)
    label_font = pygame.font.Font(None, 30)
    error_font = pygame.font.Font(None, 25)

    # Ajustar las posiciones de los cuadros de texto
    input_box_id = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 230, 300, 50)
    input_box_name = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 120, 300, 50)
    input_box_code = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 10, 300, 50)
    button_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 80, 200, 50)
    back_button_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 160, 200, 50)

    color_inactive = stt.BLUE
    color_active = stt.WHITE
    color_button = stt.GREEN
    active_id = False
    active_name = False
    active_code = False
    player_id = ""
    player_name = ""
    game_code = ""
    error_message = ""

    while True:
        screen.fill(stt.BLACK)

        # Dibujar etiquetas con mayor separación
        id_label = label_font.render("ID del jugador:", True, stt.WHITE)
        name_label = label_font.render("Nombre del jugador:", True, stt.WHITE)
        code_label = label_font.render("Código de partida:", True, stt.WHITE)
        screen.blit(id_label, (input_box_id.x, input_box_id.y - 40))  # Separación ajustada
        screen.blit(name_label, (input_box_name.x, input_box_name.y - 40))  # Separación ajustada
        screen.blit(code_label, (input_box_code.x, input_box_code.y - 40))  # Separación ajustada

        # Dibujar los cuadros de texto y el botón
        pygame.draw.rect(screen, color_active if active_id else color_inactive, input_box_id, 2)
        pygame.draw.rect(screen, color_active if active_name else color_inactive, input_box_name, 2)
        pygame.draw.rect(screen, color_active if active_code else color_inactive, input_box_code, 2)
        pygame.draw.rect(screen, color_button, button_box)
        pygame.draw.rect(screen, stt.RED, back_button_box)

        # Renderizar texto
        id_text = font.render(player_id, True, stt.WHITE)
        name_text = font.render(player_name, True, stt.WHITE)
        code_text = font.render(game_code, True, stt.WHITE)
        button_text = font.render("Unirse", True, stt.WHITE)
        back_button_text = font.render("Regresar", True, stt.WHITE)

        screen.blit(id_text, (input_box_id.x + 10, input_box_id.y + 10))
        screen.blit(name_text, (input_box_name.x + 10, input_box_name.y + 10))
        screen.blit(code_text, (input_box_code.x + 10, input_box_code.y + 10))
        screen.blit(button_text, (button_box.x + 50, button_box.y + 10))
        screen.blit(back_button_text, (back_button_box.x + 50, back_button_box.y + 10))
        
        if error_message:
            error_text = error_font.render(error_message, True, stt.RED)
            screen.blit(error_text, (screen_width // 2 - error_text.get_width() // 2, screen_height // 2 + 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_id.collidepoint(event.pos):
                    active_id = True
                    active_name = False
                    active_code = False
                elif input_box_name.collidepoint(event.pos):
                    active_name = True
                    active_id = False
                    active_code = False
                elif input_box_code.collidepoint(event.pos):
                    active_code = True
                    active_id = False
                    active_name = False
                elif button_box.collidepoint(event.pos):
                    # Validar que los campos no estén vacíos
                    if player_id and player_name and game_code:
                        # Mostrar pantalla de espera
                        try:
                            online_players = show_waiting_screen(game_code, player_id, player_name)
                        except Exception as e:
                            from menu import show_disconnected_screen, show_main_menu
                            show_disconnected_screen(screen)
                            show_main_menu(screen)
                            return "back", '', '', []
                        return  '', player_id, game_code, online_players
                    else:
                        return "back", '', '', []
                elif back_button_box.collidepoint(event.pos):
                    # Regresar al menú principal
                    return "back", '', '', []
                else:
                    active_id = False
                    active_name = False
                    active_code = False
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
                elif active_code:
                    if event.key == pygame.K_BACKSPACE:
                        game_code = game_code[:-1]
                    else:
                        game_code += event.unicode
        clock.tick(30)

def show_game_over_screen(screen, screen_width, screen_height):
    """Display the Game Over screen."""
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, stt.WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.fill(stt.BLACK)
    screen.blit(text, text_rect)
    draw_crt_effect(screen)
    pygame.display.flip()
    pygame.time.wait(6000)  # Wait for 3 seconds
    return "back"  # Return to the main menu

def show_player_data_screen():
    font = pygame.font.Font(None, 50)
    label_font = pygame.font.Font(None, 30)
    error_font = pygame.font.Font(None, 25)
    
    input_box_id = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 100, 300, 50)
    input_box_name = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50)
    button_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 120, 200, 50)
    back_button_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 200, 50)

    color_inactive = stt.BLUE
    color_active = stt.WHITE
    color_button = stt.GREEN
    active_id = False
    active_name = False
    player_id = ""
    player_name = ""
    error_message = ""

    while True:
        screen.fill(stt.BLACK)
        
        # Dibujar etiquetas
        id_label = label_font.render("ID del jugador:", True, stt.WHITE)
        name_label = label_font.render("Nombre del jugador:", True, stt.WHITE)
        screen.blit(id_label, (input_box_id.x, input_box_id.y - 30))
        screen.blit(name_label, (input_box_name.x, input_box_name.y - 30))

        # Dibujar los cuadros de texto y el botón
        pygame.draw.rect(screen, color_active if active_id else color_inactive, input_box_id, 2)
        pygame.draw.rect(screen, color_active if active_name else color_inactive, input_box_name, 2)
        pygame.draw.rect(screen, color_button, button_box)
        pygame.draw.rect(screen, stt.RED, back_button_box)

        # Renderizar texto
        id_text = font.render(player_id, True, stt.WHITE)
        name_text = font.render(player_name, True, stt.WHITE)
        button_text = font.render("Crear", True, stt.WHITE)
        back_button_text = font.render("Regresar", True, stt.WHITE)

        screen.blit(id_text, (input_box_id.x + 10, input_box_id.y + 10))
        screen.blit(name_text, (input_box_name.x + 10, input_box_name.y + 10))
        screen.blit(button_text, (button_box.x + 50, button_box.y + 10))
        screen.blit(back_button_text, (back_button_box.x + 50, back_button_box.y + 10))
        
        if error_message:
            error_text = error_font.render(error_message, True, stt.RED)
            screen.blit(error_text, (screen_width // 2 - error_text.get_width() // 2, screen_height // 2 + 70))


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
                    # Validar que los campos no estén vacíos
                    if player_id and player_name:
                        return player_id, player_name
                    else:
                        error_message = "¡El ID y el nombre son obligatorios!"
                elif back_button_box.collidepoint(event.pos):
                    # Regresar al menú principal
                    return None, None
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

def show_waiting_screen(game_code, player_id, player_name):
    font = pygame.font.Font(None, 50)
    is_game_started = False
    players = []  # Lista de jugadores conectados
    disconnected = False

    def update_players(new_players,started_flag):
        nonlocal players, disconnected, is_game_started
        players = new_players  # Almacenar los objetos completos de tipo PlayerData
        print(f"Jugadores conectados: {[player for player in players]}")
        if started_flag:
            print('assigning game started')
            is_game_started = True
        # Only set disconnected if not started, new_players is empty, and not is_game_started
        elif new_players == [] and not is_game_started and not started_flag:
            disconnected = True

    # Iniciar un hilo para escuchar los mensajes del servidor
    thread = threading.Thread(target=connect_to_server, args=(player_id, player_name, game_code, update_players))
    thread.start()

    while not is_game_started and not disconnected:
        screen.fill(stt.BLACK)

        # Mostrar el código de la partida
        code_text = font.render(f"Código de partida: {game_code}", True, stt.WHITE)
        code_rect = code_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(code_text, code_rect)

        # Mostrar mensaje de espera
        waiting_text = font.render("Esperando a otros jugadores...", True, stt.WHITE)
        waiting_rect = waiting_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(waiting_text, waiting_rect)

        # Mostrar la lista de jugadores conectados
        for i, player in enumerate(players):
            color = stt.color_map.get(player.color, stt.WHITE)


            player_text = font.render(f"Jugador {i + 1}: {player.username}", True, color)
            player_rect = player_text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 30))
            screen.blit(player_text, player_rect)

        draw_crt_effect(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    request_start_game(game_code)
                    
        clock.tick(30)
    
    if disconnected:
        from menu import show_main_menu, show_disconnected_screen
        show_disconnected_screen(screen)
        show_main_menu(screen)
        return []
    print("Game started!")
    return players

def show_disconnected_screen(screen):
    import pygame
    import settings as stt
    from background import create_background_asteroids, update_and_draw_asteroids
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 40)
    asteroids = create_background_asteroids(10)
    clock = pygame.time.Clock()
    timer = 0
    while timer < 2.5:  # Show for 2.5 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill(stt.BLACK)
        delta_time = clock.tick(stt.GAME_FPS) / 1000.0
        update_and_draw_asteroids(asteroids, screen, delta_time)
        text = font.render("Desconectado", True, stt.RED)
        text_rect = text.get_rect(center=(stt.GAME_WIDTH // 2, stt.GAME_HEIGHT // 2 - 30))
        screen.blit(text, text_rect)
        msg = small_font.render("Perdiste la conexión con el servidor", True, stt.WHITE)
        msg_rect = msg.get_rect(center=(stt.GAME_WIDTH // 2, stt.GAME_HEIGHT // 2 + 40))
        screen.blit(msg, msg_rect)
        pygame.display.flip()
        timer += delta_time
