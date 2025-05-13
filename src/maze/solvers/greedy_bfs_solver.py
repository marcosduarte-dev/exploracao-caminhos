import heapq
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveGreedyBFS(maze):
    # Função heurística de Manhattan (distância de Manhattan até o destino)
    def manhattan_distance(pos):
        return abs(pos[0] - maze.end[0]) + abs(pos[1] - maze.end[1])
    
    # Fila de prioridade para Greedy BFS
    # Formato: (heurística, contador, posição atual, caminho)
    # O contador serve para desempatar quando a heurística é igual
    start_pos = maze.start
    counter = 0
    open_set = [(manhattan_distance(start_pos), counter, start_pos, [start_pos])]
    heapq.heapify(open_set)
    
    # Conjuntos para controle
    visited = {start_pos}
    visited_history = [set(visited)]  # Histórico de células visitadas
    
    while open_set:
        # Obtém o nó atual com menor valor heurístico da fila de prioridade
        _, _, current, path = heapq.heappop(open_set)
        
        # Verifica se chegou ao destino
        if current == maze.end:
            return path, visited, visited_history
        
        x, y = current
        
        # Explora os vizinhos
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (x + dx, y + dy)
            
            if is_valid_position(maze, neighbor[0], neighbor[1]) and neighbor not in visited:
                # Calcula o valor heurístico para o vizinho
                h_score = manhattan_distance(neighbor)
                
                # Adiciona à fila de prioridade
                counter += 1
                heapq.heappush(open_set, (h_score, counter, neighbor, path + [neighbor]))
                visited.add(neighbor)
                visited_history.append(set(visited))
    
    return [], visited, visited_history  # Retorna caminho vazio se não encontrar solução 