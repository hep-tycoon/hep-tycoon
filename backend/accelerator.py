class Accelerator(object):
    """
        An abstract base class for accelerators in the game.
    """
    def __init__(self, name, technology, particles):
        self._name = name
        self._technology = technology
        self._particles = particles
        self._techtree = accelerators[technology][particles]
        if not self._techtree:
            raise Exception('Could not find a tech tree for the given technology and particles.')
        self._level = 0
        self._detectors = []

    def __str__(self):
        return 'Accelerator {}'.format(self._name)

    def upgrade(self, keep_detectors=[]):
        # to be implemented!
        pass

    @property
    def name(self):
        return self._name

    @property
    def technology(self):
        return self._technology

    @property
    def particles(self):
        return self._particles

    @property
    def level(self):
        return self._level

    @property
    def detectors(self):
        return self._detectors
    
    @property
    def slots(self):
        return self._techtree['slots']

    @property
    def rate(self):
        """
            The collision rate of the accelerator.
        """
        return self._techtree['rate']

    @property
    def quality(self):
        """
            The beam quality of the accelerator.
            Maybe we should replace this with another term.
        """
        return self._techtree['quality']

    def add_detector(self, detector):
        if len(self._detectors) < self._slots:
            self._detectors.append(detector)
        else:
            raise Exception('All available slots are already used.', 'Try to upgrade your accelerator.')

