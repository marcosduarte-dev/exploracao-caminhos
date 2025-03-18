from enums.maze_size import MazeSize
from maze.maze import Maze

def generate_mazes():
    mazes = {
        MazeSize.SMALL: Maze(10, 10),
        MazeSize.MEDIUM: Maze(50, 50),
        MazeSize.LARGE: Maze(100, 100),
        MazeSize.REPORT: {}
    }
    
    # Limpa as soluções existentes
    solutions = {
        MazeSize.SMALL: {},
        MazeSize.MEDIUM: {},
        MazeSize.LARGE: {},
    }
    
    visited_cells = {
        MazeSize.SMALL: {},
        MazeSize.MEDIUM: {},
        MazeSize.LARGE: {}
    }
    
    statistics = {
        MazeSize.SMALL: {},
        MazeSize.MEDIUM: {},
        MazeSize.LARGE: {}
    }
    
    return mazes, solutions, visited_cells, statistics

def is_valid_position(self, x, y):
    return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == 0

def set_start_end(width, height, grid):
    # Procura um ponto inicial próximo ao canto superior esquerdo
    for y in range(min(3, height)):
        for x in range(min(3, width)):
            if grid[y][x] == 0:
                start = True
                grid[y][x] = 2
                break
        else:
            continue
        break
    
    # Se não encontrou um ponto inicial válido, força uma abertura
    if not start:
        start = True
        grid[0][0] = 2
        if width > 1:
            grid[0][1] = 0
    
    # Procura um ponto final próximo ao canto inferior direito
    for y in range(height-1, max(height-4, 0), -1):
        for x in range(width-1, max(width-4, 0), -1):
            if grid[y][x] == 0:
                end = True
                grid[y][x] = 3
                break
        else:
            continue
        break
    
    # Se não encontrou um ponto final válido, força uma abertura
    if not end:
        end = True
        grid[height-1][width-1] = 3
        if width > 1 and height > 1:
            grid[height-1][width-2] = 0