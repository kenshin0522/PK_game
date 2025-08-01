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
        font = pygame.font.SysFont(self.font_name, 60)
        text_surface = font.render(turn_text, True, (0, 0, 255))  
        x = (screen.get_width() - text_surface.get_width()) // 2
        y = (screen.get_height() - text_surface.get_height()) // 2
        screen.blit(text_surface, (x, y))

    def draw_result(self, screen, result_text):
        font = pygame.font.SysFont(self.font_name, 60)
        text_surface = font.render(result_text, True, (0, 0, 255))  
        x = (screen.get_width() - text_surface.get_width()) // 2
        y = (screen.get_height() - text_surface.get_height()) // 2
        screen.blit(text_surface, (x, y))