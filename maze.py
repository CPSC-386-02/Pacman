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
        self.ghost_home = False
        self.ghost_home_entrance = False
        self.ghost_spawn_pt = False

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

        self.grid_pt_sym = ["+"] + ["1"] + ["H"] + ["S"]

        self.grid_pts_li = []
        self.ghost_home_li = []

        self.stack = Stack()
        self.maze_grid = self.read_file(txt_file)
        self.ghost_home_grid = self.ghost_home()

        self.create_list(settings, screen, self.maze_grid, self.grid_pts_li)
        self.create_list(settings, screen, self.ghost_home_grid, self.ghost_home_li)
        self.create_portal()
        self.go_home()
        self.ghost_home_li[0].ghost_home_entrance = True

    def ghost_home(self):
        return [['0', '0', '+', '0', '0'],
                ['0', '0', '|', '0', '0'],
                ['+', '0', '|', '0', '+'],
                ['+', '-', 'S', '-', '+'],
                ['+', '0', '0', '0', '+']]

    def read_file(self, txt_file):
        f = open(txt_file, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    def create_list(self, settings, screen, grid, grid_pts_li):
        self.stack.push(self.find_first_pt(settings, screen, grid))
        while not self.stack.isEmpty():
            grid_pt = self.stack.pop()
            self.add_to_list(grid_pt, grid_pts_li)

            left_neighbor = self.get_neighbor(settings, screen, gf.direction["LEFT"], grid_pt.row, grid_pt.column - 1,
                                              grid_pts_li, grid)
            right_neighbor = self.get_neighbor(settings, screen, gf.direction["RIGHT"], grid_pt.row, grid_pt.column + 1,
                                               grid_pts_li, grid)
            up_neighbor = self.get_neighbor(settings, screen, gf.direction["UP"], grid_pt.row - 1, grid_pt.column,
                                            grid_pts_li, grid)
            down_neighbor = self.get_neighbor(settings, screen, gf.direction["DOWN"], grid_pt.row + 1, grid_pt.column,
                                              grid_pts_li, grid)

            grid_pt.neighbors[gf.direction["LEFT"]] = left_neighbor
            grid_pt.neighbors[gf.direction["RIGHT"]] = right_neighbor
            grid_pt.neighbors[gf.direction["UP"]] = up_neighbor
            grid_pt.neighbors[gf.direction["DOWN"]] = down_neighbor

            self.add_to_stack(left_neighbor, grid_pts_li)
            self.add_to_stack(right_neighbor, grid_pts_li)
            self.add_to_stack(up_neighbor, grid_pts_li)
            self.add_to_stack(down_neighbor, grid_pts_li)

    def find_first_pt(self, settings, screen, grid):
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] in self.grid_pt_sym:
                    grid_pt = Grid_Pnt(settings, screen, row, col)
                    if grid[row][col] == "1":
                        grid_pt.portal_val = grid[row][col]
                    return grid_pt
        return None

    def get_neighbor(self, settings, screen, direction, row, col, grid_pts_li, grid):
        neighbor = self.follow_path(settings, screen, direction, row, col, grid)
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

    def follow_path(self, settings, screen, direction, row, col, grid):
        rows = len(grid)
        columns = len(grid[0])
        if direction == gf.direction["LEFT"] and col >= 0:
            return self.path_to_follow(settings, screen, gf.direction["LEFT"], row, col, "-", grid)
        elif direction == gf.direction["RIGHT"] and col < columns:
            return self.path_to_follow(settings, screen, gf.direction["RIGHT"], row, col, "-", grid)
        elif direction == gf.direction["UP"] and row >= 0:
            return self.path_to_follow(settings, screen, gf.direction["UP"], row, col, "|", grid)
        elif direction == gf.direction["DOWN"] and row < rows:
            return self.path_to_follow(settings, screen, gf.direction["DOWN"], row, col, "|", grid)
        else:
            return None

    def path_to_follow(self, settings, screen, direction, row, col, path, grid):
        if grid[row][col] == path:
            while grid[row][col] not in self.grid_pt_sym:
                if direction is gf.direction["LEFT"]:
                    col -= 1
                elif direction is gf.direction["RIGHT"]:
                    col += 1
                elif direction is gf.direction["UP"]:
                    row -= 1
                elif direction is gf.direction["DOWN"]:
                    row += 1
            grid_pt = Grid_Pnt(settings, screen, row, col)
            if grid[row][col] == "1":
                grid_pt.portal_val = grid[row][col]
            if grid[row][col] == "H":
                grid_pt.ghost_home = True
            if grid[row][col] == "S":
                grid_pt.ghost_spawn_pt = True
            return grid_pt
        else:
            return None

    def create_portal(self):
        portal_dict = {}
        for i in range(len(self.grid_pts_li)):
            if self.grid_pts_li[i].portal_val != 0:
                if self.grid_pts_li[i].portal_val not in portal_dict.keys():
                    portal_dict[self.grid_pts_li[i].portal_val] = [i]
                else:
                    portal_dict[self.grid_pts_li[i].portal_val] += [i]
        for key in portal_dict.keys():
            portal_1, portal_2 = portal_dict[key]
            self.grid_pts_li[portal_1].portal = self.grid_pts_li[portal_2]
            self.grid_pts_li[portal_2].portal = self.grid_pts_li[portal_1]

    def go_home(self):
        for grid_pt in self.grid_pts_li:
            if grid_pt.ghost_home:
                grid_pt_A = grid_pt
                break
        grid_pt_B = grid_pt_A.neighbors[gf.direction["LEFT"]]
        mid = (grid_pt_A.position + grid_pt_B.position) / 2.0
        mid = Vector(int(mid.x), int(mid.y))
        vec = Vector(self.ghost_home_li[0].position.x, self.ghost_home_li[0].position.y)

        for grid_pt in self.ghost_home_li:
            grid_pt.position -= vec
            grid_pt.position += mid
            for temp in self.grid_pts_li:
                if grid_pt.position.x == temp.position.x and grid_pt.position.y == temp.position.y:
                    break
            self.maze_grid.append(grid_pt)

        A = self.get_grid_pt_from_li(grid_pt_A, self.grid_pts_li)
        B = self.get_grid_pt_from_li(grid_pt_B, self.grid_pts_li)
        H = self.get_grid_pt_from_li(self.ghost_home_li[0], self.grid_pts_li)
        A.neighbors[gf.direction["LEFT"]] = H
        B.neighbors[gf.direction["RIGHT"]] = H
        H.neighbors[gf.direction["RIGHT"]] = A
        H.neighbors[gf.direction["LEFT"]] = B

    def get_grid_pt_from_li(self, grid_pt, li):
        if grid_pt is not None:
            for temp in li:
                if grid_pt.row == temp.row and grid_pt.column == temp.column:
                    return temp
        return grid_pt

    def draw(self):
        for grid_pt in self.grid_pts_li:
            grid_pt.draw()
        for grid_pt in self.ghost_home_li:
            grid_pt.draw()


