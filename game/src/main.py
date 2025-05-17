# Imports estándar de Python
import sys

# Imports de terceros
import pygame

# Imports locales o específicos del proyecto

from game import start_game
from menu import show_start_screen, show_create_game_screen, show_join_game_screen, show_game_over_screen
import settings as stt
# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = stt.GAME_WIDTH, stt.GAME_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Rectangle")


Mostrar_inicio = True


# Main game loop
if Mostrar_inicio:
    start_option = show_start_screen()
    if start_option == "join":
        show_join_game_screen()
    elif start_option == "create":
        show_create_game_screen()
    Mostrar_inicio = False

start_game(screen,screen_width,screen_height)

