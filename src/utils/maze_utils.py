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