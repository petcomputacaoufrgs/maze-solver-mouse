
# INICIALIZAÇÃO

# Definição do labirinto real (só na simulação)
    # Define layout do labirinto (matriz onde 0 é caminho livre e 1 é parede)
    # Seleciona saida e entrada

# Inicializa o labirinto conhecido pelo robô: (um labirinto com pontas na entrada e na saída e sem paredes)*1


# INÍCIO DO LOOP PRINCIPAL

# Atualiza visão do robô:
   # O robô olha para 3 direções: frente, esquerda e direita um número de quadrados igual a min(BOT_VISION_BY_SQUARES, parede mais próxima seguindo a direção)
   # Atualiza o labirinto conhecido pelo robô com a visão atual, o que pode expandir o labirinto conhecido

# Se o robô só tem uma direção possível, só vai


# Se não
    # Aplica o algoritmo de flood fill a partir da saída para preencher o labirinto conhecido com a distância mínima até a saída de cada quadrado

    # Seleciona a direção a seguir:
        # Pega as direções que levam aos menores valores de distância até a saída. 
        # Em caso de empate, dá preferância para a direção para a qual o robô está virado e depois para a direção que leve a um menor esforço de movimento (ortogonais primeiro, por último oposta)
        # Vira o robô para a direção selecionada
   
# Avança o robô

# Se o robô chegou na saída termina o loop

# ---------------------------

# OBSERVAÇÕES

# *1: depende das informações que vamos fornecer para o robô. Se fornecermos só a saída, vai ser isso mesmo. 
# Fornecendo a entrada também, o labirinto conhecido pode inicializar da posição (0, 0) até (maxRow(entrada, saida), maxCol(entrada, saída)) 

# ============================================================================

import numpy as np
from collections import deque

BOT_VISION_BY_SQUARES = 2
DIRECTIONS = ['N', 'E', 'S', 'W']
DIR_VECTORS = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}

def turn_left(dir): return DIRECTIONS[(DIRECTIONS.index(dir) - 1) % 4]
def turn_right(dir): return DIRECTIONS[(DIRECTIONS.index(dir) + 1) % 4]
def turn_back(dir): return DIRECTIONS[(DIRECTIONS.index(dir) + 2) % 4]

def in_bounds(pos, maze):
    r, c = pos
    return 0 <= r < len(maze) and 0 <= c < len(maze[0])

def neighbors(pos):
    r, c = pos
    return [(r + dr, c + dc) for dr, dc in DIR_VECTORS.values()]

# Flood fill a partir da saída
def flood_fill(known_maze, goal):
    rows, cols = len(known_maze), len(known_maze[0])


    # Define a matriz de distâncias inicialmente com todos os valores como infinito
    distances = [[float('inf')] * cols for _ in range(rows)]

    # Adiciona a saída na fila 
    queue = deque([goal])

    # Define a distância até a saída como 0
    distances[goal[0]][goal[1]] = 0

    # Enquanto houver posições na fila:
    while queue:

        # Remove a primeira posição da fila
        r, c = queue.popleft()

        # Para cada direção possível (N, E, S, W):
        for dr, dc in DIR_VECTORS.values():

            # Calcula a nova posição ao mover na direção atual a partir da posição
            nr, nc = r + dr, c + dc

            # Se a nova posição está dentro dos limites do labirinto conhecido e é um caminho livre (0):
            if in_bounds((nr, nc), known_maze) and known_maze[nr][nc] == 0:


                # E se a distância até essa nova posição é maior do que a distância até a posição atual + 1:
                if distances[nr][nc] > distances[r][c] + 1:

                    # Atualiza a distância até a nova posição (distância até a posição atual + 1) e coloca a nova posição na fila, porque tem que reatualizar as distâncias a partir dela
                    distances[nr][nc] = distances[r][c] + 1
                    queue.append((nr, nc))
    
    return distances


