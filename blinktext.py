import pygame

class BlinkText:
    def __init__(self, text, font_name='Arial', font_size=40):
        pygame.font.init()
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.text_surface = self.font.render(self.text, True, (255, 0, 0))
        self.surface = pygame.Surface((self.text_surface.get_width() + 2, self.text_surface.get_height() + 2))
        self.surface.fill((255, 255, 255))
        self.surface.blit(self.text_surface, (1, 1))
        self.visible = False
        self.show_timer = 0

    def update(self):
        if self.visible:
            current_time = pygame.time.get_ticks()
            if current_time - self.show_timer > 500:  # Blink every 500 milliseconds
                self.visible = not self.visible
                self.show_timer = current_time

    def draw(self, win, x, y):
        if self.visible:
            win.blit(self.surface, (x, y))
