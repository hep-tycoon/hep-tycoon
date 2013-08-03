"""
"""

def random_name():
    from random import choice
    from string import uppercase
    """
        Construct a random name for a scientist.
    """
    names = ['Hansen', 'Petersen', 'Klausen', 'Dungs', 'Maguire', 'Bel']
    return '{}. {}. {}'.format(choice(uppercase), choice(uppercase), choice(names))


class Scientist(object):
    """
        A scientist in the game.
    """
    def __init__(self, salary):
        import settings
        """
            Create a new scientist with a given salary.
            The name is (at this point) assigned randomly.
            All the other variables are the same for all scientists.
        """
        self._name = random_name()
        self._salary = salary
        # set parameters according to global options
        self._skill = settings.GLOBAL_SKILL
        self._firing_penalty_factor = settings.GLOBAL_FIRING_PENALTY_FACTOR
        self._firing_penalty_constant = settings.GLOBAL_FIRING_PENALTY_CONSTANT

    def __str__(self):
        """
            Return a string identifying the scientist.
            At this point it's just the name since skill and salary are the same for all of them.
        """
        return '{}'.format(self._name)

    @property
    def name(self):
        return self._name

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary):
        self._salary = salary

    @property
    def skill(self):
        return self._skill

    @property
    def firing_penalty(self):
        return self._salary * self._firing_penalty_factor + self._firing_penalty_constant