# Atualiza o labirinto conhecido a partir da visão (futuramente isso aqui vai ser definido pelos sensores)
def update_vision(real_maze, known_maze, pos, direction):

    # Pega as direções que o robô enxerga: a frente dele, a direita e a esquerda
    directions = [direction, turn_left(direction), turn_right(direction)]

    # Para cada direção que ele enxerga:
    for dir in directions:

        # Pega o vetor de direção correspondente
        dr, dc = DIR_VECTORS[dir]

        # Para cada valor de 1 até o limite de visão do robô:
        for i in range(1, BOT_VISION_BY_SQUARES + 1):
            # Multiplica o vetor da direção por esse valor para obter o quadrado i a partir da posição atual nessa direção
            nr, nc = pos[0] + dr*i, pos[1] + dc*i
             
            # Atualiza o labirinto conhecido:

            # Se a nova posição não está nos limites do labirinto (que na realidade vai ser uma parede) ou se ela for uma parede, interrompe a visão
            if not in_bounds((nr, nc), real_maze):
                break

            # Se ela estiver mas não está nos limites do labirinto conhecido, adiciona uma nova linha ou coluna ao labirinto conhecido
            if nr >= len(known_maze):
                add_row(known_maze)
            
            if nc >= len(known_maze[0]):
                add_column(known_maze)
            
            known_maze[nr][nc] = real_maze[nr][nc]
            if real_maze[nr][nc] == 1:  # Parede
                break



# Inicializa o labirinto conhecido a partir do começo e do fim e o offset em relação ao labirinto real
def initialize_known_maze(start, goal):
    r1, c1 = start
    r2, c2 = goal

    # Determina os limites do retângulo que contém o caminho entre start e goal
    max_r = max(r1, r2)
    max_c = max(c1, c2)

    # Inicializa tudo como caminho livre
    known_maze = [[0 for _ in range(max_c + 1)] for _ in range(max_r + 1)]



    # Offset do labirinto conhecido em relação ao labirinto real
    return known_maze


def take_all_possible_actions(pos, known_maze):
    actions = {}

    for dir in DIRECTIONS:
        dr, dc = DIR_VECTORS[dir]
        nr, nc = pos[0] + dr, pos[1] + dc

        # Se a nova posição seguindo a direção está dentro dos limites do labirinto (na real isso pode ser só uma parede) e é um caminho livre:
        if in_bounds((nr, nc), known_maze) and known_maze[nr][nc] == 0:
            actions[dir] = (nr, nc)

    return actions


# Decide o próximo movimento
def choose_direction(actions, direction, distances):

    # Vamos olhar para todas as ações possíveis a paritr da posição atual e colocar todas as direções com a menor distância possível em uma lista
    best_dirs = []
    min_dist = float('inf')

    # Para cada ação
    for action in actions:


        dist = distances[actions[action][0]][actions[action][1]]

        # Se a distância tomando essa ação é menor que a encontrada até agora, ela vira a melhor direção, reinicializando a lista
        if dist < min_dist:
            best_dirs = [dir]
            min_dist = dist

        # Se for igual, adiciona ela na lista de melhores direções
        elif dist == min_dist:
            best_dirs.append(dir)


    # Desempata as direções na seguinte ordem (menor esforço de movimento)
    # Prioridade: frente > lados (esquerda > direita) > lado oposto
    if direction in best_dirs:
        return direction
    elif turn_left(direction) in best_dirs:
        return turn_left(direction)
    elif turn_right(direction) in best_dirs:
        return turn_right(direction)
    elif turn_back(direction) in best_dirs:
        return turn_back(direction)
    else:
        return best_dirs[0]


# maze: list of rows
def add_column(maze):
    # Adiciona uma nova coluna ao labirinto (um valor de 0 para cada linha)
    for column in maze:
        column.append(0)


# maze: list of rows
def add_row(maze):
    # Adiciona uma nova linha ao labirinto
    maze.append([0 for _ in range (len(maze[0]))])


# FUNÇÃO PRINCIPAL
def solve_maze(real_maze, start, goal):
    known_maze = initialize_known_maze(start, goal)

    pos = start
    direction = 'N'
    path = [pos]

    while pos != goal:
        update_vision(real_maze, known_maze, pos, direction)
        actions = take_all_possible_actions(pos, known_maze)

        # Se só tem uma direção possível (volta), só volta:
        if len(actions) == 1:
            direction = list(actions.keys())[0]

        # Se não, tem que fazer uma escolha. Nesse caso, aplica o flood fill a partir do objetivo para obter as distâncias mínimas até ele
        else:
            distances = flood_fill(known_maze, goal)
            direction = choose_direction(pos, direction, distances, known_maze)

        dr, dc = DIR_VECTORS[direction]
        pos = (pos[0] + dr, pos[1] + dc)
        path.append(pos)

    return path


real_maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]
start = (1, 1)
goal = (3, 3)



path = solve_maze(real_maze, start, goal)
print("Caminho:", path)


