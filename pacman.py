from character import Character
from animation import Animation
import game_functions as gf
from fruit import Fruit

class Pacman(Character):
    def __init__(self, game, settings, screen, grid_pts, foods, sb):
        super().__init__(settings, screen, grid_pts)
        self.color = self.settings.pacman_color
        self.food_list = foods.food_list
        self.set_start_position()
        self.game = game
        self.sb = sb
        self.image = self.settings.get_image(4, 0, 32, 32)
        self.animation = None
        self.animations = {}
        Animation.set_up_pacman_animation(self, self.settings)

    def find_start_pt(self):
        for point in self.grid_pts.grid_pts_li:
            if point.pacman_start_pt:
                return point
        return None

    def set_start_position(self):
        self.direction = gf.direction["LEFT"]
        self.current_grid_pt = self.find_start_pt()
        self.nxt_grid_pt = self.current_grid_pt.neighbors[self.direction]
        # self.set_position()
        self.current_grid_pt.position.x -= (self.current_grid_pt.position.x - self.current_grid_pt.position.x) / 2
        self.set_position()

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

    def eat_food(self, ghosts, stats, sound):
        for food in self.food_list:
            dist = (self.position - food.position).magnitudeSquared()
            radius = (food.radius + self.settings.collide_radius) ** 2
            if dist <= radius:
                self.game.pellets_eaten += 1
                if self.game.pellets_eaten == 35 or self.game.pellets_eaten == 140:
                    if self.game.fruit is None:
                        self.game.fruit = Fruit(self.settings, self.screen, self.grid_pts)
                self.food_list.remove(food)
                if food.name == "power up":
                    stats.score += self.settings.power_up_points
                    sound.eat_power_up()
                    ghosts.running_away_mode()
                else:
                    sound.eat_food()
                    stats.score += self.settings.food_points
                self.sb.prep_score()
                if len(self.food_list) == 0:
                    self.appear = False
                    self.settings.ghost_speed *= 1.06
                    ghosts.hide()
                    self.game.pause.start_timer(3, "clear")
        return None

    def eat_ghost(self, ghosts, stats, sound):
        for ghost in ghosts:
            dist = (self.position - ghost.position).magnitudeSquared()
            radius = (self.settings.ghost_collide_radius + self.settings.collide_radius) ** 2
            if dist <= radius:
                if ghost is not None:
                    if ghost.mode.name == "RUN":
                        stats.score += self.settings.ghost_points[self.settings.ghost_eaten_counter]
                        self.settings.ghost_eaten_counter += 1
                        self.sb.prep_score()
                        ghost.spawn_mode(2)
                        sound.eat_ghost()
                        self.game.pause.start_timer(1)
                        self.appear = False
                        ghost.appear = False
                    elif ghost.mode.name == "CHASE" or ghost.mode.name == "SCATTER":
                        self.sb.check_high_score()
                        self.lose_life()
                        ghosts.hide()
                        self.game.pause.start_timer(3, "die")
        return None

    def update(self, dt, ghosts, stats, sb, sound):
        self.appear = True
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
                        self.set_position()
                        self.direction = gf.direction["STOP"]
        self.eat_food(ghosts, stats, sound)
        self.eat_ghost(ghosts, stats, sound)

        if self.game.fruit is not None:
            if self.eat_fruit(self.game.fruit, stats, sb, sound) or self.game.fruit.destroy:
                self.game.fruit = None

    def eat_fruit(self, fruit, stats, sb, sound):
        d = self.current_grid_pt.position - fruit.current_grid_pt.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.settings.collide_radius + fruit.settings.collide_radius)**2
        if dSquared <= rSquared:
            stats.score += fruit.points
            sound.eat_fruit()
            sb.prep_score()
            return True
        return False

    def reset(self):
        self.set_start_position()

    def lose_life(self):
        self.settings.pacman_lives -= 1

