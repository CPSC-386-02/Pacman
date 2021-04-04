import sys
import pygame as pg
from vector import Vector


direction = {"UP": Vector(0, -1), "DOWN": Vector(0, 1),
             "RIGHT": Vector(1, 0), "LEFT": Vector(-1, 0),
             "STOP": Vector(0, 0)}


def check_key_down_event():
    key_pressed = pg.key.get_pressed()
    if key_pressed[pg.K_UP]:
        return direction["UP"]
    elif key_pressed[pg.K_DOWN]:
        return direction["DOWN"]
    elif key_pressed[pg.K_RIGHT]:
        return direction["RIGHT"]
    elif key_pressed[pg.K_LEFT]:
        return direction["LEFT"]
    return None


def check_events(game):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if game.game_over:
                    game.start_game()
                else:
                    game.pause.player()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(game, mouse_x, mouse_y)
            check_scores_button(game, mouse_x, mouse_y)


def update_screen(game):
    if game.settings.game_active:
        game.screen.fill(game.settings.bg_color)
        game.maze.create_maze()
        game.foods.draw()
        if game.fruit is not None:
            game.fruit.draw()
        game.pacman.draw()
        game.ghosts.draw()
        game.sb.show_score()
    else:
        game.play_button.draw_button()
        game.score_button.draw_button()
    pg.display.flip()


def check_play_button(game, mouse_x, mouse_y):
    button_clicked = game.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not game.settings.game_active:
        game.start_game()
        game.pause.force(False)
        game.pause.start_timer(4.5)
        game.sound.play_open_song()
        game.settings.game_active = True


def check_scores_button(game, mouse_x, mouse_y):
    button_clicked = game.score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not game.settings.game_active:
        high_score_font = pg.font.SysFont("monospace", 22)
        high_score_text = high_score_font.render("Current High Score: " + str(game.stats.high_score), True, (255, 255, 255))
        game.screen.blit(high_score_text, (70, 540))
