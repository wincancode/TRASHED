import threading
import pygame
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.powerup import apply_powerup_effect
from collision import check_collisions, handle_bullet_asteroid_collisions, check_powerup_collisions
from connectivity import join_input_updates
from menu import show_game_over_screen
import settings as stt
from level import Level
from ui import draw_text, draw_progress_bar


def deencrypt_input(movement):
    # Aquí puedes implementar la lógica para desencriptar el game_code
    # Por ahora, simplemente lo devolvemos sin cambios
    return game_code



def start_game(screen,screen_width,screen_height,game_code,user_uuid,online_players=[]):
    ships = []
    lock = threading.Lock()

    for player in online_players:
        print(f"Jugador: {player.username} - UUID: {player.player_uuid} - Color: {player.color}")
        ships.append(Ship(player.player_uuid, player.color))


    # obtener la nave del jugador
    ship1 = None
    for ship in ships:
        if ship.id == user_uuid:
            ship1 = ship
            break
    
    def obtain_inputs_callback(inputs):
       print(f"Inputs recibidos: {inputs}")
        # for ship in ships:
        #     if ship.id == inputs.player_uuid:
        #         ship.update_inputs(inputs)
        #         break

    


    Input_updates_thread = threading.Thread(target=join_input_updates, args=(game_code,user_uuid,obtain_inputs_callback))
    Input_updates_thread.start()

    
    clock = pygame.time.Clock()

    asteroids = []
    messages = []
    powerups = []
    released_asteroids = []
    nuke_spawned = False

    #!!!!!!!!!!
    MIN_ASTEROIDS = 10


    for i in range(10):
        asteroids.append(Asteroid(i))


    

    def local_player_input_iterator():
        while True:
            with lock:
                nonlocal local_player_inputs
                yield local_player_inputs

    local_player_input_thread = threading.Thread(target=local_player_input_iterator)
    local_player_input_thread.start()

    local_player_inputs =         {
            "move": False,
            "stride_left": False,
            "stride_right": False,
            "stop": False,
            "is_shoot": False
        }
    

    key_action_map = {
        pygame.K_w: "move",
        pygame.K_s: "stop",
        pygame.K_a: "stride_left",
        pygame.K_d: "stride_right",
        pygame.K_SPACE: "is_shoot",
    }

    #def getInputs(deltaTime) -> None:
    #    keys = pygame.key.get_pressed()
    #    actions = {}
#
    #    for key, action in key_action_map.items():
    #        actions[action] = keys[key]
    #    
    #    print(f"Acciones del jugador local: {actions}")
    #    
    #    # Actualizar la entrada del jugador local
    #    nonlocal local_player_inputs
    #    
    #    with lock:
    #        local_player_inputs = actions


    def getInputs(deltaTime):
         keys = pygame.key.get_pressed()
         ship1.control(keys)
         ship1.updatePosition(deltaTime)

    score = 0

    # Inicializar el sistema de niveles
    level = Level()

    running = True

    nuke_cooldown = 0  # Tiempo restante para volver a spawnear asteroides tras la nuke

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.tick(stt.GAME_FPS) / 1000.0  # Convert milliseconds to seconds

        # Actualizar cooldown de la nuke
        if nuke_cooldown > 0:
            nuke_cooldown -= delta_time
            if nuke_cooldown < 0:
                nuke_cooldown = 0

        if check_collisions(ship1, asteroids, released_asteroids):
            if ship1.lives <= 0:
                show_game_over_screen(screen, screen_width, screen_height)
                running = False
                break

        # Manejar colisiones entre balas y asteroides
        for ship in ships:
            points, destroyed_count = handle_bullet_asteroid_collisions(ship.bullets, asteroids, messages, powerups, released_asteroids,nuke_spawned)
            score += points  # Sumar los puntos obtenidos al puntaje total
            level.update(destroyed_count, asteroids)  # Actualizar el progreso del nivel

        # Generar nuevos asteroides si el número es menor al mínimo y no está en cooldown de nuke
        if nuke_cooldown == 0:
            while len(asteroids) < level.min_asteroids:
                asteroids.append(Asteroid(len(asteroids), difficulty_factor=level.difficulty_factor))


        # Limpiar la pantalla
        screen.fill(stt.BLACK)

        #!!!!!!!!!!!!!!! Dibujar asteroides
        for asteroid in asteroids:
            asteroid.Update(delta_time, screen)
            asteroid.draw_health(screen)

        # Dibujar mensajes temporales
        for message in messages[:]:
            if "text" in message:
                draw_text(screen, message["text"], message["pos"], (255, 255, 255), opacity=int(message["opacity"]))
            elif "icon" in message:
                icon_img = pygame.image.load(message["icon"])
                icon_img = pygame.transform.scale(icon_img, (48, 48))
                icon_img.set_alpha(int(message["opacity"]))
                icon_rect = icon_img.get_rect(center=message["pos"])
                screen.blit(icon_img, icon_rect)

            message["timer"] -= delta_time
            message["pos"][1] -= 50 * delta_time
            message["opacity"] -= 85 * delta_time

            if message["timer"] <= 0 or message["opacity"] <= 0:
                messages.remove(message)

        for powerup in powerups[:]:
            powerup.draw(screen)
            powerup.update(delta_time)
            if check_powerup_collisions(ship1, powerup):  # Detectar si la nave recoge el potenciador
                if powerup.power_type == "nuke":
                    asteroids.clear()   # Eliminar todos los asteroides
                    released_asteroids.clear()  # Eliminar todos los asteroides liberados
                    nuke_cooldown = 5.0
                    nuke_spawned = True  # 5 segundos sin spawnear
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
        for ship in ships:
            ship.draw(screen,delta_time)

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

