# Imports estándar de Python
import sys

# Imports de terceros
import pygame

# Imports locales o específicos del proyecto

from game import start_game
from menu import show_start_screen, show_create_game_screen, show_join_game_screen, show_main_menu
from ui import draw_text
import settings as stt
# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = stt.GAME_WIDTH, stt.GAME_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Triangle")

Mostrar_inicio = True

user_uuid = ''
game_code = ''

def show_tutorial_screen(screen):
    # Tarjetas de powerups: icono y descripción
    powerups_info = [
        {"icon": stt.SHIELD_UPGRADE_ICON, "name": "Escudo", "desc": "Te protege de un impacto."},
        {"icon": stt.DAMAGE_UP_ICON, "name": "Láser Mejorado", "desc": "Aumenta el daño de tu disparo."},
        {"icon": stt.NUKE_ICON, "name": "Nuke", "desc": "Destruye todos los asteroides en pantalla (solo una vez por partida)."},
        {"icon": stt.TURBINAS_ICON, "name": "Turbina", "desc": "Aumenta la velocidad y giro de la nave."},
    ]
    running = True
    while running:
        screen.fill((30, 30, 30))
        draw_text(screen, "TUTORIAL DE POWER UPS", (screen.get_width()//2, 40), (255,255,0), font_size=40, center=True)
        y = 100
        for info in powerups_info:
            icon = pygame.image.load(info["icon"])
            icon = pygame.transform.scale(icon, (64, 64))
            screen.blit(icon, (80, y))
            draw_text(screen, info["name"], (170, y+10), (255,255,255), font_size=32)
            draw_text(screen, info["desc"], (170, y+40), (200,200,200), font_size=24)
            y += 90
        draw_text(screen, "Presiona ESC para volver", (screen.get_width()//2, y+40), (255,255,255), font_size=28, center=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

def show_controls_tutorial_screen(screen):
    controls = [
        ("W", "Acelerar hacia adelante"),
        ("S", "Frenar/desacelerar"),
        ("A", "Girar a la izquierda"),
        ("D", "Girar a la derecha"),
        ("ESPACIO", "Disparar"),
        ("ESC", "Salir o volver al menú"),
    ]
    running = True
    while running:
        screen.fill((30, 30, 30))
        draw_text(screen, "TUTORIAL DE CONTROLES", (screen.get_width()//2, 40), (0,255,255), font_size=40, center=True)
        y = 120
        for key, desc in controls:
            draw_text(screen, f"{key}", (120, y), (255,255,255), font_size=32)
            draw_text(screen, desc, (220, y), (200,200,200), font_size=28)
            y += 60
        draw_text(screen, "Presiona ESC para volver", (screen.get_width()//2, y+40), (255,255,255), font_size=28, center=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

def main_loop():
    user_uuid = ''
    game_code = ''
    online_players = []
    while True:
        show_main_menu(screen)
        while True:
            start_option = show_start_screen()
            print(f"start_option: {start_option}")
            if start_option == "join":
                result, user_uuid, game_code, online_players = show_join_game_screen()
                if result == "back":
                    continue  # Regresar al menú principal
            elif start_option == "create":
                result, user_uuid, game_code, online_players = show_create_game_screen()
                if result == "back":
                    continue  # Regresar al menú principal
            elif start_option == "tutorial":
                show_tutorial_screen(screen)
                show_controls_tutorial_screen(screen)
                continue
            else:
                continue
            break  # Salir del bucle de selección de juego

        start_game(screen, screen_width, screen_height, game_code, user_uuid, online_players)
        # Limpiar variables para la siguiente vuelta
        user_uuid = ''
        game_code = ''
        online_players = []

if __name__ == "__main__":
    main_loop()
