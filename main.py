import pygame
import numpy as np
import maze_solver
import interface as ui

# Constantes
MAZE_WIDTH = 5
MAZE_HEIGHT = 5

# Inicilização
pygame.init()

clock = pygame.time.Clock()
running = True

# Labirinto de teste (pode ser gerado futuramente)
test_maze = [
[1, 1, 1, 1, 1],
[1, 0, 0, 1, 1],
[1, 0, 1, 0, 1],
[1, 0, 0, 0, 1],
[1, 1, 1, 1, 1]
]
start = (1, 1)
goal = (3, 3)

solver = maze_solver.MazeSolver(test_maze, start, goal)
interface = ui.Interface(MAZE_WIDTH, MAZE_HEIGHT)

# Controle de tempo para o solver
last_solver_update = 0
solver_interval = 3000  # 3 segundos em milissegundos

# Queremos mostrar a posição anterior, a em que o robô estava quando calculou as distâncias.
previous_pos = start 

# Execução Principal
# Primeiro passo para inicializar instantaneamente
known_maze, distances, pos, direction, path = solver.run()
while running:
    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Renderização
    interface.draw_maze(known_maze, distances, previous_pos, direction)

    # Atualiza estado do labirinto e do mouse com próximo passo do solver
    current_time = pygame.time.get_ticks()
    
    if current_time - last_solver_update >= solver_interval:
        if pos == goal:
            previous_pos = pos
        else:
            previous_pos = pos # Atualiza posição que será mostrada na próxima iteração
            known_maze, distances, pos, direction, path = solver.run()
            last_solver_update = current_time

    clock.tick(60)  # 60 FPS

pygame.quit()