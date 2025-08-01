import pygame

from game_settings import GameSettings

class GameState:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.selected_cell = None
        self.waiting_for_click = True

        self.user_score = 0
        self.ai_score = 0
        self.user_shots = 0
        self.ai_shots = 0
        self.max_shots = 5

        self.user_turn = True
        self.show_result = False
        self.result_text = ""
        self.result_timer = 0

        self.show_turn = True
        self.turn_text = "YOUR TURN" if self.user_turn else "AI'S TURN"

        self.game_over = False

        self.user_shot_history = []
        #ゲーム全体での初回シュートを判定するフラグ
        self.is_game_first_shot = True

    def select_cell(self, row, col):
        self.selected_cell = (row, col)

    def get_selected_cell(self):
        return self.selected_cell

    def set_result(self, result):
        self.result_text = result

    def prepare_next_turn(self):
        if self.user_turn:
            self.user_shots += 1
        else:
            self.ai_shots += 1

        #最初のシュートが終了したら、初回フラグをFalseにする
        if self.is_game_first_shot:
            self.is_game_first_shot = False

        self.user_turn = not self.user_turn

        self.show_turn = True
        self.turn_text = "YOUR TURN" if self.user_turn else "AI'S TURN"
        self.result_timer = pygame.time.get_ticks()

        self.selected_cell = None
        self.waiting_for_click = False

    def add_user_shot_to_history(self, cell):
        self.user_shot_history.append(cell)

    def get_user_shot_history(self):
        return self.user_shot_history
    
    #初回フラグを取得するメソッド
    def get_is_game_first_shot(self):
        return self.is_game_first_shot

    def get_difficulty(self):
        return self.difficulty

    def reset(self):
        self.selected_cell = None
        self.waiting_for_click = True
        self.user_score = 0
        self.ai_score = 0
        self.user_shots = 0
        self.ai_shots = 0
        self.user_turn = True
        self.show_result = False
        self.result_text = ""
        self.result_timer = 0
        self.show_turn = True
        self.turn_text = "YOUR TURN"
        self.game_over = False
        self.user_shot_history = []
        #リセット時も初回フラグをTrueに戻す
        self.is_game_first_shot = True