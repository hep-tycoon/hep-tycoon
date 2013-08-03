class Technology(object):
    """
        Implement a piece of technology in the game.
        This is a base class for several other classes.
    """
    def __init__(self, name, price, running_costs, num_scientists, level, max_level, query):
        self.name = name
        self.price = price
        self.running_costs = running_costs
        self.num_scientists = num_scientists
        self.level = level
        self.max_level = max_level
        self.query = query

    def can_upgrade(self):
        return self.level < self.max_level

    def upgrade_from_tech_tree(self):
        return from_tech_tree(*self.query[:-1] + [self.level + 1])

    def json(self):
        return dict((key, getattr(self, key)) for key in ("name", "price", "running_costs", "num_scientists", "level", "max_level"))


class Accelerator(Technology):
    """
        An accelerator can store a number of experiments.
    """
    def __init__(self, slots, rate, purity, **kwargs):
        super(Accelerator, self).__init__(**kwargs)
        self.slots = slots
        self.rate = rate
        self.purity = purity
        self.detectors = []

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
    def free_slots(self):
        return self._slots - len(self._detectors)

    def json(self):
        res = Technology.json(self)
        res.update({
            "free_slots": self.free_slots,
            "slots": self.slots,
            "rate": self.rate,
            "purity": self.purity,
        })
        return res


class Detector(Technology):
    """
        A detector processes events from the accelerator and produces data.
    """
    def __init__(self, purity_factor, rate_factor, **kwargs):
        super(Detector, self).__init__(**kwargs)
        self.purity_factor = purity_factor
        self.rate_factor = rate_factor

    def process_events(self, size, purity):
        return (size * self.rate_factor, purity * self.purity_factor)


class DataCentre(Technology):
    """
        The data centre stores data until it's processed by scientists.
    """
    def __init__(self, storage_capacity, **kwargs):
        from collections import deque
        """
        """
        super(DataCentre, self).__init__(**kwargs)
        self._storage = deque(maxlen=storage_capacity)

    @property
    def storage_capacity(self):
        return self._storage.maxlen

    @storage_capacity.setter
    def storage_capacity(self, value):
        old = self._storage
        self._storage = deque(old, maxlen=value)

    @property
    def storage_used(self):
        return len(self._storage)

    @property
    def storage_free(self):
        return self.storage_capacity - self.storage_used

    def empty(self):
        return self.storage_used == 0

    def store(self, dataset):
        self._storage.append(dataset)

    def retrieve(self):
        if self.empty():
            return None
        return self._storage.popleft()


def query_tech_tree(path):
    act = techtree
    for segment in path:
        act = act[segment]
    return act

def from_tech_tree(*query):
    query = list(query)
    tech_type = query[0]
    if tech_type == "accelerators":
        tech_class = Accelerator
    elif tech_type == "detectors":
        tech_class = Detector
    elif tech_type == "datacentres":
        tech_class = DataCentre
    levels = query_tech_tree(query[:-1])
    data = levels[query[-1]].copy()
    data["level"] = query[-1]
    data["max_level"] = len(levels)
    data["query"] = query
    return tech_class(**data)


# load the technology tree from a file (beta)
techtree = None
with open('techtree.json') as tt_file:
    from json import load
    techtree = load(tt_file)
