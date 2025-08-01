import pygame
import sys
import random
from asset_loader import AssetLoader
from game_field import GameField
from ball import Ball
from goalkeeper import Goalkeeper
from game_state import GameState
from text_display import TextDisplay
from scoreboard import ScoreBoard
from game_settings import GameSettings
from collections import Counter

# 初期化
pygame.init()
WIDTH, HEIGHT = 600, 360
GRID_ROWS, GRID_COLS = 3, 3
GOAL_X, GOAL_Y = int(WIDTH / 6), 85
GOAL_WIDTH, GOAL_HEIGHT = int(WIDTH * 2 / 3), 159
LINE_COLOR = (255, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PK対決：ボール＆GKアニメーション")

# オブジェクト生成
assets = AssetLoader(WIDTH, HEIGHT)
ball = Ball(assets.ball_img, init_pos=assets.ball_init_pos, base_speed=8)
field = GameField(
    assets.goal_x,
    assets.goal_y,
    assets.goal_width,
    assets.goal_height,
    GRID_ROWS,
    GRID_COLS,
    LINE_COLOR,
    HIGHLIGHT_COLOR
)


state = None
text_display = TextDisplay(SCREEN)
scoreboard = ScoreBoard()

# リスタートボタン用
font = pygame.font.SysFont(None, 32)
restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 50, 120, 35)

game_started = False
selected_difficulty = None
gk = None

clock = pygame.time.Clock()
running = True

if not pygame.mixer.music.get_busy():
    pygame.mixer.music.play(-1)

