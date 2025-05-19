import pygame
import math

def draw_crt_effect(surface):
    """
    Aplica un filtro CRT avanzado al surface dado, inspirado en el artículo de Chris Greening.
    - Scanlines: líneas negras cada 2 píxeles, alpha 120
    - Viñeta: borde oscuro
    - Distorsión de onda senoidal (barrido horizontal)
    - Glitch RGB: separa canales de color para simular desplazamiento
    """
    width, height = surface.get_size()
    # --- Glitch RGB ---
    arr = pygame.surfarray.pixels3d(surface)
    temp = arr.copy()
    offset = 3  # Desplazamiento de glitch
    for y in range(0, height, 8):
        arr[offset:width, y, 0] = temp[0:width-offset, y, 0]  # Rojo
        arr[0:width-offset, y, 2] = temp[offset:width, y, 2]  # Azul
    del arr
    del temp

    # --- Distorsión de onda senoidal ---
    distorted = pygame.Surface((width, height)).convert_alpha()
    for y in range(height):
        shift = int(4 * math.sin(2 * math.pi * y / 64))  # Amplitud y frecuencia
        distorted.blit(surface, (shift, y), area=pygame.Rect(0, y, width, 1))
    surface.blit(distorted, (0, 0))

    # --- Scanlines ---
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 2):
        pygame.draw.line(overlay, (0, 0, 0, 120), (0, y), (width, y))
    surface.blit(overlay, (0, 0))

    # --- Viñeta ---
    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    vignette_strength = 180
    vignette_steps = 50
    for i in range(vignette_steps):
        alpha = int(vignette_strength * (i / vignette_steps))
        pygame.draw.rect(
            vignette,
            (0, 0, 0, alpha),
            (i, i, width - 2 * i, height - 2 * i),
            1
        )
    surface.blit(vignette, (0, 0))

# Efectos aplicados:
# - Glitch RGB: separa canales rojo y azul en líneas alternas.
# - Distorsión senoidal: barre la imagen horizontalmente en ondas.
# - Scanlines: líneas negras horizontales.
# - Viñeta: oscurece los bordes.
# Inspirado en: https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1
