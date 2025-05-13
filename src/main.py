import os
import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.maze_utils import generate_mazes
from ui.ui import UI
from maze.solvers.bfs_solver import solveBfs
from maze.solvers.AStartManhattan_solver import solveAstarManhattan
from maze.solvers.dijkstra_solver import solveDijkstra
from maze.solvers.johnson_solver import solveJohnson
from maze.solvers.floydWarshall_solver import solveFloydWarshall
from maze.solvers.greedy_bfs_solver import solveGreedyBFS
from maze.solvers.bidirectional_search_solver import solveBidirectionalSearch
from ui.slider import Slider

class Main:

    def __init__(self):
        """
        Inicializa a janela do jogo, carrega recursos e define o estado inicial.
        """
        pygame.init()

        # Configuração da janela
        pygame.display.set_caption(TITULO_PROJETO)
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.clock = pygame.time.Clock()

        # Caminhos para recursos
        self.current_path = os.path.dirname(__file__)
        self.sprites_path = {
            'current_tab': os.path.join(self.current_path, 'ui/sprites', 'tab_selecionado.png'),
            'normal_tab': os.path.join(self.current_path, 'ui/sprites', 'tab.png')
        }
        self.font_path = os.path.join(self.current_path, 'ui', 'font', 'Inter.ttf')

        # Inicialização de componentes
        self.ui = UI(self.font_path, self.screen)
        self.current_tab = MazeSize.SMALL
        self.current_algorithm = None
        self.sprites = self._load_sprites()
        self.zoom_level = 1.0
        self.offset_x, self.offset_y = 0, 0
        self.dragging = False
        self.drag_start_x, self.drag_start_y = 0, 0 
        self.show_visited = True  # Mostrar células visitadas
        self.show_solution = False # Mostrar células solução independente da step
        self.step_slider = None
        self.start_x = LARGURA_TELA - 400

        self.running = True

        self.mazes, self.solutions, self.visited_cells, self.statistics, self.visited_history, self.sliders = generate_mazes()

    def _load_sprites(self):
        """
        Carrega os sprites das abas.

        Returns:
            dict: Dicionário com os sprites carregados.
        """
        return {
            'sprite_current_tab': pygame.image.load(self.sprites_path['current_tab']).convert_alpha(),
            'sprite_normal_tab': pygame.image.load(self.sprites_path['normal_tab']).convert_alpha()
        }

    def handle_events(self):
        """
        Processa os eventos do jogo, como cliques do mouse e fechamento da janela.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Fecha o jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Soltar o botão esquerdo
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
            if (hasattr(self, 'sliders') and 
                self.current_tab in self.sliders and 
                self.current_algorithm in self.sliders[self.current_tab]):
                
                slider = self.sliders[self.current_tab][self.current_algorithm]
                slider.handle_event(event)

    def _handle_mouse_button_down(self, event):
        """Processa cliques do mouse."""
        if event.button == 1:  # Clique esquerdo
            # Verifica se o clique foi em uma aba
            for size, rect in self.ui.tabs.items():
                if rect.collidepoint(event.pos):
                    if(self.current_tab != size):
                        self.current_tab = size
                        self.current_algorithm = None
                    break
            # Verifica se o clique foi em um algoritmo
            for algorithm, rect in self.ui.algorithm_buttons.items():
                if rect.collidepoint(event.pos):
                    path = []
                    visited = []
                    history = []
                    time_taken = 0
                    if algorithm == Algorithm.BFS:
                        self.current_algorithm = Algorithm.BFS
                        if(self.solutions.get(self.current_tab) == {} or self.solutions[self.current_tab].get(self.current_algorithm) is None):
                            path, visited, history, time_taken = solveBfs(self.mazes[self.current_tab])
                        else:
                            path = self.solutions[self.current_tab][self.current_algorithm]
                            visited = self.visited_cells[self.current_tab][self.current_algorithm]
                            history = self.visited_history[self.current_tab][self.current_algorithm]
                            time_taken = self.statistics[self.current_tab][self.current_algorithm]["time_taken"]
                    # if algorithm == Algorithm.DFS:
                    #     # Implementar DFS
                    #     path = []
                    #     visited = []
                    #     time_taken = []
                    #     print("DFS")
                    if algorithm == Algorithm.DIJKSTRA:
                        self.current_algorithm = Algorithm.DIJKSTRA
                        if(self.solutions.get(self.current_tab) == {} or self.solutions[self.current_tab].get(self.current_algorithm) is None):
                            path, visited, history, time_taken = solveDijkstra(self.mazes[self.current_tab])
                        else:
                            path = self.solutions[self.current_tab][self.current_algorithm]
                            visited = self.visited_cells[self.current_tab][self.current_algorithm]
                            history = self.visited_history[self.current_tab][self.current_algorithm]
                            time_taken = self.statistics[self.current_tab][self.current_algorithm]["time_taken"]
                    # if algorithm == Algorithm.JOHNSON:
                    #     self.current_algorithm = Algorithm.JOHNSON
                    #     path, visited, history, time_taken = solveJohnson(self.mazes[self.current_tab])
                    # if algorithm == Algorithm.FLOYD_WARSHALL:
                    #     self.current_algorithm = Algorithm.FLOYD_WARSHALL
                    #     path, visited, history, time_taken = solveFloydWarshall(self.mazes[self.current_tab])
                    if algorithm == Algorithm.ASTAR_MANHATTAN:
                        self.current_algorithm = Algorithm.ASTAR_MANHATTAN
                        if(self.solutions.get(self.current_tab) == {} or self.solutions[self.current_tab].get(self.current_algorithm) is None):
                            path, visited, history, time_taken = solveAstarManhattan(self.mazes[self.current_tab])
                        else:
                            path = self.solutions[self.current_tab][self.current_algorithm]
                            visited = self.visited_cells[self.current_tab][self.current_algorithm]
                            history = self.visited_history[self.current_tab][self.current_algorithm]
                            time_taken = self.statistics[self.current_tab][self.current_algorithm]["time_taken"]
                    if algorithm == Algorithm.GREEDY_BFS:
                        self.current_algorithm = Algorithm.GREEDY_BFS
                        if(self.solutions.get(self.current_tab) == {} or self.solutions[self.current_tab].get(self.current_algorithm) is None):
                            path, visited, history, time_taken = solveGreedyBFS(self.mazes[self.current_tab])
                        else:
                            path = self.solutions[self.current_tab][self.current_algorithm]
                            visited = self.visited_cells[self.current_tab][self.current_algorithm]
                            history = self.visited_history[self.current_tab][self.current_algorithm]
                            time_taken = self.statistics[self.current_tab][self.current_algorithm]["time_taken"]
                    if algorithm == Algorithm.BIDIRECTIONAL_SEARCH:
                        self.current_algorithm = Algorithm.BIDIRECTIONAL_SEARCH
                        if(self.solutions.get(self.current_tab) == {} or self.solutions[self.current_tab].get(self.current_algorithm) is None):
                            path, visited, history, time_taken = solveBidirectionalSearch(self.mazes[self.current_tab])
                        else:
                            path = self.solutions[self.current_tab][self.current_algorithm]
                            visited = self.visited_cells[self.current_tab][self.current_algorithm]
                            history = self.visited_history[self.current_tab][self.current_algorithm]
                            time_taken = self.statistics[self.current_tab][self.current_algorithm]["time_taken"]
                    
                    self.solutions[self.current_tab][self.current_algorithm] = path
                    self.visited_cells[self.current_tab][self.current_algorithm] = visited
                    self.statistics[self.current_tab][self.current_algorithm] = {
                        "visited_count": len(visited),
                        "time_taken": time_taken,
                        "path_length": len(path)
                    }
                    self.visited_history[self.current_tab][self.current_algorithm] = history
                    if history and self.show_visited:
                        if not hasattr(self, 'sliders'):
                            self.sliders = {
                                MazeSize.SMALL: {},
                                MazeSize.MEDIUM: {},
                                MazeSize.LARGE: {}
                            }
                        self.sliders[self.current_tab][self.current_algorithm] = Slider(
                            self.start_x + 25, ALTURA_TELA - 30, 400 - 40, 10, 
                            0, len(history) - 1, 0
                        )
                    print("Quantidade visitada: " + str(len(visited)))
                    print("Tempo levado: " + str(time_taken) + " ms" )
                    print("Tamanho do caminho: " + str(len(path)))

                    self.statistics[self.current_tab][self.current_algorithm]

                if hasattr(self.ui, 'generate_button_rect') and self.ui.generate_button_rect.collidepoint(event.pos):
                    self.mazes, self.solutions, self.visited_cells, self.statistics, self.visited_history, self.sliders = generate_mazes()
                    self.current_algorithm = None  # limpa seleção anterior

            if event.pos[0] < 800:
                self.dragging = True
                self.drag_start_x, self.drag_start_y = event.pos

        elif event.button == 4:  # Roda do mouse para cima (zoom in)
            self.zoom_level = min(5.0, self.zoom_level + 0.1)
        elif event.button == 5:  # Roda do mouse para baixo (zoom out)
            self.zoom_level = max(0.1, self.zoom_level - 0.1)

    def _handle_mouse_motion(self, event):
        """
        Processa o movimento do mouse durante o arrasto.
        """
        if self.dragging:
            self.offset_x += event.pos[0] - self.drag_start_x
            self.offset_y += event.pos[1] - self.drag_start_y
            self.drag_start_x, self.drag_start_y = event.pos

    def update(self):
        """
        Atualiza a tela do jogo.
        """
        self.screen.fill(WHITE)  # Limpa a tela com fundo branco

        # Desenha o labirinto e as abas
        self.ui.draw_maze(
            self.mazes[self.current_tab], self.current_tab, self.current_algorithm,
            self.zoom_level, self.offset_x, self.offset_y, self.show_visited, 
            self.show_solution, self.solutions, self.visited_cells, self.statistics,
            self.visited_history, self.sliders
        )
        self.ui.draw_tabs(self.current_tab, self.sprites)
        self.ui.draw_algorithm_buttons(self.current_algorithm, self.sprites)
        #self.ui.draw_generate_button(self.screen, 20, 20)
        button_width = 50  # Tamanho do botão circular
        x = self.start_x + (650 - button_width) // 2
        self.ui.draw_generate_button(self.screen, x, 50)  # Y = 50, por exemplo

        # Desenhar estatísticas (abaixo dos controles)
        stats = self.statistics[self.current_tab].get(self.current_algorithm)
        if stats:
           self.ui.draw_statistics(self.screen, stats, self.start_x + 20, 450)


        pygame.display.flip()

    def run(self):
        """
        Executa o loop principal do jogo.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.run()