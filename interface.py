import pygame
import pygame.freetype as freetype
from maze_solver import is_wall
import ui_elements as ui
import random

# Constantes
SCREEN_WIDTH = 1280
USABLE_SCREEN_WIDTH = 890
SCREEN_HEIGHT = 720
CELL_COLOR_SATUR = 80
CELL_COLOR_VALUE = 100
MAX_COLOR_VARIANCE = 0.025
UI_LEFT_MARGIN = 25

class Interface:
    def __init__(self, maze_height, maze_width, simulation):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.sim = simulation
        self.real_maze = simulation.real_maze
        self.ui_width = SCREEN_WIDTH - USABLE_SCREEN_WIDTH
        
        # Inicializa dimensões do labirinto
        self.update_maze_dimensions(maze_width, maze_height)
        self.logo_image = pygame.transform.smoothscale(pygame.image.load('assets/logo_pet.png'), (100, 100))
        
        # Carrega ícones dos botões
        self.play_icon = pygame.image.load('assets/play_btn.png')
        self.pause_icon = pygame.image.load('assets/pause_btn.png')
        self.reset_icon = pygame.image.load('assets/reset_btn.png')
        self.restart_icon = pygame.image.load('assets/restart_btn.png')

        # Prepara UI
        self.caption_icons, self.caption_texts = self.prepare_captions()

        self.buttons = []
        btn_width = 150
        btn_height = 40
        icon_btn_size = 50
        start_y = 180 # Começa abaixo do título e da informação de passos
        btn_back_color = (50, 50, 200)
        btn_hover_color = (80, 80, 250)
        
        self.btn_restart = ui.IconButton(UI_LEFT_MARGIN, start_y, icon_btn_size, icon_btn_size,
                                       self.restart_icon, self.restart_icon, btn_back_color, btn_hover_color, self.restart_sim, initial_state=False)

        self.btn_reset = ui.IconButton(UI_LEFT_MARGIN + icon_btn_size + 10, start_y, icon_btn_size, icon_btn_size,
                                       self.reset_icon, self.reset_icon, btn_back_color, btn_hover_color, 
                                       self.reset_sim, initial_state=False)
        
        self.btn_play = ui.IconButton(UI_LEFT_MARGIN + (icon_btn_size + 10) * 2, start_y, icon_btn_size, icon_btn_size,
                                       self.play_icon, self.pause_icon, btn_back_color, btn_hover_color, 
                                       self.toggle_pause, initial_state=False)
        
        # Slider de Velocidade (Intervalo entre 10ms e 1000ms)
        self.speed_slider = ui.Slider(UI_LEFT_MARGIN + 10, start_y + 80, btn_width, 10, 1000, 100, "Intervalo")
        
        # Layout: [Novo Labirinto] [Seed Input] [Randomizar]
        maze_gen_y = start_y + 200
        seed_input_width = 90
        small_btn_width = 60
        size_input_width = 45
        spacing = 15
        label_width = 20  # Espaço para os labels L: e A:
        
        # Campos de largura e altura
        size_inputs_y = maze_gen_y - 45
        self.width_input = ui.InputBox(UI_LEFT_MARGIN + label_width, size_inputs_y, size_input_width, 30, "", str(maze_width))
        self.height_input = ui.InputBox(UI_LEFT_MARGIN + label_width + size_input_width + spacing + 15, size_inputs_y, size_input_width, 30, "", str(maze_height))
        
        self.btn_new_maze = ui.Button(UI_LEFT_MARGIN, maze_gen_y, small_btn_width, btn_height, 
                            "Gerar", (200, 50, 50), (250, 80, 80), self.new_maze)
        
        self.seed_input = ui.InputBox(UI_LEFT_MARGIN + small_btn_width + spacing, maze_gen_y, seed_input_width, btn_height, "", str(self.sim.maze_seed))
        
        self.btn_random_seed = ui.IconButton(UI_LEFT_MARGIN + small_btn_width + spacing + seed_input_width + spacing, maze_gen_y, icon_btn_size, btn_height,
                            self.restart_icon, self.restart_icon, (50, 200, 50), (80, 250, 80), self.randomize_seed, initial_state=False)

        self.ui_elements = [self.width_input, self.height_input, self.btn_new_maze, self.seed_input, self.btn_random_seed, self.btn_restart, self.btn_reset, self.btn_play, self.speed_slider]

    #Recalcula todas as dimensões visuais do labirinto baseado no tamanho
    def update_maze_dimensions(self, maze_width, maze_height):
        self.maze_width = maze_width
        self.maze_height = maze_height
        
        self.maze_coverage = 0.8
        self.font_coverage = 0.25
        self.cell_border = 4
        self.draw_num = True
        
        # Adapta escala para quando o labirinto é muito grande
        biggest_maze_axis = max(maze_width, maze_height)
        if (biggest_maze_axis > 20):
            self.maze_coverage = 1
            self.font_coverage += (biggest_maze_axis - 15) * 0.01
            if (biggest_maze_axis > 30):
                self.cell_border = 2
                if (biggest_maze_axis > 40):
                    self.draw_num = False
        
        # Calcula tamanho da célula baseado no tamanho do labirinto e da tela
        self.cell_size = min(USABLE_SCREEN_WIDTH * self.maze_coverage // maze_width, SCREEN_HEIGHT * self.maze_coverage // maze_height)
        
        # Centraliza
        maze_size = (maze_width * self.cell_size, maze_height * self.cell_size)
        self.maze_left_margin = self.ui_width + (USABLE_SCREEN_WIDTH - maze_size[0]) // 2
        self.maze_top_margin = (SCREEN_HEIGHT - maze_size[1]) // 2
        
        # Recalcula fonte de números para representar distâncias
        font_size = int(self.cell_size * self.font_coverage)
        self.num_font = pygame.freetype.SysFont(None, font_size)
        
        # Recria cache de números pré-renderizados
        self.cached_numbers = {}
        for i in range(max(maze_height, maze_width) * 2):
            text_surface, _ = self.num_font.render(str(i), fgcolor="black")
            self.cached_numbers[i] = text_surface
        
        # Reescala imagem do mouse
        self.mouse_image = pygame.transform.smoothscale(pygame.image.load('assets/mouse.png'), (self.cell_size*0.8, self.cell_size*0.8))

    def restart_sim(self):
        self.sim.reset_maze()
        # Toggle botão de play para pausado
        self.btn_play.set_state(False)
    
    def reset_sim(self):
        self.sim.reset_robot()
        # Toggle botão de play para pausado
        self.btn_play.set_state(False)

    def new_maze(self):
        # Lê o valor da seed do input box
        try:
            seed = int(self.seed_input.text) if self.seed_input.text else -1
        except ValueError:
            seed = -1  # Se não for um número válido, usa seed aleatória
        
        # Lê largura e altura, garante que sejam ímpares
        try:
            width = int(self.width_input.text) if self.width_input.text else 21
            height = int(self.height_input.text) if self.height_input.text else 21
        except ValueError:
            width, height = 21, 21
        
        # Garante que sejam ímpares
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        
        # Atualiza os campos com os valores ajustados
        self.width_input.text = str(width)
        self.width_input.txt_surface = self.width_input.font.render(self.width_input.text, True, (0, 0, 0))
        self.height_input.text = str(height)
        self.height_input.txt_surface = self.height_input.font.render(self.height_input.text, True, (0, 0, 0))
        
        self.sim.new_maze(seed, width, height)
        self.seed_input.text = str(self.sim.maze_seed)  # Atualiza o campo com a seed usada
        self.seed_input.txt_surface = self.seed_input.font.render(self.seed_input.text, True, (0, 0, 0))
        self.real_maze = self.sim.real_maze
        
        # Recalcula dimensões visuais do labirinto
        self.update_maze_dimensions(width, height)

        # Atualiza estado do botão para pausado
        self.btn_play.set_state(False)
    
    def randomize_seed(self):
        # Gera uma seed aleatória e atualiza o campo de texto
        new_seed = random.randint(0, 999999)
        self.seed_input.text = str(new_seed)
        self.seed_input.txt_surface = self.seed_input.font.render(self.seed_input.text, True, (0, 0, 0))
    
    def toggle_pause(self):
        self.sim.toggle_pause()
        # Atualiza estado visual do botão
        self.btn_play.set_state(self.sim.running)

    def prepare_captions(self):
        caption_texts = []
        caption_icons = [] # (color, rect, width=0)
        caption_font = pygame.freetype.SysFont(None, 20)
        font_height = caption_font.get_sized_height()
        captions = ["Parede Conhecida", "Parede Desconhecida", "Entrada", "Objetivo"]

        ocuppied_space = len(captions) * font_height + 20
        margin_top = SCREEN_HEIGHT - ocuppied_space - 20
        aux_margin_top = margin_top

        # Caption Icons
        colors= [
            pygame.Color("black"),
            pygame.Color(80,80,80),
            pygame.Color(200, 200, 200),
            pygame.Color(70, 170, 50)]       
        widths = [0, 4, 0, 0] # 0 para preenchido, > 0 para outline
        square_size = font_height - 5
        for color, width in zip(colors, widths):
            caption_icons.append((color, pygame.Rect(UI_LEFT_MARGIN, aux_margin_top, square_size, square_size), width))
            aux_margin_top += caption_font.get_sized_height()

        # Captions
        for caption in captions:
            text_surface, _ = caption_font.render(caption, fgcolor="black")
            text_rect = pygame.Rect(UI_LEFT_MARGIN + square_size + 5, margin_top, text_surface.get_width(), text_surface.get_height())
            caption_texts.append((text_surface, text_rect))
            margin_top += caption_font.get_sized_height()
        return caption_icons, caption_texts

    def draw_captions(self):
        for icon in self.caption_icons:
            pygame.draw.rect(self.screen, icon[0], icon[1], width=icon[2])
        for text_surface, text_rect in self.caption_texts:
            self.screen.blit(text_surface, text_rect)
    
    def draw_maze_gen_label(self):
        label_font = pygame.freetype.SysFont(None, 20)
        label_surface, _ = label_font.render("Labirinto:", fgcolor="black")
        # Posiciona ao lado dos campos de tamanho
        label_y = self.width_input.rect.y - 25
        self.screen.blit(label_surface, (UI_LEFT_MARGIN, label_y))
        
        # Labels para largura e altura
        small_label_font = pygame.freetype.SysFont(None, 18)
        width_label, _ = small_label_font.render("L:", fgcolor="black")
        height_label, _ = small_label_font.render("A:", fgcolor="black")
        # Posiciona ao lado  dos respectivos campos
        self.screen.blit(width_label, (self.width_input.rect.x - width_label.get_width() - 5, self.width_input.rect.y + (self.width_input.rect.height - width_label.get_height()) // 2))
        self.screen.blit(height_label, (self.height_input.rect.x - height_label.get_width() - 5, self.height_input.rect.y + (self.height_input.rect.height - height_label.get_height()) // 2))

    def draw_title(self):
        self.screen.blit(self.logo_image, (0, 0))
        left_margin = self.logo_image.get_width() + 5
        top_margin = self.logo_image.get_height() // 4

        title_font = pygame.freetype.SysFont(None, 36)
        title_surface, _ = title_font.render("Mico-Leão", fgcolor="brown")
        subtitle_font = pygame.freetype.SysFont(None, 24)
        subtitle_surface, _ = subtitle_font.render("Algoritmo de Navegação", fgcolor="black")

        subtitle_rect = pygame.Rect(left_margin, top_margin + title_surface.get_height() + 10, subtitle_surface.get_width(), subtitle_surface.get_height())
        self.screen.blit(subtitle_surface, subtitle_rect)
        text_center = left_margin + subtitle_surface.get_width() // 2 - title_surface.get_width() // 2
        title_rect = pygame.Rect(text_center, top_margin, title_surface.get_width(), title_surface.get_height())
        self.screen.blit(title_surface, title_rect)
    
    def draw_steps_info(self):
        #Desenha informações sobre passos tomados e passos ideais
        steps_font = pygame.freetype.SysFont(None, 20)
        steps_text = f"Passos: {self.sim.steps_taken}  Ideal: {self.sim.ideal_steps}"
        steps_surface, _ = steps_font.render(steps_text, fgcolor="black")
        # Posiciona abaixo do título
        steps_y = self.logo_image.get_height() + 30
        self.screen.blit(steps_surface, (UI_LEFT_MARGIN, steps_y))

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
        c_blue   = pygame.Color(75, 75, 245)   # Longe (Azul Escuro)
        if t < 0.33:
            # 0% a 33%: Vermelho -> Amarelo
            return c_red.lerp(c_yellow, t / 0.33)
        elif t < 0.66:
            # 33% a 66%: Amarelo -> Cinza (Neutraliza o verde)
            return c_yellow.lerp(c_white, (t - 0.33) / 0.33)
        else:
            # 66% a 100%: Cinza-> Azul
            return c_white.lerp(c_blue, (t - 0.66) / 0.34)

    def draw_maze(self, known_maze, distances, start, goal):
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
                elif (row, col) == start:
                    cell_color = pygame.Color(200, 200, 200)  # Cinza claro para a entrada
                else:
                    cell_dist = distances[row][col]
                    if cell_dist == float('inf'):
                        cell_color = pygame.Color(80, 80, 80)  # Cinza para célula inalcansável
                    else:
                        cell_color = self.get_heatmap_color(cell_dist, max_distance) # Caminho livre

                # Desenha célula, Rect(left, top, width, height) -> Retângulo.
                square_cell = pygame.Rect(self.maze_left_margin + col*self.cell_size, self.maze_top_margin + row*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, cell_color, square_cell)

                # Desenha outline preto para parede desconhecida
                if not known_wall and is_wall((row, col), self.real_maze):
                    pygame.draw.rect(self.screen, pygame.Color(80, 80, 80), square_cell, width=self.cell_border)

                # Desenha valor da distância na célula
                if self.draw_num:
                    cell_dist = distances[row][col]
                    if distances[row][col] != float('inf') and not is_wall((row, col), known_maze):
                        text_surface = self.cached_numbers.get(cell_dist)
                        if text_surface is None:  # Fallback para números fora do cache
                            text_surface, _ = self.num_font.render(str(cell_dist), fgcolor="black")
                        text_rect = text_surface.get_rect(center=square_cell.center)
                        self.screen.blit(text_surface, text_rect)
    
    def draw_scene(self, known_maze, distances, pos, direction, start, goal):
        # Limpa tela
        self.screen.fill(pygame.Color(250, 240, 215))

        self.draw_title()
        self.draw_steps_info()
        self.draw_captions()
        self.draw_maze_gen_label()
        # Desenha os novos elementos
        for element in self.ui_elements:
            element.draw(self.screen)
        self.draw_maze(known_maze, distances, start,goal)
        self.draw_mouse(pos, direction)
        
        # Desenha tela atualizada
        pygame.display.flip()