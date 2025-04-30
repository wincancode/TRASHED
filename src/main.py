import pygame
import sys
from entities.ship import Ship
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

def getInputs(deltaTime):
    keys = pygame.key.get_pressed()
    ship1.control(keys)
    ship1.updatePosition(deltaTime)



# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta_time = clock.tick(stt.GAME_FPS) / 1000.0  # Convert milliseconds to seconds

    # Fill the screen
    screen.fill(stt.BLACK)

    getInputs(delta_time)
    

    ship1.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()