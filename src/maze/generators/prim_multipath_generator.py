import random

def generate_maze(width, height, wall_removal_prob=0.8):
    """
    Gera um labirinto usando o algoritmo de Prim com múltiplos caminhos.
    O algoritmo cria um labirinto com paredes removidas aleatoriamente para adicionar loops.

    Args:
        width (int): Largura do labirinto (número de colunas).
        height (int): Altura do labirinto (número de linhas).
        wall_removal_prob (float): Probabilidade de remover uma parede durante a fase de adição de loops.

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

    walls = []
    add_walls_to_list(start_x, start_y, walls, width, height, grid)

    while walls:
        wall_idx = random.randint(0, len(walls) - 1)
        wall = walls.pop(wall_idx)
        x, y, direction = wall

        nx, ny = x + direction[0], y + direction[1]

        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
            grid[y][x] = 0
            grid[ny][nx] = 0

            add_walls_to_list(nx, ny, walls, width, height, grid)

    add_loops(int(width * height * 0.05), width, height, grid)

    start_pos, end_pos = set_start_end(width, height, grid)

    return grid, start_pos, end_pos


def add_walls_to_list(x, y, walls, width, height, grid):
    """
    Adiciona as paredes adjacentes a uma célula à lista de fronteira.

    Args:
        x (int): Coordenada x da célula.
        y (int): Coordenada y da célula.
        walls (list): Lista de paredes (fronteira).
        width (int): Largura do labirinto.
        height (int): Altura do labirinto.
        grid (list): Grade do labirinto.
    """
    # Direções: direita, baixo, esquerda, cima
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
            walls.append((nx, ny, (dx, dy)))


def add_loops(num_loops, width, height, grid):
    """
    Adiciona loops ao labirinto, removendo paredes aleatoriamente para criar múltiplos caminhos.

    Args:
        num_loops (int): Número de paredes a serem removidas para criar loops.
        width (int): Largura do labirinto.
        height (int): Altura do labirinto.
        grid (list): Grade do labirinto.
    """
    for _ in range(num_loops):
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)

        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx1, ny1 = x + dx, y + dy
            nx2, ny2 = x - dx, y - dy

            if (0 <= nx1 < width and 0 <= ny1 < height and
                0 <= nx2 < width and 0 <= ny2 < height and
                grid[ny1][nx1] == 0 and grid[ny2][nx2] == 0 and
                grid[y][x] == 1):
                grid[y][x] = 0
                break