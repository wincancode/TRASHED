import pygame
import math
import settings as stt
from entities.entity import Entity

class Bullet(Entity):
    def __init__(self, x, y, angle, laser_boost_level=0):
        self.posX = x
        self.posY = y
        self.angle = angle
        self.speed = stt.SHOT_BASE_SPEED
        self.active = True
        self.damage= 1 + laser_boost_level

        self.sprite = pygame.image.load(stt.SHOT_DEFAULT_SPRITE)
        self.sprite = pygame.transform.scale(self.sprite, (5, 10))
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()


    def updatePosition(self, delta_time):
        self.posX += self.speed * math.sin(math.radians(self.angle)) * delta_time
        self.posY -= self.speed * math.cos(math.radians(self.angle)) * delta_time

        if (self.posX < 0 or self.posX > stt.GAME_WIDTH or
            self.posY < 0 or self.posY > stt.GAME_HEIGHT):
            self.active = False

    def draw(self, screen):
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.angle)
        # Ajustar la posición para centrar el sprite rotado
        sprite_rect = rotated_sprite.get_rect(center=(self.posX, self.posY))
        screen.blit(rotated_sprite, sprite_rect.topleft)
    


        