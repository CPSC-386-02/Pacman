from character import Character
import game_functions as gf


class Fruit(Character):
    def __init__(self, settings, screen, grid_pts):
        Character.__init__(self, settings, screen, grid_pts)
        self.settings = settings
        self.name = "fruit"
        self.set_start_position()
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.image = self.settings.get_image(8, 2, 32, 32)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True

    def set_start_position(self):
        self.current_grid_pt = self.find_start_pt()
        self.nxt_grid_pt = self.current_grid_pt.neighbors[gf.direction["LEFT"]]
        self.set_position()
        self.current_grid_pt.position.x -= (self.current_grid_pt.position.x - self.current_grid_pt.position.x) / 2

    def find_start_pt(self):
        for point in self.grid_pts.grid_pts_li:
            if point.fruit_start_pt:
                return point
        return None
