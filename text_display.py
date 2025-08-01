import pygame

class TextDisplay:
    def __init__(self, screen, font_name=None, default_size=36, text_color=(0, 0, 0)):
        self.screen = screen
        self.font_name = font_name
        self.default_size = default_size
        self.text_color = text_color

    def draw_text(self, text, y, size=None, color=None):
        font_size = size if size is not None else self.default_size
        color = color if color is not None else self.text_color
        font = pygame.font.SysFont(self.font_name, font_size)
        text_surface = font.render(text, True, color)
        x = (self.screen.get_width() - text_surface.get_width()) // 2
        self.screen.blit(text_surface, (x, y))

    def draw_turn(self, screen, turn_text):
        # draw_text を利用して共通化
        self.draw_text(turn_text, screen.get_height() // 2 - 30, size=60, color=(0, 0, 255))

    def draw_result(self, screen, result_text):
        # draw_text を利用して共通化
        self.draw_text(result_text, screen.get_height() // 2 - 30, size=60, color=(0, 0, 255))