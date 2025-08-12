import os
import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.maze_utils import generate_mazes
from utils.bd_utils import open_conection, inserir_estatistica
from ui.ui import UI
from maze.solvers.bfs_solver import solveBfs
from maze.solvers.AStartManhattan_solver import solveAstarManhattan
from maze.solvers.bidirectional_search_solver import solveBidirectionalSearch
from maze.solvers.bidirectional_astar_solver import solveBidirectionalAstar
from maze.solvers.greedy_bfs_solver import solveGreedyBFS
from maze.solvers.dfs_solver import solveDfs
from ui.slider import Slider

class Main:

    def __init__(self):
        """
        Inicializa a janela do jogo, carrega recursos e define o estado inicial.
        """
        pygame.init()

        # Caminhos para recursos
        self.current_path = os.path.dirname(__file__)
        self.sprites_path = {
            'current_tab': os.path.join(self.current_path, 'ui/sprites', 'tab_selecionado.png'),
            'normal_tab': os.path.join(self.current_path, 'ui/sprites', 'tab.png')
        }
        self.font_path = os.path.join(self.current_path, 'ui', 'font', 'Inter.ttf')
        self.logo_path = os.path.join(self.current_path, 'ui/sprites', 'labirinto.png')

        # Configuração da janela
        pygame.display.set_caption(TITULO_PROJETO)
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.clock = pygame.time.Clock()
        logo = pygame.image.load(self.logo_path).convert_alpha()
        pygame.display.set_icon(logo)

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
        self.step_slider = None
        self.start_x = LARGURA_TELA - 400
        self.ui.show_slider = False  # Estado inicial do slider (desabilitado)
        self.contagem_generate_maze = 0
        self.is_loading = False

        self.running = True

        self.database = open_conection()

        self.mazes, self.solutions, self.visited_cells, self.statistics, self.visited_history, self.sliders = generate_mazes(self.database)

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
            # Verifica se o clique foi no botão toggle
            if hasattr(self.ui, 'toggle_button_rect') and self.ui.toggle_button_rect.collidepoint(event.pos):
                self.ui.show_slider = not self.ui.show_slider
                return

            # Verifica se o clique foi em uma aba
            for size, rect in self.ui.tabs.items():
                if rect.collidepoint(event.pos):
                    if(self.current_tab != size):
                        self.current_tab = size
                        self.current_algorithm = None
                    break
            # Verifica se o clique foi em um algoritmo
            for algorithm_key, rect in self.ui.algorithm_buttons.items():
                if rect.collidepoint(event.pos):
                    self.is_loading = True
                    self.update()

                    if algorithm_key == "run_all":
                        self.run_all_algorithms()
                    else:
                        path = []
                        visited = []
                        history = []
                        time_taken = 0
                        memory_used = 0

                        path, visited, history, time_taken, memory_used = self.solve_algorithm(algorithm_key)
                        
                        self.solutions[self.current_tab][self.current_algorithm] = path
                        self.visited_cells[self.current_tab][self.current_algorithm] = visited
                        self.statistics[self.current_tab][self.current_algorithm] = {
                            "visited_count": len(visited),
                            "time_taken": time_taken,
                            "path_length": (len(path) - 1),
                            "memory_used": memory_used
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

                        self.statistics[self.current_tab][self.current_algorithm]
                    
                    self.is_loading = False
                    break # Sair do loop de botões de algoritmo

            if hasattr(self.ui, 'generate_button_rect') and self.ui.generate_button_rect.collidepoint(event.pos):
                #self.contagem_generate_maze = self.contagem_generate_maze + 1
                self.contagem_generate_maze = 4
                if(self.contagem_generate_maze == 4):
                    self.is_loading = True
                    self.update()
                    self.mazes, self.solutions, self.visited_cells, self.statistics, self.visited_history, self.sliders = generate_mazes(self.database)
                    self.current_algorithm = None  # limpa seleção anterior
                    self.contagem_generate_maze = 0
                    self.is_loading = False

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
            self.solutions, self.visited_cells, self.statistics,
            self.visited_history, self.sliders
        )
        self.ui.draw_tabs(self.current_tab, self.sprites)

        if self.current_tab.value != 3:  # Se não for a aba de estatísticas

            self.ui.draw_algorithm_buttons(self.current_algorithm, self.sprites)
            button_width = 50  # Tamanho do botão circular
            x = self.start_x + (650 - button_width) // 2
            self.ui.draw_generate_button(self.screen, x, 50)  # Y = 50, por exemplo

            # Desenha o check no botão toggle
            if hasattr(self.ui, 'toggle_button_rect'):
                self.ui.draw_toggle_check(self.screen, self.ui.toggle_button_rect, self.ui.show_slider)

            # Desenhar estatísticas (abaixo dos controles)
            stats = self.statistics[self.current_tab].get(self.current_algorithm)
            if stats:
                self.ui.draw_statistics(self.screen, stats, self.start_x + 20, 450)

            if self.is_loading:
                self.ui.draw_loading_screen()

        pygame.display.flip()

    def solve_algorithm(self, algorithm):
        # Mapeamento de algoritmos para suas funções de resolução
        algorithm_solvers = {
            Algorithm.BFS: solveBfs,
            Algorithm.ASTAR_MANHATTAN: solveAstarManhattan,
            Algorithm.BIDIRECTIONAL_SEARCH: solveBidirectionalSearch,
            Algorithm.BIDIRECTIONAL_ASTAR: solveBidirectionalAstar,
            Algorithm.GREEDY_BFS: solveGreedyBFS,
            Algorithm.DFS: solveDfs,
        }

        # Definir o algoritmo atual
        self.current_algorithm = algorithm

        # Verificar se já existe solução armazenada
        if (self.solutions.get(self.current_tab) == {} or 
            self.solutions[self.current_tab].get(self.current_algorithm) is None):
            
            # Chamar a função de resolução correspondente
            solver_function = algorithm_solvers[algorithm]
            path, visited, history, time_taken, memory_used = solver_function(self.mazes[self.current_tab])

            inserir_estatistica(self.database, self.mazes[self.current_tab], algorithm, time_taken, len(visited), len(path)-1, memory_used)
        else:
            # Recuperar solução armazenada
            path = self.solutions[self.current_tab][self.current_algorithm]
            visited = self.visited_cells[self.current_tab][self.current_algorithm]
            history = self.visited_history[self.current_tab][self.current_algorithm]
            time_taken = self.statistics[self.current_tab][self.current_algorithm]["time_taken"]
            memory_used = self.statistics[self.current_tab][self.current_algorithm]["memory_used"]

        return path, visited, history, time_taken, memory_used

    def run_all_algorithms(self):
        """Executa todos os algoritmos de resolução de labirinto."""
        for algorithm in Algorithm:
            print(f"Running {algorithm.name}...")
            path, visited, history, time_taken, memory_used = self.solve_algorithm(algorithm)
            
            self.solutions[self.current_tab][algorithm] = path
            self.visited_cells[self.current_tab][algorithm] = visited
            self.statistics[self.current_tab][algorithm] = {
                "visited_count": len(visited),
                "time_taken": time_taken,
                "path_length": (len(path) - 1),
                "memory_used": memory_used
            }
            self.visited_history[self.current_tab][algorithm] = history
            if history and self.show_visited:
                if not hasattr(self, 'sliders'):
                    self.sliders = {
                        MazeSize.SMALL: {},
                        MazeSize.MEDIUM: {},
                        MazeSize.LARGE: {}
                    }
                self.sliders[self.current_tab][algorithm] = Slider(
                    self.start_x + 25, ALTURA_TELA - 30, 400 - 40, 10, 
                    0, len(history) - 1, 0
                )
        print("All algorithms finished.")

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