class Maze:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.sprite_info = None
        self.rotate_info = None
        self.images = []
        self.flash_images = []
        self.image_row = 16

    def get_maze_images(self, row=0):
        self.images = []
        for x in range(11):
            self.images.append(
                self.settings.get_image(x, self.image_row + row, self.settings.tile_width, self.settings.tile_height))

    def rotate(self, image, value):
        return pg.transform.rotate(image, value * 90)

    def read_file(self, txtfile):
        f = open(txtfile, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    def get_maze(self):
        self.sprite_info = self.read_file("maze_sprites.txt")
        self.rotate_info = self.read_file("maze_rotation.txt")

    def create_maze(self, row=0):
        self.get_maze_images(row)
        rows = len(self.sprite_info)
        cols = len(self.sprite_info[0])
        for row in range(rows):
            for col in range(cols):
                x = col * self.settings.tile_width
                y = row * self.settings.tile_height
                val = self.sprite_info[row][col]
                if val.isdecimal():
                    rotVal = self.rotate_info[row][col]
                    image = self.rotate(self.images[int(val)], int(rotVal))
                    self.screen.blit(image, (x, y))
                if val == '=':
                    self.screen.blit(self.images[10], (x, y))


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
            position = (int(position[0] + self.settings.tile_width / 2), int(position[1] + self.settings.tile_width / 2))
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
