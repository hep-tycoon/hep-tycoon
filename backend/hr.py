class HR(object):
    """
        Manage human resources in the game.
    """
    def __init__(self, max_scientists):
        """
            Initialise a new human resources manager.
        """
        self._max_scientists = max_scientists
        self._scientists = []

    def __str__(self):
        """
            The string representation of the hr manager.
            Probably only used for debugging.
        """
        return 'HR with {} scientists. Earning a total of {}.'.format(
            self.num_scientists(),
            self.sum_salary()
        )

    @property
    def scientists(self):
        """
            Return the list of currently employed scientists.
            At this time it is a pointer to the list. One might consider just giving a copy.
        """
        return self._scientists

    @property
    def max_scientists(self):
        """
            Return the maximum number of scientists that can be employed at this point.
            Depends on the technology of the facility.
        """
        return self._max_scientists

    @max_scientists.setter
    def max_scientists(self, value):
        """
            Adjust the maximum number of scientists.
            Should be done automatically whenever the infrastructure changes.
        """
        self._max_scientists = value
    
    @property
    def num_scientists(self):
        """
            Give the number of currently employed scientists.
        """
        return len(self._scientists)

    @property
    def positions(self):
        """
            The number of open positions (free slots for hiring scientists.)
        """
        return self.max_scientists - self.num_scientists

    def hire(self, salary, n=1):
        from ht_exceptions import NegativeSalaryException, NegativeNumberScientistsException
        """
            Hire n new scientists with a certain salary.
            Since at this point they are all the same it is pretty straightforward.

            If there are not enough free positions, only some of the are hired.
            The function returns the number of scientists actually hired.
        """
        if salary < 0:
            raise NegativeSalaryException()
        if n < 0:
            raise NegativeNumberScientistsException()
        if n > self.positions:
            n = self.positions  # hire as many as possible
        self._scientists.extend([Scientist(salary) for i in range(n)])
        return n

    def fire(self, n=1):
        from ht_exceptions import NegativeNumberScientistsException
        """
            Fire n scientists.
            Since they are all the same, it doesn't matter whom you fire, right?
            However, there is a penalty for firing a scientist which is a multiple of his salary.

            The function returns the number of scientists fired and the penalty for that.
        """
        if n < 0:
            raise NegativeNumberScientistsException()
        if n > self.num_scientists:
            n = self.num_scientists
        penalty = sum([s.firing_penalty for s in self._scientists[:n]])
        del(self._scientists[:n])
        return n, penalty

    def sum_salary(self):
        """
            Sum all the scientists salaries.
            Needed for calculation of running costs.
        """
        return sum([s.salary for s in self._scientists])

    def adjust_salary(self, salary):
        from ht_exceptions import NegativeSalaryException
        """
            Set the salary for all the scientists.
            This is only valid as long as all scientists are treated the same.
        """
        if salary < 0:
            raise NegativeSalaryException()
        for s in self._scientists:
            s.salary = salary


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
        self._name = Scientist.random_name()
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
    def productivity(self):
        from math import exp
        import settings
        """
            Very cool logistic function for the productivity of the scientist.
        """
        return 2.0 / (1 + exp(-settings.GLOBAL_PRODUCTIVITY_CONVERSION * self.salary)) - 1

    @property
    def skill(self):
        return self._skill

    @property
    def firing_penalty(self):
        return self._salary * self._firing_penalty_factor + self._firing_penalty_constant

    @staticmethod
    def random_name():
        from random import choice
        from string import uppercase
        """
            Construct a random name for a scientist.
        """
        names = ['Hansen', 'Petersen', 'Klausen', 'Dungs', 'Maguire', 'Bel']
        return '{}. {}. {}'.format(choice(uppercase), choice(uppercase), choice(names))
