import os
import json

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

    @property
    def can_upgrade(self):
        return self.level < self.max_level - 1

    def upgrade_from_tech_tree(self):
        assert self.can_upgrade
        return from_tech_tree(*self.query[:-1] + [self.level + 1])

    def json(self):
        return dict((key, getattr(self, key)) for key in ("name", "price", "running_costs", "num_scientists", "level", "max_level", "can_upgrade"))


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

    def get_index_by_slug(self, slug):
        for i,d in enumerate(self.detectors):
            if d.slug == slug:
                return i
        raise Exception("Slug not found")

    def add_detector(self, detector):
        """
            Add a detector to the accelerator.
            Throws an exception if no more free slots are available.
        """
        from ht_exceptions import NoMoreFreeSlotsException
        if self.free_slots <= 0:
            raise NoMoreFreeSlotsException()
        self.detectors.append(detector)

    def remove_detector(self, slug):
        del self.detectors[self.get_index_by_slug(slug)]

    def upgrade_detector(self, slug):
        i = self.get_index_by_slug(slug)
        self.detectors[i] = self.detectors[i].upgrade_from_tech_tree()

    def run(self, time):
        from data_set import DataSet
        """
            Run the accelerator for an amount of time.
            Returns the data sets produced by the experiments or something like that.
        """
        datasets = []
        size = time * self.rate
        for detector in self.detectors:
            for i in range(int(size * detector.rate_factor)):
                datasets.append(DataSet(self.purity * detector.purity_factor))
        return datasets

    @property
    def free_slots(self):
        return self.slots - len(self.detectors)

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

    @property
    def slug(self):
        return self.query[-2]

    def json(self):
        res = Technology.json(self)
        res.update({
            "purity_factor": self.purity_factor,
            "rate_factor": self.rate_factor,
            "slug": self.slug
        })
        return res



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
        from collections import deque
        """
            Update the storage capacity.
            Since deques are used, all the data has to be moved which in a way is quite realistic.
        """
        self._storage = deque(self._storage, maxlen=value)

    @property
    def storage_used(self):
        return len(self._storage)

    @property
    def storage_free(self):
        return self.storage_capacity - self.storage_used

    def empty(self):
        return self.storage_used == 0

    def store(self, data):
        from collections import Iterable
        """
            Add one or multiple datasets to the store.
            If the store is over capacity, old data is just dumped.
        """
        if isinstance(data, Iterable):
            self._storage.extend(data)
        else:
            self._storage.append(data)

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
with open(os.path.join(os.path.dirname(__file__), 'techtree.json')) as tt_file:
    techtree = json.load(tt_file)
