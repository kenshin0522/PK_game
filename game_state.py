import pygame

class GameState:
    def __init__(self):
        self.user_turn = True
        self.waiting_for_click = True
        self.show_result = False
        self.show_turn = True
        self.result_text = ""
        self.turn_text = "YOUR TURN"
        self.result_timer = 0
        self.turn_count = 0
        self.max_turns = 10
        self.game_over = False
        self.selected_cell = None

        # ▼サドンデス関連
        self.sudden_death_mode = False
        self.sudden_death_turn = 0  # サドンデス用ターン数

    def select_cell(self, row, col):
        self.selected_cell = (row, col)

    def get_selected_cell(self):
        return self.selected_cell

    def set_result(self, text):
        self.result_text = text
        self.show_result = True
        self.result_timer = pygame.time.get_ticks()

    def prepare_next_turn(self):
        self.user_turn = not self.user_turn
        self.show_turn = True
        self.result_text = ""
        self.turn_text = "YOUR TURN" if self.user_turn else "AI'S TURN"
        self.selected_cell = None
        if not self.sudden_death_mode:
            self.turn_count += 1
        else:
            self.sudden_death_turn += 1

    def is_game_over(self):
        if self.sudden_death_mode:
            return False  # サドンデス中は別の条件で終了判定（外部で処理する）
        return self.turn_count >= self.max_turns

    def start_sudden_death(self):
        self.sudden_death_mode = True
        self.sudden_death_turn = 0
        self.result_text = "SUDDEN DEATH!"
        self.result_timer = pygame.time.get_ticks()
        self.show_result = True
