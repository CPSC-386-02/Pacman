import pygame as pg
from settings import Settings
import game_functions as gf
from character import Pacman
from maze import Grid_Pnts_Group


class Game:
    def __init__(self):
        pg.init()

        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption(self.settings.title)
        # self.screen.fill(self.settings.bg_color)

        self.clock = pg.time.Clock()
        self.grid_pts = Grid_Pnts_Group(settings=self.settings, screen=self.screen)
        self.grid_pts.setupTestNodes()
        self.pacman = Pacman(settings=self.settings, screen=self.screen, grid_pts=self.grid_pts)

        self.play()

    def play(self):
        while True:
            dt = self.clock.tick(30) / 1000.0
            self.pacman.update(dt)
            gf.check_events(pacman=self.pacman)
            gf.update_screen(settings=self.settings, screen=self.screen, pacman=self.pacman, grid_pts=self.grid_pts)



def main():
    Game()


if __name__ == '__main__':
    main()
