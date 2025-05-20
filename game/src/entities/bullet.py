import pygame
import math
import settings as stt
from entities.entity import Entity

class Bullet(Entity):
    def __init__(self,id, x, y, angle, laser_boost_level=0):
        self.id= id
        self.posX = x
        self.posY = y
        self.angle = angle
        self.speed = stt.SHOT_BASE_SPEED
        self.active = True
        self.damage= 1 + laser_boost_level
        self.laser_boost_level = laser_boost_level


        sprite_scales = {
            0: (15, 35),
            1: (15, 45),
            2: (15, 50),
            3: (30, 70),
            4: (40, 80),
            5: (50, 80),  # Para nivel 5 o superior
        }

        scale = sprite_scales.get(laser_boost_level, sprite_scales[5])


        # Selección de sprite según el nivel de laser boost
        if laser_boost_level == 0:
            sprite_path = stt.SHOT_DEFAULT_SPRITE

        elif laser_boost_level == 1:
            sprite_path = getattr(stt, 'SHOT_LASER_1_SPRITE', stt.SHOT_DEFAULT_SPRITE)
        elif laser_boost_level == 2:
            sprite_path = getattr(stt, 'SHOT_LASER_2_SPRITE', stt.SHOT_DEFAULT_SPRITE)
        elif laser_boost_level == 3:
            sprite_path = getattr(stt, 'SHOT_LASER_3_SPRITE', stt.SHOT_DEFAULT_SPRITE)
        elif laser_boost_level == 4:
            sprite_path = getattr(stt, 'SHOT_LASER_4_SPRITE', stt.SHOT_DEFAULT_SPRITE)
        else:
            sprite_path = getattr(stt, 'SHOT_LASER_4_SPRITE', stt.SHOT_DEFAULT_SPRITE)

        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, scale)
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



