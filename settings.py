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
