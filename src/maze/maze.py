import random
from enums.maze_size import MazeSize
from maze.generators.dfs_generator import generate_maze

class Maze:
    def __init__(self, width, height, generator=generate_maze):
        self.width = width
        self.height = height
        self.generator = generator
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # 1 é parede, 0 é caminho
        self.start = (0, 0)
        self.end = (width-1, height-1)
        self.generate()

    def generate(self):
        self.grid = self.generator(self.width, self.height)
        
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