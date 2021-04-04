from random import randint
from stack import Stack
from character import Character
from animation import Animation
from vector import Vector
import game_functions as gf


class Ghost(Character):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.goal = Vector()
        self.mode_stack = self.setup_modes()
        self.mode = self.mode_stack.pop()
        self.mode_timer = 0
        self.spawn_pt = self.find_spawn_pt()
        self.set_guide_stack()
        self.pellets_for_release = 0
        self.released = True
        self.banned_directions = []
        self.animation = None
        self.animations = {}

    def set_start_position(self):
        self.current_grid_pt = self.find_start_pt()
        self.nxt_grid_pt = self.current_grid_pt
        self.set_position()

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

    def directions(self):
        directions = []
        for key in self.current_grid_pt.neighbors.keys():
            if self.current_grid_pt.neighbors[key] is not None:
                if key != self.direction * -1:
                    if not self.mode.name == "SPAWN":
                        if not self.current_grid_pt.ghost_home_entrance:
                            if key not in self.banned_directions:
                                directions.append(key)
                        else:
                            if key != gf.direction["DOWN"]:
                                directions.append(key)
                    else:
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
        if self.mode.name != "SPAWN" and self.mode.name != "GUIDE":
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
        for d in self.guide:
            self.mode_stack.push(Mode("GUIDE", speed_up_scale=0.5, direction=d))

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

    def set_guide_stack(self):
        self.guide = [gf.direction["UP"]]

    def reverse_direction(self):
        if self.mode.name != "GUIDE" and self.mode.name != "SPAWN":
            Character.reverse_direction(self)

    def update(self, dt, pacman, blinky=None, pellets_eaten=0):
        self.appear = True
        speedMod = self.settings.ghost_speed * self.mode.speed_up_scale
        self.position += self.direction * speedMod * dt
        self.mode_update(dt)
        self.run_animation(dt)
        if not self.released:
            if pellets_eaten >= self.pellets_for_release:
                self.banned_directions = []
                self.spawn_mode(2)
                self.released = True

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

                    self.direction = self.mode.direction
                    self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                    self.set_position()
            elif self.mode.name == "GUIDE":
                self.mode = self.mode_stack.pop()
                if self.mode.name == "GUIDE":
                    self.direction = self.mode.direction
                    self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
                    self.set_position()


class Mode:
    def __init__(self, name="", time=None, speed_up_scale=1, direction=None):
        self.name = name
        self.time = time
        self.speed_up_scale = speed_up_scale
        self.direction = direction

    def __str__(self):
        return self.name + ' - ' + str(self.time) + ' - ' + str(self.speed_up_scale) + ' - ' + str(self.direction)


class Blinky(Ghost):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.blinky_color
        self.image = self.settings.get_image(4, 2, 32, 32)
        Animation.set_up_ghost_animation(self, self.settings, 2)
        self.animation = self.animations["up"]
        self.set_start_position()

    def find_start_pt(self):
        for point in self.grid_pts.ghost_home_li:
            if point.blinky_start_pt:
                return point
        return None


class Pinky(Ghost):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.pinky_color
        self.image = self.settings.get_image(0, 3, 32, 32)
        Animation.set_up_ghost_animation(self, self.settings, 3)
        self.animation = self.animations["left"]
        self.set_start_position()

    def find_start_pt(self):
        for point in self.grid_pts.ghost_home_li:
            if point.pinky_start_pt:
                return point
        return None

    def scatter_goal(self):
        self.goal = Vector()

    def chase_goal(self, pacman, blinky=None):
        self.goal = pacman.position + pacman.direction * self.settings.tile_width * 4


class Inky(Ghost):
    def __init__(self, settings, screen, grid_pts):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.inky_color
        self.image = self.settings.get_image(2, 4, 32, 32)
        Animation.set_up_ghost_animation(self, self.settings, 4)
        self.animation = self.animations["down"]
        self.set_start_position()
        self.pellets_for_release = 30
        self.released = False
        self.banned_directions = [gf.direction["UP"]]
        self.spawn_pt = self.current_grid_pt

    def set_guide_stack(self):
        self.guide = [gf.direction["UP"], gf.direction["RIGHT"]]

    def find_start_pt(self):
        for point in self.grid_pts.ghost_home_li:
            if point.inky_start_pt:
                return point
        return None

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
        Animation.set_up_ghost_animation(self, self.settings, 5)
        self.animation = self.animations["down"]
        self.set_start_position()
        self.pellets_for_release = 60
        self.released = False
        self.banned_directions = [gf.direction["UP"]]
        self.spawn_pt = self.current_grid_pt

    def set_guide_stack(self):
        self.guide = [gf.direction["UP"], gf.direction["LEFT"]]

    def find_start_pt(self):
        for point in self.grid_pts.ghost_home_li:
            if point.clyde_start_pt:
                return point
        return None

    def scatter_goal(self):
        self.goal = Vector(0, self.settings.screen_height)

    def chase_goal(self, pacman, blinky=None):
        dist = (pacman.position - self.position).magnitudeSquared()
        if dist <= (self.settings.tile_width * 8) ** 2:
            self.scatter_goal()
        else:
            self.goal = pacman.position + pacman.direction * self.settings.tile_width * 4


class Ghost_Group():
    def __init__(self, game, settings, screen, grid_pts):
        self.settings = settings
        self.screen = screen
        self.grid_pts = grid_pts
        self.ghosts = [Blinky(self.settings, self.screen, grid_pts), Pinky(self.settings, self.screen, grid_pts),
                       Inky(self.settings, self.screen, grid_pts), Clyde(self.settings, self.screen, grid_pts)]
        self.game = game

    def __iter__(self):
        return iter(self.ghosts)

    def release(self, num_pellets_eaten):
        for ghost in self:
            if not ghost.released:
                if num_pellets_eaten >= ghost.pellets_for_release:
                    ghost.banned_directions = []
                    ghost.spawn_mode(2)
                    ghost.released = True

    def update(self, dt, pacman):
        for ghost in self:
            ghost.update(dt, pacman, self.ghosts[0], self.game.pellets_eaten)

    def running_away_mode(self):
        self.settings.ghost_eaten_counter = 0
        for ghost in self:
            ghost.running_away_mode()

    def hide(self):
        for ghost in self:
            ghost.appear = False

    def draw(self):
        for ghost in self:
            ghost.draw()
