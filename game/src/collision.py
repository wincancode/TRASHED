import pygame
from entities.powerup import PowerUp
from entities.asteroid import release_asteroids
import random

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

