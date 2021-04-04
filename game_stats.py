import pickle


class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()

        try:
            with open('score.dat', 'rb') as file:
                self.high_score = pickle.load(file)
        except:
            self.high_score = 0

    def reset_stats(self):
        self.score = 0
        self.level = 1
