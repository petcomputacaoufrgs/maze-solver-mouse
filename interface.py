import pygame
import pygame.freetype as freetype
from maze_solver import is_wall

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 100 # Pixels
CELL_COLOR_SATUR = 100
CELL_COLOR_VALUE = 100

class Interface:
    def __init__(self, maze_width, maze_height):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Carrega e escala a imagem do mouse
        self.mouse_image = pygame.transform.smoothscale(pygame.image.load('assets/mouse.png'), (CELL_SIZE*0.8, CELL_SIZE*0.8))

        self.maze_width = maze_width
        self.maze_height = maze_height
        maze_size = (maze_width * CELL_SIZE, maze_height * CELL_SIZE)
        self.maze_left_margin = (SCREEN_WIDTH - maze_size[0]) // 2 # Centraliza o labirinto
        self.maze_top_margin = (SCREEN_HEIGHT - maze_size[1]) // 2 + maze_size[1] // 2 # Pois pygame usa origem no canto superior

    def draw_debug_text(self, text, font_size=20, y_pos=10, color="black"):
        position = (10, y_pos)
        font = pygame.freetype.SysFont(None, font_size)
        text_surface, _ = font.render(text, fgcolor=color)
        self.screen.blit(text_surface, position)

    def draw_debug_maze(self, known_maze, font_size=36, color="black"):
        line_pos = self.maze_height * font_size
        position = (1000, line_pos)
        font = pygame.freetype.SysFont(None, font_size)

        for x in range(self.maze_width - 1):
            for y in range(self.maze_height - 1):
                if is_wall((x, y), known_maze):
                    text_surface, _ = font.render("#", fgcolor=color)
                else:
                    text_surface, _ = font.render(".", fgcolor=color)
                self.screen.blit(text_surface, (position[0] + x * font_size, position[1] - y * font_size))

    def draw_debug_distances(self, distances, font_size=36, color="black"):
        line_pos = self.maze_height * font_size + 50
        position = (1000, line_pos)
        font = pygame.freetype.SysFont(None, font_size)

        for x in range(self.maze_width - 1):
            for y in range(self.maze_height - 1):
                text_surface, _ = font.render(str(distances[x][y]), fgcolor=color)
                self.screen.blit(text_surface, (position[0] + x * font_size * 2, position[1] - y * font_size * 2))

    def draw_mouse(self, pos, direction):
        # Rotaciona imagem de acordo com direção
        # Pygame rotaciona no sentido anti-horário
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
        x_pos = self.maze_left_margin + pos[0]*CELL_SIZE
        y_pos = self.maze_top_margin - pos[1]*CELL_SIZE
        # Desenha o mouse com um pequeno offset para centralizá-lo já que não ocupa toda a célula
        self.screen.blit(rotated_image, (x_pos + CELL_SIZE*0.1, y_pos + CELL_SIZE*0.1), pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE))

    def draw_maze(self, known_maze, distances, pos, direction):
        # Limpa tela
        self.screen.fill("white")

        cell_color = pygame.Color('lightgray')

        for x in range(self.maze_width - 1):
            for y in range(self.maze_height - 1):
                # Controle de cor com base no tipo e peso da celula: 
                # Parede
                if is_wall((x, y), known_maze):
                    cell_color.hsva = (0, 0, 50)  # Dark gray
                # Caminho livre com peso (distância para a saída)
                else:
                    # Começa em 235 (azul), se for menos que 180 subtrai 120 (pula verde) 
                    # 235 - 120 = 115, converter distancia para valor entre 0 e 115 com regra de três
                    distance = distances[x][y]
                    max_distance = self.maze_width + self.maze_height
                    if distance == float('inf'):
                        cell_color.hsva = (0, 0, 90)  # Light gray para células não alcançáveis
                    else:
                        color_hue = distance * 115 / max_distance
                        cell_color.hsva = (color_hue, CELL_COLOR_SATUR, CELL_COLOR_VALUE)

                # Desenha célula, Rect(left, top, width, height) -> Retângulo.
                square_cell = pygame.Rect(self.maze_left_margin + x*CELL_SIZE, self.maze_top_margin - y*CELL_SIZE,CELL_SIZE, CELL_SIZE)

                pygame.draw.rect(self.screen, cell_color, square_cell)
        
        # Desenha mouse (robô)
        self.draw_mouse(pos, direction)

        # DEBUG
        self.draw_debug_text(f"Posição: {pos}, Direção: {direction}")
        self.draw_debug_distances(distances)

        # Desenha tela atualizada
        pygame.display.flip()