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


def check_events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()


def update_screen(settings, screen, pacman, grid_pts, foods):
    screen.fill(settings.bg_color)
    grid_pts.draw()
    foods.draw()
    pacman.draw()
    pg.display.flip()
