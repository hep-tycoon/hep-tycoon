from collections import namedtuple
from os import path

Level = namedtuple('Level', ['publication_target', 'grant', 'discovery'])

levels = None
with open(path.join(path.dirname(__file__), 'levels.json')) as level_file:
    from json import load
    levels = [Level(**x) for x in load(level_file)]
