from collections import namedtuple
from os import path

Level = namedtuple('Level', ['publication_target', 'grant', 'discoveries'])


def current_level():
    return levels[0]


def pop_level():
    return levels.pop(0)


levels = None
with open(path.join(path.dirname(__file__), 'levels.json')) as level_file:
    from json import load
    levels = [Level(**x) for x in load(level_file)]
