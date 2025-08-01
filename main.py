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

# 初期化
pygame.init()
WIDTH, HEIGHT = 600, 360
GRID_ROWS, GRID_COLS = 3, 3
GOAL_X, GOAL_Y = int(WIDTH / 6), 85
GOAL_WIDTH, GOAL_HEIGHT = int(WIDTH * 2 / 3), 159
CELL_WIDTH, CELL_HEIGHT = GOAL_WIDTH // 3, GOAL_HEIGHT // 3
LINE_COLOR = (255, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PK対決：ボール＆GKアニメーション")

# オブジェクト生成
assets = AssetLoader(WIDTH, HEIGHT)
field = GameField(
    assets.goal_x,
    assets.goal_y,
    assets.goal_width,
    assets.goal_height,
    GRID_ROWS,
    GRID_COLS,
    LINE_COLOR,
    HIGHLIGHT_COLOR,
    assets.ball_img
)
ball = Ball(assets.ball_img, init_pos=(285, 270))
gk = Goalkeeper(assets.gk_images, field, [WIDTH // 2, GOAL_Y + 100])
state = GameState()
text_display = TextDisplay(SCREEN)
scoreboard = ScoreBoard()

# リスタートボタン用
font = pygame.font.SysFont(None, 32)
restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 50, 120, 35)

clock = pygame.time.Clock()
running = True

def draw_restart_button():
    pygame.draw.rect(SCREEN, (100, 100, 255), restart_button)
    text = font.render("RESTART", True, (255, 255, 255))
    SCREEN.blit(text, (restart_button.x + (restart_button.width - text.get_width()) // 2,
                       restart_button.y + (restart_button.height - text.get_height()) // 2))

def reset_game():
    global ball, gk, state, scoreboard
    ball.reset()
    gk.reset()
    state = GameState()
    scoreboard = ScoreBoard()

while running:
    SCREEN.blit(assets.bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
                ball.set_target(row, col, lambda r, c: field.get_cell_center(r, c, ball.image))
                gk.set_random_guess()
                state.waiting_for_click = False

    # AIのターン処理
    if not state.user_turn and state.waiting_for_click and not state.show_result and not state.show_turn and not state.game_over:
        row, col = random.randint(0, 2), random.randint(0, 2)
        state.select_cell(row, col)
        ball.set_target(row, col, lambda r, c: field.get_cell_center(r, c, ball.image))
        gk.set_random_guess()
        state.waiting_for_click = False

    # ボール移動とゴール判定
    if ball.target:
        if ball.update():
            row, col = state.selected_cell
            if gk.guess == (row, col):
                state.set_result("SAVE")
                scoreboard.increment_shots(state.user_turn)
            else:
                state.set_result("GOAL")
                scoreboard.increment_score(state.user_turn)
            state.show_result = True
            state.result_timer = pygame.time.get_ticks()

            # ここでゲーム終了判定
            if scoreboard.is_game_over():
                winner = scoreboard.get_winner()
                if winner != "DRAW":
                    state.game_over = True
                else:
                    if not state.sudden_death_mode:
                        scoreboard.start_sudden_death()
                        state.start_sudden_death()  # GameState側でもフラグ立てる
                    else:
                        # サドンデスで両者1セット蹴り終わったらゲーム終了
                        if scoreboard.is_sudden_death_pair_complete():
                            state.game_over = True
                        else:
                            # まだペアの蹴りが完了していなければ終了しない
                            pass


    # ゴールキーパーアニメーション
    gk.update()

    # 描画
    field.draw_grid(SCREEN, state.selected_cell)
    gk.draw(SCREEN)
    ball.draw(SCREEN)
    scoreboard.draw(SCREEN, pygame.font.SysFont(None, 28))

    # 結果・ターン表示処理
    if state.show_result:
        text_display.draw_result(SCREEN, state.result_text)
        if pygame.time.get_ticks() - state.result_timer > 1000:
            state.show_result = False

            if state.game_over:
                # ゲーム終了なら何もしない（リスタート待ち）
                pass

            elif scoreboard.is_sudden_death:
                # サドンデスの場合の勝敗判定
                user_last = scoreboard.user_results[-1] if scoreboard.user_results else None
                ai_last = scoreboard.ai_results[-1] if scoreboard.ai_results else None
                if user_last != ai_last:
                    # 一方だけ成功なら終了
                    state.game_over = True
                else:
                    # 同じ結果なら次のターンへ
                    state.prepare_next_turn()
                    ball.reset()
                    gk.reset()

            else:
                # 通常のターン継続処理
                state.prepare_next_turn()
                ball.reset()
                gk.reset()
    if state.show_turn:
        text_display.draw_turn(SCREEN, state.turn_text)
        if pygame.time.get_ticks() - state.result_timer > 2000:
            state.show_turn = False
            state.waiting_for_click = True
            state.result_timer = pygame.time.get_ticks()

    if state.game_over:
        winner = scoreboard.get_winner()
        text_display.draw_result(SCREEN, f"RESULT : {winner}")
        draw_restart_button()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()