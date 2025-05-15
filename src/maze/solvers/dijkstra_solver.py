import heapq
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveDijkstra(maze):
    """
    Resolve um labirinto usando uma implementação otimizada do algoritmo de Dijkstra.
    
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
    
    # Inicializa estruturas de dados
    distances = {maze.start: 0}  # Distância do início até cada nó
    previous = {maze.start: None}  # Nó anterior no caminho mais curto
    visited = {maze.start}  # Conjunto de nós visitados
    visited_history = [set(visited)]  # Histórico de visitas
    
    # Fila de prioridade: (distância, posição)
    priority_queue = [(0, maze.start)]
    heapq.heapify(priority_queue)
    
    while priority_queue:
        # Pega o nó com menor distância
        current_distance, current = heapq.heappop(priority_queue)
        
        # Se já encontramos um caminho melhor para este nó, ignora
        if current_distance > distances[current]:
            continue
            
        # Se chegamos ao destino, reconstrói o caminho
        if current == maze.end:
            path = []
            while current is not None:
                path.append(current)
                current = previous[current]
            return path[::-1], visited, visited_history
        
        # Explora os vizinhos
        x, y = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (x + dx, y + dy)
            
            # Verifica se o vizinho é válido e não foi visitado
            if is_valid_position(maze, neighbor[0], neighbor[1]) and neighbor not in visited:
                # Calcula nova distância
                new_distance = distances[current] + 1
                
                # Se encontramos um caminho melhor
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                    visited.add(neighbor)
                    visited_history.append(set(visited))
    
    # Se não encontrou caminho
    return [], visited, visited_history 