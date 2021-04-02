import pygame as pg
from settings import Settings
import game_functions as gf
from character import Pacman, Ghost_Group
from maze import Grid_Pnts_Group, Maze, FoodGroup
from game_stats import GameStats
from scoreboard import Scoreboard


class Game:
    def __init__(self):
        pg.init()

        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption(self.settings.title)
        self.settings.get_sprite_sheet()

        self.clock = pg.time.Clock()
        self.grid_pts = Grid_Pnts_Group(settings=self.settings, screen=self.screen, txt_file="mazetest.txt")
        self.foods = FoodGroup(settings=self.settings, screen=self.screen, food_file="food.txt")
        self.pacman = Pacman(settings=self.settings, screen=self.screen, grid_pts=self.grid_pts, foods=self.foods)
        self.ghosts = Ghost_Group(settings=self.settings, screen=self.screen, grid_pts=self.grid_pts)
        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(settings=self.settings, screen=self.screen, stats=self.stats)
        self.maze = Maze(settings=self.settings, screen=self.screen)
        self.play()

    def play(self):
        while True:
            dt = self.clock.tick(30) / 1000.0
            self.pacman.update(dt=dt, ghosts=self.ghosts, stats=self.stats, sb=self.sb, sound=self.sound)
            self.ghosts.update(dt=dt, pacman=self.pacman)
            self.foods.update(dt=dt)
            self.maze.get_maze()

            gf.check_events()
            gf.update_screen(settings=self.settings, screen=self.screen, pacman=self.pacman, grid_pts=self.grid_pts,
                             foods=self.foods,
                             ghosts=self.ghosts, sb=self.sb, maze=self.maze)



def main():
    Game()


if __name__ == '__main__':
    main()
