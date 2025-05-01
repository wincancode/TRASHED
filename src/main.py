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

def getInputs(deltaTime):
    keys = pygame.key.get_pressed()
    ship1.control(keys, bullets)
    ship1.updatePosition(deltaTime)



# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta_time = clock.tick(stt.GAME_FPS) / 1000.0  # Convert milliseconds to seconds

    # Fill the screen
    screen.fill(stt.WHITE)

    for asteroid in asteroids:
        asteroid.updatePosition(delta_time)
        asteroid.draw(screen)

    for bullet in bullets[:]:
        bullet.updatePosition(delta_time)
        if not bullet.active:
            bullets.remove(bullet)
        else:
            bullet.draw(screen)

    getInputs(delta_time)
    

    ship1.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()