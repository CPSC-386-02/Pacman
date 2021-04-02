import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        # pg.mixer.music.load('sound/bg music.wav')
        # pg.mixer.music.set_volume(0.3)

        self.eating_sound = pg.mixer.music.load('Waka Waka-[AudioTrimmer.com] (2).mp3')
        pg.mixer.music.set_volume(0.22)

        # pg.mixer.Sound.stop(self.eating_sound)

        # self.explosion_sound = pg.mixer.Sound('sound/Pop.mp3')
        # pg.mixer.Sound.set_volume(self.explosion_sound, 0.22)

        # self.playing_bg = None
        # self.play()
        # self.pause_bg()

    def pause_bg(self):
        self.playing_bg = False
        pg.mixer.music.pause()

    def unpause_bg(self):
        self.playing_bg = True
        pg.mixer.music.unpause()

    def play(self):
        self.playing_bg = True
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        self.playing_bg = False
        pg.mixer.music.stop()

    def eat_food(self):
        if not pg.mixer.music.get_busy():
            pg.mixer.music.play(-1)

    def stop_eating(self):
        pg.mixer.music.stop()



    # def alien_hit(self):
    #     pg.mixer.Sound.play(self.explosion_sound)
