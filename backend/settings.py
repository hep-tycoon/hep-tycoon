"""
    Some global settings for the game.
    It's easier to have them in a central place.
"""

# Game set up
INITIAL_FUNDS = 9000001
TIME_CONVERSION = float(60*60*24*365)/30 # Real-Game time conversion factor

GRANT_BAR_CONSTANT = 1

# Scientist
GLOBAL_SKILL = 1  # the scientists' skill
GLOBAL_PRODUCTIVITY_CONVERSION = 1  # conversion factor between salary and productivity
GLOBAL_FIRING_PENALTY_FACTOR = 2
GLOBAL_FIRING_PENALTY_CONSTANT = 1
PUBLISH_TIME = 9 # In real seconds = ~1/3 game months

# Detector
GLOBAL_DETECTOR_REMOVAL_COST = 10
