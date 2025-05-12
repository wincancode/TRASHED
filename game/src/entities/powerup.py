import pygame

class PowerUp:
    def __init__(self, x, y, power_type):
        self.posX = x
        self.posY = y
        self.power_type = power_type  # Tipo de potenciador (e.g., "laser_boost")
        self.width = 100  # Ancho del texto
        self.height = 30  # Altura del texto
        self.active = True

    def draw(self, screen):
        """Dibuja el potenciador como texto en la pantalla."""
        font = pygame.font.Font(None, 36)
        if self.power_type == "shield":
            text_surface = font.render("Escudo Avanzado", True, (0, 255, 255))  # Texto cian
        elif self.power_type == "laser_boost":
            text_surface = font.render("Láser Experimental", True, (255, 255, 0))  # Texto amarillo
        else:
            return  # No dibujar nada si el tipo no es válido
        text_rect = text_surface.get_rect(center=(self.posX, self.posY))
        screen.blit(text_surface, text_rect)

    def update(self, delta_time):
        """Actualizar lógica del potenciador (si es necesario)."""
        pass