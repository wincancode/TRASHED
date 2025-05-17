import pygame
import random
import settings as stt

def create_background_asteroids(num_asteroids):
    """Crea una lista de asteroides para el fondo con tamaño reducido."""
    asteroids = []
    for _ in range(num_asteroids):
        x = random.randint(0, stt.GAME_WIDTH)
        y = random.randint(-stt.GAME_HEIGHT, 0)  # Aparecen fuera de la pantalla
        speed = random.uniform(50, 150)  # Velocidad aleatoria
        sprite = pygame.image.load(stt.ASTEROID_DEFAULT_SPRITE).convert_alpha()  # Cargar sprite
        sprite = pygame.transform.scale(sprite, (70, 70))  # Reducir tamaño a 30x30 píxeles
        asteroids.append({"x": x, "y": y, "speed": speed, "sprite": sprite})
    return asteroids

def update_and_draw_asteroids(asteroids, screen, delta_time):
    """Actualiza y dibuja los asteroides en el fondo."""
    for asteroid in asteroids:
        asteroid["y"] += asteroid["speed"] * delta_time
        if asteroid["y"] > stt.GAME_HEIGHT:  # Si sale de la pantalla, reiniciar posición
            asteroid["y"] = -asteroid["sprite"].get_height()
            asteroid["x"] = random.randint(0, stt.GAME_WIDTH)
        screen.blit(asteroid["sprite"], (asteroid["x"], asteroid["y"]))