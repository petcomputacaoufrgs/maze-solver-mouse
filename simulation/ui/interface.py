import pygame
import pygame.freetype as freetype
import simulation.ui.ui_elements as ui
from simulation.ui.theme import Theme
from simulation.ui.ui_layout import UILayout
from simulation.renderers.maze_renderer import MazeRenderer
from simulation.renderers.ui_renderer import UIRenderer
from simulation.renderers.mouse_renderer import MouseRenderer
import random

class Interface:
    def __init__(self, maze_height, maze_width, simulation):
        self._setup_display(simulation)
        self._setup_renderers()
        self.update_maze_dimensions(maze_width, maze_height)
        self._load_button_icons()
        self.ui_renderer.prepare_captions()
        self._create_control_buttons()
        self._create_maze_controls(maze_width, maze_height)
        self._initialize_ui_elements()

    def _setup_display(self, simulation):
        """Initialize display and basic attributes"""
        self.screen = pygame.display.set_mode((UILayout.SCREEN_WIDTH, UILayout.SCREEN_HEIGHT))
        self.sim = simulation
        self.real_maze = simulation.real_maze
        self.ui_width = UILayout.SCREEN_WIDTH - UILayout.USABLE_SCREEN_WIDTH

    def _setup_renderers(self):
        """Initialize all renderer components"""
        logo_image = pygame.transform.smoothscale(
            pygame.image.load('assets/logo_pet.png'), 
            UILayout.LOGO_SIZE
        )
        self.maze_renderer = MazeRenderer(self.screen)
        self.ui_renderer = UIRenderer(self.screen, logo_image)
        self.mouse_renderer = MouseRenderer(self.screen)

    def _load_button_icons(self):
        """Load button icon images"""
        self.play_icon = pygame.image.load('assets/play_btn.png')
        self.pause_icon = pygame.image.load('assets/pause_btn.png')
        self.reset_icon = pygame.image.load('assets/reset_btn.png')
        self.restart_icon = pygame.image.load('assets/restart_btn.png')
        self.rand_seed_icon = pygame.image.load('assets/rand_seed_btn.png')

    def _create_control_buttons(self):
        """Create control buttons (restart, reset, play/pause) and speed slider"""
        start_y = UILayout.CONTROL_START_Y
        
        self.btn_restart = ui.IconButton(
            UILayout.UI_LEFT_MARGIN, start_y, 
            UILayout.ICON_BTN_SIZE, UILayout.ICON_BTN_SIZE,
            self.restart_icon, self.restart_icon, 
            Theme.BTN_BLUE, Theme.hover_col(Theme.BTN_BLUE), 
            self.restart_sim, initial_state=False
        )

        self.btn_reset = ui.IconButton(
            UILayout.UI_LEFT_MARGIN + UILayout.ICON_BTN_SIZE + 10, start_y, 
            UILayout.ICON_BTN_SIZE, UILayout.ICON_BTN_SIZE,
            self.reset_icon, self.reset_icon, 
            Theme.BTN_BLUE, Theme.hover_col(Theme.BTN_BLUE), 
            self.reset_sim, initial_state=False
        )
        
        self.btn_play = ui.IconButton(
            UILayout.UI_LEFT_MARGIN + (UILayout.ICON_BTN_SIZE + 10) * 2, start_y, 
            UILayout.ICON_BTN_SIZE, UILayout.ICON_BTN_SIZE,
            self.play_icon, self.pause_icon, 
            Theme.BTN_BLUE, Theme.hover_col(Theme.BTN_BLUE), 
            self.toggle_pause, initial_state=False
        )
        
        # Slider de Velocidade (Intervalo entre 10ms e 1000ms)
        self.speed_slider = ui.Slider(
            UILayout.UI_LEFT_MARGIN + 10, 
            start_y + UILayout.SPEED_SLIDER_OFFSET_Y, 
            UILayout.BTN_WIDTH, 10, 1000, 100, "Intervalo"
        )

    def _create_maze_controls(self, maze_width, maze_height):
        """Create maze generation controls (size inputs, seed input, generate button)"""
        start_y = UILayout.CONTROL_START_Y
        maze_gen_y = start_y + UILayout.MAZE_GEN_OFFSET_Y
        size_inputs_y = maze_gen_y + UILayout.SIZE_INPUTS_OFFSET_Y
        
        # Campos de largura e altura
        self.width_input = ui.InputBox(
            UILayout.UI_LEFT_MARGIN + UILayout.LABEL_WIDTH, size_inputs_y, 
            UILayout.SIZE_INPUT_WIDTH, 30, "", str(maze_width)
        )
        self.height_input = ui.InputBox(
            UILayout.UI_LEFT_MARGIN + UILayout.LABEL_WIDTH + UILayout.SIZE_INPUT_WIDTH + UILayout.SPACING + 15, 
            size_inputs_y, UILayout.SIZE_INPUT_WIDTH, 30, "", str(maze_height)
        )
        
        # Botão de seed aleatória
        self.btn_random_seed = ui.IconButton(
            UILayout.UI_LEFT_MARGIN, 
            maze_gen_y, UILayout.ICON_BTN_SIZE, UILayout.BTN_HEIGHT,
            self.rand_seed_icon, self.rand_seed_icon, 
            Theme.BTN_GREEN, Theme.hover_col(Theme.BTN_GREEN), 
            self.randomize_seed, initial_state=False
        )
        
        # Botão Gerar
        self.btn_new_maze = ui.Button(
            UILayout.UI_LEFT_MARGIN + UILayout.ICON_BTN_SIZE + UILayout.SPACING, maze_gen_y, 
            UILayout.SMALL_BTN_WIDTH, UILayout.BTN_HEIGHT, 
            "Gerar", Theme.BTN_RED, Theme.hover_col(Theme.BTN_RED), 
            self.new_maze
        )
        
        # Campo de seed
        self.seed_input = ui.InputBox(
            UILayout.UI_LEFT_MARGIN + UILayout.ICON_BTN_SIZE + UILayout.SPACING + UILayout.SMALL_BTN_WIDTH + UILayout.SPACING, 
            maze_gen_y, UILayout.SEED_INPUT_WIDTH, UILayout.BTN_HEIGHT, 
            "", str(self.sim.maze_seed)
        )

    def _initialize_ui_elements(self):
        """Collect all UI elements into a list for event handling and rendering"""
        self.ui_elements = [
            self.width_input, 
            self.height_input, 
            self.btn_new_maze, 
            self.seed_input, 
            self.btn_random_seed, 
            self.btn_restart, 
            self.btn_reset, 
            self.btn_play, 
            self.speed_slider
        ]

    #Recalcula todas as dimensões visuais do labirinto baseado no tamanho
    def update_maze_dimensions(self, maze_width, maze_height):
        """Atualiza dimensões do labirinto em todos os renderizadores"""
        self.maze_width = maze_width
        self.maze_height = maze_height
        
        # Atualiza renderizador do labirinto
        self.maze_renderer.update_dimensions(maze_width, maze_height)
        
        # Atualiza renderizador do mouse
        self.mouse_renderer.load_and_scale_mouse(self.maze_renderer.cell_size)

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

    def draw_scene(self, known_maze, distances, pos, direction, start, goal):
        """Desenha toda a cena usando os renderizadores especializados"""
        # Limpa tela
        self.screen.fill(pygame.Color(250, 240, 215))

        # Renderiza UI
        self.ui_renderer.draw_title()
        self.ui_renderer.draw_steps_info(self.sim.steps_taken, self.sim.ideal_steps)
        self.ui_renderer.draw_captions()
        self.ui_renderer.draw_maze_generation_labels(self.width_input, self.height_input)
        
        # Desenha elementos de UI
        for element in self.ui_elements:
            element.draw(self.screen)
        
        # Renderiza labirinto e mouse
        self.maze_renderer.draw(known_maze, self.real_maze, distances, start, goal)
        self.mouse_renderer.draw(
            pos, direction, 
            self.maze_renderer.maze_left_margin, 
            self.maze_renderer.maze_top_margin
        )
        
        # Atualiza tela
        pygame.display.flip()