def draw_restart_button():
    pygame.draw.rect(SCREEN, (100, 100, 255), restart_button)
    text = font.render("RESTART", True, (255, 255, 255))
    SCREEN.blit(text, (restart_button.x + (restart_button.width - text.get_width()) // 2,
                       restart_button.y + (restart_button.height - text.get_height()) // 2))

def draw_difficulty_selection():
    SCREEN.fill((0, 0, 0))
    title_text = font.render("SELECT GK TYPE", True, (255, 255, 255))
    SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    button_width, button_height = 200, 50
    gap = 20

    random_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height - gap, button_width, button_height)
    learning_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + gap, button_width, button_height)

    difficulty_buttons = {
        GameSettings.RANDOM: random_button_rect,
        GameSettings.LEARNING: learning_button_rect
    }

    for diff_name, rect in difficulty_buttons.items():
        pygame.draw.rect(SCREEN, (50, 150, 255), rect)
        text = font.render(diff_name, True, (255, 255, 255))
        SCREEN.blit(text, (rect.x + (rect.width - text.get_width()) // 2,
                           rect.y + (rect.height - text.get_height()) // 2))

def reset_game():
    global ball, gk, state, scoreboard, game_started, selected_difficulty
    ball.reset()
    if gk:
        gk.reset()
    state = None
    game_started = False
    selected_difficulty = None
    scoreboard = ScoreBoard()
    gk = None
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.mixer.music.stop()

        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                random_button_rect = pygame.Rect(WIDTH // 2 - 200 // 2, HEIGHT // 2 - 50 - 20, 200, 50)
                learning_button_rect = pygame.Rect(WIDTH // 2 - 200 // 2, HEIGHT // 2 + 20, 200, 50)

                if random_button_rect.collidepoint(mouse_pos):
                    selected_difficulty = GameSettings.RANDOM
                elif learning_button_rect.collidepoint(mouse_pos):
                    selected_difficulty = GameSettings.LEARNING

                if selected_difficulty:
                    state = GameState(selected_difficulty)
                    gk = Goalkeeper(assets.gk_images, assets.gk_center, selected_difficulty)
                    ball.reset()
                    game_started = True
            continue

        if state.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                reset_game()
            continue

        if state.show_result or state.show_turn:
            continue

        if state.user_turn and state.waiting_for_click and event.type == pygame.MOUSEBUTTONDOWN:
            result = field.detect_clicked_cell(*event.pos)
            if result is not None:
                row, col = result
                state.select_cell(row, col)
                state.add_user_shot_to_history(state.selected_cell)

                gk.set_guess_and_animation(state.get_user_shot_history(), state.selected_cell, state.get_is_game_first_shot())

                ball.set_target(row, col, lambda r, c: field.get_cell_center(r, c))
                state.waiting_for_click = False

    # AIのターン処理
    if game_started and not state.user_turn and state.waiting_for_click and not state.show_result and not state.show_turn and not state.game_over:
        ai_shot_target = None

        print(f"\n--- AIのシュート処理開始 ---")
        # ★AIのシュートは常にランダムにする
        ai_shot_target = (random.randint(0, 2), random.randint(0, 2))
        print(f"  AI: 常にランダムに {ai_shot_target} にシュート")

        row, col = ai_shot_target
        state.select_cell(row, col)

        # GKはAIのシュート方向の履歴を学習しないため、空の履歴とゲームの初回フラグを渡す
        gk.set_guess_and_animation([], state.selected_cell, state.get_is_game_first_shot()) 

        ball.set_target(row, col, lambda r, c: field.get_cell_center(r, c))
        state.waiting_for_click = False
        print(f"--- AIのシュート処理終了 ---\n")

    # ボール移動とゴール判定
    if game_started and ball.target:
        difficulty_settings = GameSettings.get_difficulty_settings(state.get_difficulty())
        if gk.prediction_match_type == "FULL_MATCH":
            ball.set_speed(ball._base_speed * difficulty_settings['ball_speed_multiplier_hit'])
        elif gk.prediction_match_type == "COL_MATCH":
            ball.set_speed(ball._base_speed * (difficulty_settings['ball_speed_multiplier_hit'] + difficulty_settings['ball_speed_multiplier_miss']) / 2)
        else: # "NONE"
            ball.set_speed(ball._base_speed * difficulty_settings['ball_speed_multiplier_miss'])

        if ball.update():
            row, col = state.get_selected_cell() # ボールの最終着弾セル

            print(f"--- ターン終了時の判定 ---")
            print(f"ボールのターゲットセル: ({row}, {col})")
            print(f"GKが学習で予測したセル (gk.guess): {gk.guess}")
            print(f"GKが実際に飛んだセル (gk.gk_action_target): {gk.gk_action_target}")
            print(f"GK予測一致タイプ (アニメーション用): {gk.prediction_match_type}")
            print(f"GKが実際に飛んだセルとボールのターゲットが一致したか: {gk.actual_move_match_ball}")


            is_saved_outcome = False
            # GKが実際に飛んだセルがボールのターゲットセルと「完全に一致」した場合、必ずセーブ成功
            if gk.actual_move_match_ball:
                is_saved_outcome = True
                print(f"GKがボールの着弾セルに飛び、セーブ成功！")
            else:
                print(f"GKがボールの着弾セルに飛んでいない。")

            if is_saved_outcome:
                state.set_result("SAVE")
                scoreboard.record_shot_result(state.user_turn, "SAVE")
            else:
                state.set_result("GOAL")
                scoreboard.record_shot_result(state.user_turn, "GOAL")

            state.show_result = True
            state.result_timer = pygame.time.get_ticks()

    # ゴールキーパーアニメーション
    if game_started and gk:
        gk.update()

    # 描画
    if game_started:
        SCREEN.blit(assets.bg_image, (0, 0))

        field.draw_grid(SCREEN, state.get_selected_cell())
        if gk:
            gk.draw(SCREEN)
        ball.draw(SCREEN)
        scoreboard.draw(SCREEN)

        # 結果・ターン表示処理
        if state.show_result:
            text_display.draw_result(SCREEN, state.result_text)
            if pygame.time.get_ticks() - state.result_timer > 1000:
                state.show_result = False
                if scoreboard.is_game_over():
                    state.game_over = True
                    pygame.mixer.music.stop()
                else:
                    state.prepare_next_turn()
                    ball.reset()
                    if gk:
                        gk.reset()
                state.result_timer = pygame.time.get_ticks()

        if state.show_turn:
            text_display.draw_turn(SCREEN, state.turn_text)
            if pygame.time.get_ticks() - state.result_timer > 2000:
                state.show_turn = False
                state.waiting_for_click = True

        if state.game_over:
            winner = scoreboard.get_winner()
            text_display.draw_result(SCREEN, f"RESULT : {winner}")
            draw_restart_button()
    else:
        draw_difficulty_selection()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()