import math
import pygame
from entities.entity import Entity
from entities.bullet import Bullet
import settings as stt


class Ship(Entity):
    
    def __init__(self,id,color):
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
        self.set_color(color)
        self.space_pressed = False
        self.lives = 3
        self.laser_boost_level = 0
        self.shield_charges = 0  # Número de cargas del escudo
        self.shield_active = False  # Indica si el escudo está activo
        self.bullets = []

    
    def lose_life(self):
        """Reduce la vida de la nave en 1."""
        self.lives -= 1
    
    def activate_shield(self):
        """Activa el escudo si hay cargas disponibles."""
        if self.shield_charges > 0:
            self.shield_active = True

    def block_impact(self):
        """Bloquea un impacto y reduce las cargas del escudo."""
        if self.shield_active:
            self.shield_charges -= 1
            if self.shield_charges <= 0:
                self.shield_active = False
            return True  # Impacto bloqueado
        return False  # Impacto no bloqueado

    def control(self, keys):
        if keys["move"]:
            #accelerate where the ship is facing
            self.accelerationX = self.acceleration *math.sin(math.radians(self.angle))
            self.accelerationY = -self.acceleration *math.cos(math.radians(self.angle))

        else:
            self.accelerationX = 0
            self.accelerationY = 0
        if keys["stop"]:
            self.accelerationX = 0
            self.accelerationY = 0
            # Aplicar desaceleración rápida
            self.speedX *= 0.98  # Reduce la velocidad en el eje X
            self.speedY *= 0.98 # Reduce la velocidad en el eje Y
            
        if keys["stride_left"]:
            self.rotate(-self.angle_speed)
        if keys["stride_right"]:
            self.rotate(self.angle_speed)
        if keys["is_shoot"]:
            if not self.space_pressed:
                self.shoot()
                self.space_pressed = True
        else:
            self.space_pressed = False
    
    def shoot(self):
        bullet = Bullet(self.posX, self.posY, self.angle, self.laser_boost_level)
        self.bullets.append(bullet)

    def draw(self, screen, delta_time):
        """Dibuja la nave y, si está activo, el escudo."""
        # Llamar al método draw de la clase base para dibujar la nave
        super().draw(screen)

        # Dibujar las balas
        for bullet in self.bullets[:]:
            bullet.Update(delta_time, screen)
            # if not bullet.active:
            #     self.bullets.remove(bullet)

        # Dibujar el escudo si está activo
        if self.shield_active:
            pygame.draw.circle(
                screen,
                (0, 255, 255),  # Color del escudo (cian)
                (int(self.posX), int(self.posY)),  # Centro del círculo
                self.width,  # Radio del círculo (igual al ancho de la nave)
                3  # Grosor del borde del círculo
            )

    def setState(self, state):
        """Establece el estado de la nave."""
        if state is None or not hasattr(state, "position") or state.position is None:
            return

        pos = state.position
        if getattr(pos, "x", None) is not None and getattr(pos, "y", None) is not None:
            self.set_pos(pos.x, pos.y)
        if hasattr(pos, "angle") and pos.angle is not None:
            self.set_angle(pos.angle)
        if hasattr(pos, "speedX") and pos.speedX is not None:
            self.speedX = pos.speedX
        if hasattr(pos, "speedY") and pos.speedY is not None:
            self.speedY = pos.speedY
        if hasattr(pos, "accelerationX") and pos.accelerationX is not None:
            self.accelerationX = pos.accelerationX
        if hasattr(pos, "accelerationY") and pos.accelerationY is not None:
            self.accelerationY = pos.accelerationY
        if hasattr(pos, "speed",) and pos.speed is not None:
            self.set_speed(pos.speed)