import random

class Goalkeeper:
    def __init__(self, gk_images, field, center_pos):
        self.images = gk_images  # dict: {(row, col): (image, offset)}
        self.center_pos = list(center_pos)
        self.current_pos = list(center_pos)
        self.image = self.images["idle"]
        self.target_offset = [0, 0]
        self.current_frame = 0
        self.jump_frames = 15
        self.field = field
        self.guess = None  # (row, col)

    def set_random_guess(self):
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        self.guess = (row, col)
        self._set_animation_by_guess()

    def _set_animation_by_guess(self):
        key = self.guess
        if key in self.images:
            self.image, offset = self.images[key]
            self.target_offset = offset
        else:
            self.image = self.images["ready"]
            self.target_offset = [0, 0]
        self.current_frame = self.jump_frames

    def update(self):
        if self.current_frame > 0:
            ratio = (self.jump_frames - self.current_frame + 1) / self.jump_frames
            self.current_pos[0] = self.center_pos[0] + self.target_offset[0] * ratio
            self.current_pos[1] = self.center_pos[1] + self.target_offset[1] * ratio
            self.current_frame -= 1

    def draw(self, screen):
        if self.image:
            rect = self.image.get_rect(center=self.current_pos)
            screen.blit(self.image, rect)

    def reset(self):
        self.image = self.images["idle"]
        self.current_pos = list(self.center_pos)
        self.current_frame = 0
        self.target_offset = [0, 0]
        self.guess = None