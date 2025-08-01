import pygame

class AssetLoader:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.goal_x = int(width / 6)
        self.goal_y = 85
        self.goal_width = int(width * 2 / 3)
        self.goal_height = 159

        self.gk_center = (width // 2, self.goal_y + 100)
        self.ball_init_pos = [285, 270]

        self.bg_image = self.load_and_scale("images/goal_background.png", (width, height))
        self.ball_img = self.load_and_scale_alpha("images/ball.png", (35, 35))
        self.gk_images = self.load_gk_images()
        self.font = pygame.font.SysFont(None, 36)  

    def load_and_scale(self, path, size):
        return pygame.transform.scale(pygame.image.load(path).convert(), size)

    def load_and_scale_alpha(self, path, size):
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

    def load_gk_images(self):
        def gk_img(path, size):
            return self.load_and_scale_alpha(path, size)

        return {
            "idle": gk_img("images/gk_idle.png", (60, 180)),
            "ready": gk_img("images/gk_ready.png", (80, 180)),
            (2, 0): (gk_img("images/gk_save_left_down.png", (180, 150)), [-60, +10]),
            (2, 2): (gk_img("images/gk_save_right_down.png", (180, 150)), [+60, +10]),
            (0, 0): (gk_img("images/gk_save_left_up.png", (200, 140)), [-70, -20]),
            (0, 2): (gk_img("images/gk_save_right_up.png", (200, 140)), [+70, -20]),
            (1, 0): (gk_img("images/gk_save_left_middle.png", (180, 100)), [-50, +20]),
            (1, 2): (gk_img("images/gk_save_right_middle.png", (180, 100)), [+50, +20]),
            (1, 1): (gk_img("images/gk_save_middle_middle.png", (70, 140)), [0, 0]),
            (0, 1): (gk_img("images/gk_save_middle_up.png", (80, 180)), [0, 0]),
            (2, 1): (gk_img("images/gk_save_middle_down.png", (65, 130)), [0, 0]),
        }