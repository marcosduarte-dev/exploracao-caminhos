import heapq
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveDijkstra(maze):
    """
    Resolve um labirinto usando o algoritmo de Dijkstra.

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

    # Fila de prioridade: (custo_acumulado, posição_atual, caminho)
    heap = [(0, maze.start, [maze.start])]
    visited = set()
    visited_history = []

    while heap:
        cost, current, path = heapq.heappop(heap)
        if current in visited:
            continue

        visited.add(current)
        visited_history.append(set(visited))

        if current == maze.end:
            return path, visited, visited_history

        x, y = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)

            if is_valid_position(maze, nx, ny) and next_pos not in visited:
                # Aqui o custo de cada movimento é 1, mas poderia ser customizado
                heapq.heappush(heap, (cost + 1, next_pos, path + [next_pos]))

    # Se o destino não for alcançado
    return [], visited, visited_history
