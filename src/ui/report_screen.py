import pygame
from utils.config import *
from enums.colour import *
from enums.maze_size import MazeSize
from enums.algorithms import Algorithm
from utils.bd_utils import buscar_estatisticas, buscar_estatisticas_por_algoritmo, calcular_estatisticas_gerais, limpar_estatisticas

class ScrollableTable:
    """Classe para gerenciar tabelas com scroll."""
    
    def __init__(self, x, y, width, height, row_height=20, max_visible_rows=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.row_height = row_height
        self.scroll_y = 0
        self.max_visible_rows = max_visible_rows or (height // row_height)
        self.total_rows = 0
        self.is_scrollable = False
        # Estado do scrollbar
        self._scrollbar_width = 8
        self._thumb_rect = None
        self._dragging = False
        self._drag_offset = 0
        
    def update_scroll(self, total_rows):
        """Atualiza o scroll baseado no número total de linhas."""
        self.total_rows = total_rows
        self.is_scrollable = total_rows > self.max_visible_rows
        if self.scroll_y > max(0, total_rows - self.max_visible_rows):
            self.scroll_y = max(0, total_rows - self.max_visible_rows)
    
    def _is_mouse_over_area(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)
    
    def _compute_thumb(self):
        """Calcula o retângulo do thumb do scrollbar e o retorna."""
        if not self.is_scrollable or self.total_rows == 0:
            self._thumb_rect = None
            return None
        track_x = self.x + self.width - self._scrollbar_width - 2
        visible_ratio = self.max_visible_rows / float(self.total_rows)
        thumb_h = max(20, int(visible_ratio * self.height))
        max_scroll = max(1, self.total_rows - self.max_visible_rows)
        track_h = self.height - thumb_h
        # Posição do thumb proporcional ao scroll
        thumb_y = int(self.y + (self.scroll_y / max_scroll) * track_h) if track_h > 0 else self.y
        self._thumb_rect = pygame.Rect(track_x, thumb_y, self._scrollbar_width, thumb_h)
        return self._thumb_rect
    
    def handle_scroll_event(self, event):
        """Processa eventos de scroll (roda do mouse, botoes 4/5 e arraste do thumb)."""
        if not self.is_scrollable:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        over_area = self._is_mouse_over_area(mouse_pos)
        thumb = self._compute_thumb()
        
        # Arraste do thumb
        if event.type == pygame.MOUSEBUTTONDOWN and getattr(event, 'button', 0) == 1:
            if thumb and thumb.collidepoint(mouse_pos):
                self._dragging = True
                self._drag_offset = mouse_pos[1] - thumb.y
                return True
            # Clique na trilha para pular uma página
            if over_area and thumb and mouse_pos[0] >= thumb.x:
                if mouse_pos[1] < thumb.y:
                    self.scroll_y = max(0, self.scroll_y - self.max_visible_rows)
                elif mouse_pos[1] > thumb.bottom:
                    self.scroll_y = min(max(0, self.total_rows - self.max_visible_rows), self.scroll_y + self.max_visible_rows)
                return True
        
        if event.type == pygame.MOUSEBUTTONUP and getattr(event, 'button', 0) == 1:
            if self._dragging:
                self._dragging = False
                return True
        
        if event.type == pygame.MOUSEMOTION and self._dragging:
            # Converter posição do mouse para scroll_y
            thumb = self._compute_thumb()
            if thumb:
                track_top = self.y
                track_h = self.height - thumb.height
                new_thumb_top = max(track_top, min(mouse_pos[1] - self._drag_offset, track_top + track_h))
                # Proporção ao longo da trilha
                ratio = 0.0 if track_h == 0 else (new_thumb_top - track_top) / float(track_h)
                max_scroll = max(0, self.total_rows - self.max_visible_rows)
                self.scroll_y = int(round(ratio * max_scroll))
                return True
        
        # Scroll por roda do mouse somente se cursor estiver sobre a área
        if over_area:
            dy = 0
            if event.type == pygame.MOUSEWHEEL:
                dy = event.y
            elif event.type == pygame.MOUSEBUTTONDOWN and getattr(event, 'button', 0) in (4, 5):
                dy = 1 if event.button == 4 else -1
            if dy != 0:
                max_scroll = max(0, self.total_rows - self.max_visible_rows)
                self.scroll_y = max(0, min(self.scroll_y - dy, max_scroll))
                return True
        
        return False
    
    def get_visible_range(self):
        """Retorna o range de linhas visíveis."""
        start_row = self.scroll_y
        end_row = min(start_row + self.max_visible_rows, self.total_rows)
        return start_row, end_row
    
    def draw_scrollbar(self, screen, color=(200, 200, 200)):
        """Desenha a barra de scroll."""
        if not self.is_scrollable:
            return
        
        thumb = self._compute_thumb()
        if not thumb:
            return
        # Desenhar trilha levemente visível
        track_x = self.x + self.width - self._scrollbar_width - 2
        pygame.draw.rect(screen, (230,230,230), (track_x, self.y, self._scrollbar_width, self.height), border_radius=4)
        # Desenhar o thumb
        pygame.draw.rect(screen, color, thumb, border_radius=4)

class ReportScreen:
    """
    Classe responsável por gerenciar a tela de relatórios com estatísticas.
    """

    def __init__(self, font_path, screen, database, local_statistics=None):
        """
        Inicializa a tela de relatórios.

        Args:
            font_path (str): Caminho para o arquivo de fonte.
            screen (pygame.Surface): Superfície onde a interface será desenhada.
            database: Conexão com o banco de dados.
            local_statistics (dict, opcional): Estatísticas locais da memória.
        """
        self.screen = screen
        self.font = pygame.font.Font(font_path, 20)
        self.small_font = pygame.font.Font(font_path, 16)
        self.tiny_font = pygame.font.Font(font_path, 14)
        self.font_path = font_path
        self.database = database
        self.local_statistics = local_statistics
        
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
        
        # Tabelas com scroll
        self.algorithm_table = ScrollableTable(70, 330, LARGURA_TELA - 140, 140, 20, 6)
        self.executions_table = ScrollableTable(70, 550, LARGURA_TELA - 140, 120, 20, 5)
        
        # Atualizar dados iniciais
        self.atualizar_dados()
        
    def atualizar_dados(self):
        """Atualiza os dados das estatísticas do banco ou da memória local."""
        if self.database:
            # Usar banco de dados se disponível
            self.estatisticas = buscar_estatisticas(self.database, self.filtro_tamanho)
            self.estatisticas_gerais = calcular_estatisticas_gerais(self.database)
            self.estatisticas_por_algoritmo = buscar_estatisticas_por_algoritmo(self.database)
        else:
            # Usar dados locais se banco não disponível
            self.estatisticas = self._converter_estatisticas_locais()
            self.estatisticas_gerais = self._calcular_estatisticas_gerais_locais()
            self.estatisticas_por_algoritmo = self._agrupar_estatisticas_por_algoritmo()
        
        # Atualizar scroll das tabelas
        self.algorithm_table.update_scroll(len(self.estatisticas_por_algoritmo))
        self.executions_table.update_scroll(len(self.estatisticas))
        
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
        
        # Processar eventos de scroll das tabelas
        if self.algorithm_table.handle_scroll_event(event):
            return True
        if self.executions_table.handle_scroll_event(event):
            return True
                
        return False
    
    def limpar_estatisticas(self):
        """Limpa todas as estatísticas do banco de dados ou da memória local."""
        if self.database:
            if limpar_estatisticas(self.database):
                self.atualizar_dados()
                print("Estatísticas limpas com sucesso!")
            else:
                print("Erro ao limpar estatísticas!")
        else:
            # Limpar dados locais
            if self.local_statistics:
                for tab in self.local_statistics:
                    self.local_statistics[tab].clear()
                self.atualizar_dados()
                print("Estatísticas locais limpas com sucesso!")
    
    def _converter_estatisticas_locais(self):
        """Converte estatísticas locais para o formato esperado pela tela."""
        if not self.local_statistics:
            return []
        
        estatisticas_convertidas = []
        
        for tab, algorithms in self.local_statistics.items():
            if tab == MazeSize.REPORT:
                continue
                
            # Obter dimensões do labirinto baseado na aba
            tamanho_labirinto = None
            if tab == MazeSize.SMALL:
                tamanho_labirinto = 10
            elif tab == MazeSize.MEDIUM:
                tamanho_labirinto = 50
            elif tab == MazeSize.LARGE:
                tamanho_labirinto = 100
            
            # Aplicar filtro se necessário
            if self.filtro_tamanho and tamanho_labirinto != self.filtro_tamanho:
                continue
            
            for algorithm, stats in algorithms.items():
                if stats:  # Se há estatísticas para este algoritmo
                    estatistica_convertida = {
                        'algoritmo': algorithm.value,
                        'tamanho_labirinto': tamanho_labirinto,
                        'tempo_execucao': stats.get('time_taken', 0),
                        'celulas_visitadas': stats.get('visited_count', 0),
                        'tamanho_caminho': stats.get('path_length', 0),
                        'memoria': stats.get('memory_used', 0)
                    }
                    estatisticas_convertidas.append(estatistica_convertida)
        
        return estatisticas_convertidas
    
    def _calcular_estatisticas_gerais_locais(self):
        """Calcula estatísticas gerais a partir dos dados locais."""
        estatisticas = self._converter_estatisticas_locais()
        
        if not estatisticas:
            return {}
        
        total_execucoes = len(estatisticas)
        tempo_medio = sum(stat['tempo_execucao'] for stat in estatisticas) / total_execucoes
        celulas_visitadas_medio = sum(stat['celulas_visitadas'] for stat in estatisticas) / total_execucoes
        caminho_medio = sum(stat['tamanho_caminho'] for stat in estatisticas) / total_execucoes
        memoria_media = sum(stat['memoria'] for stat in estatisticas) / total_execucoes
        
        return {
            'total_execucoes': total_execucoes,
            'tempo_medio': tempo_medio,
            'celulas_visitadas_medio': celulas_visitadas_medio,
            'caminho_medio': caminho_medio,
            'memoria_media': memoria_media
        }
    
    def _agrupar_estatisticas_por_algoritmo(self):
        """Agrupa estatísticas locais por algoritmo."""
        estatisticas = self._converter_estatisticas_locais()
        
        if not estatisticas:
            return {}
        
        stats_por_algoritmo = {}
        for stat in estatisticas:
            algo_id = stat['algoritmo']
            if algo_id not in stats_por_algoritmo:
                stats_por_algoritmo[algo_id] = []
            stats_por_algoritmo[algo_id].append(stat)
        
        return stats_por_algoritmo
    
    def atualizar_estatisticas_locais(self, novas_estatisticas):
        """Atualiza as estatísticas locais com novos dados."""
        if self.local_statistics and novas_estatisticas:
            self.local_statistics.update(novas_estatisticas)
            self.atualizar_dados()
    
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
        
        # Indicador de fonte de dados
        fonte_dados = "Banco de Dados" if self.database else "Dados Locais"
        fonte_text = self.tiny_font.render(f"Fonte: {fonte_dados}", True, self.warning_color)
        fonte_rect = fonte_text.get_rect(topright=(LARGURA_TELA - 20, 10))
        self.screen.blit(fonte_text, fonte_rect)
    
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
            
            # Obter range de linhas visíveis
            start_row, end_row = self.algorithm_table.get_visible_range()
            algoritmos_list = list(self.estatisticas_por_algoritmo.items())
            
            # Dados dos algoritmos (apenas os visíveis)
            row_y = header_y + 30
            for i in range(start_row, end_row):
                if i >= len(algoritmos_list):
                    break
                    
                algo_id, stats_list = algoritmos_list[i]
                
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
                    
                    for j, value in enumerate(data):
                        value_text = self.tiny_font.render(value, True, self.text_color)
                        x = 70 + sum(column_widths[:j])
                        self.screen.blit(value_text, (x, row_y))
                    
                    row_y += 20
            
            # Desenhar barra de scroll
            self.algorithm_table.draw_scrollbar(self.screen, self.border_color)
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
            
            # Obter range de linhas visíveis
            start_row, end_row = self.executions_table.get_visible_range()
            
            # Dados das execuções (apenas os visíveis)
            row_y = header_y + 30
            for i in range(start_row, end_row):
                if i >= len(self.estatisticas):
                    break
                    
                stat = self.estatisticas[-(i + 1)]  # Mais recentes primeiro
                
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
                
                for j, value in enumerate(data):
                    value_text = self.tiny_font.render(value, True, self.text_color)
                    x = 70 + sum(column_widths[:j])
                    self.screen.blit(value_text, (x, row_y))
                
                row_y += 20
            
            # Desenhar barra de scroll
            self.executions_table.draw_scrollbar(self.screen, self.border_color)
        else:
            no_data_text = self.small_font.render("Nenhuma execução recente disponível", True, self.warning_color)
            self.screen.blit(no_data_text, (70, 530)) 