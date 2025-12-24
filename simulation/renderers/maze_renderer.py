"""Renderizador para o labirinto e heatmap de distâncias"""

import pygame
from maze_solver import is_wall
from simulation.ui.theme import Theme
from simulation.ui.ui_layout import UILayout


class MazeRenderer:
    """Gerencia a renderização do labirinto com heatmap de distâncias"""
    
    def __init__(self, screen):
        self.screen = screen
        self.maze_width = 0
        self.maze_height = 0
        self.cell_size = 0
        self.maze_left_margin = 0
        self.maze_top_margin = 0
        self.cell_border = 4
        self.draw_num = True
        self.maze_coverage = 0.8
        self.font_coverage = 0.35
        self.num_font = None
        self.cached_numbers = {}
    
    def update_dimensions(self, maze_width, maze_height):
        """Recalcula todas as dimensões visuais do labirinto baseado no tamanho"""
        self.maze_width = maze_width
        self.maze_height = maze_height
        
        self.maze_coverage = 0.8
        self.font_coverage = 0.35
        self.cell_border = 4
        self.draw_num = True
        
        # Adapta escala para quando o labirinto é muito grande
        biggest_maze_axis = max(maze_width, maze_height)
        if biggest_maze_axis > UILayout.MAZE_LARGE_THRESHOLD:
            self.maze_coverage = 1
            self.font_coverage += (biggest_maze_axis - 15) * 0.01
            if biggest_maze_axis > UILayout.MAZE_VERY_LARGE_THRESHOLD:
                self.cell_border = 2
                self.draw_num = False
                if biggest_maze_axis > UILayout.MAZE_HUGE_THRESHOLD:
                    self.cell_border = 1
        
        # Calcula tamanho da célula baseado no tamanho do labirinto e da tela
        self.cell_size = min(
            UILayout.USABLE_SCREEN_WIDTH * self.maze_coverage // maze_width,
            UILayout.SCREEN_HEIGHT * self.maze_coverage // maze_height
        )
        
        # Centraliza
        ui_width = UILayout.SCREEN_WIDTH - UILayout.USABLE_SCREEN_WIDTH
        maze_size = (maze_width * self.cell_size, maze_height * self.cell_size)
        self.maze_left_margin = ui_width + (UILayout.USABLE_SCREEN_WIDTH - maze_size[0]) // 2
        self.maze_top_margin = (UILayout.SCREEN_HEIGHT - maze_size[1]) // 2
        
        # Recalcula fonte de números para representar distâncias
        font_size = int(self.cell_size * self.font_coverage)
        self.num_font = pygame.freetype.SysFont("Consolas", font_size)
        
        # Recria cache de números pré-renderizados
        self._create_number_cache(maze_width, maze_height)
    
    def _create_number_cache(self, maze_width, maze_height):
        """Cria cache de números pré-renderizados para melhor performance"""
        self.cached_numbers = {}
        for i in range(max(maze_height, maze_width) * 2):
            text_surface, _ = self.num_font.render(str(i), fgcolor="black")
            self.cached_numbers[i] = text_surface
    
    def get_heatmap_color(self, distance, max_dist):
        """Calcula cor do heatmap baseado na distância"""
        # Limita variação de cor a cada célula para manter gradiente suave
        color_ratio = max(max_dist, 1 / UILayout.MAX_COLOR_VARIANCE)
        t = max(0, min(1, distance / color_ratio))

        # 4 pontos de controle de cor
        c_red = Theme.HEAT_NEAR      # Perto (Vermelho)
        c_yellow = Theme.HEAT_MID    # Médio-Perto (Amarelo claro)
        c_white = Theme.HEAT_NEUTRAL # Centro (Neutro/Cinza)
        c_blue = Theme.HEAT_FAR      # Longe (Azul Escuro)
        
        if t < 0.33:
            # 0% a 33%: Vermelho -> Amarelo
            return c_red.lerp(c_yellow, t / 0.33)
        elif t < 0.66:
            # 33% a 66%: Amarelo -> Cinza (Neutraliza o verde)
            return c_yellow.lerp(c_white, (t - 0.33) / 0.33)
        else:
            # 66% a 100%: Cinza -> Azul
            return c_white.lerp(c_blue, (t - 0.66) / 0.34)
    
    def draw(self, known_maze, real_maze, distances, start, goal):
        """Desenha o labirinto com heatmap de distâncias"""
        max_distance = max(
            distances[x][y]
            for x in range(len(distances))
            for y in range(len(distances[x]))
            if distances[x][y] != float('inf')
        )

        # Desenha células do labirinto
        for row in range(self.maze_height):
            for col in range(self.maze_width):
                self._draw_cell(row, col, known_maze, real_maze, distances, 
                               start, goal, max_distance)
    
    def _draw_cell(self, row, col, known_maze, real_maze, distances, 
                   start, goal, max_distance):
        """Desenha uma célula individual do labirinto"""
        # Determina cor da célula
        known_wall = is_wall((row, col), known_maze)
        
        if known_wall:
            cell_color = Theme.WALL_KNOWN
        elif (row, col) == goal:
            cell_color = Theme.GOAL
        elif (row, col) == start:
            cell_color = Theme.START
        else:
            cell_dist = distances[row][col]
            if cell_dist == float('inf'):
                cell_color = Theme.WALL_UNKNOWN
            else:
                cell_color = self.get_heatmap_color(cell_dist, max_distance)

        # Desenha célula
        square_cell = pygame.Rect(
            self.maze_left_margin + col * self.cell_size,
            self.maze_top_margin + row * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, cell_color, square_cell)

        # Desenha outline para parede desconhecida
        if not known_wall and is_wall((row, col), real_maze):
            pygame.draw.rect(self.screen, pygame.Color(80, 80, 80), 
                           square_cell, width=self.cell_border)

        # Desenha valor da distância na célula
        if self.draw_num:
            self._draw_distance_number(row, col, distances, known_maze, square_cell)
    
    def _draw_distance_number(self, row, col, distances, known_maze, square_cell):
        """Desenha o número da distância em uma célula"""
        cell_dist = distances[row][col]
        if cell_dist != float('inf') and not is_wall((row, col), known_maze):
            text_surface = self.cached_numbers.get(cell_dist)
            if text_surface is None:  # Fallback para números fora do cache
                text_surface, _ = self.num_font.render(str(cell_dist), fgcolor="black")
            text_rect = text_surface.get_rect(center=square_cell.center)
            self.screen.blit(text_surface, text_rect)
    
    def get_cell_position(self, row, col):
        """Retorna a posição em pixels de uma célula do labirinto"""
        x_pos = self.maze_left_margin + col * self.cell_size
        y_pos = self.maze_top_margin + row * self.cell_size
        return (x_pos, y_pos)
