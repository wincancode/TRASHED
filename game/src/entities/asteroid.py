import random
import pygame
from entities.entity import Entity
import settings as stt
import math
import time

class Asteroid(Entity):
    def __init__(self, id, difficulty_factor=1):
        super().__init__(id)
        self.set_sprite(pygame.image.load(stt.ASTEROID_DEFAULT_SPRITE))
        base_size = random.randint(20, 50)
        self.set_dimensions(base_size + (difficulty_factor * 5), base_size + (difficulty_factor * 5))
        self.set_pos(
            random.randint(0, stt.GAME_WIDTH),
            random.randint(0, stt.GAME_HEIGHT)
        )
        self.set_speed(random.uniform(50, 150))
        self.set_angle(random.uniform(0, 360))
        self.set_active(True)

        # Vida basada en el tamaño del asteroide y el nivel de dificultad
        self.max_health = (self.width // 10) + difficulty_factor
        self.health = self.max_health


    def updatePosition(self, delta_time):
        self.speedX = self.speed * math.cos(math.radians(self.angle))
        self.speedY = self.speed * math.sin(math.radians(self.angle))

        super().updatePosition(delta_time)

        if (self.posX < -100 or self.posX > stt.GAME_WIDTH + 100 or 
            self.posY < -100 or self.posY > stt.GAME_HEIGHT + 100):
            self.respawn()
    
    def respawn(self):
        self.set_pos(
            random.choice([-50, stt.GAME_WIDTH + 50]), random.randint(-50, stt.GAME_HEIGHT + 50)
        )
        self.set_angle(random.uniform(0, 360))


    def draw_health(self, screen, x=None, y=None):
        """Dibuja la vida del asteroide encima de él, usando x, y si se proporcionan."""
        font = pygame.font.Font(None, 20)
        draw_x = x if x is not None else self.posX
        draw_y = y if y is not None else self.posY
        health_text = font.render(f"{self.health}", True, (255, 255, 255))  # Blanco
        text_rect = health_text.get_rect(center=(draw_x, draw_y - self.height // 2 - 10))
        screen.blit(health_text, text_rect)



def release_asteroids(ship, released_asteroids):
    """Libera asteroides alrededor de la nave al romperse el escudo."""
    safe_radius = 50  # Distancia segura desde el centro de la nave
    for i in range(8):  # Generar 8 asteroides en diferentes direcciones
        angle = math.radians(i * 45)  # Ángulos predefinidos (0, 45, 90, ..., 315) en radianes
        asteroid = Asteroid(-1, difficulty_factor=0)  # Vida mínima
        asteroid.set_pos(
            ship.posX + safe_radius * math.cos(angle),  # Calcular la posición X
            ship.posY + safe_radius * math.sin(angle)   # Calcular la posición Y
        )
        asteroid.set_angle(math.degrees(angle))  # Establecer el ángulo en grados
        asteroid.set_speed(200)  # Velocidad alta
        asteroid.health = 1  # Vida mínima
        asteroid.max_health = 1
        released_asteroids.append(asteroid)