from random import randint

import pygame as pg
from vector import Vector
import game_functions as gf
from stack import Stack
from animation import Animation


class Character:
    def __init__(self, settings, screen, grid_pts):
        self.settings = settings
        self.screen = screen
        self.direction = gf.direction["STOP"]

        self.grid_pts = grid_pts
        self.current_grid_pt = grid_pts.grid_pts_li[0]
        self.nxt_grid_pt = self.current_grid_pt
        self.position = self.current_grid_pt.position.copy()
        self.appear = True
        self.color = None
        self.image = None
        self.sprite_sheet = self.settings.sprite_sheet

    def check_nxt_grid_pt(self):
        if self.nxt_grid_pt is not None:
            dist_btw_2_grid_pts = self.nxt_grid_pt.position - self.current_grid_pt.position
            dist_btw_pacman_and_grid_pt = self.position - self.current_grid_pt.position
            return dist_btw_pacman_and_grid_pt.magnitudeSquared() >= dist_btw_2_grid_pts.magnitudeSquared()
        return False

    def reverse_direction(self):
        if self.direction is gf.direction["UP"]:
            self.direction = gf.direction["DOWN"]
        elif self.direction is gf.direction["DOWN"]:
            self.direction = gf.direction["UP"]
        elif self.direction is gf.direction["LEFT"]:
            self.direction = gf.direction["RIGHT"]
        elif self.direction is gf.direction["RIGHT"]:
            self.direction = gf.direction["LEFT"]

        temp = self.current_grid_pt
        self.current_grid_pt = self.nxt_grid_pt
        self.nxt_grid_pt = temp

    def portal(self):
        if self.current_grid_pt.portal is not None:
            self.current_grid_pt = self.current_grid_pt.portal
            self.position = self.current_grid_pt.position.copy()

    def draw(self):
        if self.appear:
            if self.image is not None:
                position = self.position.asTuple()
                position = (position[0] - self.settings.tile_width / 2, position[1] - self.settings.tile_height / 2)
                self.screen.blit(self.image, position)
            else:
                position = self.position.asInt()
                pg.draw.circle(self.screen, self.color, position, self.settings.radius)


class Pacman(Character):
    def __init__(self, settings, screen, grid_pts, foods):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.pacman_color
        self.food_list = foods.food_list
        self.image = self.settings.get_image(4, 0, 32, 32)
        self.animation = None
        self.animations = {}
        Animation.set_up_pacman_animation(self)
        print(self.animations)

    def move_by_key(self, direction):
        if self.direction is gf.direction["STOP"]:
            if self.current_grid_pt.neighbors[direction] is not None:
                self.direction = direction
                self.nxt_grid_pt = self.current_grid_pt.neighbors[direction]
        else:
            if direction == self.direction * -1:
                self.reverse_direction()
            if self.check_nxt_grid_pt():
                self.current_grid_pt = self.nxt_grid_pt
                self.portal()
                if self.current_grid_pt.neighbors[direction] is not None:
                    if self.current_grid_pt.ghost_home_entrance:
                        if self.current_grid_pt.neighbors[self.direction] is not None:
                            self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                        else:
                            self.position = self.current_grid_pt.position.copy()
                            self.direction = gf.direction["STOP"]
                    else:
                        self.nxt_grid_pt = self.current_grid_pt.neighbors[direction]
                        if self.direction != direction:
                            self.position = self.current_grid_pt.position.copy()
                            self.direction = direction
                else:
                    if self.current_grid_pt.neighbors[self.direction] is not None:
                        self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                    else:
                        self.position = self.current_grid_pt.position.copy()
                        self.direction = gf.direction["STOP"]

    def eat_food(self, ghosts, stats, sb):
        for food in self.food_list:
            dist = (self.position - food.position).magnitudeSquared()
            radius = (food.radius + self.settings.collide_radius) ** 2
            if dist <= radius:
                self.food_list.remove(food)
                if food.name == "power up":
                    ghosts.running_away_mode()
                    stats.score += self.settings.power_up_points
                    sb.prep_score()
                else:
                    stats.score += self.settings.food_points
                    sb.prep_score()
                    return True

        return False

    def eat_ghost(self, ghosts, stats, sb):
        for ghost in ghosts:
            dist = (self.position - ghost.position).magnitudeSquared()
            radius = (self.settings.ghost_collide_radius + self.settings.collide_radius) ** 2
            if dist <= radius:
                if ghost is not None:
                    if ghost.mode.name == "RUN":
                        ghost.spawn_mode(2)
                        stats.score += self.settings.ghost_points
                        sb.prep_score()

    def run_animation(self, dt):
        if self.direction == gf.direction["UP"]:
            self.animation = self.animations["up"]
        elif self.direction == gf.direction["DOWN"]:
            self.animation = self.animations["down"]
        elif self.direction == gf.direction["LEFT"]:
            self.animation = self.animations["left"]
        elif self.direction == gf.direction["RIGHT"]:
            self.animation = self.animations["right"]
        elif self.direction == gf.direction["STOP"]:
            self.animation = self.animations["idle"]
        self.image = self.animation.update(dt)

    def update(self, dt, ghosts, stats, sb, sound):
        self.position += self.direction * self.settings.character_speed * dt
        self.run_animation(dt)
        direction = gf.check_key_down_event()
        if direction:
            self.move_by_key(direction)
        else:
            if self.direction is not gf.direction["STOP"]:
                if self.check_nxt_grid_pt():
                    self.current_grid_pt = self.nxt_grid_pt
                    self.portal()
                    if self.current_grid_pt.neighbors[self.direction] is not None:
                        self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                    else:
                        self.position = self.current_grid_pt.position.copy()
                        self.direction = gf.direction["STOP"]
        if self.eat_food(ghosts, stats, sb):
            sound.eat_food()
        # else:
        #     sound.stop_eating()
        self.eat_ghost(ghosts, stats, sb)


