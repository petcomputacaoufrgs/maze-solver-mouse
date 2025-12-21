import numpy as np
from collections import deque
from enum import Enum

BOT_VISION_BY_SQUARES = 2
DIRECTIONS = ['N', 'E', 'S', 'W']
DIR_VECTORS = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

# Métodos auxiliares
def is_wall(pos, maze):
    r, c = pos
    return maze[r][c] == 1 # 1 é Parede, 0 é caminho livre

class MazeSolver:
    def __init__(self, real_maze, start, goal):
        self.real_maze = real_maze
        self.known_maze = np.zeros_like(real_maze)
        self.distances = np.zeros_like(real_maze)
        self.start = start
        self.goal = goal
        self.pos = start
        self.direction = 'N'
        self.path = [self.pos]
        
    def turn_left(self, dir): return DIRECTIONS[(DIRECTIONS.index(dir) - 1) % 4]
    def turn_right(self, dir): return DIRECTIONS[(DIRECTIONS.index(dir) + 1) % 4]
    def turn_back(self, dir): return DIRECTIONS[(DIRECTIONS.index(dir) + 2) % 4]

    def in_bounds(self, pos, maze):
        r, c = pos
        return 0 <= r < len(maze) and 0 <= c < len(maze[0])

    def neighbors(self, pos):
        r, c = pos
        return [(r + dr, c + dc) for dr, dc in DIR_VECTORS.values()]

    # Flood fill a partir da saída
    def flood_fill(self, known_maze, goal):
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
                if self.in_bounds((nr, nc), known_maze) and known_maze[nr][nc] == 0:

                    # E se a distância até essa nova posição é maior do que a distância até a posição atual + 1:
                    if distances[nr][nc] > distances[r][c] + 1:

                        # Atualiza a distância até a nova posição (distância até a posição atual + 1) e coloca a nova posição na fila, porque tem que reatualizar as distâncias a partir dela
                        distances[nr][nc] = distances[r][c] + 1
                        queue.append((nr, nc))
        
        return distances

    # Atualiza o labirinto conhecido a partir da visão (futuramente isso aqui vai ser definido pelos sensores)
    def update_vision(self, real_maze, known_maze, pos, direction):

        # Pega as direções que o robô enxerga: a frente dele, a direita e a esquerda
        directions = [direction, self.turn_left(direction), self.turn_right(direction)]

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
                if not self.in_bounds((nr, nc), real_maze):
                    break

                # Se ela estiver mas não está nos limites do labirinto conhecido, adiciona uma nova linha ou coluna ao labirinto conhecido
                if nr >= len(known_maze):
                    self.add_row(known_maze)
                
                if nc >= len(known_maze[0]):
                    self.add_column(known_maze)
                
                known_maze[nr][nc] = real_maze[nr][nc]
                if real_maze[nr][nc] == 1:  # Parede
                    break

    # Inicializa o labirinto conhecido a partir do começo e do fim e o offset em relação ao labirinto real
    def initialize_known_maze(self, start, goal):
        r1, c1 = start
        r2, c2 = goal

        # Determina os limites do retângulo que contém o caminho entre start e goal
        max_r = max(r1, r2)
        max_c = max(c1, c2)

        # Inicializa tudo como caminho livre
        known_maze = [[0 for _ in range(max_c + 1)] for _ in range(max_r + 1)]

        # Offset do labirinto conhecido em relação ao labirinto real
        return known_maze


    def take_all_possible_actions(self, pos, known_maze):
        actions = {}

        for dir in DIRECTIONS:
            dr, dc = DIR_VECTORS[dir]
            nr, nc = pos[0] + dr, pos[1] + dc

            # Se a nova posição seguindo a direção está dentro dos limites do labirinto (na real isso pode ser só uma parede) e é um caminho livre:
            if self.in_bounds((nr, nc), known_maze) and known_maze[nr][nc] == 0:
                actions[dir] = (nr, nc)

        return actions


    # Decide o próximo movimento
    def choose_direction(self, actions, direction, distances):
        # Vamos olhar para todas as ações possíveis a partir da posição atual e colocar todas as direções com a menor distância possível em uma lista
        best_dirs = []
        min_dist = float('inf')

        # Para cada ação
        for action in actions:
            dist = distances[actions[action][0]][actions[action][1]]

            # Se a distância tomando essa ação é menor que a encontrada até agora, ela vira a melhor direção, reinicializando a lista
            if dist < min_dist:
                best_dirs = [action]
                min_dist = dist

            # Se for igual, adiciona ela na lista de melhores direções
            elif dist == min_dist:
                best_dirs.append(action)

        # Desempata as direções na seguinte ordem (menor esforço de movimento)
        # Prioridade: frente > lados (esquerda > direita) > lado oposto
        if direction in best_dirs:
            return direction
        elif self.turn_left(direction) in best_dirs:
            return self.turn_left(direction)
        elif self.turn_right(direction) in best_dirs:
            return self.turn_right(direction)
        elif self.turn_back(direction) in best_dirs:
            return self.turn_back(direction)
        else:
            return best_dirs[0]


    # maze: list of rows
    def add_column(self, maze):
        # Adiciona uma nova coluna ao labirinto (um valor de 0 para cada linha)
        for column in maze:
            column.append(0)


    # maze: list of rows
    def add_row(self, maze):
        # Adiciona uma nova linha ao labirinto
        maze.append([0 for _ in range (len(maze[0]))])


    # FUNÇÃO PRINCIPAL
    def run(self):
        while self.pos != self.goal:
            self.update_vision(self.real_maze, self.known_maze, self.pos, self.direction)
            actions = self.take_all_possible_actions(self.pos, self.known_maze)

            # Se só tem uma direção possível (volta), só volta:
            if len(actions) == 1:
                self.direction = list(actions.keys())[0]
            # Se não, tem que fazer uma escolha. Nesse caso, aplica o flood fill a partir do objetivo para obter as distâncias mínimas até ele
            else:
                self.distances = self.flood_fill(self.known_maze, self.goal)
                # Pausa execução aqui para atualizar matriz de distâncias na interface
                yield self.known_maze, self.distances, self.pos, self.direction, self.path
                
                self.direction = self.choose_direction(actions, self.direction, self.distances)
                # Pausa execução aqui para atualizar rotação na interface
                yield self.known_maze, self.distances, self.pos, self.direction, self.path

            dr, dc = DIR_VECTORS[self.direction]
            self.pos = (self.pos[0] + dr, self.pos[1] + dc)
            self.path.append(self.pos)
            # Pausa execução aqui para atualizar movimento na interface
            yield self.known_maze, self.distances, self.pos, self.direction, self.path
            