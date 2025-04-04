import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm

class UI:
    """
    Classe responsável por gerenciar a interface gráfica do labirinto.

    Atributos:
        screen (pygame.Surface): Superfície onde a interface será desenhada.
        font (pygame.font.Font): Fonte usada para textos principais.
        small_font (pygame.font.Font): Fonte usada para textos secundários.
        tabs (dict): Dicionário que armazena os retângulos das abas para detecção de clique.
    """

    def __init__(self, font_path, screen):
        """
        Inicializa a interface gráfica.

        Args:
            font_path (str): Caminho para o arquivo de fonte.
            screen (pygame.Surface): Superfície onde a interface será desenhada.
        """
        self.screen = screen
        self.font = pygame.font.Font(font_path, 20)  # Fonte principal
        self.small_font = pygame.font.Font(font_path, 16)  # Fonte secundária
        self.tabs = {}  # Armazena os retângulos das abas
        self.algorithm_buttons = {} # Armazena os restângulos dos algoritmos

    def draw_maze(self, maze, current_tab, current_algorithm, zoom_level, offset_x, offset_y, show_visited, show_solution,
        solutions, visited_cells, statistics, visited_history, sliders):
        """
        Desenha o labirinto na tela.

        Args:
            maze (Maze): Objeto do labirinto a ser desenhado.
            current_tab (MazeSize): Tamanho do labirinto atual (aba selecionada).
            current_algorithm (str): Algoritmo atual selecionado.
            zoom_level (float): Nível de zoom aplicado ao labirinto.
            offset_x (int): Deslocamento horizontal do labirinto.
            offset_y (int): Deslocamento vertical do labirinto.
            show_visited (bool): Se True, mostra as células visitadas.
            solutions (dict): Dicionário com as soluções para cada algoritmo.
            visited_cells (dict): Dicionário com as células visitadas para cada algoritmo.
            statistics (dict): Dicionário com estatísticas de execução dos algoritmos.
            visited_history (dict): Dicionário com todas as etapas executada pelo algoritmo.
            sliders (dict): Dicionário com os steppers gerados para cada algoritmo.
        """
        if current_tab == MazeSize.REPORT:
            # Modo de relatório: limpa a tela e exibe o relatório
            self.screen.fill(WHITE)
            print("DEVE DESENHAR REPORT")  # TODO: Implementar tela de relatório
            return

        if maze is None:
            return  # Se não houver labirinto, não desenha nada

        # Calcula o tamanho da célula com base no zoom
        base_cell_size = min(600 // maze.width, 600 // maze.height)
        cell_size = max(1, int(base_cell_size * zoom_level))

        # Calcula as dimensões totais do labirinto
        total_width = maze.width * cell_size
        total_height = maze.height * cell_size

        # Centraliza o labirinto na área de visualização
        maze_area_width = min(800, LARGURA_TELA - 400)  # Espaço para os controles à direita
        maze_area_height = ALTURA_TELA - 45

        center_x = maze_area_width // 2
        center_y = maze_area_height // 2

        start_x = center_x - total_width // 2 + offset_x
        start_y = center_y - total_height // 2 + offset_y

        # Desenha o fundo da área do labirinto
        self._draw_maze_background(maze_area_width, maze_area_height)

        # Desenha as bordas tracejadas ao redor do labirinto
        self._draw_dashed_borders(maze_area_width, maze_area_height)

        # Desenha as células do labirinto
        self._draw_maze_cells(maze, cell_size, start_x, start_y, maze_area_width, maze_area_height)

        # Desenha células visitadas, se a opção estiver ativada
        if show_visited and current_algorithm in visited_cells[current_tab]:
            # Verifica se temos histórico e slider para esse algoritmo e aba
            if (current_algorithm in visited_history[current_tab] and 
                current_algorithm in sliders[current_tab]):
                
                history = visited_history[current_tab][current_algorithm]
                step = sliders[current_tab][current_algorithm].value
                self._draw_visited_cells(history, maze, cell_size, start_x, start_y, step)
            else:
                self._draw_visited_cells(
                    visited_cells[current_tab][current_algorithm], 
                    maze, cell_size, start_x, start_y
                )

        # Desenha a solução, se disponível
        if ((current_algorithm in solutions[current_tab] and 
        (not show_visited or sliders[current_tab][current_algorithm].value == len(history) - 1))
            or show_solution):
            if(current_algorithm != None):
                self._draw_solution(solutions[current_tab][current_algorithm], maze, cell_size, start_x, start_y)

        # Desenha a grade se o zoom for suficiente
        if cell_size >= 5:
            self._draw_grid(maze, cell_size, start_x, start_y)

        # Desenha o painel lateral
        self.draw_sidebar(maze_area_width, current_algorithm, current_tab, statistics, show_visited, zoom_level, visited_history, sliders)

    def _draw_maze_background(self, maze_area_width, maze_area_height):
        """
        Desenha o fundo da área do labirinto.

        Args:
            maze_area_width (int): Largura da área do labirinto.
            maze_area_height (int): Altura da área do labirinto.
        """
        pygame.draw.rect(self.screen, GRAY, (0, 45, maze_area_width, maze_area_height - 1))

    def _draw_dashed_borders(self, maze_area_width, maze_area_height):
        """
        Desenha bordas tracejadas ao redor da área do labirinto.

        Args:
            maze_area_width (int): Largura da área do labirinto.
            maze_area_height (int): Altura da área do labirinto.
        """
        dash_length = 10  # Comprimento de cada traço
        gap_length = 5    # Espaço entre os traços

        # Bordas superior, inferior, esquerda e direita
        for x in range(0, maze_area_width, dash_length + gap_length):
            pygame.draw.line(self.screen, BLACK, (x, 45), (x + dash_length, 45), 2)  # Superior
            pygame.draw.line(self.screen, BLACK, (x, 45 + maze_area_height - 1), (x + dash_length, 45 + maze_area_height - 1), 2)  # Inferior

        for y in range(45, 45 + maze_area_height - 1, dash_length + gap_length):
            pygame.draw.line(self.screen, BLACK, (0, y), (0, y + dash_length), 2)  # Esquerda
            pygame.draw.line(self.screen, BLACK, (maze_area_width, y), (maze_area_width, y + dash_length), 2)  # Direita

    def _draw_maze_cells(self, maze, cell_size, start_x, start_y, maze_area_width, maze_area_height):
        """
        Desenha as células do labirinto.

        Args:
            maze (Maze): Objeto do labirinto.
            cell_size (int): Tamanho de cada célula.
            start_x (int): Posição inicial X do labirinto.
            start_y (int): Posição inicial Y do labirinto.
            maze_area_width (int): Largura da área do labirinto.
            maze_area_height (int): Altura da área do labirinto.
        """
        for y in range(maze.height):
            for x in range(maze.width):
                rect_x = start_x + x * cell_size
                rect_y = start_y + y * cell_size

                # Verifica se a célula está visível na tela
                if (rect_x + cell_size < 0 or rect_x > maze_area_width or
                    rect_y + cell_size < 45 or rect_y > maze_area_height + 45):
                    continue

                # Desenha a célula com base no valor
                if maze.grid[y][x] == 1:  # Parede
                    pygame.draw.rect(self.screen, BLACK, (rect_x, rect_y, cell_size, cell_size))
                elif maze.grid[y][x] == 0:  # Caminho
                    pygame.draw.rect(self.screen, WHITE, (rect_x, rect_y, cell_size, cell_size))
                elif maze.grid[y][x] == 2:  # Ponto inicial
                    pygame.draw.rect(self.screen, GREEN, (rect_x, rect_y, cell_size, cell_size))
                elif maze.grid[y][x] == 3:  # Ponto final
                    pygame.draw.rect(self.screen, RED, (rect_x, rect_y, cell_size, cell_size))

    def _draw_grid(self, maze, cell_size, start_x, start_y):
        """
        Desenha a grade do labirinto.

        Args:
            maze (Maze): Objeto do labirinto.
            cell_size (int): Tamanho de cada célula.
            start_x (int): Posição inicial X do labirinto.
            start_y (int): Posição inicial Y do labirinto.
        """
        for y in range(maze.height + 1):
            pygame.draw.line(self.screen, GRAY, 
                            (start_x, start_y + y * cell_size),
                            (start_x + maze.width * cell_size, start_y + y * cell_size), 1)
        for x in range(maze.width + 1):
            pygame.draw.line(self.screen, GRAY,
                            (start_x + x * cell_size, start_y),
                            (start_x + x * cell_size, start_y + maze.height * cell_size), 1)

    def _draw_visited_cells(self, visited, maze, cell_size, start_x, start_y, step=None):
        """
        Desenha as células visitadas, opcionalmente limitando ao passo especificado pelo slider.

        Args:
            visited (list ou list[set]): Lista de células visitadas ou histórico de visitas.
            maze (Maze): Objeto do labirinto.
            cell_size (int): Tamanho de cada célula.
            start_x (int): Posição inicial X do labirinto.
            start_y (int): Posição inicial Y do labirinto.
            step (int, opcional): Passo específico a ser mostrado, para uso com o slider.
        """
        # Determina quais células desenhar com base no passo do slider
        cells_to_draw = visited
        if isinstance(visited, list) and step is not None and step < len(visited):
            cells_to_draw = visited[step]
        
        for pos in cells_to_draw:
            if pos != maze.start and pos != maze.end:  # Não sobrescreve início e fim
                rect_x = start_x + pos[0] * cell_size
                rect_y = start_y + pos[1] * cell_size
                pygame.draw.rect(self.screen, LIGHT_CYAN, (rect_x, rect_y, cell_size, cell_size))

    def _draw_solution(self, path, maze, cell_size, start_x, start_y):
        """
        Desenha a solução do labirinto.

        Args:
            path (list): Lista de células que compõem a solução.
            maze (Maze): Objeto do labirinto.
            cell_size (int): Tamanho de cada célula.
            start_x (int): Posição inicial X do labirinto.
            start_y (int): Posição inicial Y do labirinto.
        """
        for pos in path:
            if pos != maze.start and pos != maze.end:  # Não sobrescreve início e fim
                rect_x = start_x + pos[0] * cell_size
                rect_y = start_y + pos[1] * cell_size
                pygame.draw.rect(self.screen, YELLOW, (rect_x, rect_y, cell_size, cell_size))

    def draw_sidebar(self, start_x, current_algorithm, current_tab, statistics, show_visited, zoom_level, visited_history, sliders, step_slider=None, step_count=0):
        """
        Desenha o painel lateral com controles e informações.

        Args:
            start_x (int): Posição X inicial do painel.
            current_algorithm (str): Algoritmo atual selecionado.
            current_tab (MazeSize): Tamanho do labirinto atual (aba selecionada).
            statistics (dict): Dicionário com estatísticas de execução dos algoritmos.
            show_visited (bool): Se True, mostra as células visitadas.
            zoom_level (float): Nível de zoom aplicado ao labirinto.
        """
        # Área do painel lateral
        sidebar_width = LARGURA_TELA - start_x;
        sidebar_rect = pygame.Rect(start_x, 45,sidebar_width, ALTURA_TELA)
        pygame.draw.rect(self.screen, GRAY, sidebar_rect)
        pygame.draw.line(self.screen, BLACK, (start_x, 45), (start_x, ALTURA_TELA), 2)

        # Título
        title = self.font.render("Controles", True, BLACK)
        self.screen.blit(title, (start_x + 20, 65))

        if (current_tab in sliders and 
            current_algorithm in sliders[current_tab]):

            slider = sliders[current_tab][current_algorithm]
            history = visited_history[current_tab][current_algorithm]
            
            # Renderiza texto do passo atual
            steps_text = self.font.render(f"Passo: {slider.value + 1}/{slider.max_val + 1}", True, BLACK)
            self.screen.blit(steps_text, (start_x + 20, ALTURA_TELA - 68)) # ALTURA, SE SOBREESCREVER
            
            # Desenha o slider
            slider.draw(self.screen)
            
            # Adiciona botões de navegação para passos (opcional)
            '''prev_rect = pygame.Rect(start_x + 20, 250, 30, 30)
            next_rect = pygame.Rect(start_x + sidebar_width - 50, 250, 30, 30)
            
            pygame.draw.rect(self.screen, (200, 200, 200), prev_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), next_rect)
            
            prev_text = self.font.render("<", True, BLACK)
            next_text = self.font.render(">", True, BLACK)
            
            self.screen.blit(prev_text, (prev_rect.centerx - 5, prev_rect.centery - 8))
            self.screen.blit(next_text, (next_rect.centerx - 5, next_rect.centery - 8))'''

    def draw_tabs(self, current_tab, sprites):
        """
        Desenha as abas de seleção de tamanho do labirinto.

        Args:
            current_tab (MazeSize): Tamanho do labirinto atual (aba selecionada).
            sprites (dict): Dicionário com sprites das abas.
        """
        tab_width = LARGURA_TELA // MazeSize.size()
        tab_height = 40

        tab_rect = pygame.Rect(0, 0, LARGURA_TELA, 45)
        pygame.draw.rect(self.screen, WHITE, tab_rect)

        for i, size in enumerate(MazeSize):
            # Posição e dimensões da aba
            tab_btn = pygame.Rect(i * tab_width, 0, tab_width - 10, tab_height)

            # Sprite da aba
            if size == current_tab:
                sprite = sprites['sprite_current_tab']
            else:
                sprite = sprites['sprite_normal_tab']

            scaled_sprite = pygame.transform.scale(sprite, (tab_btn.width, tab_btn.height))
            self.screen.blit(scaled_sprite, tab_btn)

            # Texto da aba
            text = self.font.render(f"{size.name}", True, BLACK)
            text_rect = text.get_rect(center=(tab_btn.centerx, tab_btn.centery))
            self.screen.blit(text, text_rect)

            # Armazena o retângulo para detecção de clique
            self.tabs[size] = tab_btn

    def draw_algorithm_buttons(self, current_algorithm, sprites):
        """
        Desenha os botões de seleção de algoritmo.

        Args:
            current_algorithm (Algorithm): Algoritmo atual (botão selecionado).
            sprites (dict): Dicionário com sprites dos botões.
        """
        button_width = 250
        button_height = 40
        button_x = LARGURA_TELA - 380  # Posição X à esquerda da tela

        for i, algorithm in enumerate(Algorithm):
            # Posição e dimensões do botão
            button = pygame.Rect(button_x, (i * button_height) + 100, button_width, button_height - 10)

            # Sprite do botão
            if algorithm == current_algorithm:
                sprite = sprites['sprite_current_tab']
            else:
                sprite = sprites['sprite_normal_tab']

            scaled_sprite = pygame.transform.scale(sprite, (button.width, button.height))
            self.screen.blit(scaled_sprite, button)

            # Texto do botão
            text = self.small_font.render(f"{algorithm.display_name}", True, BLACK)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            self.screen.blit(text, text_rect)

            # Armazena o retângulo para detecção de clique
            self.algorithm_buttons[algorithm] = button

        return self.algorithm_buttons