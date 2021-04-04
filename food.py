from vector import Vector
import pygame as pg

class Food:
    def __init__(self, settings, screen, x, y):
        self.name = "food"
        self.settings = settings
        self.screen = screen
        self.position = Vector(x, y)
        self.appear = True
        self.radius = self.settings.food_radius

    def draw(self):
        if self.appear:
            position = self.position.asInt()
            position = (
                int(position[0] + self.settings.tile_width / 2), int(position[1] + self.settings.tile_width / 2))
            pg.draw.circle(self.screen, (255, 255, 255), position, self.radius)


class PowerUp(Food):
    def __init__(self, settings, screen, x, y):
        super().__init__(settings, screen, x, y)
        self.name = "power up"
        self.timer = 0
        self.radius = self.settings.power_up_radius

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.settings.flash_t:
            self.appear = not self.appear
            self.timer = 0


class FoodGroup:
    def __init__(self, screen, settings, food_file):
        self.screen = screen
        self.settings = settings
        self.food_list = []
        self.power_up_list = []
        self.create_food_list(food_file)

    def read_file(self, food_file):
        f = open(food_file, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    def create_food_list(self, food_file):
        grid = self.read_file(food_file)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 'p':
                    self.food_list.append(Food(self.settings, self.screen, col * self.settings.tile_width,
                                               row * self.settings.tile_height))
                elif grid[row][col] == 'P':
                    food = PowerUp(self.settings, self.screen, col * self.settings.tile_width,
                                   row * self.settings.tile_height)
                    self.food_list.append(food)
                    self.power_up_list.append(food)

    def update(self, dt):
        for power_up in self.power_up_list:
            power_up.update(dt)

    def draw(self):
        for food in self.food_list:
            food.draw()