import pygame

class GameField:
    def __init__(self, goal_x, goal_y, goal_width, goal_height, rows, cols, line_color, highlight_color):
        self.goal_rect = pygame.Rect(goal_x, goal_y, goal_width, goal_height)
        self.rows = rows
        self.cols = cols
        self.line_color = line_color
        self.highlight_color = highlight_color
        self.cell_width = self.goal_rect.width // self.cols
        self.cell_height = self.goal_rect.height // self.rows

    def draw_grid(self, screen, selected_cell=None):
        pygame.draw.rect(screen, self.line_color, self.goal_rect, 2)

        for i in range(1, self.rows):
            pygame.draw.line(screen, self.line_color,
                             (self.goal_rect.left, self.goal_rect.top + i * self.cell_height),
                             (self.goal_rect.right, self.goal_rect.top + i * self.cell_height), 2)
        for i in range(1, self.cols):
            pygame.draw.line(screen, self.line_color,
                             (self.goal_rect.left + i * self.cell_width, self.goal_rect.top),
                             (self.goal_rect.left + i * self.cell_width, self.goal_rect.bottom), 2)

        if selected_cell:
            row, col = selected_cell
            x = self.goal_rect.left + col * self.cell_width
            y = self.goal_rect.top + row * self.cell_height
            highlight_rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
            pygame.draw.rect(screen, self.highlight_color, highlight_rect, 3)

    def detect_clicked_cell(self, mouse_x, mouse_y):
        if self.goal_rect.collidepoint(mouse_x, mouse_y):
            relative_x = mouse_x - self.goal_rect.left
            relative_y = mouse_y - self.goal_rect.top
            col = relative_x // self.cell_width
            row = relative_y // self.cell_height
            return int(row), int(col)
        return None

    def get_cell_center(self, row, col):
        cell_left = self.goal_rect.left + col * self.cell_width
        cell_top = self.goal_rect.top + row * self.cell_height

        center_x = cell_left + self.cell_width // 2
        center_y = cell_top + self.cell_height // 2

        return (center_x, center_y)