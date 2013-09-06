"""
    Some global settings for the game.
    It's easier to have them in a central place.
"""

# Game set up
INITIAL_FUNDS = 300000
# real time to game time conversion factor
TIME_CONVERSION = float(60 * 60 * 24 * 365) / 30

GRANT_BAR_CONSTANT = 1.

# Scientist
GLOBAL_SKILL = .5  # the scientists' skill
# conversion factor between salary and productivity
GLOBAL_PRODUCTIVITY_CONVERSION = 1. / 1000
GLOBAL_FIRING_PENALTY_FACTOR = 2.
GLOBAL_FIRING_PENALTY_CONSTANT = 1.
PUBLISH_TIME = 9.  # in real seconds = ~1/3 game months

# Detector
GLOBAL_DETECTOR_REMOVAL_COST = 10000.
