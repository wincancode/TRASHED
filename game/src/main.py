import pygame
import sys
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.bullet import Bullet
import settings as stt

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = stt.GAME_WIDTH, stt.GAME_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Rectangle")

# Colors

ship1 = Ship(1)

clock = pygame.time.Clock()

asteroids = []
bullets = []

for i in range(10):
    asteroids.append(Asteroid(i))

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

def show_join_game_screen():
    font = pygame.font.Font(None, 50)
    input_box = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50)
    color_inactive = stt.BLUE
    color_active = stt.WHITE
    color = color_inactive
    active = False
    text = ""

    while True:
        screen.fill(stt.BLACK)

        # Draw prompt text
        prompt_text = font.render("Ingrese el código de la partida:", True, stt.WHITE)
        prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(prompt_text, prompt_rect)

        # Draw input box
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(text, True, stt.WHITE)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        input_box.w = max(300, text_surface.get_width() + 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # Logica de Conexion
                        # Aquí puedes agregar la lógica para conectarte a la partida con el código ingresado
                        print(f"Código ingresado: {text}")
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        pygame.display.flip()
        clock.tick(60)

def show_create_game_screen():
    font_title = pygame.font.Font(None, 74)
    font_code = pygame.font.Font(None, 50)

    # Generar un código de partida aleatorio
    import random
    game_code = "".join([str(random.randint(0, 9)) for _ in range(4)])

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

def getInputs(deltaTime):
    keys = pygame.key.get_pressed()
    ship1.control(keys, bullets)
    ship1.updatePosition(deltaTime)

Mostrar_inicio = True

# Main game loop
running = True
if Mostrar_inicio:
    start_option = show_start_screen()
    if start_option == "join":
        show_join_game_screen()
    elif start_option == "create":
        show_create_game_screen()
    Mostrar_inicio = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta_time = clock.tick(stt.GAME_FPS) / 1000.0  # Convert milliseconds to seconds

    # Fill the screen
    screen.fill(stt.BLACK)

    for asteroid in asteroids:
        asteroid.Update(delta_time,screen)

    for bullet in bullets[:]:
        bullet.Update(delta_time,screen)
        if not bullet.active:
            bullets.remove(bullet)
        

    getInputs(delta_time)
    

    ship1.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()