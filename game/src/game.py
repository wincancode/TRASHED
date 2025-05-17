


import pygame
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.powerup import apply_powerup_effect
from collision import check_collisions, handle_bullet_asteroid_collisions, check_powerup_collisions
from menu import show_game_over_screen
import settings as stt
from level import Level
from ui import draw_text, draw_progress_bar

def start_game(screen,screen_width,screen_height):
    ship1 = Ship(1)

    clock = pygame.time.Clock()

    asteroids = []
    bullets = []
    messages = []
    powerups = []
    released_asteroids = []

    MIN_ASTEROIDS = 10

    for i in range(10):
        asteroids.append(Asteroid(i))



    def getInputs(deltaTime):
        keys = pygame.key.get_pressed()
        ship1.control(keys, bullets)
        ship1.updatePosition(deltaTime)


    score = 0

    # Inicializar el sistema de niveles
    level = Level()

    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.tick(stt.GAME_FPS) / 1000.0  # Convert milliseconds to seconds

        if check_collisions(ship1, asteroids, released_asteroids):
            if ship1.lives <= 0:
                show_game_over_screen(screen, screen_width, screen_height)
                running = False
                break

        # Manejar colisiones entre balas y asteroides
        points, destroyed_count = handle_bullet_asteroid_collisions(bullets, asteroids, messages, powerups, released_asteroids)
        score += points  # Sumar los puntos obtenidos al puntaje total
        level.update(destroyed_count, asteroids)  # Actualizar el progreso del nivel

        # Generar nuevos asteroides si el número es menor al mínimo
        while len(asteroids) < level.min_asteroids:
            asteroids.append(Asteroid(len(asteroids), difficulty_factor=level.difficulty_factor))


        # Limpiar la pantalla
        screen.fill(stt.BLACK)

        # Dibujar asteroides
        for asteroid in asteroids:
            asteroid.Update(delta_time, screen)
            asteroid.draw_health(screen)

        # Dibujar balas
        for bullet in bullets[:]:
            bullet.Update(delta_time, screen)
            if not bullet.active:
                bullets.remove(bullet)

        # Dibujar mensajes temporales
        for message in messages[:]:
            message["timer"] -= delta_time
            message["pos"][1] -= 50 * delta_time
            message["opacity"] -= 85 * delta_time

            if message["timer"] <= 0 or message["opacity"] <= 0:
                messages.remove(message)
            else:
                draw_text(screen, message["text"], message["pos"], (255, 255, 255), opacity=int(message["opacity"]))

        for powerup in powerups[:]:
            powerup.draw(screen)
            powerup.update(delta_time)
            if check_powerup_collisions(ship1, powerup):  # Detectar si la nave recoge el potenciador
                apply_powerup_effect(ship1, powerup.power_type, messages)  # Pasar la lista de mensajes
                powerups.remove(powerup)

        for asteroid in released_asteroids[:]:
            asteroid.Update(delta_time, screen)
            asteroid.draw_health(screen)
            if asteroid.health <= 0:
                released_asteroids.remove(asteroid)

        # Mostrar el mensaje de "Subiste de Nivel"
        if level.level_up_message_timer > 0:
            level.level_up_message_timer -= delta_time
            draw_text(screen, "¡Subiste de Nivel!", (screen_width // 2, screen_height // 2), (255, 255, 0), font_size=50, center=True)

        # Dibujar la nave
        getInputs(delta_time)
        ship1.draw(screen)

        # Mostrar la puntuación acumulada
        draw_text(screen, f"Puntos: {score}", (10, 10), (255, 255, 255))

        # Mostrar las vidas
        draw_text(screen, f"Vidas: {ship1.lives}", (screen_width - 120, 10), (255, 255, 255))

        # Mostrar el nivel actual
        draw_text(screen, f"Nivel: {level.current_level}", (screen_width // 2 - 50, 10), (255, 255, 255))

        # Dibujar la barra de progreso para el siguiente nivel
        draw_progress_bar(
            screen,
            x=10, y=50,  # Posición de la barra
            width=200, height=20,  # Tamaño de la barra
            progress=level.asteroids_destroyed,  # Progreso actual
            max_progress=level.asteroids_to_next_level,  # Progreso máximo
            color=(0, 255, 0),  # Color de la barra (verde)
            bg_color=(50, 50, 50)  # Color de fondo (gris oscuro)
        )

        # Actualizar la pantalla
        pygame.display.flip()

