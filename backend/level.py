from collections import namedtuple
from os import path

Level = namedtuple('Level', ['publication_target', 'grant', 'discoveries'])


def has_more_levels():
    return len(levels) > 0

def current_level():
    if has_more_levels():
        return levels[0]

def pop_level():
    if has_more_levels():
        return levels.pop(0)

levels = None
with open(path.join(path.dirname(__file__), 'levels.json')) as level_file:
    from json import load
    levels = [Level(**x) for x in load(level_file)]
