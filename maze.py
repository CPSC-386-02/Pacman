import pygame as pg
from vector import Vector
import game_functions as gf
from stack import Stack


class Grid_Pnt:
    def __init__(self, settings, screen, row, column):
        self.settings = settings
        self.screen = screen
        self.row, self.column = row, column
        self.position = Vector(column * self.settings.tile_width, row * self.settings.tile_height)
        self.neighbors = {gf.direction["UP"]: None, gf.direction["DOWN"]: None,
                          gf.direction["LEFT"]: None, gf.direction["RIGHT"]: None}
        self.portal = None
        self.portal_val = 0

    def draw(self):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pg.draw.line(self.screen, (255, 255, 255), line_start, line_end, 4)
                pg.draw.circle(self.screen, (255, 0, 0), self.position.asInt(), 12)


class Grid_Pnts_Group:
    def __init__(self, settings, screen, txt_file):
        self.settings = settings
        self.screen = screen
        self.portal_sym = ["1"]
        self.grid_pt_sym = ["+"]+ ["1"]
        self.grid_pts_li = []
        self.stack = Stack()
        self.create_list(settings, screen, txt_file, self.grid_pts_li)
        self.create_portal()

    def read_file(self, txt_file):
        f = open(txt_file, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    def create_list(self, settings, screen, txt_file, grid_pts_li):
        self.grid = self.read_file(txt_file)
        self.stack.push(self.find_first_pt(settings, screen, len(self.grid), len(self.grid[0])))
        while not self.stack.isEmpty():
            grid_pt = self.stack.pop()
            self.add_to_list(grid_pt, grid_pts_li)

            left_neighbor = self.get_neighbor(settings, screen, gf.direction["LEFT"], grid_pt.row, grid_pt.column - 1, grid_pts_li)
            right_neighbor = self.get_neighbor(settings, screen, gf.direction["RIGHT"], grid_pt.row, grid_pt.column + 1, grid_pts_li)
            up_neighbor = self.get_neighbor(settings, screen, gf.direction["UP"], grid_pt.row - 1, grid_pt.column, grid_pts_li)
            down_neighbor = self.get_neighbor(settings, screen, gf.direction["DOWN"], grid_pt.row + 1, grid_pt.column, grid_pts_li)

            grid_pt.neighbors[gf.direction["LEFT"]] = left_neighbor
            grid_pt.neighbors[gf.direction["RIGHT"]] = right_neighbor
            grid_pt.neighbors[gf.direction["UP"]] = up_neighbor
            grid_pt.neighbors[gf.direction["DOWN"]] = down_neighbor

            self.add_to_stack(left_neighbor, grid_pts_li)
            self.add_to_stack(right_neighbor, grid_pts_li)
            self.add_to_stack(up_neighbor, grid_pts_li)
            self.add_to_stack(down_neighbor, grid_pts_li)

    def find_first_pt(self, settings, screen, rows, cols):
        for row in range(rows):
            for col in range(cols):
                if self.grid[row][col] in self.grid_pt_sym:
                    grid_pt = Grid_Pnt(settings, screen, row, col)
                    if self.grid[row][col] in self.portal_sym:
                        grid_pt.portal_val = self.grid[row][col]
                    return grid_pt
        return None

    def get_neighbor(self, settings, screen, direction, row, col, grid_pts_li):
        neighbor = self.follow_path(settings, screen, direction, row, col)
        if neighbor is not None:
            for pt in grid_pts_li:
                if neighbor.position.x == pt.position.x and neighbor.position.y == pt.position.y:
                    return pt
        return neighbor

    def add_to_list(self, grid_pt, grid_pts_li):
        if not self.check_list(grid_pt, grid_pts_li):
            grid_pts_li.append(grid_pt)

    def add_to_stack(self, grid_pt, grid_pts_li):
        if grid_pt is not None and not self.check_list(grid_pt, grid_pts_li):
            self.stack.push(grid_pt)

    def check_list(self, grid_pt, grid_pts_li):
        for pt in grid_pts_li:
            if grid_pt.position.x == pt.position.x and grid_pt.position.y == pt.position.y:
                return True
        return False

    def follow_path(self, settings, screen, direction, row, col):
        rows = len(self.grid)
        columns = len(self.grid[0])
        if direction == gf.direction["LEFT"] and col >= 0:
            return self.path_to_follow(settings, screen, gf.direction["LEFT"], row, col, "-")
        elif direction == gf.direction["RIGHT"] and col < columns:
            return self.path_to_follow(settings, screen, gf.direction["RIGHT"], row, col, "-")
        elif direction == gf.direction["UP"] and row >= 0:
            return self.path_to_follow(settings, screen, gf.direction["UP"], row, col, "|")
        elif direction == gf.direction["DOWN"] and row < rows:
            return self.path_to_follow(settings, screen, gf.direction["DOWN"], row, col, "|")
        else:
            return None

    def path_to_follow(self, settings, screen, direction, row, col, path):
        if self.grid[row][col] == path:
            while self.grid[row][col] not in self.grid_pt_sym:
                if direction is gf.direction["LEFT"]:   col -= 1
                elif direction is gf.direction["RIGHT"]:    col += 1
                elif direction is gf.direction["UP"]:   row -= 1
                elif direction is gf.direction["DOWN"]: row += 1
            grid_pt = Grid_Pnt(settings, screen, row, col)
            if self.grid[row][col] in self.portal_sym:
                grid_pt.portal_val = self.grid[row][col]
            return grid_pt
        else:
            return None

    def create_portal(self):
        portalDict = {}
        for i in range(len(self.grid_pts_li)):
            if self.grid_pts_li[i].portal_val != 0:
                if self.grid_pts_li[i].portal_val not in portalDict.keys():
                    portalDict[self.grid_pts_li[i].portal_val] = [i]
                else:
                    portalDict[self.grid_pts_li[i].portal_val] += [i]
        for key in portalDict.keys():
            node1, node2 = portalDict[key]
            self.grid_pts_li[node1].portal = self.grid_pts_li[node2]
            self.grid_pts_li[node2].portal = self.grid_pts_li[node1]

    def draw(self):
        for grid_pt in self.grid_pts_li:
            grid_pt.draw()


class Food:
    def __init__(self, settings, screen, x, y):
        self.settings = settings
        self.screen = screen
        self.position = Vector(x, y)
        self.appear = True
        self.radius = self.settings.food_radius

    def draw(self):
        if self.appear:
            pg.draw.circle(self.screen, (255, 255, 255), self.position.asInt(),  self.radius)


class PowerUp(Food):
    def __init__(self, settings, screen, x, y):
        super(PowerUp, self).__init__(settings, screen, x, y)
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
                    self.food_list.append(Food(self.settings, self.screen, col * self.settings.tile_width, row * self.settings.tile_height))
                elif grid[row][col] == 'P':
                    food = PowerUp(self.settings, self.screen, col * self.settings.tile_width, row * self.settings.tile_height)
                    self.food_list.append(food)
                    self.power_up_list.append(food)

    def update(self, dt):
        for power_up in self.power_up_list:
            power_up.update(dt)

    def draw(self):
        for food in self.food_list:
            food.draw()
