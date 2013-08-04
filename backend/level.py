from collections import namedtuple

Level = namedtuple('Level', ['publication_target', 'grant', 'discovery'])

levels = None
with open(os.path.join(os.path.dirname(__file__), 'levels.json')) as level_file:
    from json import load
    levels = [Level(**x) for x in load(level_file)]
