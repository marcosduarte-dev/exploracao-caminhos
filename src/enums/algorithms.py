from enum import Enum

class Algorithm(Enum):
    """
    Enumeração que representa os algoritmos disponíveis para execução.
    Cada algoritmo é associado a um valor inteiro único, que pode ser usado para identificá-lo.
    Adicionar novos algoritmos aqui automaticamente os disponibiliza para uso no sistema.
    """

    BFS = 0
    #DFS = 1
    DIJKSTRA = 2
    GREEDY_BFS = 3
    #JOHNSON = 3
    #FLOYD_WARSHALL = 4
    BIDIRECTIONAL_SEARCH = 4
    ASTAR_MANHATTAN = 5  
    #ASTAR_EUCLIDIANA = 6
    #ACO = 7
    

    def __str__(self):
        """
        Retorna uma representação legível do algoritmo.
        """
        return f"{self.name} ({self.value})"
    
    @classmethod
    def size(cls):
        """
        Retorna o número total de tamanhos disponíveis no enum.
        """
        return len(cls)
    
    @property
    def display_name(self):
        """
        Substitui caracteres para deixar nomes mais legiveis
        """
        name = self.name.replace("_", " ")
        name = name.replace("ASTAR", "A*")
        return name