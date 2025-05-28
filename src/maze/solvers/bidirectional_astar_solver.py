import heapq
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveBidirectionalAstar(maze):
    """
    Resolve um labirinto usando uma implementação bidirecional do algoritmo A* com distância de Manhattan.
    
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
    
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (x + dx, y + dy)
            if is_valid_position(maze, new_pos[0], new_pos[1]):
                neighbors.append(new_pos)
        return neighbors

    def reconstruct_path(forward_parent, backward_parent, meeting_point):
        # Reconstrói o caminho do início até o ponto de encontro
        forward_path = []
        current = meeting_point
        while current in forward_parent:
            forward_path.append(current)
            current = forward_parent[current]
        forward_path.append(maze.start)
        forward_path.reverse()

        # Reconstrói o caminho do ponto de encontro até o fim
        backward_path = []
        current = meeting_point
        while current in backward_parent:
            backward_path.append(current)
            current = backward_parent[current]
        backward_path.append(maze.end)

        # Combina os caminhos
        return forward_path[1:] + backward_path[1:-1]

    # Inicialização das estruturas para busca em ambas as direções
    forward_open = [(manhattan_distance(maze.start, maze.end), 0, maze.start, [maze.start])]
    backward_open = [(manhattan_distance(maze.end, maze.start), 0, maze.end, [maze.end])]
    heapq.heapify(forward_open)
    heapq.heapify(backward_open)

    # Dicionários para armazenar os pais e custos
    forward_parent = {maze.start: None}
    backward_parent = {maze.end: None}
    forward_g_score = {maze.start: 0}
    backward_g_score = {maze.end: 0}

    # Conjuntos para controle de nós visitados
    forward_visited = {maze.start}
    backward_visited = {maze.end}
    
    # Histórico de células visitadas
    visited_history = [set(forward_visited | backward_visited)]
    
    # Contadores para desempate
    forward_counter = 1
    backward_counter = 1

    while forward_open and backward_open:
        # Expande a busca para frente
        _, _, current_forward, _ = heapq.heappop(forward_open)
        
        for neighbor in get_neighbors(current_forward):
            if neighbor not in forward_visited:
                tentative_g_score = forward_g_score[current_forward] + 1
                
                if neighbor not in forward_g_score or tentative_g_score < forward_g_score[neighbor]:
                    forward_g_score[neighbor] = tentative_g_score
                    forward_parent[neighbor] = current_forward
                    f_score = tentative_g_score + manhattan_distance(neighbor, maze.end)
                    forward_counter += 1
                    heapq.heappush(forward_open, (f_score, forward_counter, neighbor, []))
                    forward_visited.add(neighbor)
                    visited_history.append(set(forward_visited | backward_visited))
                    
                    if neighbor in backward_visited:
                        path = reconstruct_path(forward_parent, backward_parent, neighbor)
                        return path, forward_visited | backward_visited, visited_history

        # Expande a busca para trás
        _, _, current_backward, _ = heapq.heappop(backward_open)
        
        for neighbor in get_neighbors(current_backward):
            if neighbor not in backward_visited:
                tentative_g_score = backward_g_score[current_backward] + 1
                
                if neighbor not in backward_g_score or tentative_g_score < backward_g_score[neighbor]:
                    backward_g_score[neighbor] = tentative_g_score
                    backward_parent[neighbor] = current_backward
                    f_score = tentative_g_score + manhattan_distance(neighbor, maze.start)
                    backward_counter += 1
                    heapq.heappush(backward_open, (f_score, backward_counter, neighbor, []))
                    backward_visited.add(neighbor)
                    visited_history.append(set(forward_visited | backward_visited))
                    
                    if neighbor in forward_visited:
                        path = reconstruct_path(forward_parent, backward_parent, neighbor)
                        return path, forward_visited | backward_visited, visited_history

    return [], forward_visited | backward_visited, visited_history 