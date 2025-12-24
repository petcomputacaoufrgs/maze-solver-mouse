import random as rand
import pygame
import numpy as np
import maze_solver
import simulation.maze_generator as maze_gen

class Simulation:
    def __init__(self, maze_height=51, maze_width=51):
        self.maze_width = maze_width
        self.maze_height = maze_height
        # Inicilização
        pygame.init()

        self.clock = pygame.time.Clock()
        
        self.maze_seed = rand.randint(0, 999999)
        self.known_maze = np.zeros((self.maze_height, self.maze_width))
        self.real_maze, self.start, self.goal = maze_gen.generate_maze(self.maze_height, self.maze_width, seed=self.maze_seed)
        self.pos = self.start
        self.direction = 'N'
        self.steps_taken = 0
        self.solver = maze_solver.MazeSolver(self.real_maze, self.start, self.goal)
        self.solver_gen = self.solver.run()
        # Flood fill inicial para já mostrar cores de distância
        self.distances = self.solver.flood_fill(self.known_maze, self.goal)
        # Calcula passos ideais com flood fill no labirinto real
        self.ideal_steps = self.calculate_ideal_steps()
        # Controle de estado
        self.running = False
        # Controle de tempo para o solver
        self.last_solver_update = 0
        self.solver_interval = 100 # Default

    def update_controls(self, interval):
        self.solver_interval = interval

    def get_state(self):
        return self.pos, self.direction, self.known_maze, self.distances, self.running

    def toggle_pause(self):
        self.running = not self.running

    # Apenas reseta posição e direção do robô para início
    def reset_robot(self):
        self.pos = self.start
        self.direction = 'N'
        self.steps_taken = 0
        self.solver.restart_robot()
        self.solver_gen = self.solver.run()
        self.running = False

    # Esquece paredes e distâncias, mas mantém o labirinto
    def reset_maze(self):
        self.known_maze = np.zeros((self.maze_height, self.maze_width))
        self.pos = self.start
        self.direction = 'N'
        self.steps_taken = 0
        self.solver = maze_solver.MazeSolver(self.real_maze, self.start, self.goal)
        self.solver_gen = self.solver.run()  # Recria o gerador com o novo solver
        self.distances = self.solver.flood_fill(self.known_maze, self.goal)
        self.running = False

    def new_maze(self, seed=-1, width=None, height=None):
        # Inicializa gerador de números aleatórios com semente para reprodutibilidade
        if seed == -1:
            seed = rand.randint(0, 100000)
        self.maze_seed = seed
        
        # Atualiza dimensões se fornecidas
        if width is not None:
            self.maze_width = width
        if height is not None:
            self.maze_height = height
        
        # Gera novo labirinto com as dimensões atualizadas
        self.known_maze = np.zeros((self.maze_height, self.maze_width))
        self.real_maze, self.start, self.goal = maze_gen.generate_maze(self.maze_height, self.maze_width, seed=seed)
        # Calcula passos ideais antes de resetar o maze
        self.ideal_steps = self.calculate_ideal_steps()
        self.reset_maze()
    
    def calculate_ideal_steps(self):
        """Calcula o número ideal de passos usando flood fill no labirinto real"""
        # Cria um maze completo para flood fill
        real_maze_complete = self.real_maze.copy()
        distances = self.solver.flood_fill(real_maze_complete, self.goal)
        # Retorna a distância da posição inicial até o objetivo
        return int(distances[self.start[0]][self.start[1]])
    
    def simulation_next_step(self):
        current_time = pygame.time.get_ticks()
        if self.running and (current_time - self.last_solver_update >= self.solver_interval):
            # Atualiza estado do labirinto e do robô com próximo passo do solver
            try:
                self.known_maze, self.distances, self.pos, self.direction, has_moved = next(self.solver_gen)
                # Reseta intervalo de tempo apenas se houve mudança de posição ou direção
                if has_moved != "distance_update":
                    self.last_solver_update = current_time
                if has_moved == "movement_update":
                    self.steps_taken += 1
            except StopIteration:
                self.running = False  # Para a simulação quando o solver terminar
    
    def get_render_data(self):
        """Retorna dados necessários para o renderer desenhar o labirinto"""
        return {
            'known_maze': self.known_maze,
            'distances': self.distances,
            'real_maze': self.real_maze,
            'pos': self.pos,
            'direction': self.direction,
            'start': self.start,
            'goal': self.goal
        }
