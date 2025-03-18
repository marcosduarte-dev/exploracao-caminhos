from enum import Enum

class MazeSize(Enum):
    """
    Enumeração que define os tamanhos disponíveis para o labirinto.
    Cada tamanho está associado a um valor inteiro e a uma descrição das dimensões.
    """

    SMALL = 0  # Labirinto pequeno: 10x10
    MEDIUM = 1  # Labirinto médio: 50x50
    LARGE = 2  # Labirinto grande: 100x100
    REPORT = 3  # Modo de relatório (não possui dimensões específicas)

    def get_dimensions(self):
        """
        Retorna as dimensões do labirinto com base no tamanho selecionado.
        Se o tamanho for REPORT, retorna None.
        """
        dimensions = {
            MazeSize.SMALL: (10, 10),
            MazeSize.MEDIUM: (50, 50),
            MazeSize.LARGE: (100, 100),
            MazeSize.REPORT: None
        }
        return dimensions[self]

    @classmethod
    def size(cls):
        """
        Retorna o número total de tamanhos disponíveis no enum.
        """
        return len(cls)

    def __str__(self):
        """
        Retorna uma representação legível do tamanho do labirinto.
        """
        if self == MazeSize.REPORT:
            return f"{self.name} - Modo de relatório"
        return f"{self.name} - {self.get_dimensions()[0]}x{self.get_dimensions()[1]}"