import pygame
import numpy as np
import maze_solver
import maze_generator as maze_gen

class Simulation:
    def __init__(self, maze_height=51, maze_width=51):
        self.maze_width = maze_width
        self.maze_height = maze_height
        # Inicilização
        pygame.init()

        self.clock = pygame.time.Clock()
        
        self.known_maze = np.zeros((self.maze_height, self.maze_width))
        self.real_maze, self.start, self.goal = maze_gen.generate_maze(self.maze_height, self.maze_width)
        self.pos = self.start
        self.direction = 'N'
        self.solver = maze_solver.MazeSolver(self.real_maze, self.start, self.goal)
        self.solver_gen = self.solver.run()
        # Flood fill inicial para já mostrar cores de distância
        self.distances = self.solver.flood_fill(self.known_maze, self.goal) 
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
        self.solver.restart_robot()
        self.solver_gen = self.solver.run()
        self.running = False

    # Esquece paredes e distâncias, mas mantém o labirinto
    def reset_maze(self):
        self.known_maze = np.zeros((self.maze_height, self.maze_width))
        self.pos = self.start
        self.direction = 'N'
        self.solver = maze_solver.MazeSolver(self.real_maze, self.start, self.goal)
        self.solver_gen = self.solver.run()  # Recria o gerador com o novo solver
        self.distances = self.solver.flood_fill(self.known_maze, self.goal)
        self.running = False
    
    def new_maze(self):
        # Lógica para gerar novo maze_gen e reiniciar variáveis
        self.real_maze, self.start, self.goal = maze_gen.generate_maze(self.maze_height, self.maze_width)
        self.reset_maze()

    def simulation_next_step(self):
        current_time = pygame.time.get_ticks()
        if self.running and (current_time - self.last_solver_update >= self.solver_interval):
            # Atualiza estado do labirinto e do robô com próximo passo do solver
            try:
                self.known_maze, self.distances, self.pos, self.direction, has_moved = next(self.solver_gen)
                # Reseta intervalo de tempo apenas se houve mudança de posição ou direção
                if has_moved:
                    self.last_solver_update = current_time
            except StopIteration:
                self.running = False  # Para a simulação quando o solver terminar
