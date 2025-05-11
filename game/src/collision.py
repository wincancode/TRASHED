import pygame
import settings as stt

def check_collisions(ship, asteroids):
    """Check for collisions between the ship and asteroids."""
    ship_rect = pygame.Rect(ship.posX - ship.width // 2, ship.posY - ship.height // 2, ship.width, ship.height)
    for asteroid in asteroids:
        asteroid_rect = pygame.Rect(asteroid.posX - asteroid.width // 2, asteroid.posY - asteroid.height // 2, asteroid.width, asteroid.height)
        if ship_rect.colliderect(asteroid_rect):
            ship.lose_life()  # Reduce una vida de la nave
            asteroids.remove(asteroid)  # Opcional: elimina el asteroide tras la colisión
            if ship.lives <= 0:
                return True  # Devuelve True solo si las vidas llegan a 0
    return False  # Devuelve False si la nave aún tiene vidas

def handle_bullet_asteroid_collisions(bullets, asteroids, messages):
    """Check for collisions between bullets and asteroids."""
    total_points = 0  # Total de puntos obtenidos en esta iteración
    destroyed_count = 0  # Contador de asteroides destruidos
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.posX - bullet.width // 2, bullet.posY - bullet.height // 2, bullet.width, bullet.height)
        for asteroid in asteroids[:]:
            asteroid_rect = pygame.Rect(asteroid.posX - asteroid.width // 2, asteroid.posY - asteroid.height // 2, asteroid.width, asteroid.height)
            if bullet_rect.colliderect(asteroid_rect):
                bullets.remove(bullet)  # Remove the bullet

                asteroid.health -= 1  # Decrease the asteroid's health

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
                break
    return total_points, destroyed_count  # Devuelve los puntos y el número de asteroides destruidos