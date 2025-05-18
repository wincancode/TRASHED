import os

#needed constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Base directory of the project

# Game settings
GAME_WIDTH = 800  # Width of the game window in pixels
GAME_HEIGHT = 600  # Height of the game window in pixels
GAME_FPS = 60  # Frames per second for the game

#Glow settings
GLOW_INTENSITY = 50  # Glow effect intensity for the ship
GLOW_PROPAGATION = 4  # Propagation speed of the glow effect
GLOW_ALPHA = 255  # Initial alpha value for the glow effect
GLOW_ALPHA_DECAY = 50  # Decay rate of the alpha value for the glow effect
GLOW = False  # Enable glow effect for the ship

# Colors
WHITE = (255, 255, 255)  # RGB color for white
BLACK = (0, 0, 0)  # RGB color for black
RED = (255, 0, 0)  # RGB color for red
GREEN = (0, 255, 0)  # RGB color for green
BLUE = (0, 0, 255)  # RGB color for blue
YELLOW = (255, 255, 0)  # RGB color for yellow

color_map = {
    "green": GREEN,
    "red": RED,
    "blue": BLUE,
    "yellow": YELLOW
}

# Ship constants 
SHIP_BASE_SPEED = 80  # Base speed of the ship in units per second
SHIP_BASE_ACCELERATION = 100   # Base acceleration of the ship in units per second
SHIP_DEACCELERATION_RATE = 40 
SHIP_BASE_TURN_RATE = 1.2  # Base turn rate of the ship in radians per second
SHIP_BASE_TURN_ACCELERATION = 1.2  # Base turn acceleration of the ship in radians per second
SHIP_DEFAULT_SPRITE = os.path.join(BASE_DIR,"..","assets","sprites", "ship.png")  # Default sprite for the ship
SHIP_LIVES = 3  # Number of lives for the ship

# Shot constants
SHOT_BASE_SPEED = 300  # Base speed of the shot in units per second
SHOT_BASE_DAMAGE = 1  # Base damage of the shot
SHOT_DEFAULT_SPRITE = os.path.join(BASE_DIR,"..","assets","sprites", "shoot1.png")  
SHOT_LASER_1_SPRITE = os.path.join(BASE_DIR,"..","assets","sprites", "shoot2.png") 
SHOT_LASER_2_SPRITE = os.path.join(BASE_DIR,"..","assets","sprites", "shoot3.png")
SHOT_LASER_3_SPRITE = os.path.join(BASE_DIR,"..","assets","sprites", "shoot4.png")
SHOT_LASER_4_SPRITE = os.path.join(BASE_DIR,"..","assets","sprites", "shoot5.png")

# Ship sprite dimensions
SHIP_WIDTH = 30  # Width of the ship in pixels
SHIP_HEIGHT = 30  # Height of the ship in pixels

# Asteroid  constants
ASTEROID_BASE_SPEED = 5  # Base speed of the asteroid in units per second
ASTEROID_BASE_ACCELERATION = 0.5  # Base acceleration of the asteroid in units per second
ASTEROID_VARIANCE = 0.5  # Variance in speed for asteroids
ASTEROID_DEFAULT_SPRITE = os.path.join(BASE_DIR,"..","assets","sprites", "asteroid.png")  # Default sprite for the asteroid

# Powerup asset image paths
SHIELD_UPGRADE_ICON = os.path.join(BASE_DIR, "..", "assets", "sprites", "ShieldUpgrade.png")
DAMAGE_UP_ICON = os.path.join(BASE_DIR, "..", "assets", "sprites", "DamageUp.png")
NUKE_ICON = os.path.join(BASE_DIR, "..", "assets", "sprites", "Nuke.png")
TURBINAS_ICON = os.path.join(BASE_DIR, "..", "assets", "sprites", "Turbinas.png")



