class Animation:
    def __init__(self, animation_type):
        self.type = animation_type
        self.frames = []
        self.current_frame = 0
        self.finished = False
        self.speed = 0
        self.dt = 0
        self.animations = {}

    def reset(self):
        self.current_frame = 0
        self.finished = False

    def add_frame(self, frame):
        self.frames.append(frame)

    def update(self, dt):
        if self.type == "loop":
            self.loop(dt)
        elif self.type == "once":
            self.once(dt)
        elif self.type == "static":
            self.current_frame = 0
        return self.frames[self.current_frame]

    def next_frame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0

    def loop(self, dt):
        self.next_frame(dt)
        if self.current_frame == len(self.frames):
            self.current_frame = 0

    def once(self, dt):
        if not self.finished:
            self.next_frame(dt)
            if self.current_frame == len(self.frames) - 1:
                self.finished = True

    def set_up_pacman_animation(self):
        animations = Animation("loop")
        animations.speed = 30
        animations.add_frame(self.settings.get_image(4, 0, 32, 32))
        animations.add_frame(self.settings.get_image(0, 0, 32, 32))
        animations.add_frame(self.settings.get_image(0, 1, 32, 32))
        animations.add_frame(self.settings.get_image(0, 0, 32, 32))
        self.animations["left"] = animations

        animations = Animation("loop")
        animations.speed = 30
        animations.add_frame(self.settings.get_image(4, 0, 32, 32))
        animations.add_frame(self.settings.get_image(1, 0, 32, 32))
        animations.add_frame(self.settings.get_image(1, 1, 32, 32))
        animations.add_frame(self.settings.get_image(1, 0, 32, 32))
        self.animations["right"] = animations

        animations = Animation("loop")
        animations.speed = 30
        animations.add_frame(self.settings.get_image(4, 0, 32, 32))
        animations.add_frame(self.settings.get_image(2, 0, 32, 32))
        animations.add_frame(self.settings.get_image(2, 1, 32, 32))
        animations.add_frame(self.settings.get_image(2, 0, 32, 32))
        self.animations["down"] = animations

        animations = Animation("loop")
        animations.speed = 30
        animations.add_frame(self.settings.get_image(4, 0, 32, 32))
        animations.add_frame(self.settings.get_image(3, 0, 32, 32))
        animations.add_frame(self.settings.get_image(3, 1, 32, 32))
        animations.add_frame(self.settings.get_image(3, 0, 32, 32))
        self.animations["up"] = animations

        animations = Animation("once")
        animations.speed = 10
        for x in range(11):
            animations.add_frame(self.settings.get_image(x, 7, 32, 32))
        self.animations["death"] = animations

        animations = Animation("static")
        animations.add_frame(self.settings.get_image(4, 0, 32, 32))
        self.animations["idle"] = animations

    def set_up_ghost_animation(self, ghost_type):
        animations = Animation("loop")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(0, ghost_type, 32, 32))
        animations.add_frame(self.settings.get_image(1, ghost_type, 32, 32))
        self.animations["up"] = animations

        animations = Animation("loop")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(2, ghost_type, 32, 32))
        animations.add_frame(self.settings.get_image(3, ghost_type, 32, 32))
        self.animations["down"] = animations

        animations = Animation("loop")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(4, ghost_type, 32, 32))
        animations.add_frame(self.settings.get_image(5, ghost_type, 32, 32))
        self.animations["left"] = animations

        animations = Animation("loop")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(6, ghost_type, 32, 32))
        animations.add_frame(self.settings.get_image(7, ghost_type, 32, 32))
        self.animations["right"] = animations

        animations = Animation("loop")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(0, 6, 32, 32))
        animations.add_frame(self.settings.get_image(1, 6, 32, 32))
        self.animations["run"] = animations

        animations = Animation("loop")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(0, 6, 32, 32))
        animations.add_frame(self.settings.get_image(2, 6, 32, 32))
        animations.add_frame(self.settings.get_image(1, 6, 32, 32))
        animations.add_frame(self.settings.get_image(3, 6, 32, 32))
        self.animations["flash"] = animations

        animations = Animation("static")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(4, 6, 32, 32))
        self.animations["spawn_up"] = animations

        animations = Animation("static")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(5, 6, 32, 32))
        self.animations["spawn_down"] = animations

        animations = Animation("static")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(6, 6, 32, 32))
        self.animations["spawn_left"] = animations

        animations = Animation("static")
        animations.speed = 10
        animations.add_frame(self.settings.get_image(7, 6, 32, 32))
        self.animations["spawn_right"] = animations
