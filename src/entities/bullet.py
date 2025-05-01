import pygame
import math
import settings as stt

class Bullet:
    def __init__(self, x, y, angle):
        self.posX = x
        self.posY = y
        self.angle = angle
        self.speed = stt.SHOT_BASE_SPEED
        self.active = True

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
        screen.blit(self.sprite, (self.posX, self.posY))
        

        