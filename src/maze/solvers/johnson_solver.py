import heapq
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveJohnson(maze):
    """
    Resolve um labirinto usando o algoritmo de Johnson (adaptado).
    Assume que todas as arestas têm peso 1 e não há pesos negativos.
    
    Args:
        maze (Maze): Objeto com .start, .end e .grid
    
    Returns:
        tuple: (path, visited, visited_history)
    """
    rows, cols = len(maze.grid), len(maze.grid[0])
    
    # Lista de posições válidas (onde grid[x][y] == 0)
    valid_positions = [
        (x, y)
        for x in range(rows)
        for y in range(cols)
        if is_valid_position(maze, x, y)
    ]

    # Mapeia todas as posições válidas com potencial infinito, exceto start
    h = {pos: float('inf') for pos in valid_positions}
    h[maze.start] = 0

    # === Bellman-Ford para calcular os potenciais ===
    for _ in range(len(valid_positions) - 1):
        for (x, y) in valid_positions:
            for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                nx, ny = x + dx, y + dy
                if is_valid_position(maze, nx, ny):
                    u, v = (x, y), (nx, ny)
                    if h[u] + 1 < h[v]:
                        h[v] = h[u] + 1

    # === Verificação de ciclos negativos (não esperados) ===
    for (x, y) in valid_positions:
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if is_valid_position(maze, nx, ny):
                u, v = (x, y), (nx, ny)
                if h[u] + 1 < h[v]:
                    # Ciclo negativo detectado
                    return [], set(), []

    # === Dijkstra com pesos reponderados ===
    heap = [(0, maze.start, [maze.start])]
    visited = set()
    visited_history = [set()]

    while heap:
        cost, (x, y), path = heapq.heappop(heap)

        if (x, y) in visited:
            continue

        visited.add((x, y))
        visited_history.append(set(visited))

        if (x, y) == maze.end:
            return path, visited, visited_history

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if is_valid_position(maze, nx, ny) and (nx, ny) not in visited:
                # Peso ajustado (como em Johnson)
                u, v = (x, y), (nx, ny)
                adjusted_weight = 1 + h[u] - h[v]
                heapq.heappush(heap, (cost + adjusted_weight, v, path + [v]))

    return [], visited, visited_history
