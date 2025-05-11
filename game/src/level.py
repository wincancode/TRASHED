class Level:
    def __init__(self):
        self.current_level = 1
        self.asteroids_destroyed = 0
        self.asteroids_to_next_level = 10
        self.level_up_message_timer = 0
        self.score = 0
        self.min_asteroids = 10
        self.difficulty_factor = 1  # Factor de dificultad inicial

    def update(self, destroyed_count, asteroids):
        """Actualizar el progreso del nivel."""
        self.asteroids_destroyed += destroyed_count
        if self.asteroids_destroyed >= self.asteroids_to_next_level:
            self.current_level += 1
            self.asteroids_destroyed = 0
            self.asteroids_to_next_level += 5
            self.level_up_message_timer = 3.0
            self.increase_difficulty(asteroids)

    def increase_difficulty(self, asteroids):
        """Incrementar la dificultad del juego."""
        self.difficulty_factor += 1  # Incrementar el factor de dificultad
        for asteroid in asteroids:
            asteroid.max_health += 1  # Incrementar la vida máxima
            asteroid.health = asteroid.max_health  # Restaurar la vida al máximo
            asteroid.set_dimensions(asteroid.width + 5, asteroid.height + 5)  # Incrementar el tamaño