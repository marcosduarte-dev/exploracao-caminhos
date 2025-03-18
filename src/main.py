import os
import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.maze_utils import generate_mazes
from ui.ui import UI

class Main:
    """
    Classe principal que gerencia o loop do jogo e a interação com o usuário.
    """

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
        self.current_tab = MazeSize.SMALL  # Tamanho inicial do labirinto
        self.current_algorithm = Algorithm.BFS  # Algoritmo inicial
        self.sprites = self._load_sprites()  # Carrega sprites das abas
        self.zoom_level = 1.0  # Nível de zoom inicial
        self.offset_x, self.offset_y = 0, 0  # Deslocamento do labirinto
        self.dragging = False  # Estado de arrasto do labirinto
        self.drag_start_x, self.drag_start_y = 0, 0  # Posição inicial do arrasto
        self.show_visited = False  # Mostrar células visitadas

        # Estado do jogo
        self.running = True

        # Gera os labirintos iniciais e estruturas relacionadas
        self.mazes, self.solutions, self.visited_cells, self.statistics = generate_mazes()

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

    def _handle_mouse_button_down(self, event):
        """
        Processa cliques do mouse.

        Args:
            event (pygame.event.Event): Evento de clique do mouse.
        """
        if event.button == 1:  # Clique esquerdo
            # Verifica se o clique foi em uma aba
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

    def _handle_mouse_motion(self, event):
        """
        Processa o movimento do mouse durante o arrasto.

        Args:
            event (pygame.event.Event): Evento de movimento do mouse.
        """
        if self.dragging:
            # Atualiza o deslocamento com base no movimento do mouse
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
            self.solutions, self.visited_cells, self.statistics
        )
        self.ui.draw_tabs(self.current_tab, self.sprites)

        pygame.display.flip()  # Atualiza a tela

    def run(self):
        """
        Executa o loop principal do jogo.
        """
        while self.running:
            self.handle_events()  # Processa eventos
            self.update()  # Atualiza a tela
            self.clock.tick(60)  # Limita a 60 FPS

        pygame.quit()  # Encerra o pygame ao sair do loop


if __name__ == "__main__":
    main = Main()
    main.run()