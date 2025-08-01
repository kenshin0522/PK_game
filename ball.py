class Ball:
    def __init__(self, image, init_pos=(285, 270), speed=8):
        self.image = image
        self.init_pos = init_pos  # 初期位置を明示（互換性維持）
        self.speed = speed
        self.reset()

    def reset(self):
        self.pos = list(self.init_pos)
        self.target = None
        self.selected_cell = None

    def set_target(self, row, col, get_cell_center_func):
        self.selected_cell = (row, col)
        self.target = get_cell_center_func(row, col)

    def update(self):
        if self.target:
            dx = self.target[0] - self.pos[0]
            dy = self.target[1] - self.pos[1]
            dist = (dx**2 + dy**2) ** 0.5

            if dist < self.speed:
                self.pos = list(self.target)
                self.target = None
                return True  # 到達
            else:
                self.pos[0] += self.speed * dx / dist
                self.pos[1] += self.speed * dy / dist

        return False  # まだ到達していない

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def get_selected_cell(self):
        return self.selected_cell