class Pauser(object):
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pause_time = 0
        self.player_paused = paused
        self.pause_type = None

    def update(self, dt):
        if not self.player_paused:
            if self.paused:
                self.timer += dt
                if self.timer >= self.pause_time:
                    self.timer = 0
                    self.paused = False

    def start_timer(self, pause_time, pause_type=None):
        self.pause_time = pause_time
        self.pause_type = pause_type
        self.timer = 0
        self.paused = True

    def player(self):
        self.player_paused = not self.player_paused
        if self.player_paused:
            self.paused = True
        else:
            self.paused = False

    def force(self, pause):
        self.paused = pause
        self.player_paused = pause
        self.timer = 0
        self.pause_time = 0

    def settle_pause(self, game):
        if self.pause_type == "die":
            game.pacman_died()
        else:
            game.beat_level()

