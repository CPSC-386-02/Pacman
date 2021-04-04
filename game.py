import pygame as pg
from settings import Settings
import game_functions as gf
from pacman import Pacman
from ghost import Ghost_Group
from maze import Grid_Pnts_Group, Maze
from food import FoodGroup
from pauser import Pauser
from levels import LevelController
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from score_button import ScoreButton
from sound import Sound


class Game:
    def __init__(self):
        pg.init()

        self.settings = Settings()

        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption(self.settings.title)
        self.settings.get_sprite_sheet()
        # self.screen.fill(self.settings.bg_color)

        self.clock = pg.time.Clock()
        self.pellets_eaten = 0
        self.fruit = None
        self.pause = Pauser(True)
        self.level = LevelController()

        # Text to show the game title
        self.game_title_font = pg.font.SysFont("inkfree", 60)
        self.game_title = self.game_title_font.render("PAC-MAN", True, (253, 254, 0))

        # Pacman and ghosts images for start screen
        self.pacman_img = self.settings.get_image(0, 1, 32, 32)
        self.pacman_img = pg.transform.scale(self.pacman_img, (100, 100))

        self.ghost_one = self.settings.get_image(2, 2, 32, 32)
        self.ghost_one = pg.transform.scale(self.ghost_one, (100, 100))
        self.ghost_two = self.settings.get_image(0, 3, 32, 32)
        self.ghost_two = pg.transform.scale(self.ghost_two, (100, 100))
        self.ghost_three = self.settings.get_image(4, 4, 32, 32)
        self.ghost_three = pg.transform.scale(self.ghost_three, (100, 100))
        self.ghost_four = self.settings.get_image(6, 5, 32, 32)
        self.ghost_four = pg.transform.scale(self.ghost_four, (100, 100))

        self.start_game()
        self.play()

    def start_game(self):
        self.level.reset()
        level_map = self.level.get_level()
        self.game_over = False
        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(settings=self.settings, screen=self.screen, stats=self.stats)
        self.sound = Sound()
        self.maze = Maze(settings=self.settings, screen=self.screen)
        self.maze.get_maze()
        self.grid_pts = Grid_Pnts_Group(settings=self.settings, screen=self.screen, txt_file=level_map["mazename"])
        self.foods = FoodGroup(settings=self.settings, screen=self.screen, food_file=level_map["foodname"])
        self.pacman = Pacman(game=self,settings=self.settings, screen=self.screen, grid_pts=self.grid_pts, foods=self.foods, sb=self.sb)
        self.ghosts = Ghost_Group(game=self, settings=self.settings, screen=self.screen, grid_pts=self.grid_pts)
        self.pellets_eaten = 0
        self.settings.pacman_lives = self.settings.starting_lives
        self.fruit = None
        self.pause.force(True)

    def start_level(self):
        level_map = self.level.get_level()
        self.screen.fill(self.settings.bg_color)
        self.grid_pts = Grid_Pnts_Group(settings=self.settings, screen=self.screen, txt_file=level_map["mazename"])
        self.foods = FoodGroup(settings=self.settings, screen=self.screen, food_file=level_map["foodname"])
        self.pacman.grid_pts.grid_pts_li = self.grid_pts.grid_pts_li
        self.pacman.grid_pts = self.grid_pts
        self.pacman.food_list = self.foods.food_list
        self.pacman.reset()
        self.ghosts = Ghost_Group(game=self, settings=self.settings, screen=self.screen, grid_pts=self.grid_pts)
        self.pellets_eaten = 0
        self.sb.score_int = 0
        self.fruit = None
        self.pause.force(True)

    def restart_level(self):
        self.pacman.reset()
        self.ghosts = Ghost_Group(game=self, settings=self.settings, screen=self.screen, grid_pts=self.grid_pts)
        self.fruit = None

    def play(self):
        self.screen.fill((0, 0, 0))
        self.play_button = Button(self.screen, "Play")
        self.score_button = ScoreButton(self.screen, "High Score")
        while True:
            if self.settings.game_active:
                if not self.game_over:
                    dt = self.clock.tick(30) / 1000.0
                    if not self.pause.paused:
                        self.sound.unpause_bg()
                        self.ghosts.update(dt=dt, pacman=self.pacman)
                        self.pacman.update(dt=dt, ghosts=self.ghosts, stats=self.stats, sb=self.sb, sound=self.sound)
                        if self.fruit is not None:
                            self.fruit.update(dt=dt)
                        if self.pause.pause_type != None:
                            self.pause.settle_pause(self)
                        self.foods.update(dt=dt)
                    self.pause.update(dt)
            else:
                self.screen.blit(self.game_title, (100, 20))
                self.screen.blit(self.pacman_img, (175, 200))
                self.screen.blit(self.ghost_one, (175, 80))
                self.screen.blit(self.ghost_two, (175, 320))
                self.screen.blit(self.ghost_three, (300, 200))
                self.screen.blit(self.ghost_four, (50, 200))
            gf.check_events(game=self)
            gf.update_screen(game=self)

    def pacman_died(self):
        if self.settings.pacman_lives == 0:
            self.screen.fill((0, 0, 0))
            self.game_over = True
            self.settings.game_active = False
        else:
            self.restart_level()
        self.sound.pause_bg()
        self.sound.pacman_die()
        self.pause.pause_type = None

    def beat_level(self):
        self.level.next_level()
        self.start_level()
        self.pause.pause_type = None


def main():
    Game()


if __name__ == '__main__':
    main()
