import pygame

class PowerUp:
    def __init__(self, x, y, power_type):
        self.posX = x
        self.posY = y
        self.power_type = power_type  # Tipo de potenciador (e.g., "laser_boost")
        self.width = 48  # Tamaño del icono
        self.height = 48
        self.active = True

        # Cargar iconos desde la carpeta de assets/sprites
        if self.power_type == "shield":
            self.icon = pygame.image.load("game/assets/sprites/ShieldUpgrade.png")
        elif self.power_type == "laser_boost":
            self.icon = pygame.image.load("game/assets/sprites/DamageUp.png")
        elif self.power_type == "nuke":
            self.icon = pygame.image.load("game/assets/sprites/Nuke.png")
        elif self.power_type == "turbina":
            self.icon = pygame.image.load("game/assets/sprites/Turbinas.png")
        else:
            self.icon = None

        if self.icon:
            self.icon = pygame.transform.scale(self.icon, (self.width, self.height))

    def draw(self, screen):
        """Dibuja el potenciador como icono en la pantalla."""
        if self.icon:
            icon_rect = self.icon.get_rect(center=(self.posX, self.posY))
            screen.blit(self.icon, icon_rect)

    def update(self, delta_time):
        """Actualizar lógica del potenciador (si es necesario)."""
        pass

def apply_powerup_effect(ship, power_type, messages):
    """Aplica el efecto del potenciador a la nave y muestra un icono y texto correspondiente."""
    if power_type == "laser_boost":
        ship.laser_boost_level += 1  # Incrementar el nivel del láser
        messages.append({
            "icon": "game/assets/sprites/DamageUp.png",
            "type": "laser_boost",
            "pos": [ship.posX, ship.posY - 50],
            "opacity": 255,
            "timer": 3.0
        })
        messages.append({
            "text": f"Láser mejorado: Nivel {ship.laser_boost_level}",
            "pos": [ship.posX, ship.posY - 90],
            "opacity": 255,
            "timer": 2.0
        })
    elif power_type == "shield":
        ship.shield_charges += 1  # Incrementar las cargas del escudo
        ship.shield_active = True  # Activar el escudo
        messages.append({
            "icon": "game/assets/sprites/ShieldUpgrade.png",
            "type": "shield",
            "pos": [ship.posX, ship.posY - 50],
            "opacity": 255,
            "timer": 3.0
        })
        messages.append({
            "text": f"Escudo mejorado: {ship.shield_charges} cargas",
            "pos": [ship.posX, ship.posY - 90],
            "opacity": 255,
            "timer": 2.0
        })
    elif power_type == "nuke":
        messages.append({
            "icon": "game/assets/sprites/Nuke.png",
            "type": "nuke",
            "pos": [ship.posX, ship.posY - 50],
            "opacity": 255,
            "timer": 3.0
        })
        messages.append({
            "text": "¡Nuke activada! Todos los asteroides destruidos.",
            "pos": [ship.posX, ship.posY - 90],
            "opacity": 255,
            "timer": 2.0
        })
    elif power_type == "turbina":
        # Aumentar la velocidad máxima y la velocidad de rotación de la nave en un 20% cada vez
        ship.set_max_speed(ship.get_max_speed() * 1.2)
        ship.set_max_angle_speed(ship.get_max_angle_speed() * 1.2)
        if hasattr(ship, 'turbina_boost'):
            ship.turbina_boost += 1
        else:
            ship.turbina_boost = 1
        messages.append({
            "icon": "game/assets/sprites/Turbinas.png",
            "type": "turbina",
            "pos": [ship.posX, ship.posY - 50],
            "opacity": 255,
            "timer": 3.0
        })
        messages.append({
            "text": f"Turbina mejorada: Nivel {ship.turbina_boost}",
            "pos": [ship.posX, ship.posY - 90],
            "opacity": 255,
            "timer": 2.0
        })



