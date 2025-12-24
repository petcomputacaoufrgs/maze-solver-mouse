import pygame
import interface
import simulation

# Constantes
MAZE_WIDTH = 21
MAZE_HEIGHT = 21

# Inicilização
pygame.init()
clock = pygame.time.Clock()

sim = simulation.Simulation(MAZE_HEIGHT, MAZE_WIDTH)

# Cria interface passando a simulação
interface = interface.Interface(MAZE_HEIGHT, MAZE_WIDTH, sim)

# Renderiza o estado inicial antes de começar a simulação já com distâncias do flood fill
interface.draw_scene(sim.known_maze, sim.distances, sim.pos, sim.direction, sim.start, sim.goal)
pygame.display.flip()

screen_open = True
while screen_open:
    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_open = False
        # Repassa eventos para a UI
        for element in interface.ui_elements:
            element.handle_event(event)

    # Atualiza o tempo do solver com base no slider
    solver_interval = interface.speed_slider.value
    sim.update_controls(solver_interval)

    # Avança a simulação
    sim.simulation_next_step()

    # Renderização
    interface.draw_scene(sim.known_maze, sim.distances, sim.pos, sim.direction, sim.start, sim.goal)
    clock.tick(60)  # 60 FPS

pygame.quit()