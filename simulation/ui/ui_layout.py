"""Constantes de layout para a interface do usuário"""

class UILayout:
    """Configurações de layout e dimensionamento da interface"""
    
    # Dimensões da tela
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    USABLE_SCREEN_WIDTH = 890
    UI_LEFT_MARGIN = 25
    
    # Dimensões de botões
    ICON_BTN_SIZE = 50
    BTN_WIDTH = 150
    BTN_HEIGHT = 40
    SMALL_BTN_WIDTH = 60
    
    # Dimensões de inputs
    SIZE_INPUT_WIDTH = 45
    SEED_INPUT_WIDTH = 90
    
    # Espaçamento
    SPACING = 15
    LABEL_WIDTH = 20
    
    # Posições verticais
    CONTROL_START_Y = 180
    SPEED_SLIDER_OFFSET_Y = 80
    MAZE_GEN_OFFSET_Y = 200
    SIZE_INPUTS_OFFSET_Y = -45
    STEPS_INFO_Y = 130
    TITLE_TOP_MARGIN_RATIO = 0.25
    
    # Logo
    LOGO_SIZE = (100, 100)
    LOGO_MARGIN = 5
    
    # Captions
    CAPTION_BOTTOM_MARGIN = 20
    CAPTION_SPACING = 20
    CAPTION_SQUARE_SIZE_OFFSET = 5
    CAPTION_ICON_TEXT_SPACING = 5
    
    # Labirinto
    CELL_COLOR_SATUR = 80
    CELL_COLOR_VALUE = 100
    MAX_COLOR_VARIANCE = 0.025
    
    # Adaptação para labirintos grandes
    MAZE_LARGE_THRESHOLD = 20
    MAZE_VERY_LARGE_THRESHOLD = 30
    MAZE_HUGE_THRESHOLD = 70
    
    # Mouse
    MOUSE_SIZE_RATIO = 0.8
    MOUSE_OFFSET_RATIO = 0.1
