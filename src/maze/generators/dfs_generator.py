import random

def generate_maze(width, height):
    """
    Gera um labirinto usando o algoritmo DFS (Busca em Profundidade).
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

    # Inicializa a grade do labirinto com paredes (1)
    grid = [[1 for _ in range(width)] for _ in range(height)]

    # Escolhe um ponto inicial aleatório dentro dos limites do labirinto
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    grid[start_y][start_x] = 0  # Marca a posição inicial como caminho (0)

    # Inicializa a fronteira com a posição inicial
    frontier = [(start_x, start_y)]

    # Enquanto houver células na fronteira
    while frontier:
        # Escolhe uma célula aleatória da fronteira para explorar
        current_x, current_y = frontier.pop(random.randint(0, len(frontier) - 1))

        # Define as direções possíveis (cima, direita, baixo, esquerda)
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)  # Embaralha as direções para aleatoriedade

        for dx, dy in directions:
            # Calcula a nova posição (pulando uma célula para criar corredores)
            nx, ny = current_x + dx, current_y + dy

            # Verifica se a nova posição está dentro dos limites do labirinto
            if 0 <= nx < width and 0 <= ny < height:
                # Se a célula for uma parede, abre um caminho
                if grid[ny][nx] == 1:
                    # Remove a parede entre a célula atual e a nova célula
                    grid[current_y + dy // 2][current_x + dx // 2] = 0
                    grid[ny][nx] = 0  # Marca a nova célula como caminho
                    frontier.append((nx, ny))  # Adiciona a nova célula à fronteira

    # Define a posição de início e fim no labirinto
    start_pos, end_pos = set_start_end(width, height, grid)

    return grid, start_pos, end_pos