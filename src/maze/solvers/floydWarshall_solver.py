from utils.maze_utils import is_valid_position, Benchmark
import math

@Benchmark.measure
def solveFloydWarshall(maze):
    """
    Resolve um labirinto usando o algoritmo Floyd-Warshall.
    
    Args:
        maze (Maze): Objeto do labirinto contendo:
            - start: Tupla (x,y) com a posição inicial
            - end: Tupla (x,y) com a posição final
            - grid: Matriz representando o labirinto (0=caminho, 1=parede)
    
    Returns:
        tuple: Contendo três elementos:
            - list: Caminho da solução como lista de coordenadas [(x1,y1), (x2,y2), ...]
            - set: Todas as células visitadas durante a busca
            - list: Histórico das células visitadas
    """
    
    # Lista de todas posições válidas do labirinto
    rows, cols = len(maze.grid), len(maze.grid[0])
    nodes = [(x, y) for x in range(rows) for y in range(cols) if is_valid_position(maze, x, y)]

    index_map = {pos: i for i, pos in enumerate(nodes)}
    rev_map = {i: pos for pos, i in index_map.items()}
    n = len(nodes)

    # Inicializa matriz de distâncias e predecessores
    dist = [[math.inf] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0
        next_node[i][i] = i

    # Adiciona arestas entre vizinhos válidos
    for i, (x, y) in enumerate(nodes):
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if is_valid_position(maze, nx, ny):
                j = index_map[(nx, ny)]
                dist[i][j] = 1
                next_node[i][j] = j

    # Floyd-Warshall: atualiza as distâncias mínimas
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    # Reconstrução do caminho
    visited = set()
    visited_history = []

    start_idx = index_map.get(maze.start)
    end_idx = index_map.get(maze.end)

    if start_idx is None or end_idx is None or next_node[start_idx][end_idx] is None:
        return [], visited, visited_history  # Sem caminho possível

    path = []
    u = start_idx
    while u != end_idx:
        path.append(rev_map[u])
        visited.add(rev_map[u])
        visited_history.append(set(visited))
        u = next_node[u][end_idx]
        if u is None:
            return [], visited, visited_history  # Caminho quebrado

    path.append(rev_map[end_idx])
    visited.add(rev_map[end_idx])
    visited_history.append(set(visited))

    return path, visited, visited_history
