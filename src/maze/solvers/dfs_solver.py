from collections import deque
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
@Benchmark.measure_memory
def solveDfs(maze):
    """
    Resolve um labirinto usando o algoritmo Depth-First Search (DFS).
    
    Args:
        maze (Maze): Objeto do labirinto contendo:
            - start: Tupla (x,y) com a posição inicial
            - end: Tupla (x,y) com a posição final
            - grid: Matriz representando o labirinto (0=caminho, 1=parede)
    
    Returns:
        tuple: Contendo três elementos:
            - list: Caminho da solução como lista de coordenadas [(x1,y1), (x2,y2), ...]
            - set: Todas as células visitadas durante a busca
            - set: Histórico do momento que visitou as células
    """
    
    # Inicializa a pilha para DFS com:
    # - Primeiro elemento: posição inicial
    # - Segundo elemento: caminho percorrido (inicia só com a posição inicial)
    stack = deque([(maze.start, [maze.start])])
    
    # Conjunto para armazenar posições já visitadas (evita revisitar)
    visited = {maze.start}
    visited_history = [set(visited)]  # Histórico de células visitadas
    
    # Loop principal da DFS
    while stack:
        # Remove o último elemento da pilha
        (x, y), path = stack.pop()
        
        # Verifica se chegou ao destino
        if (x, y) == maze.end:
            return path, visited, visited_history  # Retorna solução encontrada
            
        # Explora os 4 vizinhos (direita, baixo, esquerda, cima)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy  # Calcula nova posição
            
            # Verifica se a nova posição é válida (caminho e não visitada)
            if is_valid_position(maze, nx, ny) and (nx, ny) not in visited:
                # Adiciona à pilha com o novo caminho (path + nova posição)
                stack.append(((nx, ny), path + [(nx, ny)]))
                # Marca como visitada
                visited.add((nx, ny))
                visited_history.append(set(visited))
    
    # Se a pilha esvaziar sem encontrar solução
    return [], visited, visited_history   # Retorna caminho vazio
