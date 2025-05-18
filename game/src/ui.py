import pygame

def draw_text(screen, text, pos, color, font_size=36, opacity=255, center=False):
    """Dibuja texto en la pantalla."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(opacity)
    if center:
        text_rect = text_surface.get_rect(center=pos)
    else:
        text_rect = text_surface.get_rect(topleft=pos)
    screen.blit(text_surface, text_rect)

def draw_progress_bar(screen, x, y, width, height, progress, max_progress, color, bg_color):
    """Dibuja una barra de progreso en la pantalla."""
    # Dibujar el fondo de la barra
    pygame.draw.rect(screen, bg_color, (x, y, width, height))
    
    # Calcular el ancho de la barra de progreso
    progress_width = int((progress / max_progress) * width)
    
    # Dibujar la barra de progreso
    pygame.draw.rect(screen, color, (x, y, progress_width, height))