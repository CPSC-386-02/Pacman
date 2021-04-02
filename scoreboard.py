import pygame.font


class Scoreboard:
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 16)

        self.score_label_position = (0, 0)
        self.score_position = (0, 16)
        self.level_label_position = (368, 0)
        self.level_position = (368, 16)

        self.prep_score_label()
        self.prep_score()
        self.prep_level_label()
        self.prep_level()
        self.prep_lives()

    def prep_score_label(self):
        self.score_label = self.font.render("SCORE", 1, self.text_color)

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score = self.font.render(score_str.zfill(8), 1, self.text_color)

    def prep_level_label(self):
        self.level_label = self.font.render("LEVEL", 1, self.text_color)

    def prep_level(self):
        self.level = self.font.render(str(self.stats.level).zfill(3), 1, self.text_color)

    def prep_lives(self):
        self.lives = self.settings.get_image(0, 1, 32, 32)

    def show_score(self):
        self.screen.blit(self.score_label, self.score_label_position)
        self.screen.blit(self.score, self.score_position)
        self.screen.blit(self.level_label, self.level_label_position)
        self.screen.blit(self.level, self.level_position)
        for i in range(self.settings.pacman_lives):
            x = 10 + 42 * i
            y = self.settings.screen_height - 32
            self.screen.blit(self.lives, (x, y))

