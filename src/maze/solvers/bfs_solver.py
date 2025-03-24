from collections import deque
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveBfs(maze):
    """
    Resolve um labirinto usando o algoritmo Breadth-First Search (BFS).
    
    Args:
        maze (Maze): Objeto do labirinto contendo:
            - start: Tupla (x,y) com a posição inicial
            - end: Tupla (x,y) com a posição final
            - grid: Matriz representando o labirinto (0=caminho, 1=parede)
    
    Returns:
        tuple: Contendo três elementos:
            - list: Caminho da solução como lista de coordenadas [(x1,y1), (x2,y2), ...]
            - set: Todas as células visitadas durante a busca
    """
    
    # Inicializa a fila para BFS com:
    # - Primeiro elemento: posição inicial
    # - Segundo elemento: caminho percorrido (inicia só com a posição inicial)
    queue = deque([(maze.start, [maze.start])])
    
    # Conjunto para armazenar posições já visitadas (evita revisitar)
    visited = {maze.start}
    
    # Loop principal da BFS
    while queue:
        # Remove o primeiro elemento da fila
        (x, y), path = queue.popleft()
        
        # Verifica se chegou ao destino
        if (x, y) == maze.end:
            return path, visited  # Retorna solução encontrada
            
        # Explora os 4 vizinhos (direita, baixo, esquerda, cima)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy  # Calcula nova posição
            
            # Verifica se a nova posição é válida (caminho e não visitada)
            if is_valid_position(maze, nx, ny) and (nx, ny) not in visited:
                # Adiciona à fila com o novo caminho (path + nova posição)
                queue.append(((nx, ny), path + [(nx, ny)]))
                # Marca como visitada
                visited.add((nx, ny))
    
    # Se a fila esvaziar sem encontrar solução
    return [], visited  # Retorna caminho vazio