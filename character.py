import pygame as pg
import game_functions as gf


class Character:
    def __init__(self, settings, screen, grid_pts):
        self.settings = settings
        self.screen = screen
        self.direction = gf.direction["STOP"]

        self.grid_pts = grid_pts
        self.current_grid_pt = grid_pts.grid_pts_li[0]
        self.nxt_grid_pt = self.current_grid_pt
        self.position = self.current_grid_pt.position.copy()
        self.appear = True
        self.color = None
        self.image = None
        self.sprite_sheet = self.settings.sprite_sheet

    def set_position(self):
        self.position = self.current_grid_pt.position.copy()

    def check_nxt_grid_pt(self):
        if self.nxt_grid_pt is not None:
            dist_btw_2_grid_pts = self.nxt_grid_pt.position - self.current_grid_pt.position
            dist_btw_pacman_and_grid_pt = self.position - self.current_grid_pt.position
            return dist_btw_pacman_and_grid_pt.magnitudeSquared() >= dist_btw_2_grid_pts.magnitudeSquared()
        return False

    def reverse_direction(self):
        if self.direction is gf.direction["UP"]:
            self.direction = gf.direction["DOWN"]
        elif self.direction is gf.direction["DOWN"]:
            self.direction = gf.direction["UP"]
        elif self.direction is gf.direction["LEFT"]:
            self.direction = gf.direction["RIGHT"]
        elif self.direction is gf.direction["RIGHT"]:
            self.direction = gf.direction["LEFT"]

        temp = self.current_grid_pt
        self.current_grid_pt = self.nxt_grid_pt
        self.nxt_grid_pt = temp

    def portal(self):
        if self.current_grid_pt.portal is not None:
            self.current_grid_pt = self.current_grid_pt.portal
            self.set_position()

    def draw(self):
        if self.appear:
            if self.image is not None:
                position = self.position.asTuple()
                position = (position[0] - self.settings.tile_width / 2, position[1] - self.settings.tile_height / 2)
                self.screen.blit(self.image, position)
            else:
                position = self.position.asInt()
                pg.draw.circle(self.screen, self.color, position, self.settings.radius)
