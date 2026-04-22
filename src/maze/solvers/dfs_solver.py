from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
@Benchmark.measure_memory
def solveDfs(maze):
    """
    Resolve um labirinto usando o algoritmo Depth-First Search (DFS) com recursão.
    
    Args:
        maze (Maze): Objeto do labirinto contendo:
            - start: Tupla (x,y) com a posição inicial
            - end: Tupla (x,y) com a posição final
            - grid: Matriz representando o labirinto (0=caminho, 1=parede)
    
    Returns:
        tuple: Contendo três elementos:
            - list: Caminho da solução como lista de coordenadas [(x1,y1), (x2,y2), ...]
            - set: Todas as células visitadas durante a busca
            - list: Histórico do momento que visitou as células
    """
    
    # Conjunto para armazenar posições já visitadas (evita revisitar)
    visited = set()
    visited_history = []  # Histórico de células visitadas

    def dfs_recursive(x, y, path):
        # Adiciona a posição atual aos visitados e ao histórico
        visited.add((x, y))
        visited_history.append(set(visited))

        # Verifica se chegou ao destino
        if (x, y) == maze.end:
            return path  # Retorna o caminho da solução

        # Explora os 4 vizinhos (direita, baixo, esquerda, cima)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy  # Calcula nova posição

            # Verifica se a nova posição é válida (caminho e não visitada)
            if is_valid_position(maze, nx, ny) and (nx, ny) not in visited:
                # Chama recursivamente para o vizinho
                result = dfs_recursive(nx, ny, path + [(nx, ny)])
                # Se encontrou um caminho, retorna o resultado
                if result:
                    return result
        
        # Se nenhum vizinho levou à solução, retorna None
        return None

    # Inicia a busca recursiva a partir da posição inicial
    solution_path = dfs_recursive(maze.start[0], maze.start[1], [maze.start])
    
    # Retorna o caminho encontrado (ou vazio) e os dados da busca
    return solution_path if solution_path else [], visited, visited_history
