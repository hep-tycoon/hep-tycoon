GameManager(object):
    """
        The core piece of code that manages the game.
    """
    def __init__(self, lab_name, accelerator_geometry, accelerator_particles):
        from hr import HR
        import settings
        """
        """
        self._lab_name = lab_name
        self._data_centre = technology.from_tech_tree('Data Centre', level=0)  # working on this
        self._accelerator = technology.from_tech_tree('Accelerator', type=accelerator_type, 0)
        self._funds = settings.INITIAL_FUNDS - self._accelerator.price
        self._hr_manager = HR(self._accelerator.num_scientists)

    @property
    def funds(self):
        return self._funds

    @property
    def all_technology(self):
        return [self._accelerator, self._data_centre] + self._accelerator.detectors

    def accelerator_start(self): pass
    
    def accelerator_stop(self): pass

    @GameManager.upgrade_technology_hook
    def accelerator_upgrade(self): pass
    
    def detector_buy(self): pass
    
    def detector_remove(self): pass
    
    @GameManager.upgrade_technology_hook
    def detector_upgrade(self): pass
    
    @GameManager.upgrade_technology_hook
    def datacentre_upgrade(self): pass
    
    def hr_hire(self): pass
    
    def hr_fire(self): pass
    
    def hr_adjust_salary(self): pass

    def pay_running_costs(self): pass
    
    def pay_salaries(self): pass

    @staticmethod
    def upgrade_technology_hook(original_function):
        def new_function(*args, **kwargs):
            result = original_function(args, kwargs)
            # update maximum number of scientists
            self._hr_manager.max_scientists = sum([t.num_scientists for t in self.all_technology])
            return result
        return new_function
