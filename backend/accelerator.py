class Accelerator:
    """
        An abstract base class for accelerators in the game.
    """
    def __init__(self, name, price, slots, rate, quality):
        self._name = name
        self._price = price
        self._slots = slots
        self._detectors = []
        self._rate = rate
        self._quality = quality

    def __str__(self):
        return 'Accelerator {}'.format(self._name)

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def slots(self):
        return self._slots

    @property
    def detectors(self):
        return self._detectors

    @property
    def rate(self):
        return self._rate

    @property
    def quality(self):
        return self._quality

    def add_detector(self, detector):
        if len(self._detectors) < self._slots:
            self._detectors.append(detector)
        else:
            raise Exception('All available slots are already used.', 'Try to upgrade your accelerator.')

# maybe we should to this differently ('upgrade' function for example)
#linear_ee_accelerator_1 = Accelerator('Linear ee Accelerator Lv. 1', 1, 1, 1, 1)
#linear_ee_accelerator_2 = Accelerator('Linear ee Accelerator Lv. 2', 1, 2, 1, 1)
#linear_ee_accelerator_3 = Accelerator('Linear ee Accelerator Lv. 3', 1, 3, 1, 1)
#linear_ee_accelerator_4 = Accelerator('Linear ee Accelerator Lv. 4', 1, 4, 1, 1)
#
#linear_pp_accelerator_1 = Accelerator('Linear pp Accelerator Lv. 1', 1, 1, 1, 1)
#linear_pp_accelerator_2 = Accelerator('Linear pp Accelerator Lv. 2', 1, 2, 1, 1)
#linear_pp_accelerator_3 = Accelerator('Linear pp Accelerator Lv. 3', 1, 3, 1, 1)
#linear_pp_accelerator_4 = Accelerator('Linear pp Accelerator Lv. 4', 1, 4, 1, 1)
#
#circular_ee_accelerator_1 = Accelerator('Circular ee Accelerator Lv. 1', 1, 1, 1, 1)
#circular_ee_accelerator_2 = Accelerator('Circular ee Accelerator Lv. 2', 1, 2, 1, 1)
#circular_ee_accelerator_3 = Accelerator('Circular ee Accelerator Lv. 3', 1, 3, 1, 1)
#circular_ee_accelerator_4 = Accelerator('Circular ee Accelerator Lv. 4', 1, 4, 1, 1)
#
#circular_pp_accelerator_1 = Accelerator('Circular pp Accelerator Lv. 1', 1, 1, 1, 1)
#circular_pp_accelerator_2 = Accelerator('Circular pp Accelerator Lv. 2', 1, 2, 1, 1)
#circular_pp_accelerator_3 = Accelerator('Circular pp Accelerator Lv. 3', 1, 3, 1, 1)
#circular_pp_accelerator_4 = Accelerator('Circular pp Accelerator Lv. 4', 1, 4, 1, 1)
