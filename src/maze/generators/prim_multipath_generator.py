# generators/prim_multipath_generator.py

import random
from utils.maze_utils import set_start_end

def generate_maze(width, height, wall_removal_prob=0.8):

    grid = [[1 for _ in range(width)] for _ in range(height)]
    
    # Escolhe uma célula inicial aleatória
    start_x = random.randint(0, width-1)
    start_y = random.randint(0, height-1)
    grid[start_y][start_x] = 0
    
    # Lista de fronteira (paredes adjacentes a caminhos)
    walls = []
    
     # Adiciona as paredes adjacentes à célula inicial
    add_walls_to_list(start_x, start_y, walls, width, height, grid)
    
    # Enquanto houver paredes na fronteira
    while walls:
        # Escolhe uma parede aleatória
        wall_idx = random.randint(0, len(walls) - 1)
        wall = walls.pop(wall_idx)
        x, y, direction = wall
        
        # Verifica a célula na direção da parede
        nx, ny = x + direction[0], y + direction[1]
        
        # Se estiver nos limites e for uma parede
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
            # Remove a parede (criando um caminho)
            grid[y][x] = 0
            grid[ny][nx] = 0
            
            # Adiciona as novas paredes à lista
            add_walls_to_list(nx, ny, walls, width, height, grid)

    # Fase 2: Adicionar conexões extras para múltiplos caminhos
    add_loops(int(width * height * 0.05), width, height, grid)  # 5% da área em conexões extras
    
    # Definir entrada e saída
    set_start_end(width, height, grid)

    return grid

def add_walls_to_list(x, y, walls, width, height, grid):
    # Direções: direita, baixo, esquerda, cima
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
            walls.append((nx, ny, (dx, dy)))

def add_loops(num_loops, width, height, grid):
    for _ in range(num_loops):
        # Escolhe uma parede aleatória (que não seja de borda)
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        
        # Direções para verificar
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx1, ny1 = x + dx, y + dy
            nx2, ny2 = x - dx, y - dy
            
            # Se ambos os lados da parede são caminhos, podemos criar um loop
            if (0 <= nx1 < width and 0 <= ny1 < height and 
                0 <= nx2 < width and 0 <= ny2 < height and
                grid[ny1][nx1] == 0 and grid[ny2][nx2] == 0 and
                grid[y][x] == 1):
                grid[y][x] = 0  # Remove a parede
                break
