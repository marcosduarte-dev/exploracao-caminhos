import random
from collections import deque

def generate_maze(width, height):
    """
    Gera um labirinto usando o algoritmo BFS (Busca em Largura).
    O algoritmo cria um labirinto perfeito (sem áreas inacessíveis e com um único caminho entre quaisquer dois pontos).

    Args:
        width (int): Largura do labirinto (número de colunas).
        height (int): Altura do labirinto (número de linhas).

    Returns:
        list: Uma matriz (lista de listas) representando o labirinto, onde:
              - 0 representa um caminho.
              - 1 representa uma parede.
              - 2 representa o ponto inicial.
              - 3 representa o ponto final.
    """
    from utils.maze_utils import set_start_end

    grid = [[1 for _ in range(width)] for _ in range(height)]

    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    grid[start_y][start_x] = 0

    queue = deque([(start_x, start_y)])

    while queue:
        current_x, current_y = queue.popleft()

        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions) 

        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy

            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == 1:
                    grid[current_y + dy // 2][current_x + dx // 2] = 0
                    grid[ny][nx] = 0 
                    queue.append((nx, ny))

    start_pos, end_pos = set_start_end(width, height, grid)

    return grid, start_pos, end_pos