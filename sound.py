import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        pg.mixer.music.load('Sound/siren.wav')
        pg.mixer.music.set_volume(0.3)

        self.begin = pg.mixer.Sound('Sound/open song.wav')
        pg.mixer.Sound.set_volume(self.begin, 0.22)

        self.eating = pg.mixer.Sound('Sound/eating.wav')
        pg.mixer.Sound.set_volume(self.eating, 0.22)

        self.power_up = pg.mixer.Sound('Sound/power up.wav')
        pg.mixer.Sound.set_volume(self.power_up, 0.22)

        self.eating_fruit = pg.mixer.Sound('Sound/eat fruit.wav')
        pg.mixer.Sound.set_volume(self.eating, 0.22)

        self.eating_ghost = pg.mixer.Sound('Sound/eat ghost.wav')
        pg.mixer.Sound.set_volume(self.eating, 0.22)

        self.die = pg.mixer.Sound('Sound/death.wav')
        pg.mixer.Sound.set_volume(self.die, 0.22)

        self.play()
        self.pause_bg()

    def pause_bg(self):
        pg.mixer.music.pause()

    def unpause_bg(self):
        pg.mixer.music.unpause()

    def play(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def eat_food(self):
        pg.mixer.Sound.play(self.eating)

    def eat_power_up(self):
        pg.mixer.Sound.play(self.power_up)

    def eat_fruit(self):
        pg.mixer.Sound.play(self.eating_fruit)

    def eat_ghost(self):
        pg.mixer.Sound.play(self.eating_ghost)

    def pacman_die(self):
        pg.mixer.Sound.play(self.die)

    def play_open_song(self):
        pg.mixer.Sound.play(self.begin)
