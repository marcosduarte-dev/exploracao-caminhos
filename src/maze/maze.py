import random
from enums.maze_size import MazeSize
from maze.generators.prim_multipath_generator import generate_maze

class Maze:
    """
    Classe que representa um labirinto.

    Atributos:
        width (int): Largura do labirinto (número de colunas).
        height (int): Altura do labirinto (número de linhas).
        generator (function): Função geradora do labirinto (padrão: PRIM Multipath).
        grid (list): Matriz que representa o labirinto, onde 1 é parede e 0 é caminho.
        start (tuple): Posição inicial do labirinto (linha, coluna).
        end (tuple): Posição final do labirinto (linha, coluna).
    """

    def __init__(self, width, height, generator=generate_maze):
        """
        Inicializa o labirinto com as dimensões especificadas e um gerador opcional.

        Args:
            width (int): Largura do labirinto.
            height (int): Altura do labirinto.
            generator (function): Função geradora do labirinto (padrão: PRIM Multipath).
        """
        self.width = width
        self.height = height
        self.generator = generator
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # Inicializa o labirinto com paredes (1)
        self.start = (0, 0)  # Posição inicial padrão
        self.end = (width - 1, height - 1)  # Posição final padrão
        self.generate()  # Gera o labirinto

    def generate(self):
        """
        Gera o labirinto usando o gerador especificado.
        Atualiza a grade do labirinto e define as posições de início e fim.
        """
        self.grid, self.start, self.end = self.generator(self.width, self.height)  # Gera o labirinto

    def __str__(self):
        """
        Retorna uma representação legível do labirinto.

        Returns:
            str: String formatada representando o labirinto.
        """
        maze_str = ""
        for row in self.grid:
            maze_str += " ".join(str(cell) for cell in row) + "\n"
        return maze_str

    def get_cell(self, x, y):
        """
        Retorna o valor de uma célula específica no labirinto.

        Args:
            x (int): Coordenada x (coluna) da célula.
            y (int): Coordenada y (linha) da célula.

        Returns:
            int: Valor da célula (0 para caminho, 1 para parede).
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        raise IndexError("Coordenadas fora dos limites do labirinto.")

    def set_cell(self, x, y, value):
        """
        Define o valor de uma célula específica no labirinto.

        Args:
            x (int): Coordenada x (coluna) da célula.
            y (int): Coordenada y (linha) da célula.
            value (int): Valor a ser definido (0 para caminho, 1 para parede).
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value
        else:
            raise IndexError("Coordenadas fora dos limites do labirinto.")