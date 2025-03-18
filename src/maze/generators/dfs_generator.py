import random
from utils.maze_utils import set_start_end

def generate_maze(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]
    
    # Escolhe um ponto inicial aleatório
    start_x = random.randint(0, width-1)
    start_y = random.randint(0, height-1)
    grid[start_y][start_x] = 0
    
    frontier = [(start_x, start_y)]
    
    while frontier:
        current_x, current_y = frontier.pop(random.randint(0, len(frontier) - 1))
        
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == 1:
                    grid[current_y + dy//2][current_x + dx//2] = 0
                    grid[ny][nx] = 0
                    frontier.append((nx, ny))

    set_start_end(width, height, grid)
    
    return grid