import pygame

def apply_crt_effect(surface, scanline_alpha=40, vignette_strength=0.4, glow_strength=16, glow_radius=8):
    """
    Ultra-fast retro effect: scanlines + vignette (vectorized vignette) + optional glow.
    """
    width, height = surface.get_size()
    crt_surface = surface.copy()
    # --- Glow effect (simple blur) ---
    if glow_strength > 0 and glow_radius > 0:
        glow = pygame.Surface((width, height), pygame.SRCALPHA)
        glow.blit(surface, (0, 0))
        for i in range(1, glow_radius+1, 2):
            alpha = max(1, glow_strength // (i+1))
            blurred = pygame.transform.smoothscale(glow, (max(1, width//(i+1)), max(1, height//(i+1))))
            blurred = pygame.transform.smoothscale(blurred, (width, height))
            blurred.set_alpha(alpha)
            crt_surface.blit(blurred, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    # --- Scanlines ---
    scanline = pygame.Surface((width, 1), pygame.SRCALPHA)
    scanline.fill((0, 0, 0, scanline_alpha))
    for y in range(0, height, 2):
        crt_surface.blit(scanline, (0, y))
    # --- Fast vignette using alpha gradient only at borders ---
    border = int(min(width, height) * 0.12)
    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    vignette.fill((0,0,0,0))
    # Top and bottom
    for y in range(border):
        alpha = int(255 * vignette_strength * (1 - y / border))
        pygame.draw.line(vignette, (0,0,0,alpha), (0, y), (width-1, y))
        pygame.draw.line(vignette, (0,0,0,alpha), (0, height-1-y), (width-1, height-1-y))
    # Left and right
    for x in range(border):
        alpha = int(255 * vignette_strength * (1 - x / border))
        pygame.draw.line(vignette, (0,0,0,alpha), (x, 0), (x, height-1))
        pygame.draw.line(vignette, (0,0,0,alpha), (width-1-x, 0), (width-1-x, height-1))
    crt_surface.blit(vignette, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
    return crt_surface
