import pygame

class ScoreBoard:
    def __init__(self):
        self.user_results = []
        self.ai_results = []
        self.font = pygame.font.SysFont(None, 28) # ここでフォントを初期化

    def record_shot_result(self, is_user, result_type):
        if is_user:
            self.user_results.append(result_type)
        else:
            self.ai_results.append(result_type)

    def get_winner(self):
        user_goals = self.user_results.count("GOAL")
        ai_goals = self.ai_results.count("GOAL")
        if user_goals > ai_goals:
            return "YOU WIN"
        elif user_goals < ai_goals:
            return "YOU LOSE"
        else:
            return "DRAW"

    def is_game_over(self):
        return len(self.user_results) >= 5 and len(self.ai_results) >= 5

    def draw(self, screen): # font 引数を削除
        # ユーザ側の表示
        for i in range(5):
            color = (100, 100, 100)
            if i < len(self.user_results):
                if self.user_results[i] == "GOAL":
                    color = (0, 255, 0)
                elif self.user_results[i] == "SAVE":
                    color = (255, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(20 + i * 25, 20, 20, 20))

        # AI側の表示
        for i in range(5):
            color = (100, 100, 100)
            if i < len(self.ai_results):
                if self.ai_results[i] == "GOAL":
                    color = (0, 255, 0)
                elif self.ai_results[i] == "SAVE":
                    color = (255, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(20 + i * 25, 50, 20, 20))