class Ball:
    def __init__(self, image, init_pos=(285, 270), base_speed=8): # base_speedを導入
        self.image = image
        self.init_pos = init_pos
        self._base_speed = base_speed # 基本速度
        self._current_speed = base_speed # 現在の速度
        self.reset()

    def reset(self):
        self.pos = list(self.init_pos)
        self.target = None
        self._current_speed = self._base_speed # リセット時に基本速度に戻す

    def set_target(self, row, col, get_cell_center_func):
        self.target = get_cell_center_func(row, col)

    def set_speed(self, speed): # 速度を動的に変更するメソッドを追加
        self._current_speed = speed

    def get_speed(self): # 現在の速度を取得するメソッドを追加
        return self._current_speed

    def update(self):
        if self.target:
            dx = self.target[0] - self.pos[0]
            dy = self.target[1] - self.pos[1]
            dist = (dx**2 + dy**2) ** 0.5

            if dist < self._current_speed: # _current_speedを使用
                self.pos = list(self.target)
                self.target = None
                return True
            else:
                self.pos[0] += self._current_speed * dx / dist # _current_speedを使用
                self.pos[1] += self._current_speed * dy / dist # _current_speedを使用

        return False

    def draw(self, screen):
        screen.blit(self.image, self.pos)