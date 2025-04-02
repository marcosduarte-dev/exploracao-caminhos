import heapq
from utils.maze_utils import is_valid_position, Benchmark

@Benchmark.measure
def solveAstarManhattan(maze):
    # Função heurística de Manhattan (distância de Manhattan até o destino)
    def manhattan_distance(pos):
        return abs(pos[0] - maze.end[0]) + abs(pos[1] - maze.end[1])
    
    # Fila de prioridade para A*
    # Formato: (f_score, contador, posição atual, caminho)
    # O contador serve para desempatar quando f_score é igual
    start_pos = maze.start
    counter = 0
    open_set = [(manhattan_distance(start_pos), counter, start_pos, [start_pos])]
    heapq.heapify(open_set)
    
    # Conjuntos para controle
    visited = {start_pos}
    visited_history = [set(visited)]  # Histórico de células visitadas
    
    # Para cada nó, g_score é o custo do caminho mais barato do início até o nó
    g_score = {start_pos: 0}
    
    while open_set:
        # Obtém o nó atual com menor f_score da fila de prioridade
        _, _, current, path = heapq.heappop(open_set)
        
        # Verifica se chegou ao destino
        if current == maze.end:
            return path, visited, visited_history
        
        x, y = current
        
        # Explora os vizinhos
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (x + dx, y + dy)
            
            if is_valid_position(maze, neighbor[0], neighbor[1]):
                # Calcula tentative_g_score
                tentative_g_score = g_score[current] + 1
                
                # Se este caminho para o vizinho é melhor que o anterior
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Atualiza os valores para este vizinho
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + manhattan_distance(neighbor)
                    
                    # Adiciona à fila de prioridade somente se não visitado
                    if neighbor not in visited:
                        counter += 1
                        heapq.heappush(open_set, (f_score, counter, neighbor, path + [neighbor]))
                        visited.add(neighbor)
                        visited_history.append(set(visited))
    
    return [], visited, visited_history  # Retorna caminho vazio se não encontrar solução