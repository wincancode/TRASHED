import pygame
import math
import settings as stt
from entities.powerup import PowerUp
import random
from entities.asteroid import Asteroid

def check_collisions(ship, asteroids, released_asteroids):
    """Check for collisions between the ship y todos los asteroides."""
    ship_rect = pygame.Rect(ship.posX - ship.width // 2, ship.posY - ship.height // 2, ship.width, ship.height)

    # Verificar colisiones con asteroides normales
    for asteroid in asteroids[:]:
        asteroid_rect = pygame.Rect(asteroid.posX - asteroid.width // 2, asteroid.posY - asteroid.height // 2, asteroid.width, asteroid.height)
        if ship_rect.colliderect(asteroid_rect):
            if ship.block_impact():  # Si el escudo bloquea el impacto
                asteroids.remove(asteroid)  # Eliminar el asteroide
                release_asteroids(ship, released_asteroids)  # Liberar asteroides al romperse el escudo
                return False  # No perder vida
            else:
                ship.lose_life()  # Reducir una vida de la nave
                asteroids.remove(asteroid)  # Eliminar el asteroide
                return True  # Perder vida

    # Verificar colisiones con asteroides liberados
    for asteroid in released_asteroids[:]:
        asteroid_rect = pygame.Rect(asteroid.posX - asteroid.width // 2, asteroid.posY - asteroid.height // 2, asteroid.width, asteroid.height)
        if ship_rect.colliderect(asteroid_rect):
            if ship.block_impact():  # Si el escudo bloquea el impacto
                released_asteroids.remove(asteroid)  # Eliminar el asteroide liberado
                return False  # No perder vida
            else:
                ship.lose_life()  # Reducir una vida de la nave
                released_asteroids.remove(asteroid)  # Eliminar el asteroide liberado
                return True  # Perder vida

    return False

def handle_bullet_asteroid_collisions(bullets, asteroids, messages, powerups, released_asteroids):
    """Check for collisions between bullets y todos los asteroides."""
    total_points = 0  # Total de puntos obtenidos en esta iteración
    destroyed_count = 0  # Contador de asteroides destruidos

    # Colisiones con asteroides normales
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.posX - bullet.width // 2, bullet.posY - bullet.height // 2, bullet.width, bullet.height)
        for asteroid in asteroids[:]:
            asteroid_rect = pygame.Rect(asteroid.posX - asteroid.width // 2, asteroid.posY - asteroid.height // 2, asteroid.width, asteroid.height)
            if bullet_rect.colliderect(asteroid_rect):
                bullets.remove(bullet)  # Remove the bullet
                asteroid.health -= bullet.damage  # Decrease the asteroid's health

                if asteroid.health <= 0:
                    asteroids.remove(asteroid)
                    destroyed_count += 1  # Incrementar el contador de asteroides destruidos

                    # Calcular puntos según el tamaño del asteroide
                    points = asteroid.width  # Por ejemplo, el ancho del asteroide determina los puntos
                    total_points += points  # Sumar los puntos al total

                    # Agregar un mensaje temporal con los puntos obtenidos
                    messages.append({
                        "text": f"+{points} puntos",
                        "pos": [asteroid.posX, asteroid.posY],
                        "opacity": 255,
                        "timer": 3.0
                    })

                    # Generar un potenciador con una probabilidad del 50%
                    if random.random() < 0.5:
                        power_type = random.choice(["laser_boost", "shield"])  # Elegir aleatoriamente el tipo de potenciador
                        powerups.append(PowerUp(asteroid.posX, asteroid.posY, power_type))
                break

    # Colisiones con asteroides liberados
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.posX - bullet.width // 2, bullet.posY - bullet.height // 2, bullet.width, bullet.height)
        for asteroid in released_asteroids[:]:
            asteroid_rect = pygame.Rect(asteroid.posX - asteroid.width // 2, asteroid.posY - asteroid.height // 2, asteroid.width, asteroid.height)
            if bullet_rect.colliderect(asteroid_rect):
                bullets.remove(bullet)  # Remove the bullet
                released_asteroids.remove(asteroid)  # Eliminar el asteroide liberado
                break

    return total_points, destroyed_count  # Devuelve los puntos y el número de asteroides destruidos

def check_powerup_collisions(ship, powerup):
    """Detecta si la nave recoge un potenciador."""
    ship_rect = pygame.Rect(ship.posX - ship.width // 2, ship.posY - ship.height // 2, ship.width, ship.height)
    powerup_rect = pygame.Rect(powerup.posX - powerup.width // 2, powerup.posY - powerup.height // 2, powerup.width, powerup.height)
    return ship_rect.colliderect(powerup_rect)

def apply_powerup_effect(ship, power_type, messages):
    """Aplica el efecto del potenciador a la nave."""
    if power_type == "laser_boost":
        ship.laser_boost_level += 1  # Incrementar el nivel del láser
        messages.append({
            "text": f"Láser mejorado: Nivel {ship.laser_boost_level}",
            "pos": [ship.posX, ship.posY - 50],
            "opacity": 255,
            "timer": 3.0
        })
    elif power_type == "shield":
        ship.shield_charges += 1  # Incrementar las cargas del escudo
        ship.shield_active = True  # Activar el escudo
        messages.append({
            "text": f"Escudo mejorado: {ship.shield_charges} cargas",
            "pos": [ship.posX, ship.posY - 50],
            "opacity": 255,
            "timer": 3.0
        })

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