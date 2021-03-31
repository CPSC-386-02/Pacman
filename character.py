import pygame as pg
from vector import Vector
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
            self.position = self.current_grid_pt.position.copy()

    def update(self, dt):
        self.position += self.direction * self.settings.character_speed * dt
        if self.direction is not gf.direction["STOP"]:
            if self.check_nxt_grid_pt():
                self.current_grid_pt = self.nxt_grid_pt
                self.portal()
                if self.current_grid_pt.neighbors[self.direction] is not None:
                    self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                else:
                    self.position = self.current_grid_pt.position.copy()
                    self.direction = gf.direction["STOP"]

    def draw(self):
        if self.appear:
            position = self.position.asInt()
            pg.draw.circle(self.screen, self.settings.pacman_color, position, self.settings.radius)


class Pacman(Character):
    def __init__(self, settings, screen, grid_pts, foods):
        super().__init__(settings, screen, grid_pts)
        self.settings = settings
        self.screen = screen
        self.direction = gf.direction["STOP"]

        self.grid_pts = grid_pts
        self.current_grid_pt = grid_pts.grid_pts_li[0]
        self.nxt_grid_pt = self.current_grid_pt
        self.position = self.current_grid_pt.position.copy()

        self.food_list = foods.food_list

    def move_by_key(self, direction):
        if self.direction is gf.direction["STOP"]:
            if self.current_grid_pt.neighbors[direction] is not None:
                self.direction = direction
                self.nxt_grid_pt = self.current_grid_pt.neighbors[direction]
        else:
            if direction == self.direction * -1:
                self.reverse_direction()
            if self.check_nxt_grid_pt():
                self.current_grid_pt = self.nxt_grid_pt
                self.portal()
                if self.current_grid_pt.neighbors[direction] is not None:
                    self.nxt_grid_pt = self.current_grid_pt.neighbors[direction]
                    if self.direction != direction:
                        self.position = self.current_grid_pt.position.copy()
                        self.direction = direction
                else:
                    if self.current_grid_pt.neighbors[self.direction] is not None:
                        self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                    else:
                        self.position = self.current_grid_pt.position.copy()
                        self.direction = gf.direction["STOP"]

    def eat(self):
        for food in self.food_list:
            dist = (self.position - food.position).magnitudeSquared()
            radius = (food.radius + self.settings.collide_radius) ** 2
            if dist <= radius:
                self.food_list.remove(food)
        return None

    def update(self, dt):
        self.position += self.direction * self.settings.character_speed * dt
        direction = gf.check_key_down_event()
        if direction:
            self.move_by_key(direction)
        else:
            if self.direction is not gf.direction["STOP"]:
                if self.check_nxt_grid_pt():
                    self.current_grid_pt = self.nxt_grid_pt
                    self.portal()
                    if self.current_grid_pt.neighbors[self.direction] is not None:
                        self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                    else:
                        self.position = self.current_grid_pt.position.copy()
                        self.direction = gf.direction["STOP"]
        self.eat()

    def draw(self):
        p = self.position.asInt()
        pg.draw.circle(self.screen, self.settings.pacman_color, p, self.settings.radius)

