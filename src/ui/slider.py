import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val=0, max_val=100, initial_val=0):
        """
        Inicializa o slider com as dimensões e valores especificados.
        
        Args:
            x (int): Posição X do canto superior esquerdo do slider.
            y (int): Posição Y do canto superior esquerdo do slider.
            width (int): Largura da barra do slider.
            height (int): Altura da barra do slider.
            min_val (int): Valor mínimo do slider (padrão: 0).
            max_val (int): Valor máximo do slider (padrão: 100).
            initial_val (int): Valor inicial do slider (padrão: 0).
        """
        # Retângulo que representa a barra do slider
        self.rect = pygame.Rect(x, y, width, height)
        # Retângulo que representa o botão deslizante (knob)
        self.knob_rect = pygame.Rect(x, y, 15, height + 6)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val  # Valor atual do slider
        self.dragging = False  # Indica se o botão está sendo arrastado
        self.update_knob_position()  # Posiciona o knob de acordo com o valor inicial
        
    def update_knob_position(self):
        """Atualiza a posição do knob com base no valor atual do slider."""
        # Calcula a proporção do valor atual em relação ao intervalo (min_val, max_val)
        if self.max_val == self.min_val:
            ratio = 0  # Evita divisão por zero
        else:
            ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        # Define a posição X do knob com base na proporção calculada
        self.knob_rect.centerx = self.rect.left + int(ratio * self.rect.width)
        # Centraliza verticalmente o knob em relação à barra
        self.knob_rect.centery = self.rect.centery
        
    def handle_event(self, event):
        """
        Processa eventos do pygame (mouse) para interação com o slider.
        
        Args:
            event: Evento do pygame a ser processado (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION).
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se o clique foi no knob para começar a arrastar
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # Para de arrastar quando o botão do mouse é solto
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Move o knob enquanto estiver sendo arrastado
            self.move_knob(event.pos[0])
            
    def move_knob(self, x_pos):
        """
        Move o knob para a posição X especificada e atualiza o valor do slider.
        
        Args:
            x_pos (int): Posição X do mouse (coordenada horizontal).
        """
        # Garante que o knob não saia dos limites da barra
        x_pos = max(self.rect.left, min(x_pos, self.rect.right))
        # Calcula a nova proporção com base na posição X
        ratio = (x_pos - self.rect.left) / self.rect.width
        # Atualiza o valor do slider com base na proporção
        self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
        # Atualiza a posição do knob
        self.update_knob_position()
        
    def draw(self, surface):
        """Desenha o slider na superfície especificada."""
        # Desenha a barra do slider (fundo cinza claro com borda cinza escuro)
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)
        
        # Desenha o knob (botão deslizante cinza médio com borda cinza escuro)
        pygame.draw.rect(surface, (150, 150, 150), self.knob_rect)
        pygame.draw.rect(surface, (50, 50, 50), self.knob_rect, 2)