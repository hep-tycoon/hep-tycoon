class HR:
    """
        Manage human resources in the game.
    """
    def __init__(self):
        self._scientists = []

    def __str__(self):
        return 'HR with {} scientists. Earning a total of {}.'.format(
            self.num_scientists(),
            self.sum_salary()
        )

    @property
    def scientists(self):
        return self._scientists  # or do we want a copy?

    def num_scientists(self):
        return len(self._scientists)

    def hire(self, salary, n=1):
        from scientist import Scientist
        """
            Hire n new scientists with a certain salary.
            Since at this point they are all the same it is pretty straightforward.
        """
        self._scientists.extend([Scientist(salary) for i in range(n)])

    def fire(self, n=1):
        """
            Fire n scientists.
            Since they are all the same, it doesn't matter whom you fire, right?
        """
        self._scientists = self._scientists[:-n]

    def sum_salary(self):
        """
            Sum all the scientists salaries.
            Needed for calculation of running costs.
        """
        return sum([s.salary for s in self._scientists])

    def adjust_salaries(self, salary):
        """
            Set the salary for all the scientists.
            This is only valid as long as all scientists are treated the same.
        """
        for s in self._scientists:
            s.salary = salary
