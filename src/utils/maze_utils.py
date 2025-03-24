from enums.maze_size import MazeSize
from maze.maze import Maze
from functools import wraps
import time

def generate_mazes():
    """
    Gera labirintos para cada tamanho definido no enum MazeSize.

    Retorna:
        tuple: Uma tupla contendo quatro dicionários:
            - mazes: Labirintos gerados para cada tamanho.
            - solutions: Estrutura para armazenar soluções de cada labirinto.
            - visited_cells: Estrutura para armazenar células visitadas durante a solução.
            - statistics: Estatísticas coletadas durante a solução dos labirintos.
    """
    # Inicializa os labirintos para cada tamanho
    mazes = {
        MazeSize.SMALL: Maze(10, 10),
        MazeSize.MEDIUM: Maze(50, 50),
        MazeSize.LARGE: Maze(100, 100),
        MazeSize.REPORT: {}  # Modo de relatório não precisa de labirinto
    }

    # Inicializa as estruturas para soluções, células visitadas e estatísticas
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


def is_valid_position(maze, x, y):
    """
    Verifica se uma posição é válida no labirinto (dentro dos limites e é um caminho).

    Args:
        x (int): Coordenada x (coluna) da célula.
        y (int): Coordenada y (linha) da célula.

    Returns:
        bool: True se a posição é válida, False caso contrário.
    """
    return 0 <= x < maze.width and 0 <= y < maze.height and maze.grid[y][x] != 1


def set_start_end(width, height, grid):
    """
    Define as posições de início e fim no labirinto.

    Args:
        width (int): Largura do labirinto.
        height (int): Altura do labirinto.
        grid (list): Grade do labirinto.

    Returns:
        tuple: Posições de início e fim no formato ((x_inicio, y_inicio), (x_fim, y_fim)).
    """
    start_pos = _find_start_position(width, height, grid)
    end_pos = _find_end_position(width, height, grid)

    return start_pos, end_pos


def _find_start_position(width, height, grid):
    """
    Encontra uma posição de início válida no canto superior esquerdo do labirinto.

    Args:
        width (int): Largura do labirinto.
        height (int): Altura do labirinto.
        grid (list): Grade do labirinto.

    Returns:
        tuple: Posição de início no formato (x, y).
    """
    # Procura um ponto inicial próximo ao canto superior esquerdo
    for y in range(min(3, height)):
        for x in range(min(3, width)):
            if grid[y][x] == 0:
                grid[y][x] = 2  # Marca como início
                return (x, y)

    # Se não encontrou um ponto inicial válido, força uma abertura
    grid[0][0] = 2  # Marca como início
    if width > 1:
        grid[0][1] = 0  # Abre uma célula adjacente
    return (0, 0)


def _find_end_position(width, height, grid):
    """
    Encontra uma posição de fim válida no canto inferior direito do labirinto.

    Args:
        width (int): Largura do labirinto.
        height (int): Altura do labirinto.
        grid (list): Grade do labirinto.

    Returns:
        tuple: Posição de fim no formato (x, y).
    """
    # Procura um ponto final próximo ao canto inferior direito
    for y in range(height - 1, max(height - 4, 0), -1):
        for x in range(width - 1, max(width - 4, 0), -1):
            if grid[y][x] == 0:
                grid[y][x] = 3  # Marca como fim
                return (x, y)

    # Se não encontrou um ponto final válido, força uma abertura
    grid[height - 1][width - 1] = 3  # Marca como fim
    if width > 1 and height > 1:
        grid[height - 1][width - 2] = 0  # Abre uma célula adjacente
    return (width - 1, height - 1)


class Benchmark:
    """
    Classe utilitária para medição de tempo de execução.
    """
    @staticmethod
    def measure(func):
        """
        Decorador que mede o tempo de execução em milissegundos.
        
        Args:
            func (callable): Função a ser decorada
            
        Returns:
            tuple: Resultado original da função + tempo em ms (como último elemento)
        """
        @wraps(func)
        def timed(*args, **kwargs):
            start = time.perf_counter_ns()
            result = func(*args, **kwargs)
            end = time.perf_counter_ns()
            
            elapsed_ms = (end - start) / 1_000_000  # Converte para milissegundos
            
            if isinstance(result, tuple):
                return (*result, elapsed_ms)
            return (result, elapsed_ms)
            
        return timed