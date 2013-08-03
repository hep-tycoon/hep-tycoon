HepTycoonGameManager(object):
    import settings
    """
    """
    def __init__(self, lab_name, accelerator_geometry, accelerator_particles):
        self._lab_name = lab_name
        self._data_centre = technology.from_tech_tree('Data Centre', level=0)  # working on this
        self._accelerator = technology.from_tech_tree('Accelerator', type=accelerator_type, 0)
        self._funds = settings.INITIAL_FUNDS - self._accelerator.price
        self._hr_manager = None

    @property
    def funds(self):
        return self._funds
