import random
from game_settings import GameSettings
from collections import Counter

class Goalkeeper:
    def __init__(self, gk_images, center_pos, difficulty):
        self.images = gk_images
        self.center_pos = list(center_pos)
        self.current_pos = list(center_pos)
        self.image = self.images["idle"]
        self.target_offset = [0, 0]
        self.current_frame = 0
        self.base_jump_frames = 15
        self.jump_frames = self.base_jump_frames

        self.guess = None
        self.gk_action_target = None

        self.prediction_match_type = "NONE"
        self.actual_move_match_ball = False

        self.difficulty_settings = GameSettings.get_difficulty_settings(difficulty)
        self.save_probability = self.difficulty_settings['gk_save_probability']
        self.prediction_history_length = self.difficulty_settings['gk_prediction_history_length']
        self.prediction_fail_chance = self.difficulty_settings.get('gk_prediction_fail_chance', 0.0)

    #is_game_first_shotを引数で受け取る
    def set_guess_and_animation(self, history_to_learn_from, current_ball_target, is_game_first_shot):
        print(f"\n--- GKの予測処理開始 ---")
        print(f"現在のシュート履歴 (全量): {history_to_learn_from}")
        print(f"履歴の長さ: {len(history_to_learn_from)}")
        print(f"ゲームの初回シュート判定 (is_game_first_shot): {is_game_first_shot}")

        # GKの予測 (guess) を決定するロジック
        # Learning GKモードで、かつゲーム全体で初回シュートの場合
        if self.difficulty_settings['name'] == GameSettings.LEARNING and is_game_first_shot:
            self.guess = (random.randint(0, 2), random.randint(0, 2))
            print(f"  学習GKのゲーム初回シュート（履歴なし）: 予測 = {self.guess} (ランダム)")
        # RANDOM GKモードの場合、または履歴がある学習GKモードの場合
        else:
            if self.difficulty_settings['name'] == GameSettings.RANDOM:
                self.guess = (random.randint(0, 2), random.randint(0, 2))
                print(f"  RANDOM GK: 予測 = {self.guess} (ランダム)")
            else: # 学習GKで履歴がある場合
                print(f"  学習GK。全履歴を学習ロジック実行中...")
                recent_shots = history_to_learn_from[:] # 全履歴を参照
                print(f"  学習対象のシュート履歴 (全量): {recent_shots}")

                recent_shots_cols = [shot[1] for shot in recent_shots]
                col_counts = Counter(recent_shots_cols)
                most_common_cols = col_counts.most_common(1)
                predicted_col = most_common_cols[0][0] if most_common_cols else random.randint(0, 2)
                print(f"  最も多い列: {most_common_cols} -> 予測列: {predicted_col}")

                shots_in_predicted_col = [shot[0] for shot in recent_shots if shot[1] == predicted_col]
                row_counts_in_col = Counter(shots_in_predicted_col)
                most_common_rows_in_col = row_counts_in_col.most_common(1)
                predicted_row = most_common_rows_in_col[0][0] if most_common_rows_in_col else random.randint(0, 2)
                print(f"  予測列({predicted_col})内の最も多い行: {most_common_rows_in_col} -> 予測行: {predicted_row}")

                self.guess = (predicted_row, predicted_col)
                print(f"  GKの学習予測 (self.guess): {self.guess}")

        # GKの「予測」とボールのターゲットがどれだけ一致したかを判定 (アニメーション速度調整用)
        self.prediction_match_type = "NONE"
        if self.guess is not None and current_ball_target is not None:
            if self.guess == current_ball_target:
                self.prediction_match_type = "FULL_MATCH"
            elif self.guess[1] == current_ball_target[1]:
                self.prediction_match_type = "COL_MATCH"
        print(f"  GK予測の一致タイプ (アニメーション用): {self.prediction_match_type}")


        # 実際にGKが飛ぶセル (gk_action_target) を決定するロジック
        # is_game_first_shotを渡す
        self.gk_action_target = self._determine_gk_action_target(is_game_first_shot)
        print(f"  GKが実際に飛ぶセル (gk_action_target): {self.gk_action_target}")

        self._set_animation_by_action_target()
        # is_game_first_shotを渡す
        self._adjust_animation_speed(is_game_first_shot)

        # 実際に飛んだセルとボールのターゲットセルが一致したか
        self.actual_move_match_ball = (self.gk_action_target == current_ball_target)
        print(f"  GKが実際に飛んだセルとボールのターゲットが一致したか: {self.actual_move_match_ball}")
        print(f"--- GKの予測処理終了 ---\n")


    # is_game_first_shotを引数で受け取る
    def _determine_gk_action_target(self, is_game_first_shot):
        """GKの学習予測(self.guess)に基づいて、実際にGKが飛ぶセルを決定する。
           学習予測のセルに飛ぶ確率を高くし、隣接セルにも飛ぶ可能性を持たせる。"""
        # Learning GKモードで、かつゲーム全体で初回シュートの場合
        if self.difficulty_settings['name'] == GameSettings.LEARNING and is_game_first_shot:
            chosen_target = (random.randint(0, 2), random.randint(0, 2))
            print(f"  _determine_gk_action_target: 学習GKの初回シュートのため、完全にランダムな {chosen_target} に飛ぶ")
            return chosen_target
        # それ以外のケース (RANDOM GK、または履歴がある学習GK)
        else:
            if self.guess is None:
                return (random.randint(0, 2), random.randint(0, 2))

            predicted_row, predicted_col = self.guess
            
            if self.difficulty_settings['name'] == GameSettings.RANDOM:
                chosen_target = (random.randint(0, 2), random.randint(0, 2))
                print(f"  _determine_gk_action_target: RANDOM GKのため {chosen_target} に飛ぶ")
                return chosen_target
            else: # 学習GKで履歴がある場合 (is_game_first_shotがFalse)
                # 学習したマスに飛ぶ確率 (例: 80%)
                if random.random() < 0.8:
                    print(f"  _determine_gk_action_target: 学習予測 {self.guess} に飛ぶ")
                    return (predicted_row, predicted_col)
                else:
                    # 学習したマスの「周辺」の隣接マスに飛ぶ (例: 20%)
                    possible_adjacent_targets = []
                    for r_offset in [-1, 0, 1]:
                        for c_offset in [-1, 0, 1]:
                            if r_offset == 0 and c_offset == 0:
                                continue
                            
                            adj_row, adj_col = predicted_row + r_offset, predicted_col + c_offset
                            if 0 <= adj_row <= 2 and 0 <= adj_col <= 2:
                                possible_adjacent_targets.append((adj_row, adj_col))
                    
                    if possible_adjacent_targets:
                        chosen_target = random.choice(possible_adjacent_targets)
                        print(f"  _determine_gk_action_target: 学習予測周辺 {self.guess} からランダムに {chosen_target} に飛ぶ")
                        return chosen_target
                    else:
                        print(f"  _determine_gk_action_target: 隣接マスがないため学習予測 {self.guess} にフォールバック")
                        return (predicted_row, predicted_col)

    def _set_animation_by_action_target(self):
        """GKが実際に飛ぶセル(gk_action_target)に基づいて適切なアニメーションとオフセットを設定する"""
        key = self.gk_action_target
        if key in self.images:
            self.image, offset = self.images[key]
            self.target_offset = offset
        else:
            self.image = self.images["idle"]
            self.target_offset = [0, 0]
        self.current_frame = self.jump_frames

    # ★修正: is_game_first_shotを引数で受け取る
    def _adjust_animation_speed(self, is_game_first_shot):
        """GKの予測（guess）とボールの列の一致に応じてアニメーション速度を調整する"""
        # 初回シュートの場合は速度調整を行わない
        if self.difficulty_settings['name'] == GameSettings.LEARNING and not is_game_first_shot:
            if self.prediction_match_type == "FULL_MATCH":
                self.jump_frames = int(self.base_jump_frames * 0.7)
            elif self.prediction_match_type == "COL_MATCH":
                self.jump_frames = int(self.base_jump_frames * 0.9)
            else:
                self.jump_frames = int(self.base_jump_frames * 1.3)
        else: # RANDOM GKの場合、または学習GKの初回（履歴がない）
            self.jump_frames = self.base_jump_frames
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
        self.gk_action_target = None
        self.jump_frames = self.base_jump_frames
        self.prediction_match_type = "NONE"
        self.actual_move_match_ball = False
        # is_first_shot_of_game は GameState が管理するので、ここではリセットしない