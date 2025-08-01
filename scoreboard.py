import pygame

class ScoreBoard:
    def __init__(self):
        self.user_results = []  
        self.ai_results = []    
        self.is_sudden_death = False
        self.sudden_death_turn = 0  # 0: user, 1: ai

    def start_sudden_death(self):
        self.is_sudden_death = True
        self.sudden_death_turn = 0

    def increment_score(self, is_user):
        if is_user:
            self.user_results.append("GOAL")
        else:
            self.ai_results.append("GOAL")

    def increment_shots(self, is_user):
        if is_user:
            # セーブ（失敗）はGOAL以外の扱いで記録
            self.user_results.append("SAVE")
        else:
            self.ai_results.append("SAVE")

    def get_winner(self):
        if not self.is_sudden_death:
            user_goals = self.user_results.count("GOAL")
            ai_goals = self.ai_results.count("GOAL")
            if user_goals > ai_goals:
                return "YOU WIN"
            elif user_goals < ai_goals:
                return "YOU LOSE"
            else:
                return "DRAW"
        else:
            # サドンデス勝敗判定は最新の蹴りで決まる
            if self.user_results[-1] == "GOAL" and self.ai_results[-1] != "GOAL":
                return "YOU WIN"
            elif self.ai_results[-1] == "GOAL" and self.user_results[-1] != "GOAL":
                return "YOU LOSE"
            else:
                return "DRAW"

    def is_game_over(self):
        user_kicks = len(self.user_results)
        ai_kicks = len(self.ai_results)

        user_goals = self.user_results.count("GOAL")
        ai_goals = self.ai_results.count("GOAL")

        if not self.is_sudden_death:
            # 通常PK戦の終了判定
            remaining_user = 5 - user_kicks
            remaining_ai = 5 - ai_kicks

            # 残り本数と得点差から早期決着判定
            if user_goals > ai_goals + remaining_ai:
                return True
            if ai_goals > user_goals + remaining_user:
                return True

            return user_kicks >= 5 and ai_kicks >= 5

        else:
            # サドンデスは交互に蹴った結果で判定
            if user_kicks > 5 and ai_kicks > 5:
                # 最新の蹴りの結果が異なれば終了
                if self.user_results[-1] != self.ai_results[-1]:
                    return True
            return False

    def draw(self, screen, font):
        max_display = max(len(self.user_results), len(self.ai_results), 5)
        # ユーザ側の表示
        for i in range(max_display):
            color = (100, 100, 100)  # 未蹴:灰色
            if i < len(self.user_results):
                if self.user_results[i] == "GOAL":
                    color = (0, 255, 0)  # 緑
                elif self.user_results[i] == "SAVE":
                    color = (255, 0, 0)  # 赤
            pygame.draw.rect(screen, color, pygame.Rect(20 + i * 25, 20, 20, 20))

        # AI側の表示
        for i in range(max_display):
            color = (100, 100, 100)
            if i < len(self.ai_results):
                if self.ai_results[i] == "GOAL":
                    color = (0, 255, 0)
                elif self.ai_results[i] == "SAVE":
                    color = (255, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(20 + i * 25, 50, 20, 20))
    
    def is_sudden_death_pair_complete(self):
        # サドンデス中に先行と後攻が両方1回ずつ蹴っているか判定する
        # 例: user_resultsとai_resultsの長さが同じで、かつサドンデスモード中ならTrue
        if not self.is_sudden_death:
            return False
        return len(self.user_results) == len(self.ai_results) and len(self.user_results) > 5

