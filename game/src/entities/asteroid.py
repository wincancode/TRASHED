import random
import pygame
from entities.entity import Entity
import settings as stt
import math

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

    def draw_health(self, screen):
        """Dibuja la vida del asteroide encima de él."""
        font = pygame.font.Font(None, 20)
        health_text = font.render(f"{self.health}", True, (255, 255, 255))  # Blanco
        text_rect = health_text.get_rect(center=(self.posX, self.posY - self.height // 2 - 10))
        screen.blit(health_text, text_rect)