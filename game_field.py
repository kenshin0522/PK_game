import pygame

class GameField:
    def __init__(self, goal_x, goal_y, goal_width, goal_height, rows, cols, line_color, highlight_color, ball_image=None):
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_width = goal_width
        self.goal_height = goal_height
        self.rows = rows
        self.cols = cols
        self.line_color = line_color
        self.highlight_color = highlight_color
        self.cell_width = goal_width // cols
        self.cell_height = goal_height // rows
        self.selected_cell = None

        # 初期ボール位置の設定（中央セル）
        if ball_image:
            center_row = rows // 2
            center_col = cols // 2
            self.ball_start_pos = self.get_cell_center(center_row, center_col, ball_image)
        else:
            self.ball_start_pos = [goal_x + goal_width // 2, goal_y + goal_height // 2]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.goal_x + col * self.cell_width
                y = self.goal_y + row * self.cell_height
                rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
                color = self.highlight_color if self.selected_cell == (row, col) else self.line_color
                pygame.draw.rect(screen, color, rect, 3 if self.selected_cell == (row, col) else 2)

    def draw_grid(self, screen, selected_cell):
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.goal_x + col * self.cell_width
                y = self.goal_y + row * self.cell_height
                rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
                color = self.highlight_color if selected_cell == (row, col) else self.line_color
                pygame.draw.rect(screen, color, rect, 3 if selected_cell == (row, col) else 2)

    def set_selected_cell(self, row, col):
        self.selected_cell = (row, col)

    def get_selected_cell(self):
        return self.selected_cell

    def get_cell_center(self, row, col, ball_image):
        x = self.goal_x + col * self.cell_width + self.cell_width // 2
        y = self.goal_y + row * self.cell_height + self.cell_height // 2
        return [x - ball_image.get_width() // 2, y - ball_image.get_height() // 2]

    def detect_clicked_cell(self, mx, my):
        if self.goal_x <= mx < self.goal_x + self.goal_width and self.goal_y <= my < self.goal_y + self.goal_height:
            col = (mx - self.goal_x) // self.cell_width
            row = (my - self.goal_y) // self.cell_height
            return (row, col)
        return None

    def get_clicked_cell(self, pos):
        return self.detect_clicked_cell(*pos)