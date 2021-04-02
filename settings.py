import pygame as pg


class Settings:
    def __init__(self):
        self.tile_width = 16
        self.tile_height = 16
        self.rows = 36
        self.cols = 28
        self.screen_width = self.cols * self.tile_width
        self.screen_height = self.rows * self.tile_height
        self.bg_color = (0, 0, 0)
        self.title = "Pacman"

        self.character_speed = 100
        self.pacman_color = (255, 255, 0)
        self.pacman_lives = 3
        self.radius = 5
        self.collide_radius = 5

        self.food_points = 10
        self.food_radius = 2

        self.power_up_points = 20
        self.power_up_radius = 5
        self.flash_t = 0.1

        self.ghost_points = 100
        self.ghost_speed = 75
        self.ghost_collide_radius = 5

        self.blinky_color = (255, 0, 0)
        self.pinky_color = (255, 100, 150)
        self.inky_color = (100, 255, 255)
        self.clyde_color = (230, 190, 40)

    def get_sprite_sheet(self):
        self.sprite_sheet = pg.image.load("spritesheet.png").convert()
        self.sprite_sheet.set_colorkey((255, 0, 255))

    def get_image(self, x, y, width, height):
        x *= width
        y *= height
        self.sprite_sheet.set_clip(pg.Rect(x, y, width, height))
        return self.sprite_sheet.subsurface(self.sprite_sheet.get_clip())
