import pygame
import os

class AssetLoader:
    def __init__(self, width, height):
        pygame.mixer.init() # Pygameミキサーの初期化

        self.width = width
        self.height = height
        # ゴール座標とサイズ (main.py と同じ値)
        self.goal_x = int(width / 6)
        self.goal_y = 85 # main.py の値に合わせる
        self.goal_width = int(width * 2 / 3)
        self.goal_height = 159 # main.py の値に合わせる

        # 初期位置とセンター座標
        self.gk_center = (width // 2, self.goal_y + 100)
        self.ball_init_pos = [285, 270]

        self.base_path = os.path.dirname(__file__)
        self.assets_path = os.path.join(self.base_path, 'images')

        self.bg_image = self.load_and_scale(os.path.join(self.assets_path, "goal_background.png"), (width, height))
        self.ball_img = self.load_and_scale_alpha(os.path.join(self.assets_path, "ball.png"), (35, 35))
        self.gk_images = self.load_gk_images()

        # サウンドのロード
        self.shot_sound = None
        self.goal_sound = None
        self.save_sound = None

        # 背景BGMのロード
        self._load_music('wonderland.wav', volume=0.3)


    def load_and_scale(self, path, size):
        try:
            return pygame.transform.scale(pygame.image.load(path).convert(), size)
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            pygame.quit()
            exit()

    def load_and_scale_alpha(self, path, size):
        try:
            return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            pygame.quit()
            exit()

    def load_gk_images(self):
        def gk_img(filename, size):
            return self.load_and_scale_alpha(os.path.join(self.assets_path, filename), size)

        return {
            "idle": gk_img("gk_idle.png", (60, 180)),
            "ready": gk_img("gk_ready.png", (80, 180)),
            (2, 0): (gk_img("gk_save_left_down.png", (180, 150)), [-60, +10]),
            (2, 2): (gk_img("gk_save_right_down.png", (180, 150)), [+60, +10]),
            (0, 0): (gk_img("gk_save_left_up.png", (200, 140)), [-70, -20]),
            (0, 2): (gk_img("gk_save_right_up.png", (200, 140)), [+70, -20]),
            (1, 0): (gk_img("gk_save_left_middle.png", (180, 100)), [-50, +20]),
            (1, 2): (gk_img("gk_save_right_middle.png", (180, 100)), [+50, +20]),
            (1, 1): (gk_img("gk_save_middle_middle.png", (70, 140)), [0, 0]),
            (0, 1): (gk_img("gk_save_middle_up.png", (80, 180)), [0, 0]),
            (2, 1): (gk_img("gk_save_middle_down.png", (65, 130)), [0, 0]),
        }

    def _load_sound(self, filename, volume=1.0):
        path = os.path.join(self.assets_path, filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except pygame.error as e:
            print(f"Warning: Could not load sound {path}: {e}. Sound will not play.")
            return None

    def _load_music(self, filename, volume=1.0):
        path = os.path.join(self.assets_path, filename)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
        except pygame.error as e:
            print(f"Error loading music {path}: {e}")