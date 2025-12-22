import numpy as np
import random
from enum import Enum

class Direction(Enum):
    UP = 2
    RIGHT = 3
    DOWN = 4
    LEFT = 5

move_vectors = {Direction.UP: (-1, 0), Direction.RIGHT: (0, 1), Direction.DOWN: (1, 0), Direction.LEFT: (0, -1)}

# Cria listas de posições vizinhas com um espaço entre elas para orgiem "pular" para uma delas
def list_jump_spaces(maze, pos):
    available_spaces = [] # (pos, move_dir)
    for move_dir, (row_move, column_move) in move_vectors.items():
        jump_pos = (pos[0] + row_move*2, pos[1] + column_move*2)
        
        # Adiciona para lista se estiver dentro dos limites e não for parede
        inside_height = jump_pos[0] > 0 and jump_pos[0] < len(maze)
        inside_width = jump_pos[1] > 0 and jump_pos[1] < len(maze[0])
        if inside_height and inside_width:
            if maze[jump_pos[0], jump_pos[1]] != 1:
                available_spaces.append((jump_pos, move_dir))
    return available_spaces

def debug_print_maze(maze, pos, height, width):
    # Imprime labirinto gerado no console
        for row in range(height):
            for column in range(width):
                if pos == (row, column):
                    print("X", end=" ")
                elif maze[row, column] == 1:
                    print("\u25FB", end=" ")
                else:
                    match (maze[row, column]):
                        case Direction.UP.value:
                            print("^", end=" ")
                        case Direction.RIGHT.value:
                            print(">", end=" ")
                        case Direction.DOWN.value:
                            print("v", end=" ")
                        case Direction.LEFT.value:
                            print("<", end=" ")
            print()
        print("\n========================================\n")

# Origin Shift: Algoritmo de geração de labirintos ideais (sem loops e áreas inacessíveis)
def generate_maze(height, width, iterations = -1, seed = -1):
    if width % 2 == 0 or height % 2 == 0:
        raise Exception(" Labirinto deve ter dimensões ímpares.")

    # Inicializa gerador de números aleatórios com semente para reprodutibilidade
    if seed == -1:
        seed = random.randint(0, 10000)  # Inicializa gerador de números aleatórios
    random.seed(seed)

    # Heurística de iterações para labirinto diferente o suficiente do original
    if iterations == -1:
        iterations = width * height * 100
    
    # Cria labirinto inicial ideal
    maze = np.zeros((height, width))
    for row in range(height):
        if row % 2 == 0:
            for column in range(width-1):
                maze[row, column] = Direction.RIGHT.value
            maze[row, width-1] = Direction.DOWN.value
        else:
            for column in range(width-1):
                maze[row, column] = 1 # Parede
            maze[row, width-1] = Direction.DOWN.value
    
    # "Bagunça" labirinto a partir da origem (ponto inferior direito) trocando caminhos livres de lugar
    pos = (height - 1, width - 1) # Posição inicial (indexada em 0)
    maze[pos] = 0
    for _ in range(iterations):
        #debug_print_maze(maze, pos, height, width)
        # Escolhe próxima posição para "pular"
        available_spaces = list_jump_spaces(maze, pos)
        if len(available_spaces) > 0:
            new_pos_index = random.randint(0, len(available_spaces) - 1)
            (new_pos, move_dir) = available_spaces[new_pos_index]

            # Se pulo passou por parede, remove abrindo novo caminho
            (row_dif, column_dif) = move_vectors[Direction(move_dir)]
            passed_pos = (pos[0] + row_dif, pos[1] + column_dif)
            if maze[passed_pos] == 1:
                maze[passed_pos] = 0  # Remove parede (cria caminho novo)

            # Adiciona parede para bloquear o caminho antigo da nova posição
            # (criamos um novo caminho de origem para nova posição então precisamos bloquear o antigo)
            org_move_dir = maze[new_pos]
            (row_dif, column_dif) = move_vectors[Direction(org_move_dir)]
            old_path_pos = new_pos[0] + row_dif, new_pos[1] + column_dif
            maze[old_path_pos] = 1 # Parede

            # Atualizar direção da posição original, a que foi pulada (passed_pos) e nova origem (0)
            maze[pos] = move_dir.value
            maze[passed_pos] = move_dir.value
            maze[new_pos] = 0  # Origem

            pos = new_pos
        else:
            break
    
    # Define entrada e saída para que fiquem distantes
    goal = pos
    startRow = 1
    startColumn = 1
    if pos[0] > height // 2:
        startRow = 0
    else:
        startRow = height - 1

    if pos[1] > width // 2:
        startColumn = 0
    else:
        startColumn = width - 1

    print("Start Position:", (startRow, startColumn))
    print("Goal Position:", goal)

    # Limpa labirinto (remove direções, deixa só paredes e caminhos livres)
    for row in range(height):
        for column in range(width):
            if maze[row, column] != 1:
                maze[row, column] = 0
    
    return maze, (startRow, startColumn), goal





