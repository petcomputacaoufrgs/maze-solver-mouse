import pygame

class IconButton:
    # Botão com ícone que pode alternar entre dois estados visuais
    def __init__(self, x, y, width, height, icon_false, icon_true, color, hover_color, callback, initial_state=False):
        # icon_false: imagem mostrada quando state = False
        # icon_true: imagem mostrada quando state = True
        self.rect = pygame.Rect(x, y, width, height)
        self.icon_false = icon_false
        self.icon_true = icon_true
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.state = initial_state

    def set_state(self, state):
        self.state = state

    def toggle_state(self):
        self.state = not self.state

    def draw(self, screen):
        # Muda a cor se o mouse estiver em cima
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(screen, current_color, self.rect, border_radius=5)
        
        # Desenha o ícone apropriado baseado no estado
        icon = self.icon_true if self.state else self.icon_false
        # Centraliza o ícone no botão
        icon_rect = icon.get_rect(center=self.rect.center)
        screen.blit(icon, icon_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        # Muda a cor se o mouse estiver em cima
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(screen, current_color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, 10)
        self.handle_rect = pygame.Rect(x, y - 5, 15, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        
        # Posiciona o handle inicialmente
        pos_ratio = (initial_val - min_val) / (max_val - min_val)
        self.handle_rect.centerx = x + (pos_ratio * width)

    def draw(self, screen):
        font = pygame.font.SysFont(None, 18)
        # Desenha a trilha e o handle
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.handle_rect)
        
        # Texto do valor
        val_surf = font.render(f"{self.label}: {int(self.value)}ms", True, (0, 0, 0))
        screen.blit(val_surf, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Limita o movimento dentro da trilha
            new_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            self.handle_rect.centerx = new_x
            # Converte posição x em valor
            pos_ratio = (new_x - self.rect.left) / self.rect.width
            self.value = self.min_val + pos_ratio * (self.max_val - self.min_val)

class InputBox:
    def __init__(self, x, y, width, height, label="Seed:", initial_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = initial_text
        self.label = label
        self.font = pygame.font.SysFont(None, 32)
        self.txt_surface = self.font.render(initial_text, True, (0, 0, 0))
        self.active = False
        self.first_click = False  # Flag para limpar texto no primeiro clique

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Se o usuário clicar na caixa, ela fica ativa
            if self.rect.collidepoint(event.pos):
                was_inactive = not self.active
                self.active = True
                # Se estava inativo e foi clicado, marcar para limpar na primeira tecla
                if was_inactive:
                    self.first_click = True
            else:
                self.active = False
                self.first_click = False
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.first_click = False
                    return self.text  # Retorna o texto ao apertar Enter
                elif event.key == pygame.K_BACKSPACE:
                    if self.first_click:
                        # Se é o primeiro input, limpa tudo
                        self.text = ""
                        self.first_click = False
                    else:
                        self.text = self.text[:-1]
                else:
                    # Se é o primeiro input após clicar, substitui o texto
                    if self.first_click and event.unicode.isdigit():
                        self.text = ""
                        self.first_click = False
                    # Aceita apenas números e limita a 6 dígitos
                    if event.unicode.isdigit() and len(self.text) < 6:
                        self.text += event.unicode
                
                # Re-renderiza o texto
                self.txt_surface = self.font.render(self.text, True, (0, 0, 0))
        return None

    def draw(self, screen):
        # Desenha o Label acima da caixa
        if self.label:
            label_surf = self.font.render(self.label, True, (0, 0, 0))
            screen.blit(label_surf, (self.rect.x, self.rect.y - 20))
        
        # Desenha o texto centralizado dentro da caixa
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)
        
        # Desenha a borda da caixa
        pygame.draw.rect(screen, self.color, self.rect, 2)