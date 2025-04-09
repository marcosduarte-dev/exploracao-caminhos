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
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_rect = pygame.Rect(x, y, 15, height + 6)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        self.update_knob_position() 
        
    def update_knob_position(self):
        """Atualiza a posição do knob com base no valor atual do slider."""
        if self.max_val == self.min_val:
            ratio = 0
        else:
            ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.knob_rect.centerx = self.rect.left + int(ratio * self.rect.width)
        self.knob_rect.centery = self.rect.centery
        
    def handle_event(self, event):
        """
        Processa eventos do pygame (mouse) para interação com o slider.
        
        Args:
            event: Evento do pygame a ser processado (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION).
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.move_knob(event.pos[0])
            
    def move_knob(self, x_pos):
        """
        Move o knob para a posição X especificada e atualiza o valor do slider.
        
        Args:
            x_pos (int): Posição X do mouse (coordenada horizontal).
        """
        x_pos = max(self.rect.left, min(x_pos, self.rect.right))
        ratio = (x_pos - self.rect.left) / self.rect.width
        self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
        self.update_knob_position()
        
    def draw(self, surface):
        """Desenha o slider na superfície especificada."""
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)
        
        pygame.draw.rect(surface, (150, 150, 150), self.knob_rect)
        pygame.draw.rect(surface, (50, 50, 50), self.knob_rect, 2)