import random
import pygame
from entities.entity import Entity
import settings as stt
import math

class Asteroid(Entity):
    def __init__(self, id):
        super().__init__(id)
        self.set_sprite(pygame.image.load(stt.ASTEROID_DEFAULT_SPRITE))
        self.set_dimensions(random.randint(20, 50), random.randint(20, 50))
        self.set_pos(
            random.randint(0, stt.GAME_WIDTH),
            random.randint(0, stt.GAME_HEIGHT)
        )
        self.set_speed(random.uniform(50, 150))
        self.set_angle(random.uniform(0, 360))
        self.set_active(True)

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