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
        self.radius = 10
        self.collide_radius = 5

        self.food_points = 10
        self.food_radius = 5

        self.power_up_points = 20
        self.power_up_radius = 7.5
        self.flash_t = 0.1

        self.ghost_points = 100
        self.ghost_speed = 75
        self.ghost_collide_radius = 5

        self.blinky_color = (255, 0, 0)
        self.pinky_color = (255, 100, 150)
        self.inky_color = (100, 255, 255)
        self.clyde_color = (230, 190, 40)
