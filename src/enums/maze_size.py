from enum import Enum

class MazeSize(Enum):
    SMALL = 0  # 10x10
    MEDIUM = 1  # 50x50
    LARGE = 2  # 100x100
    REPORT = 3  # Relatório

    @classmethod
    def size(cls):
        return len(cls)