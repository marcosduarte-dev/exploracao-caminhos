import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.bd_utils import buscar_estatisticas, buscar_estatisticas_por_algoritmo, calcular_estatisticas_gerais, limpar_estatisticas

class ReportScreen:
    """
    Classe responsável por gerenciar a tela de relatórios com estatísticas.
    """

    def __init__(self, font_path, screen, database):
        """
        Inicializa a tela de relatórios.

        Args:
            font_path (str): Caminho para o arquivo de fonte.
            screen (pygame.Surface): Superfície onde a interface será desenhada.
            database: Conexão com o banco de dados.
        """
        self.screen = screen
        self.font = pygame.font.Font(font_path, 20)
        self.small_font = pygame.font.Font(font_path, 16)
        self.tiny_font = pygame.font.Font(font_path, 14)
        self.font_path = font_path
        self.database = database
        
        # Cores modernas
        self.primary_color = (255, 255, 255)  # Branco
        self.secondary_color = (240, 240, 240)  # Cinza muito claro
        self.accent_color = (41, 176, 233)  # Azul claro
        self.text_color = (70, 70, 70)  # Cinza escuro suave
        self.button_color = (230, 230, 230)  # Cinza claro para botões
        self.button_hover_color = (220, 220, 220)  # Cinza um pouco mais escuro para hover
        self.sidebar_color = (245, 245, 245)  # Cinza muito claro para sidebar
        self.border_color = (200, 200, 200)  # Cinza claro para bordas
        self.success_color = (60, 179, 113)  # Verde
        self.warning_color = (255, 165, 0)  # Laranja
        self.error_color = (220, 53, 69)  # Vermelho
        
        # Estado da tela
        self.filtro_tamanho = None  # None = todos, 10, 50, 100
        self.estatisticas = []
        self.estatisticas_gerais = {}
        self.estatisticas_por_algoritmo = {}
        
        # Botões
        self.filter_buttons = {}
        self.reset_button = None
        
        # Atualizar dados iniciais
        self.atualizar_dados()
        
    def atualizar_dados(self):
        """Atualiza os dados das estatísticas do banco."""
        self.estatisticas = buscar_estatisticas(self.database, self.filtro_tamanho)
        self.estatisticas_gerais = calcular_estatisticas_gerais(self.database)
        self.estatisticas_por_algoritmo = buscar_estatisticas_por_algoritmo(self.database)
        
    def handle_events(self, event):
        """
        Processa eventos da tela de relatórios.
        
        Args:
            event: Evento do pygame
            
        Returns:
            bool: True se o evento foi processado, False caso contrário
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Verificar clique nos botões de filtro
            for tamanho, button_rect in self.filter_buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    self.filtro_tamanho = tamanho
                    self.atualizar_dados()
                    return True
            
            # Verificar clique no botão reset
            if self.reset_button and self.reset_button.collidepoint(mouse_pos):
                self.limpar_estatisticas()
                return True
                
        return False
    
    def limpar_estatisticas(self):
        """Limpa todas as estatísticas do banco de dados."""
        if limpar_estatisticas(self.database):
            self.atualizar_dados()
            print("Estatísticas limpas com sucesso!")
        else:
            print("Erro ao limpar estatísticas!")
    
    def draw(self):
        """Desenha a tela de relatórios."""
        # Limpar tela
        self.screen.fill(WHITE)
        
        # Desenhar título
        self._draw_title()
        
        # Desenhar botões de filtro
        self._draw_filter_buttons()
        
        # Desenhar botão reset
        self._draw_reset_button()
        
        # Desenhar estatísticas gerais
        self._draw_general_stats()
        
        # Desenhar estatísticas por algoritmo
        self._draw_algorithm_stats()
        
        # Desenhar lista de execuções recentes
        self._draw_recent_executions()
    
    def _draw_title(self):
        """Desenha o título da tela de relatórios."""
        title = self.font.render("Relatório de Estatísticas", True, self.text_color)
        title_rect = title.get_rect(center=(LARGURA_TELA // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Subtítulo com filtro ativo
        if self.filtro_tamanho:
            subtitle = self.small_font.render(f"Filtro: Labirintos {self.filtro_tamanho}x{self.filtro_tamanho}", True, self.accent_color)
        else:
            subtitle = self.small_font.render("Mostrando todos os tamanhos", True, self.accent_color)
        
        subtitle_rect = subtitle.get_rect(center=(LARGURA_TELA // 2, 55))
        self.screen.blit(subtitle, subtitle_rect)
    
    def _draw_filter_buttons(self):
        """Desenha os botões de filtro por tamanho."""
        button_width = 120
        button_height = 35
        start_x = 50
        start_y = 80
        spacing = 20
        
        # Botão "Todos"
        todos_button = pygame.Rect(start_x, start_y, button_width, button_height)
        color = self.accent_color if self.filtro_tamanho is None else self.button_color
        pygame.draw.rect(self.screen, color, todos_button, border_radius=8)
        pygame.draw.rect(self.screen, self.border_color, todos_button, 1, border_radius=8)
        
        text_color = WHITE if self.filtro_tamanho is None else self.text_color
        todos_text = self.small_font.render("Todos", True, text_color)
        todos_text_rect = todos_text.get_rect(center=todos_button.center)
        self.screen.blit(todos_text, todos_text_rect)
        
        self.filter_buttons[None] = todos_button
        
        # Botões para cada tamanho
        tamanhos = [10, 50, 100]
        for i, tamanho in enumerate(tamanhos):
            button_x = start_x + (button_width + spacing) * (i + 1)
            button = pygame.Rect(button_x, start_y, button_width, button_height)
            
            color = self.accent_color if self.filtro_tamanho == tamanho else self.button_color
            pygame.draw.rect(self.screen, color, button, border_radius=8)
            pygame.draw.rect(self.screen, self.border_color, button, 1, border_radius=8)
            
            text_color = WHITE if self.filtro_tamanho == tamanho else self.text_color
            size_text = self.small_font.render(f"{tamanho}x{tamanho}", True, text_color)
            size_text_rect = size_text.get_rect(center=button.center)
            self.screen.blit(size_text, size_text_rect)
            
            self.filter_buttons[tamanho] = button
    
    def _draw_reset_button(self):
        """Desenha o botão de reset."""
        button_width = 100
        button_height = 35
        button_x = LARGURA_TELA - button_width - 50
        button_y = 80
        
        self.reset_button = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Verificar hover
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.reset_button.collidepoint(mouse_pos)
        
        color = self.error_color if not is_hovered else (200, 40, 50)
        pygame.draw.rect(self.screen, color, self.reset_button, border_radius=8)
        pygame.draw.rect(self.screen, self.border_color, self.reset_button, 1, border_radius=8)
        
        reset_text = self.small_font.render("Limpar Tudo", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_text_rect)
    
    def _draw_general_stats(self):
        """Desenha as estatísticas gerais."""
        # Container para estatísticas gerais
        stats_rect = pygame.Rect(50, 130, LARGURA_TELA - 100, 120)
        pygame.draw.rect(self.screen, self.sidebar_color, stats_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.border_color, stats_rect, 1, border_radius=10)
        
        # Título da seção
        title = self.font.render("Estatísticas Gerais", True, self.text_color)
        self.screen.blit(title, (70, 140))
        
        if self.estatisticas_gerais:
            # Estatísticas
            stats = self.estatisticas_gerais
            y_offset = 170
            
            # Primeira linha
            execucoes_text = self.small_font.render(f"Total de execuções: {stats['total_execucoes']}", True, self.text_color)
            tempo_text = self.small_font.render(f"Tempo médio: {stats['tempo_medio']:.2f} ms", True, self.text_color)
            
            self.screen.blit(execucoes_text, (70, y_offset))
            self.screen.blit(tempo_text, (350, y_offset))
            
            # Segunda linha
            celulas_text = self.small_font.render(f"Células visitadas (médio): {stats['celulas_visitadas_medio']:.1f}", True, self.text_color)
            caminho_text = self.small_font.render(f"Tamanho do caminho (médio): {stats['caminho_medio']:.1f}", True, self.text_color)
            
            self.screen.blit(celulas_text, (70, y_offset + 25))
            self.screen.blit(caminho_text, (350, y_offset + 25))
            
            # Terceira linha
            memoria_text = self.small_font.render(f"Memória (média): {stats['memoria_media']:.2f} MB", True, self.text_color)
            self.screen.blit(memoria_text, (70, y_offset + 50))
        else:
            no_data_text = self.small_font.render("Nenhuma estatística disponível", True, self.warning_color)
            self.screen.blit(no_data_text, (70, 170))
    
    def _draw_algorithm_stats(self):
        """Desenha as estatísticas por algoritmo."""
        # Container para estatísticas por algoritmo
        stats_rect = pygame.Rect(50, 270, LARGURA_TELA - 100, 200)
        pygame.draw.rect(self.screen, self.sidebar_color, stats_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.border_color, stats_rect, 1, border_radius=10)
        
        # Título da seção
        title = self.font.render("Estatísticas por Algoritmo", True, self.text_color)
        self.screen.blit(title, (70, 280))
        
        if self.estatisticas_por_algoritmo:
            # Cabeçalho da tabela
            header_y = 310
            headers = ["Algoritmo", "Execuções", "Tempo Médio", "Células (médio)", "Caminho (médio)", "Memória (média)"]
            column_widths = [150, 80, 120, 120, 120, 120]
            
            for i, header in enumerate(headers):
                header_text = self.tiny_font.render(header, True, self.text_color)
                x = 70 + sum(column_widths[:i])
                self.screen.blit(header_text, (x, header_y))
            
            # Linha separadora
            pygame.draw.line(self.screen, self.border_color, (70, header_y + 20), (LARGURA_TELA - 70, header_y + 20), 1)
            
            # Dados dos algoritmos
            row_y = header_y + 30
            for algo_id, stats_list in self.estatisticas_por_algoritmo.items():
                if row_y > 450:  # Limitar altura
                    break
                    
                # Calcular médias para este algoritmo
                if stats_list:
                    tempo_medio = sum(s['tempo_execucao'] for s in stats_list) / len(stats_list)
                    celulas_medio = sum(s['celulas_visitadas'] for s in stats_list) / len(stats_list)
                    caminho_medio = sum(s['tamanho_caminho'] for s in stats_list) / len(stats_list)
                    memoria_media = sum(s['memoria'] for s in stats_list) / len(stats_list)
                    
                    # Nome do algoritmo
                    try:
                        algo_name = Algorithm(algo_id).display_name
                    except:
                        algo_name = f"Algoritmo {algo_id}"
                    
                    # Dados da linha
                    data = [
                        algo_name,
                        str(len(stats_list)),
                        f"{tempo_medio:.2f} ms",
                        f"{celulas_medio:.1f}",
                        f"{caminho_medio:.1f}",
                        f"{memoria_media:.2f} MB"
                    ]
                    
                    for i, value in enumerate(data):
                        value_text = self.tiny_font.render(value, True, self.text_color)
                        x = 70 + sum(column_widths[:i])
                        self.screen.blit(value_text, (x, row_y))
                    
                    row_y += 20
        else:
            no_data_text = self.small_font.render("Nenhuma estatística por algoritmo disponível", True, self.warning_color)
            self.screen.blit(no_data_text, (70, 310))
    
    def _draw_recent_executions(self):
        """Desenha a lista de execuções recentes."""
        # Container para execuções recentes
        stats_rect = pygame.Rect(50, 490, LARGURA_TELA - 100, 180)
        pygame.draw.rect(self.screen, self.sidebar_color, stats_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.border_color, stats_rect, 1, border_radius=10)
        
        # Título da seção
        title = self.font.render("Execuções Recentes", True, self.text_color)
        self.screen.blit(title, (70, 500))
        
        if self.estatisticas:
            # Cabeçalho da tabela
            header_y = 530
            headers = ["Tamanho", "Algoritmo", "Tempo", "Células", "Caminho", "Memória"]
            column_widths = [80, 150, 100, 80, 80, 100]
            
            for i, header in enumerate(headers):
                header_text = self.tiny_font.render(header, True, self.text_color)
                x = 70 + sum(column_widths[:i])
                self.screen.blit(header_text, (x, header_y))
            
            # Linha separadora
            pygame.draw.line(self.screen, self.border_color, (70, header_y + 20), (LARGURA_TELA - 70, header_y + 20), 1)
            
            # Dados das execuções (mostrar apenas as 5 mais recentes)
            recent_stats = self.estatisticas[-5:] if len(self.estatisticas) > 5 else self.estatisticas
            row_y = header_y + 30
            
            for stat in reversed(recent_stats):  # Mais recentes primeiro
                if row_y > 650:  # Limitar altura
                    break
                    
                # Nome do algoritmo
                try:
                    algo_name = Algorithm(stat['algoritmo']).display_name
                except:
                    algo_name = f"Algoritmo {stat['algoritmo']}"
                
                # Dados da linha
                data = [
                    f"{stat['tamanho_labirinto']}x{stat['tamanho_labirinto']}",
                    algo_name,
                    f"{stat['tempo_execucao']:.2f} ms",
                    str(stat['celulas_visitadas']),
                    str(stat['tamanho_caminho']),
                    f"{stat['memoria']:.2f} MB"
                ]
                
                for i, value in enumerate(data):
                    value_text = self.tiny_font.render(value, True, self.text_color)
                    x = 70 + sum(column_widths[:i])
                    self.screen.blit(value_text, (x, row_y))
                
                row_y += 20
        else:
            no_data_text = self.small_font.render("Nenhuma execução recente disponível", True, self.warning_color)
            self.screen.blit(no_data_text, (70, 530)) 