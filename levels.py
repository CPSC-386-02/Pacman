class LevelController(object):
    def __init__(self):
        self.level = 0
        self.levels_dict = {
            0: {"mazename": "mazetest.txt", "foodname": "food.txt", "row": 0, "fruit": "cherry"}
        }

    def next_level(self):
        self.level += 1

    def reset(self):
        self.level = 0

    def get_level(self):
        return self.levels_dict[self.level % len(self.levels_dict)]
