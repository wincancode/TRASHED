# Imports estándar de Python
import sys

# Imports de terceros
import pygame

# Imports locales o específicos del proyecto

from game import start_game
from menu import show_start_screen, show_create_game_screen, show_join_game_screen, show_main_menu
import settings as stt
# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = stt.GAME_WIDTH, stt.GAME_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Rectangle")

show_main_menu(screen)


Mostrar_inicio = True

user_uuid = ''
game_code = ''

if Mostrar_inicio:
    while True:
        start_option = show_start_screen()
        if start_option == "join":
            result, user_uuid, game_code = show_join_game_screen()
            if result == "back":
                continue  # Volver al menú principal
        elif start_option == "create":
            result, user_uuid, game_code = show_create_game_screen()
            if result == "back":
                continue  # Volver al menú principal
        break

start_game(screen, screen_width, screen_height, game_code, user_uuid)

