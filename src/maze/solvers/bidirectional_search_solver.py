from collections import deque
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveBidirectionalSearch(maze):
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

        return forward_path[1:] + backward_path[1:-1]

    # Inicialização das filas para busca em ambas as direções
    forward_queue = deque([maze.start])
    backward_queue = deque([maze.end])

    # Dicionários para armazenar os pais de cada nó em ambas as direções
    forward_parent = {maze.start: None}
    backward_parent = {maze.end: None}

    # Conjuntos para controle de nós visitados em ambas as direções
    forward_visited = {maze.start}
    backward_visited = {maze.end}
    
    # Histórico de células visitadas
    visited_history = [set(forward_visited | backward_visited)]

    while forward_queue and backward_queue:
        # Expande a busca para frente
        current_forward = forward_queue.popleft()
        for neighbor in get_neighbors(current_forward):
            if neighbor not in forward_visited:
                forward_visited.add(neighbor)
                forward_parent[neighbor] = current_forward
                forward_queue.append(neighbor)
                visited_history.append(set(forward_visited | backward_visited))
                
                # Verifica se encontrou um nó visitado pela busca para trás
                if neighbor in backward_visited:
                    path = reconstruct_path(forward_parent, backward_parent, neighbor)
                    return path, forward_visited | backward_visited, visited_history

        # Expande a busca para trás
        current_backward = backward_queue.popleft()
        for neighbor in get_neighbors(current_backward):
            if neighbor not in backward_visited:
                backward_visited.add(neighbor)
                backward_parent[neighbor] = current_backward
                backward_queue.append(neighbor)
                visited_history.append(set(forward_visited | backward_visited))
                
                # Verifica se encontrou um nó visitado pela busca para frente
                if neighbor in forward_visited:
                    path = reconstruct_path(forward_parent, backward_parent, neighbor)
                    return path, forward_visited | backward_visited, visited_history

    return [], forward_visited | backward_visited, visited_history  # Retorna caminho vazio se não encontrar solução 