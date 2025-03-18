from enum import Enum

class Algorithm(Enum):
    """
    Enumeração que representa os algoritmos disponíveis para execução.
    Cada algoritmo é associado a um valor inteiro único, que pode ser usado para identificá-lo.
    Adicionar novos algoritmos aqui automaticamente os disponibiliza para uso no sistema.
    """

    BFS = 0  # Breadth-First Search: Algoritmo de busca em largura, utilizado para explorar nós em grafos ou árvores nível por nível.
    DFS = 1  # Depth-First Search: Algoritmo de busca em profundidade, que explora o máximo possível ao longo de cada ramo antes de retroceder.
    ASTAR = 2  # A* (A Estrela): Algoritmo de busca que utiliza heurísticas para encontrar o caminho mais curto entre dois pontos.
    DIJKSTRA = 3  # Dijkstra: Algoritmo de busca que encontra o caminho mais curto entre dois nós em um grafo com pesos não negativos.

    # Exemplo de como adicionar um novo algoritmo:
    # NOVO_ALGORITMO = 4  # Descrição breve do novo algoritmo.

    def __str__(self):
        """
        Retorna uma representação legível do algoritmo.
        """
        return f"{self.name} ({self.value}) - {self.__doc__}"