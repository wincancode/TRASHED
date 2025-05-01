import pygame
import settings as stt
from utils import clamp_abs


class Entity:
    def __init__(self,id,posX = 0,posY = 0):
        self.id = id
        
        # Set initial position
        self.posX = posX
        self.posY = posY
        self.angle = 0

        # Set attributes for velocity and acceleration
        self.speed = 0
        self.acceleration = 0
        self.max_speed = 0
        self.max_acceleration = 0
        self.angle_speed = 0
        self.max_angle_speed = 0

        # Set attributes for active state and dimensions
        self.speedX = 0
        self.speedY = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.width = 0
        self.height = 0
        self.sprite = None
        self.active = True   
        
    def updatePosition(self, delta_time) -> None:
        self.posX += self.speedX * delta_time
        self.posY += self.speedY * delta_time

        
        # Update velocity based on acceleration
        self.speedX += self.accelerationX * delta_time
        self.speedY += self.accelerationY * delta_time

        if self.accelerationX == 0:
            self.speedY -= stt.SHIP_DEACCELERATION_RATE * delta_time * (1 if self.speedY > 0 else -1)
            if abs(self.speedY) < 0.01:
                self.speedY = 0

        if self.accelerationY == 0:
            self.speedX -= stt.SHIP_DEACCELERATION_RATE * delta_time * (1 if self.speedX > 0 else -1)
            if abs(self.speedX) < 0.01:
                self.speedX = 0

        self.set_current_speed(self.speedX, self.speedY)

        accelerationX = self.accelerationX - stt.SHIP_DEACCELERATION_RATE * delta_time * (1 if self.accelerationX > 0 else -1)
        accelerationY = self.accelerationY - stt.SHIP_DEACCELERATION_RATE * delta_time * (1 if self.accelerationY > 0 else -1)

        self.set_current_acceleration(accelerationX, accelerationY)

        print(f"acceleration:{self.accelerationY}")
        print(f"speed: {self.speedY}")
       
    def rotate(self, angle):
        self.angle += angle * self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def glow(self, screen):
        for i in range(1,stt.GLOW_INTENSITY):
            # Create a glow effect by the same sprite slightly larger and with a decaying alpha
            glow_sprite = pygame.transform.scale(self.sprite, (self.width + i * stt.GLOW_PROPAGATION, self.height + i *stt.GLOW_PROPAGATION))
            # Set the alpha value for the glow effect
            glow_sprite.set_alpha(stt.GLOW_ALPHA - i*stt.GLOW_ALPHA_DECAY)
            # Get the rectangle for positioning
            rect = glow_sprite.get_rect(center=(self.posX, self.posY))
            # Draw the glow effect on the screen
            screen.blit(glow_sprite, rect.topleft)
            

    def draw(self, screen):
        if self.sprite:
            # Sc    Zale the original sprite to the desired dimensions
            scaled_sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            # Rotate the scaled sprite
            rotated_sprite = pygame.transform.rotate(scaled_sprite, -self.angle)
            # Get the rectangle for positioning
            rect = rotated_sprite.get_rect(center=(self.posX, self.posY))

            if(stt.GLOW):
                self.glow(screen)

            # Draw the rotated sprite on the screen
            screen.blit(rotated_sprite, rect.topleft)
            
    
    
    # Getters
    def get_pos(self):
        return self.posX, self.posY

    def get_angle(self):
        return self.angle
    
    def get_speed(self):
        return self.speed

    def get_acceleration(self):
        return self.acceleration

    def get_max_speed(self):
        return self.max_speed
    
    def get_max_acceleration(self):
        return self.max_acceleration

    def get_angle_speed(self):
        return self.angle_speed

    def get_max_angle_speed(self):
        return self.max_angle_speed

    def get_current_speed(self):
        return self.speedX, self.speedY

    def get_current_acceleration(self):
        return self.accelerationX, self.accelerationY

    def get_dimensions(self):
        return self.width, self.height

    def get_sprite(self):
        return self.sprite

    def is_active(self):
        return self.active

    # Setters
    def set_pos(self, x, y):
        self.posX = x
        self.posY = y

    def set_angle(self, angle):
        self.angle = angle

    def set_speed(self, speed):
        self.speed = speed

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def set_max_acceleration(self, max_acceleration):
        self.max_acceleration = max_acceleration

    def set_angle_speed(self, angle_speed):
        self.angle_speed = angle_speed

    def set_max_angle_speed(self, max_angle_speed):
        self.max_angle_speed = max_angle_speed

    def set_current_speed(self, speedX, speedY):
        self.speedX = clamp_abs(speedX, self.max_speed)
        self.speedY = clamp_abs(speedY, self.max_speed)

    def set_current_acceleration(self, accelerationX, accelerationY):
        self.accelerationX = clamp_abs(accelerationX, self.max_acceleration,1)
        self.accelerationY = clamp_abs(accelerationY, self.max_acceleration,1)

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def set_sprite(self, sprite):
        self.sprite = sprite

    def set_active(self, active):
        self.active = active