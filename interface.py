import pygame
import pygame.freetype as freetype
from maze_solver import is_wall

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_COLOR_SATUR = 80
CELL_COLOR_VALUE = 100
MAX_COLOR_VARIANCE = 0.025

class Interface:
    def __init__(self, maze_height, maze_width , real_maze):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Calcula tamanho da célula baseado no tamanho do labirinto e da tela
        self.cell_size = min(SCREEN_WIDTH * 0.8 // maze_width, SCREEN_HEIGHT * 0.8 // maze_height)

        # Carrega e escala a imagem do mouse
        self.mouse_image = pygame.transform.smoothscale(pygame.image.load('assets/mouse.png'), (self.cell_size*0.8, self.cell_size*0.8))

        self.real_maze = real_maze
        self.maze_width = maze_width
        self.maze_height = maze_height
        maze_size = (maze_width * self.cell_size, maze_height * self.cell_size)
        self.maze_left_margin = (SCREEN_WIDTH - maze_size[0]) // 2 # Centraliza horizontalmente
        # Centraliza verticalmente (topo do labirinto)
        self.maze_top_margin = (SCREEN_HEIGHT - maze_size[1]) // 2

    def draw_debug_text(self, text, font_size=20, y_pos=10, color="black"):
        position = (10, y_pos)
        font = pygame.freetype.SysFont(None, font_size)
        text_surface, _ = font.render(text, fgcolor=color)
        self.screen.blit(text_surface, position)

    def draw_debug_maze(self, known_maze, font_size=36, color="black"):
        line_pos = self.maze_height * font_size
        position = (1000, line_pos)
        font = pygame.freetype.SysFont(None, font_size)

        for row in range(self.maze_height):
            for column in range(self.maze_width):
                if is_wall((row, column), known_maze):
                    text_surface, _ = font.render("#", fgcolor=color)
                else:
                    text_surface, _ = font.render(".", fgcolor=color)
                self.screen.blit(text_surface, (position[0] + row * font_size, position[1] - column * font_size))

    def draw_debug_distances(self, distances, color="black"):
        font_size = self.cell_size // 4
        position = (1000, 20)
        font = pygame.freetype.SysFont(None, font_size)

        for row in range(min(self.maze_height, len(distances))):
            for column in range(min(self.maze_width, len(distances[0]) if row < len(distances) else 0)):
                if distances[row][column] == float('inf'):
                    text_surface, _ = font.render("#", fgcolor=color)
                else:
                    text_surface, _ = font.render(str(int(distances[row][column])), fgcolor=color)
                self.screen.blit(text_surface, (position[0] + column * font_size * 1.5, position[1] + row * font_size * 1.5))
    def draw_mouse(self, pos, direction):
        # Rotaciona imagem de acordo com direção
        # Pygame rotaciona no sentido anti-horário e a imagem começa apontando para o norte
        angle = 0
        match direction:
            case "N":
                angle = 0
            case "E":
                angle = -90
            case "S":
                angle = 180
            case "W":
                angle = 90
        rotated_image = pygame.transform.rotate(self.mouse_image, angle)

        # Posição atual do mouse
        x_pos = self.maze_left_margin + pos[1]*self.cell_size
        y_pos = self.maze_top_margin + pos[0]*self.cell_size
        # Desenha o mouse com um pequeno offset para centralizá-lo já que não ocupa toda a célula
        self.screen.blit(rotated_image, (x_pos + self.cell_size*0.1, y_pos + self.cell_size*0.1), pygame.Rect(0, 0, self.cell_size, self.cell_size))

    def get_heatmap_color(self, distance, max_dist):
        # Limita variação de cor a cada célula para manter gradiente suave
        color_ratio = max(max_dist, 1 / MAX_COLOR_VARIANCE)
        t = max(0, min(1, distance/color_ratio))

        # 4 pontos de controle de cor
        c_red    = pygame.Color(255, 50, 50)   # Perto (Vermelho)
        c_yellow = pygame.Color(255, 255, 100) # Médio-Perto (Amarelo claro)
        c_white  = pygame.Color(200, 200, 200) # Centro (Neutro/Cinza)
        c_blue   = pygame.Color(30, 30, 150)   # Longe (Azul Escuro)
        if t < 0.33:
            # 0% a 33%: Vermelho -> Amarelo
            return c_red.lerp(c_yellow, t / 0.33)
        elif t < 0.66:
            # 33% a 66%: Amarelo -> Cinza (Neutraliza o verde)
            return c_yellow.lerp(c_white, (t - 0.33) / 0.33)
        else:
            # 66% a 100%: Cinza-> Azul
            return c_white.lerp(c_blue, (t - 0.66) / 0.34)
        
    def draw_maze(self, known_maze, distances, pos, direction, goal):
        # Limpa tela
        self.screen.fill("white")

        max_distance = max(
            distances[x][y] 
            for x in range(len(distances))
            for y in range(len(distances[x]))
            if distances[x][y] != float('inf')
        )

        # Desenha células do labirinto
        cell_color = pygame.Color('lightgray')
        for row in range(self.maze_height):
            for col in range(self.maze_width):
                # Controle de cor com base no tipo e peso da celula: 
                known_wall = is_wall((row, col), known_maze)
                if known_wall:
                    cell_color = pygame.Color(0, 0, 0)  # Preto para paredes
                elif (row, col) == goal:
                    cell_color = pygame.Color(70, 170, 50)  # Verde claro para a saída
                # Caminho livre com peso (distância para a saída)
                else:
                    distance = distances[row][col]
                    if distance == float('inf'):
                        cell_color = pygame.Color(230, 230, 230)  # Cinza claro para células não alcançáveis
                    else:
                        cell_color = self.get_heatmap_color(distance, max_distance)

                # Desenha célula, Rect(left, top, width, height) -> Retângulo.
                square_cell = pygame.Rect(self.maze_left_margin + col*self.cell_size, self.maze_top_margin + row*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, cell_color, square_cell)

                # Desenha outline preto para parede desconhecida
                if not known_wall and is_wall((row, col), self.real_maze):
                    pygame.draw.rect(self.screen, pygame.Color(80, 80, 80), square_cell, width=4)

                # Desenha valor da distância na célula
                if distances[row][col] != float('inf') and not is_wall((row, col), known_maze):
                    font_size = self.cell_size // 4
                    font = pygame.freetype.SysFont(None, font_size)
                    text_surface, _ = font.render(str(int(distances[row][col])), fgcolor="black")
                    text_rect = text_surface.get_rect(center=square_cell.center)
                    self.screen.blit(text_surface, text_rect)

        # Desenha mouse (robô)
        self.draw_mouse(pos, direction)

        # DEBUG
        self.draw_debug_text(f"Posição: {pos}, Direção: {direction}")
        #self.draw_debug_distances(distances)

        # Desenha tela atualizada
        pygame.display.flip()