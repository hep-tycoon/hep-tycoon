class HTException(Exception):
    def __init__(self, title, msg):
        self._title = title
        self._msg = msg

    def __str__(self):
        return '{}\n{}'.format(self.title, self.msg)

    @property
    def title(self):
        return self._title

    @property
    def msg(self):
        return self._msg


class NegativeSalaryException(HTException):
    def __init__(self):
        super(NegativeSalaryException, self).__init__(
            'negative salary',
            'You cannot provide a negative salary.'
        )


class NegativeNumberScientistsException(HTException):
    def __init__(self):
        super(NegativeNumberScientistsException, self).__init__(
            'negative number of scientists',
            'You cannot provide a negative number of scientists.'
        )


class NoMoreFreeSlotsException(HTException):
    def __init__(self):
        super(NoMoreFreeSlotsException, self).__init__(
            'no more free slots',
            'You cannot add another detector since there are no more free slots.'    
        )
