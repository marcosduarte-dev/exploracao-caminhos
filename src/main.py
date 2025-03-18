import os
import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.maze_utils import generate_mazes
from ui.ui import UI

class Main:
    def __init__(self):
        pygame.init()
        
        # Configuração de janela
        pygame.display.set_caption(TITULO_PROJETO)
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.clock = pygame.time.Clock()
        
        # Caminhos
        self.current_path = os.path.dirname(__file__)
        self.sprites_path = {
            'current_tab': os.path.join(self.current_path, 'ui/sprites', 'tab_selecionado.png'),
            'normal_tab': os.path.join(self.current_path, 'ui/sprites', 'tab.png')
        }
        self.font_path = os.path.join(self.current_path, 'ui', 'font', 'Inter.ttf')
        
        # Inicialização de componentes
        self.ui = UI(self.font_path, self.screen)
        self.current_tab = MazeSize.SMALL
        self.current_algorithm = Algorithm.BFS
        self.sprites = self.load_sprites()
        self.zoom_level = 1.0
        self.offset_x, self.offset_y = 0, 0
        self.dragging = False
        self.drag_start_x, self.drag_start_y = 0, 0
        self.show_visited = False 
        
        # Estado do jogo
        self.running = True

        # Gera os labirintos iniciais
        self.mazes, self.solutions, self.visited_cells, self.statistics = generate_mazes()

    def load_sprites(self):
        return {
            'sprite_current_tab': pygame.image.load(self.sprites_path['current_tab']).convert_alpha(),
            'sprite_normal_tab': pygame.image.load(self.sprites_path['normal_tab']).convert_alpha()
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_events(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Soltar o botão esquerdo
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    # Atualiza o deslocamento com base no movimento do mouse
                    self.offset_x += event.pos[0] - self.drag_start_x
                    self.offset_y += event.pos[1] - self.drag_start_y
                    self.drag_start_x, self.drag_start_y = event.pos

    def handle_mouse_events(self, event):
        if event.button == 1:  # Clique esquerdo
            for size, rect in self.ui.tabs.items():
                if rect.collidepoint(event.pos):
                    self.current_tab = size
                    break
            # Inicia o arrasto do labirinto
            if event.pos[0] < 800:  # Dentro da área do labirinto
                self.dragging = True
                self.drag_start_x, self.drag_start_y = event.pos

        elif event.button == 4:  # Roda do mouse para cima (zoom in)
                self.zoom_level = min(5.0, self.zoom_level + 0.1)
        elif event.button == 5:  # Roda do mouse para baixo (zoom out)
                self.zoom_level = max(0.1, self.zoom_level - 0.1)

    def update(self):
        self.screen.fill(WHITE)
        self.ui.draw_tabs(self.current_tab, self.sprites)
        self.ui.draw_maze(self.mazes[self.current_tab], self.current_tab, self.current_algorithm, self.zoom_level, self.offset_x, self.offset_y, self.show_visited, self.solutions, self.visited_cells, self.statistics)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.run()