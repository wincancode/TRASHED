import math
import threading
import time
import pygame
from entities.ship import Ship
from entities.asteroid import Asteroid
from entities.powerup import apply_powerup_effect
from collision import check_collisions, handle_bullet_asteroid_collisions, check_powerup_collisions
from connectivity import join_game_state_updates
import server.service_pb2 as service_pb2
from menu import show_game_over_screen
import settings as stt
from level import Level
from ui import draw_text, draw_progress_bar
from crt import apply_crt_effect




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

    
    clock = pygame.time.Clock()

    asteroids = []
    asteroid_map = {}  # id -> asteroid for interpolation
    messages = []
    powerups = []
    released_asteroids = []
    last_server_update = time.time()
    local_player_inputs = {
        "move": False,
        "stride_left": False,
        "stride_right": False,
        "stop": False,
        "is_shoot": False
    }

    INTERPOLATION_DELAY = 1.0 / 60  # Adjust to your server tick rate

    def obtain_game_state_callback(state):
        nonlocal last_server_update
        with lock:
            # Update ships
            for ship in ships:
                ship_state = state.playerStates[ship.id]
                ship.setState(ship_state)
                if ship.id == user_uuid:
                    ship1.set_health(ship_state.health)

            # Update asteroids from server state (with interpolation)
            asteroid_ids = set()
            if hasattr(state, 'asteroids'):
                for asteroid_state in state.asteroids:
                    asteroid_ids.add(asteroid_state.id)
                    if asteroid_state.id in asteroid_map:
                        asteroid = asteroid_map[asteroid_state.id]
                        asteroid.prev_posX = getattr(asteroid, 'next_posX', asteroid.posX)
                        asteroid.prev_posY = getattr(asteroid, 'next_posY', asteroid.posY)
                        asteroid.next_posX = asteroid_state.x
                        asteroid.next_posY = asteroid_state.y
                        asteroid.last_update_time = time.time()
                        asteroid.set_dimensions(asteroid_state.width, asteroid_state.height)
                        asteroid.set_speed(asteroid_state.speed)
                        asteroid.set_angle(asteroid_state.angle)
                        asteroid.health = asteroid_state.health
                        asteroid.max_health = asteroid_state.max_health
                        asteroid.set_active(True)
                    else:
                        asteroid = Asteroid(asteroid_state.id)
                        asteroid.prev_posX = asteroid_state.x
                        asteroid.prev_posY = asteroid_state.y
                        asteroid.next_posX = asteroid_state.x
                        asteroid.next_posY = asteroid_state.y
                        asteroid.last_update_time = time.time()
                        asteroid.set_pos(asteroid_state.x, asteroid_state.y)
                        asteroid.set_dimensions(asteroid_state.width, asteroid_state.height)
                        asteroid.set_speed(asteroid_state.speed)
                        asteroid.set_angle(asteroid_state.angle)
                        asteroid.health = asteroid_state.health
                        asteroid.max_health = asteroid_state.max_health
                        asteroid.set_active(True)
                        asteroid_map[asteroid_state.id] = asteroid
                # Remove asteroids not present in the server state
                for aid in list(asteroid_map.keys()):
                    if aid not in asteroid_ids:
                        del asteroid_map[aid]
            # Update asteroids list for rendering
            asteroids.clear()
            asteroids.extend(asteroid_map.values())

            # Update bullets for each ship (shared pool, assign to all ships for now)
            for ship in ships:
                ship.bullets.clear()
            if hasattr(state, 'bullets'):
                from entities.bullet import Bullet
                for bullet_state in state.bullets:


                    bullet = Bullet(
                        bullet_state.id,
                        bullet_state.x,
                        bullet_state.y,
                        bullet_state.angle
                    )
                    bullet.speed = bullet_state.speed
                    bullet.active = bullet_state.active
                    bullet.damage = bullet_state.damage
                    bullet.width = bullet_state.width
                    bullet.height = bullet_state.height

                    #find the existing bullets 
                    found = False
                    for ship in ships:
                        for existing_bullet in ship.bullets:
                            if existing_bullet.id == bullet_state.id:
                                existing_bullet.set_pos(bullet_state.x, bullet_state.y)
                                existing_bullet.set_speed(bullet_state.speed)
                                existing_bullet.set_angle(bullet_state.angle)
                                existing_bullet.active = bullet_state.active
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        # Add the bullet to the first ship's bullets list
                        if ships:
                            ships[0].bullets.append(bullet)
            
            #Update level state 
            if hasattr(state, 'level'):
                level.current_level = state.level.current_level
                level.score = state.level.score
                level.asteroids_destroyed = state.level.asteroids_destroyed
                level.asteroids_to_next_level = state.level.asteroids_to_next_level
                level.difficulty_factor = state.level.difficulty_factor
                level.level_up_message_timer = state.level.level_up_message_timer                




        # keys = {}

        # keys["move"] = inputs.input.move
        # keys["stride_left"] = inputs.input.stride_left
        # keys["stride_right"] = inputs.input.stride_right
        # keys["stop"] = inputs.input.stop
        # keys["is_shoot"] = inputs.input.is_shoot

        # with lock:
        #     nonlocal ships
        #     for ship in ships:   
        #         if ship.id == inputs.player.player_uuid:
        #             ship.control(keys)
                

    def local_player_input_iterator():
        while True:
            with lock:
                nonlocal local_player_inputs                
                yield service_pb2.PlayerState(
                code=game_code,
                player_uuid= user_uuid,
                timestamp=int(pygame.time.get_ticks()),
                input=service_pb2.Input(
                    move=local_player_inputs["move"],
                    stride_left=local_player_inputs["stride_left"],
                    stride_right=local_player_inputs["stride_right"],
                    stop=local_player_inputs["stop"],
                    is_shoot=local_player_inputs["is_shoot"]
                    )
                )
            time.sleep(0.01)  # Delay to control the rate of sending inputs

    Input_updates_thread = threading.Thread(
        target=join_game_state_updates,
        args=(game_code,user_uuid,obtain_game_state_callback,local_player_input_iterator)
    )
    Input_updates_thread.start()


    key_action_map = {
        pygame.K_w: "move",
        pygame.K_s: "stop",
        pygame.K_a: "stride_left",
        pygame.K_d: "stride_right",
        pygame.K_SPACE: "is_shoot",
    }


    def getInputs(deltaTime) -> None:
        keys = pygame.key.get_pressed()
        actions = {}

        for key, action in key_action_map.items():
            actions[action] = keys[key]

        # Actualizar la entrada del jugador local
        nonlocal local_player_inputs
        
        with lock:
            local_player_inputs = actions


    # def getInputs(deltaTime):
    #      keys = pygame.key.get_pressed()
    #      ship1.control(keys)
    #      ship1.updatePosition(deltaTime)


    # Inicializar el sistema de niveles
    level = Level()

    running = True
    disconnected = False

    def handle_disconnection():
        from menu import show_disconnected_screen, show_main_menu
        show_disconnected_screen(screen)
        show_main_menu(screen)

    # Thread to monitor input updates and catch disconnection
    def input_updates_wrapper():
        try:
            join_game_state_updates(game_code, user_uuid, obtain_game_state_callback, local_player_input_iterator)
        except Exception as e:
            print(f"[GAME] Disconnected from server: {e}")
            nonlocal disconnected
            disconnected = True

    Input_updates_thread = threading.Thread(target=input_updates_wrapper)
    Input_updates_thread.start()

    nuke_cooldown = 0  # Tiempo restante para volver a spawnear asteroides tras la nuke

    while running:
        if disconnected:
            handle_disconnection()
            return "back"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.tick(stt.GAME_FPS) / 1000.0  # Convert milliseconds to seconds

        # if check_collisions(ship1, asteroids, released_asteroids):
        #     if ship1.lives <= 0:
        #         show_game_over_screen(screen, screen_width, screen_height)
        #         running = False
        #         break

        # Manejar colisiones entre balas y asteroides
        # for ship in ships:
        #     points, destroyed_count = handle_bullet_asteroid_collisions(ship.bullets, asteroids, messages, powerups, released_asteroids)
        #     score += points  # Sumar los puntos obtenidos al puntaje total
        #     level.update(destroyed_count, asteroids)  # Actualizar el progreso del nivel

        # Generar nuevos asteroides si el número es menor al mínimo
        # while len(asteroids) < level.min_asteroids:
        #      asteroids.append(Asteroid(len(asteroids), difficulty_factor=level.difficulty_factor))


        # Limpiar la pantalla
        screen.fill(stt.BLACK)

        # --- Draw game as usual to a temporary surface ---
        temp_surface = pygame.Surface((screen_width, screen_height)).convert_alpha()
        temp_surface.fill(stt.BLACK)

        for asteroid in asteroids:
            now = time.time()
            t = min((now - getattr(asteroid, 'last_update_time', now)) / INTERPOLATION_DELAY, 1.0)
            interp_x = getattr(asteroid, 'prev_posX', asteroid.posX) * (1 - t) + getattr(asteroid, 'next_posX', asteroid.posX) * t
            interp_y = getattr(asteroid, 'prev_posY', asteroid.posY) * (1 - t) + getattr(asteroid, 'next_posY', asteroid.posY) * t
            asteroid.draw_at(temp_surface, interp_x, interp_y)
            asteroid.draw_health(temp_surface,interp_x,interp_y)

        # Dibujar mensajes temporales
        for message in messages[:]:
            if "text" in message:
                draw_text(temp_surface, message["text"], message["pos"], (255, 255, 255), opacity=int(message["opacity"]))
            elif "icon" in message:
                icon_img = pygame.image.load(message["icon"])
                icon_img = pygame.transform.scale(icon_img, (48, 48))
                icon_img.set_alpha(int(message["opacity"]))
                icon_rect = icon_img.get_rect(center=message["pos"])
                temp_surface.blit(icon_img, icon_rect)

            message["timer"] -= delta_time
            message["pos"][1] -= 50 * delta_time
            message["opacity"] -= 85 * delta_time

            if message["timer"] <= 0 or message["opacity"] <= 0:
                messages.remove(message)

        for powerup in powerups[:]:
            powerup.draw(temp_surface)
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
            asteroid.Update(delta_time, temp_surface)
            asteroid.draw_health(temp_surface,asteroid.posX,asteroid.posY)
            # if asteroid.health <= 0:
            #     released_asteroids.remove(asteroid)

        # Mostrar el mensaje de "Subiste de Nivel"
        if level.level_up_message_timer > 0:
            level.level_up_message_timer -= delta_time
            draw_text(temp_surface, "¡Subiste de Nivel!", (screen_width // 2, screen_height // 2), (255, 255, 0), font_size=50, center=True)

        # Dibujar la nave
        if pygame.key.get_focused():
            getInputs(delta_time)

        for ship in ships:
            #not render dead ships
            if ship.lives <= 0:
                continue

            ship.draw(temp_surface,delta_time)
            ship.updatePosition(delta_time)  # Update the ship's position with a small delta time

        #check if game ended 
        if all(ship.lives <= 0 for ship in ships):
            show_game_over_screen(screen, screen_width, screen_height)
            running = False
            break
        
            

        # Mostrar la puntuación acumulada
        draw_text(temp_surface, f"Puntos: {level.score}", (10, 10), (255, 255, 255))

        # Mostrar las vidas
        draw_text(temp_surface, f"Vidas: {ship1.lives}", (screen_width - 120, 10), (255, 255, 255))

        # Mostrar el nivel actual
        draw_text(temp_surface, f"Nivel: {level.current_level}", (screen_width // 2 - 50, 10), (255, 255, 255))

        # Dibujar la barra de progreso para el siguiente nivel
        draw_progress_bar(
            temp_surface,
            x=10, y=50,  # Posición de la barra
            width=200, height=20,  # Tamaño de la barra
            progress=level.asteroids_destroyed,  # Progreso actual
            max_progress=level.asteroids_to_next_level,  # Progreso máximo
            color=(0, 255, 0),  # Color de la barra (verde)
            bg_color=(50, 50, 50)  # Color de fondo (gris oscuro)
        )
        # --- Apply CRT effect and blit to screen ---
        crt_surface = apply_crt_effect(temp_surface, scanline_alpha=60, vignette_strength=1, glow_strength=8, glow_radius=4)
        screen.blit(crt_surface, (0, 0))
        pygame.display.flip()
    
    return "back"
