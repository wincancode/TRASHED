import math
import pygame
from entities.entity import Entity
import settings as stt


class Ship(Entity):
    
    def __init__(self,id):
        super().__init__(id)
        self.set_sprite(pygame.image.load(stt.SHIP_DEFAULT_SPRITE))
        self.set_dimensions(stt.SHIP_WIDTH, stt.SHIP_HEIGHT)
        self.set_acceleration(stt.SHIP_BASE_ACCELERATION)
        self.set_speed(stt.SHIP_BASE_SPEED)
        self.set_angle_speed(stt.SHIP_BASE_TURN_RATE)
        self.set_max_speed(stt.SHIP_BASE_SPEED)
        self.set_max_acceleration(stt.SHIP_BASE_ACCELERATION)
        self.set_max_angle_speed(stt.SHIP_BASE_TURN_RATE)
        self.set_pos(stt.GAME_WIDTH / 2, stt.GAME_HEIGHT / 2)
        self.set_angle(360)
        self.set_active(True)

    def control(self, keys):
        if keys[pygame.K_w]:
            #accelerate where the ship is facing
            self.accelerationX = self.acceleration *math.sin(math.radians(self.angle))
            self.accelerationY = -self.acceleration *math.cos(math.radians(self.angle))
        if keys[pygame.K_s]:
            self.accelerationX = 0
            self.accelerationY = 0
        if keys[pygame.K_a]:
            self.rotate(-self.angle_speed)
        if keys[pygame.K_d]:
            self.rotate(self.angle_speed)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def shoot(self):
        print(f"Shooting from {self.id} at angle {self.angle}!")