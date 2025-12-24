import pygame

class Theme:
    # Cores de Fundo
    CANVAS_BG = (250, 240, 215)  # Fundo principal
    SIDEBAR_BG = (230, 220, 200) # Fundo da área de controles
    
    # Cores de Estado do Labirinto
    WALL_KNOWN = (0, 0, 0)
    WALL_UNKNOWN = (80, 80, 80)
    GOAL = (70, 170, 50)
    START = (180, 180, 180)
    
    # Cores de Calor (Heatmap) baseadas no get_heatmap_color original
    HEAT_NEAR = pygame.Color(255, 50, 50)   
    HEAT_MID = pygame.Color(255, 255, 100)
    HEAT_NEUTRAL = pygame.Color(200, 200, 200)
    HEAT_FAR = pygame.Color(75, 75, 245)

    # Estilo de UI
    BTN_PRIMARY = (50, 50, 200)
    BTN_TEXT = (255, 255, 255)
    BTN_BLUE = (50, 50, 200)
    BTN_RED = (200, 50, 50)
    BTN_GREEN = (50, 200, 50)

    def hover_col(color):
        """Retorna uma cor ligeiramente mais clara para hover effects."""
        return tuple(min(255, c + 30) for c in color)