class GameSettings:
    LEARNING = "Learning GK" # 学習ありキーパー
    RANDOM = "Random GK"     # 完全ランダムキーパー

    DIFFICULTY_SETTINGS = {
        RANDOM: { # 学習なしキーパー
            'name': RANDOM,
            'gk_save_probability': 1.0, # 予測が当たった場合、100%セーブ
            'gk_prediction_history_length': 0, # 履歴を全く使わない（完全ランダム）
            'gk_prediction_fail_chance': 0.0, # 予測が当たったら必ずその位置に飛ぶ（意図的に外さない）
            'ball_speed_multiplier_hit': 1.0, # ボール速度の調整（ヒット時）
            'ball_speed_multiplier_miss': 1.0, # ボール速度の調整（ミス時）
            'gk_jump_frames_multiplier_hit': 1.0, # GKジャンプフレームの調整（ヒット時）
            'gk_jump_frames_multiplier_miss': 1.0 # GKジャンプフレームの調整（ミス時）
        },
        LEARNING: { # 学習ありキーパー
            'name': LEARNING,
            'gk_save_probability': 1.0, # 予測が当たった場合、100%セーブ
            'gk_prediction_history_length': 5, # 5回分の履歴から予測（学習能力あり）
            'gk_prediction_fail_chance': 0.0, # 予測が当たったら必ずその位置に飛ぶ（意図的に外さない）
            'ball_speed_multiplier_hit': 1.2, # 学習GKが予測を当てた場合、ボールを少し速く見せる
            'ball_speed_multiplier_miss': 0.8, # 学習GKが予測を外した場合、ボールを少し遅く見せる
            'gk_jump_frames_multiplier_hit': 0.8, # 学習GKが予測を当てた場合、GKアニメを少し速く見せる
            'gk_jump_frames_multiplier_miss': 1.2 # 学習GKが予測を外した場合、GKアニメを少し遅く見せる
        }
    }

    @classmethod
    def get_difficulty_settings(cls, difficulty):
        return cls.DIFFICULTY_SETTINGS.get(difficulty, cls.DIFFICULTY_SETTINGS[cls.RANDOM])