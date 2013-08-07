from collections import namedtuple
from os import path

Level = namedtuple('Level', ['publication_target', 'grant', 'discoveries'])

class Levels():
    def __init__(self):
        with open(path.join(path.dirname(__file__), 'levels.json')) as level_file:
            from json import load
            self.levels = [Level(**x) for x in load(level_file)]

    def current_level(self):
        return self.levels[0]

    def pop_level(self):
        return self.levels.pop(0)

