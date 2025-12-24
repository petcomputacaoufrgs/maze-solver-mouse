"""Renderizador para o mouse/robô no labirinto"""

import pygame
from simulation.ui.ui_layout import UILayout


class MouseRenderer:
    """Gerencia a renderização e rotação do mouse no labirinto"""
    
    def __init__(self, screen):
        self.screen = screen
        self.mouse_image = None
        self.cell_size = 0
    
    def load_and_scale_mouse(self, cell_size):
        """Carrega e escala a imagem do mouse baseado no tamanho da célula"""
        self.cell_size = cell_size
        mouse_size = int(cell_size * UILayout.MOUSE_SIZE_RATIO)
        self.mouse_image = pygame.transform.smoothscale(
            pygame.image.load('assets/mouse.png'),
            (mouse_size, mouse_size)
        )
    
    def draw(self, pos, direction, maze_left_margin, maze_top_margin):
        """Desenha o mouse na posição especificada com a direção correta"""
        # Rotaciona imagem de acordo com direção
        # Pygame rotaciona no sentido anti-horário e a imagem começa apontando para o norte
        angle = self._get_rotation_angle(direction)
        rotated_image = pygame.transform.rotate(self.mouse_image, angle)

        # Posição atual do mouse
        x_pos = maze_left_margin + pos[1] * self.cell_size
        y_pos = maze_top_margin + pos[0] * self.cell_size
        
        # Desenha o mouse com um pequeno offset para centralizá-lo
        offset = self.cell_size * UILayout.MOUSE_OFFSET_RATIO
        self.screen.blit(
            rotated_image,
            (x_pos + offset, y_pos + offset),
            pygame.Rect(0, 0, self.cell_size, self.cell_size)
        )
    
    def _get_rotation_angle(self, direction):
        """Retorna o ângulo de rotação baseado na direção"""
        angles = {
            "N": 0,
            "E": -90,
            "S": 180,
            "W": 90
        }
        return angles.get(direction, 0)
