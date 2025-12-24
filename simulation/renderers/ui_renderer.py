"""Renderizador para elementos de UI (títulos, legendas, labels)"""

import pygame
import pygame.freetype as freetype
from simulation.ui.theme import Theme
from simulation.ui.ui_layout import UILayout


class UIRenderer:
    """Gerencia a renderização de elementos de interface (título, legendas, etc)"""
    
    def __init__(self, screen, logo_image):
        self.screen = screen
        self.logo_image = logo_image
        self.caption_icons = []
        self.caption_texts = []
    
    def prepare_captions(self):
        """Prepara os elementos de legenda do labirinto"""
        caption_texts = []
        caption_icons = []
        caption_font = pygame.freetype.SysFont(None, 20)
        font_height = caption_font.get_sized_height()
        captions = ["Parede Conhecida", "Parede Desconhecida", "Entrada", "Objetivo"]

        occupied_space = len(captions) * font_height + UILayout.CAPTION_SPACING
        margin_top = UILayout.SCREEN_HEIGHT - occupied_space - UILayout.CAPTION_BOTTOM_MARGIN
        aux_margin_top = margin_top

        # Caption Icons
        colors = [
            Theme.WALL_KNOWN,
            Theme.WALL_UNKNOWN,
            Theme.START,
            Theme.GOAL
        ]
        widths = [0, 4, 0, 0]  # 0 para preenchido, > 0 para outline
        square_size = font_height - UILayout.CAPTION_SQUARE_SIZE_OFFSET
        
        for color, width in zip(colors, widths):
            caption_icons.append((
                color,
                pygame.Rect(UILayout.UI_LEFT_MARGIN, aux_margin_top, 
                          square_size, square_size),
                width
            ))
            aux_margin_top += caption_font.get_sized_height()

        # Captions
        for caption in captions:
            text_surface, _ = caption_font.render(caption, fgcolor="black")
            text_rect = pygame.Rect(
                UILayout.UI_LEFT_MARGIN + square_size + UILayout.CAPTION_ICON_TEXT_SPACING,
                margin_top,
                text_surface.get_width(),
                text_surface.get_height()
            )
            caption_texts.append((text_surface, text_rect))
            margin_top += caption_font.get_sized_height()
        
        self.caption_icons = caption_icons
        self.caption_texts = caption_texts
        return caption_icons, caption_texts
    
    def draw_captions(self):
        """Desenha as legendas do labirinto"""
        for icon in self.caption_icons:
            pygame.draw.rect(self.screen, icon[0], icon[1], width=icon[2])
        for text_surface, text_rect in self.caption_texts:
            self.screen.blit(text_surface, text_rect)
    
    def draw_title(self):
        """Desenha título e logo"""
        self.screen.blit(self.logo_image, (0, 0))
        left_margin = self.logo_image.get_width() + UILayout.LOGO_MARGIN
        top_margin = int(self.logo_image.get_height() * UILayout.TITLE_TOP_MARGIN_RATIO)

        title_font = pygame.freetype.SysFont(None, 36)
        title_surface, _ = title_font.render("Mico-Leão", fgcolor="brown")
        subtitle_font = pygame.freetype.SysFont(None, 24)
        subtitle_surface, _ = subtitle_font.render("Algoritmo de Navegação", fgcolor="black")

        subtitle_rect = pygame.Rect(
            left_margin,
            top_margin + title_surface.get_height() + 10,
            subtitle_surface.get_width(),
            subtitle_surface.get_height()
        )
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        text_center = left_margin + subtitle_surface.get_width() // 2 - title_surface.get_width() // 2
        title_rect = pygame.Rect(
            text_center,
            top_margin,
            title_surface.get_width(),
            title_surface.get_height()
        )
        self.screen.blit(title_surface, title_rect)
    
    def draw_steps_info(self, steps_taken, ideal_steps):
        """Desenha informações sobre passos tomados e passos ideais"""
        steps_font = pygame.freetype.SysFont(None, 20)
        steps_text = f"Passos: {steps_taken}  Ideal: {ideal_steps}"
        steps_surface, _ = steps_font.render(steps_text, fgcolor="black")
        steps_y = UILayout.STEPS_INFO_Y
        self.screen.blit(steps_surface, (UILayout.UI_LEFT_MARGIN, steps_y))
    
    def draw_maze_generation_labels(self, width_input, height_input):
        """Desenha labels para controles de geração de labirinto"""
        label_font = pygame.freetype.SysFont(None, 20)
        label_surface, _ = label_font.render("Labirinto:", fgcolor="black")
        label_y = width_input.rect.y - 25
        self.screen.blit(label_surface, (UILayout.UI_LEFT_MARGIN, label_y))
        
        # Labels para largura e altura
        small_label_font = pygame.freetype.SysFont(None, 18)
        width_label, _ = small_label_font.render("L:", fgcolor="black")
        height_label, _ = small_label_font.render("A:", fgcolor="black")
        
        # Posiciona ao lado dos respectivos campos
        self.screen.blit(width_label, (
            width_input.rect.x - width_label.get_width() - 5,
            width_input.rect.y + (width_input.rect.height - width_label.get_height()) // 2
        ))
        self.screen.blit(height_label, (
            height_input.rect.x - height_label.get_width() - 5,
            height_input.rect.y + (height_input.rect.height - height_label.get_height()) // 2
        ))