class Ghost(Character):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.goal = Vector()
        self.mode_stack = self.setup_modes()
        self.mode = self.mode_stack.pop()
        self.mode_timer = 0
        self.spawn_pt = self.find_spawn_pt()
        self.animation = None
        self.animations = {}

    def directions(self):
        directions = []
        for key in self.current_grid_pt.neighbors.keys():
            if self.current_grid_pt.neighbors[key] is not None:
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.back_track())
        return directions

    def closest_direction(self, directions):
        distances = []
        for direction in directions:
            diff_vec = self.current_grid_pt.position + direction * self.settings.tile_width - self.goal
            distances.append(diff_vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

    def randomize_direction(self, directions):
        print(directions)
        index = randint(0, len(directions) - 1)
        return directions[index]

    def back_track(self):
        if self.direction * -1 == gf.direction["UP"]:
            return gf.direction["UP"]
        if self.direction * -1 == gf.direction["DOWN"]:
            return gf.direction["DOWN"]
        if self.direction * -1 == gf.direction["LEFT"]:
            return gf.direction["LEFT"]
        if self.direction * -1 == gf.direction["RIGHT"]:
            return gf.direction["RIGHT"]

    def running_away_mode(self):
        if self.mode.name != "SPAWN":
            if self.mode.name != "RUN":
                if self.mode.time is not None:
                    dt = self.mode.time - self.mode_timer
                    self.mode_stack.push(Mode(self.mode.name, dt))
                else:
                    self.mode_stack.push(Mode(self.mode.name))
                self.mode = Mode("RUN", 7, 0.5)
                self.mode_timer = 0
            else:
                self.mode = Mode("RUN", 7, 0.5)
                self.mode_timer = 0
            self.reverse_direction()

    def spawn_mode(self, speed_up_scale):
        self.mode = Mode("SPAWN", None, speed_up_scale)
        self.mode_timer = 0

    def find_spawn_pt(self):
        for grid_pt in self.grid_pts.ghost_home_li:
            if grid_pt.ghost_spawn_pt:
                break
        return grid_pt

    def spawn_goal(self):
        self.goal = self.spawn_pt.position

    def random_goal(self):
        x = randint(0, self.settings.screen_width)
        y = randint(0, self.settings.screen_height)
        self.goal = Vector(x, y)

    def setup_modes(self):
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER", time=5))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        return modes

    def scatter_goal(self):
        self.goal = Vector((self.settings.screen_width, self.settings.screen_height)[0], 0)

    def chase_goal(self, pacman, blinky=None):
        self.goal = pacman.position

    def mode_update(self, dt):
        self.mode_timer += dt
        if self.mode.time is not None:
            if self.mode_timer >= self.mode.time:
                self.reverse_direction()
                self.mode = self.mode_stack.pop()
                self.mode_timer = 0

    # def portalSlowdown(self):
    #     self.speed = 100
    #     if self.current_grid_pt.portal or self.nxt_grid_pt.portal:
    #         self.speed = 50

    # def update(self, dt):
    #     self.position += self.direction * self.settings.ghost_speed * dt
    #     if self.check_nxt_grid_pt():
    #         self.current_grid_pt = self.nxt_grid_pt
    #         self.portal()
    #         directions = self.directions()
    #         self.direction = self.getClosestDirection(directions)
    #         self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
    #         self.position = self.current_grid_pt.position.copy()

    def run_animation(self, dt):
        if self.mode.name == "SPAWN":
            if self.direction == gf.direction["UP"]:
                self.animation = self.animations["spawn_up"]
            elif self.direction == gf.direction["DOWN"]:
                self.animation = self.animations["spawn_down"]
            elif self.direction == gf.direction["LEFT"]:
                self.animation = self.animations["spawn_left"]
            elif self.direction == gf.direction["RIGHT"]:
                self.animation = self.animations["spawn_right"]

        if self.mode.name in ["CHASE", "SCATTER"]:
            if self.direction == gf.direction["UP"]:
                self.animation = self.animations["up"]
            elif self.direction == gf.direction["DOWN"]:
                self.animation = self.animations["down"]
            elif self.direction == gf.direction["LEFT"]:
                self.animation = self.animations["left"]
            elif self.direction == gf.direction["RIGHT"]:
                self.animation = self.animations["right"]

        if self.mode.name == "RUN":
            if self.mode_timer >= (self.mode.time * 0.7):
                self.animation = self.animations["flash"]
            else:
                self.animation = self.animations["run"]
        self.image = self.animation.update(dt)

    def update(self, dt, pacman, blinky=None):
        self.appear = True
        self.position += self.direction * self.settings.ghost_speed * self.mode.speed_up_scale * dt
        self.mode_update(dt)
        if self.mode.name == "CHASE":
            self.chase_goal(pacman, blinky)
        elif self.mode.name == "SCATTER":
            self.scatter_goal()
        elif self.mode.name == "RUN":
            self.random_goal()
        elif self.mode.name == "SPAWN":
            self.spawn_goal()
        if self.check_nxt_grid_pt():
            self.current_grid_pt = self.nxt_grid_pt
            self.portal()
            directions = self.directions()
            self.direction = self.closest_direction(directions)
            self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
            self.position = self.current_grid_pt.position.copy()
            if self.mode.name == "SPAWN":
                if self.position == self.goal:
                    self.mode = self.mode_stack.pop()
        self.run_animation(dt)


class Mode:
    def __init__(self, name="", time=None, speed_up_scale=1.0, direction=None):
        self.name = name
        self.time = time
        self.speed_up_scale = speed_up_scale
        self.direction = direction


class Blinky(Ghost):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.blinky_color
        self.image = self.settings.get_image(4,2,32,32)
        Animation.set_up_ghost_animation(self, 2)
        self.animation = self.animations["up"]


class Pinky(Ghost):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.pinky_color
        self.image = self.settings.get_image(0, 3, 32, 32)
        Animation.set_up_ghost_animation(self, 3)
        self.animation = self.animations["left"]

    def scatter_goal(self):
        self.goal = Vector()

    def chase_goal(self, pacman, blinky=None):
        self.goal = pacman.position + pacman.direction * self.settings.tile_width * 4


class Inky(Ghost):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.inky_color
        self.image = self.settings.get_image(2, 4, 32, 32)
        Animation.set_up_ghost_animation(self, 4)
        self.animation = self.animations["down"]

    def scatter_goal(self):
        self.goal = Vector(self.settings.screen_width, self.settings.screen_height)

    def chase_goal(self, pacman, blinky=None):
        vec = pacman.position + pacman.direction * self.settings.tile_width * 4 * 2
        self.goal = blinky.position + (vec - blinky.position) * 2


class Clyde(Ghost):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.clyde_color
        self.image = self.settings.get_image(2, 5, 32, 32)
        Animation.set_up_ghost_animation(self, 5)
        self.animation = self.animations["down"]

    def scatter_goal(self):
        self.goal = Vector(0, self.settings.screen_height)

    def chase_goal(self, pacman, blinky=None):
        dist = (pacman.position - self.position).magnitudeSquared()
        if dist <= (self.settings.tile_width * 8) ** 2:
            self.scatter_goal()
        else:
            self.goal = pacman.position + pacman.direction * self.settings.tile_width * 4


class Ghost_Group:
    def __init__(self, settings, screen, grid_pts):
        self.settings = settings
        self.screen = screen
        self.grid_pts = grid_pts
        self.ghosts = [Blinky(self.settings, self.screen, grid_pts), Pinky(self.settings, self.screen, grid_pts),
                       Inky(self.settings, self.screen, grid_pts), Clyde(self.settings, self.screen, grid_pts)]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt, pacman):
        for ghost in self:
            ghost.update(dt, pacman, self.ghosts[0])

    def running_away_mode(self):
        for ghost in self:
            ghost.running_away_mode()

    # def update_points(self):
    #     for ghost in self:
    #         ghost.points *= 2
    #
    # def resetPoints(self):
    #     for ghost in self:
    #         ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.appear = False

    def draw(self):
        for ghost in self:
            ghost.draw()
