import pygame
import numpy as np
import maze_solver
import interface as ui
import maze_generator as maze_gen

# Constantes
MAZE_WIDTH = 15
MAZE_HEIGHT = 15

# Inicilização
pygame.init()

clock = pygame.time.Clock()
running = True
initialization_complete = False
initialization_start_time = 0

known_maze = np.zeros((MAZE_HEIGHT, MAZE_WIDTH))
real_maze, start, goal = maze_gen.generate_maze(MAZE_HEIGHT, MAZE_WIDTH)
pos = start
direction = 'N'
solver = maze_solver.MazeSolver(real_maze, start, goal)
interface = ui.Interface(MAZE_HEIGHT, MAZE_WIDTH, real_maze)

# Controle de tempo para o solver
last_solver_update = 0
solver_interval = 250  # 250 milissegundos
initialization_buffer = 100  # 100ms de buffer para garantir que a janela está carregada

# Execução Principal
solver_gen = solver.run()
previous_pos = start
previous_dir = direction

# Renderiza o estado inicial antes de começar a simulação já com distâncias do flood fill
distances = solver.flood_fill(known_maze, goal)
interface.draw_maze(known_maze, distances, pos, direction, goal)
pygame.display.flip()
initialization_start_time = pygame.time.get_ticks()

# Flood fill inicial para já mostrar cores de distância
#distances = solver.flood_fill(solver.known_maze, solver.goal)
while running:
    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    
    # Aguarda o buffer de inicialização antes de começar a simulação
    if not initialization_complete:
        if current_time - initialization_start_time >= initialization_buffer:
            initialization_complete = True
            last_solver_update = current_time  # Inicializa o contador após o buffer
        # Durante a inicialização, continua renderizando o estado inicial
        interface.draw_maze(known_maze, distances, pos, direction, goal)
        clock.tick(60)
        continue

    # Atualiza estado do labirinto e do mouse com próximo passo do solver
    if current_time - last_solver_update >= solver_interval:
        if pos != goal:
            try:
                known_maze, distances, pos, direction, path = next(solver_gen)
                while pos == previous_pos and direction == previous_dir:
                    known_maze, distances, pos, direction, path = next(solver_gen)
                previous_pos = pos
                previous_dir = direction
                last_solver_update = current_time
            except StopIteration:
                running = False

    # Renderização
    interface.draw_maze(known_maze, distances, pos, direction, goal)

    clock.tick(60)  # 60 FPS

pygame.quit()