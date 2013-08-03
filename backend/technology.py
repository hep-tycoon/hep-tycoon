class Technology(object):
    """
        Implement a piece of technology in the game.
        This is a base class for several other classes.
    """
    def __init__(self, name, price, running_costs):
        self._name = name
        self._price = price
        self._running_costs = running_costs

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def running_costs(self):
        return self._running_costs


class Accelerator(Technology):
    """
        An accelerator can store a number of experiments.
    """
    def __init__(self, name, price, running_costs, slots, rate, purity):
        super(Accelerator, self).__init__(name, price, running_costs)
        self._slots = slots
        self._rate = rate
        self._purity = purity
        self._detectors = []

    def add_detector(self, detector):
        """
            Add a detector to the accelerator.
            Throws an exception if no more free slots are available.
        """
        from ht_exceptions import NoMoreFreeSlotsException
        if self.free_slots <= 0:
            raise NoMoreFreeSlotsException()
        self._detectors.append(detector)

    def run(self, time):
        """
            Run the accelerator for an amount of time.
            Returns the data sets produced by the experiments or something like that.
        """
        pass  # implement!

    @property
    def slots(self):
        return self._slots

    @property
    def free_slots(self):
        return self._slots - len(self._detectors)

    @property
    def detectors(self):
        return self._detectors

    @property
    def rate(self):
        return self._rate

    @property
    def purity(self):
        return self._purity


class Detector(Technology):
    """
        A detector processes events from the accelerator and produces data.
    """
    def __init__(self, name, price, running_costs, purity_factor, rate_factor):
        super(Detector, self).__init__(name, price, running_costs)
        self._purity_factor = purity_factor
        self._rate_factor = rate_factor

    @property
    def purity_factor(self):
        return self._purity_factor

    @property
    def rate_factor(self):
        return self._rate_factor


def DataCentre(Technology):
    """
        The data centre stores data until it's processed by scientists.
    """
    def __init__(self, name, price, running_costs, storage_capacity):
        super(DataCentre, self).__init__(name, price, running_costs)
        self._storage_capacity = storage_capacity

    @property
    def storage_capacity(self):
        return self._storage_capacity


# load the technology tree from a file (beta)
techtree = None
with open('techtree.json') as tt_file:
    from json import load
    techtree = load(tt_file)
