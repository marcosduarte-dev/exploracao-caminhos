# generators/prim_multipath_generator.py

import random

def generate_maze(width, height, wall_removal_prob=0.8):
    """
    Gera um labirinto com múltiplos caminhos usando o algoritmo de Prim modificado.
    
    :param width: Largura do labirinto.
    :param height: Altura do labirinto.
    :param wall_removal_prob: Probabilidade de remover uma parede (0 a 1).
                              Valores mais altos criam mais caminhos.
    :return: Grid do labirinto.
    """
    # Inicializa o grid com paredes
    grid = [[1 for _ in range(width)] for _ in range(height)]
    
    # Escolhe um ponto inicial aleatório
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    grid[start_y][start_x] = 0  # Marca a célula inicial como caminho
    
    # Lista de paredes fronteiriças
    walls = []
    
    # Adiciona as paredes adjacentes à célula inicial
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx, ny = start_x + dx, start_y + dy
        if 0 <= nx < width and 0 <= ny < height:
            walls.append((nx, ny, start_x, start_y))  # (parede_x, parede_y, célula_x, célula_y)
    
    while walls:
        # Escolhe uma parede aleatória da lista
        wall_x, wall_y, cell_x, cell_y = walls.pop(random.randint(0, len(walls) - 1))
        
        # Verifica se a célula oposta à parede está dentro dos limites
        opposite_x = wall_x + (wall_x - cell_x)
        opposite_y = wall_y + (wall_y - cell_y)
        
        if 0 <= opposite_x < width and 0 <= opposite_y < height:
            # Se a célula oposta for uma parede, decide se remove a parede
            if grid[opposite_y][opposite_x] == 1 and random.random() < wall_removal_prob:
                # Remove a parede e marca as células como caminho
                grid[wall_y][wall_x] = 0
                grid[opposite_y][opposite_x] = 0
                
                # Adiciona as paredes adjacentes à nova célula
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    nx, ny = opposite_x + dx, opposite_y + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
                        walls.append((nx, ny, opposite_x, opposite_y))
    
    return grid