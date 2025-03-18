import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize

class UI:
    def __init__(self, font_path, screen):
        self.screen = screen
        self.font = pygame.font.Font(font_path, 20)
        self.small_font = pygame.font.Font(font_path, 16)
        self.tabs = {}

    def draw_maze(self, maze, current_tab, current_algorithm, zoom_level, offset_x, offset_y, show_visited, solutions, visited_cells, statistics):
        if current_tab == MazeSize.REPORT:
            # Limpa a tela
            self.screen.fill(WHITE)
            #TODO TELA REPORT
            print("DEVE DESENHAR REPORT")
            #self.draw_report(statistics)
            return
        
        if maze is None:
            return
        
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

        # Desenha um fundo para a área do labirinto
        pygame.draw.rect(self.screen, GRAY, (0, 45, maze_area_width, maze_area_height - 1))

        dash_length = 10  # Comprimento de cada traço
        gap_length = 5    # Espaço entre os traços

        # Borda superior
        for x in range(0, maze_area_width, dash_length + gap_length):
            pygame.draw.line(self.screen, BLACK, (x, 45), (x + dash_length, 45), 2)

        # Borda inferior
        for x in range(0, maze_area_width, dash_length + gap_length):
            pygame.draw.line(self.screen, BLACK, (x, 45 + maze_area_height - 1), (x + dash_length, 45 + maze_area_height - 1), 2)

        # Borda esquerda
        for y in range(45, 45 + maze_area_height - 1, dash_length + gap_length):
            pygame.draw.line(self.screen, BLACK, (0, y), (0, y + dash_length), 2)

        # Borda direita
        for y in range(45, 45 + maze_area_height - 1, dash_length + gap_length):
            pygame.draw.line(self.screen, BLACK, (maze_area_width, y), (maze_area_width, y + dash_length), 2)

        # Desenha as células do labirinto
        for y in range(maze.height):
            for x in range(maze.width):
                rect_x = start_x + x * cell_size
                rect_y = start_y + y * cell_size
                
                # Verifica se a célula está visível na tela
                if (rect_x + cell_size < 0 or rect_x > maze_area_width or
                    rect_y + cell_size < 45 or rect_y > maze_area_height + 45):
                    continue
                
                if maze.grid[y][x] == 1:  # Parede
                    pygame.draw.rect(self.screen, BLACK, (rect_x, rect_y, cell_size, cell_size))
                elif maze.grid[y][x] == 0:  # Caminho
                    pygame.draw.rect(self.screen, WHITE, (rect_x, rect_y, cell_size, cell_size))
                elif maze.grid[y][x] == 2: # Ponto inicial
                    pygame.draw.rect(self.screen, GREEN, (rect_x, rect_y, cell_size, cell_size))
                elif maze.grid[y][x] == 3: # Ponto final
                    pygame.draw.rect(self.screen, RED, (rect_x, rect_y, cell_size, cell_size))

        # Desenha uma grade se o zoom for suficiente
        if cell_size >= 5:
            for y in range(maze.height + 1):
                pygame.draw.line(self.screen, GRAY, 
                                (start_x, start_y + y * cell_size),
                                (start_x + maze.width * cell_size, start_y + y * cell_size), 1)
            for x in range(maze.width + 1):
                pygame.draw.line(self.screen, GRAY,
                                (start_x + x * cell_size, start_y),
                                (start_x + x * cell_size, start_y + maze.height * cell_size), 1)

         # Desenha células visitadas se a opção estiver ativada
        if show_visited and current_algorithm in visited_cells[current_tab]:
            visited = visited_cells[current_tab][current_algorithm]
            for pos in visited:
                if pos != maze.start and pos != maze.end:  # Não sobrescreve início e fim
                    rect_x = start_x + pos[0] * cell_size
                    rect_y = start_y + pos[1] * cell_size
                    pygame.draw.rect(self.screen, LIGHT_CYAN, (rect_x, rect_y, cell_size, cell_size))
        
        # Desenha a solução se disponível
        if current_algorithm in solutions[current_tab]:
            path = solutions[current_tab][current_algorithm]
            for pos in path:
                if pos != maze.start and pos != maze.end:  # Não sobrescreve início e fim
                    rect_x = start_x + pos[0] * cell_size
                    rect_y = start_y + pos[1] * cell_size
                    pygame.draw.rect(self.screen, YELLOW, (rect_x, rect_y, cell_size, cell_size))

        # TODO - CRIAR O PAINEL LATERAL
        self.draw_sidebar(maze_area_width, current_algorithm, current_tab, statistics, show_visited, zoom_level)

    def draw_sidebar(self, start_x, current_algorithm, current_tab, statistics, show_visited, zoom_level):
        # Área do painel lateral
        sidebar_rect = pygame.Rect(start_x, 45, LARGURA_TELA - start_x, ALTURA_TELA)
        pygame.draw.rect(self.screen, GRAY, sidebar_rect)
        pygame.draw.line(self.screen, BLACK, (start_x, 45), (start_x, ALTURA_TELA), 2)
        
        # Título
        title = self.font.render("Controles", True, BLACK)
        self.screen.blit(title, (start_x + 20, 65))

    def draw_tabs(self, current_tab, sprites):
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