import random
from enums.maze_size import MazeSize

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # 1 é parede, 0 é caminho
        self.start = (0, 0)
        self.end = (width-1, height-1)
        self.generate_bfs()

    def generate_bfs(self):
        # Algoritmo de geração: DFS com backtracking
        # Começamos com todas as células como paredes
        # Depois escolhemos um ponto inicial e escavamos caminhos

        # Inicializa todas as células como paredes
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Escolhe um ponto inicial aleatório (garantindo que seja ímpar para ter caminhos mais largos)
        start_x = random.randint(0, self.width-1)
        start_y = random.randint(0, self.height-1)
        self.grid[start_y][start_x] = 0
        
        # Lista de células fronteiriças para explorar
        frontier = [(start_x, start_y)]
        
        while frontier:
            # Escolhe uma célula aleatória da fronteira
            current_x, current_y = frontier.pop(random.randint(0, len(frontier) - 1))
            
            # Direções possíveis: (dx, dy)
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                
                # Verifica se a nova posição está dentro dos limites
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Se for uma parede, podemos escavar
                    if self.grid[ny][nx] == 1:
                        # Escava um caminho conectando as células
                        self.grid[current_y + dy//2][current_x + dx//2] = 0
                        self.grid[ny][nx] = 0
                        frontier.append((nx, ny))
        
        # Ajusta os pontos inicial e final para serem caminhos válidos
        # Procura um ponto inicial próximo ao canto superior esquerdo
        for y in range(min(3, self.height)):
            for x in range(min(3, self.width)):
                if self.grid[y][x] == 0:
                    self.start = (x, y)
                    break
            else:
                continue
            break
        
        # Se não encontrou um ponto inicial válido, força uma abertura
        if self.grid[self.start[1]][self.start[0]] != 0:
            self.start = (0, 0)
            self.grid[0][0] = 0
            self.grid[0][1] = 0
        
        # Procura um ponto final próximo ao canto inferior direito
        for y in range(self.height-1, max(self.height-4, 0), -1):
            for x in range(self.width-1, max(self.width-4, 0), -1):
                if self.grid[y][x] == 0:
                    self.end = (x, y)
                    break
            else:
                continue
            break
        
        # Se não encontrou um ponto final válido, força uma abertura
        if self.grid[self.end[1]][self.end[0]] != 0:
            self.end = (self.width-1, self.height-1)
            self.grid[self.height-1][self.width-1] = 0
            self.grid[self.height-1][self.width-2] = 0