def upgrade_technology_hook(original_function):
    def new_function(self, *args, **kwargs):
        result = original_function(self, *args, **kwargs)
        self.update_max_number_scientists()  # update maximum number of scientists
        return result
    return new_function


class GameManager(object):
    """
        The core piece of code that manages the game.
    """
    def __init__(self, lab_name, accelerator_geometry, accelerator_particles):
        from hr import HR
        import settings
        """
        """
        self._lab_name = lab_name
        self._data_centre = technology.from_tech_tree('datacentre', 0)
        self._accelerator = technology.from_tech_tree('accelerator', accelerator_geometry, accelerator_particles, 0)
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

    @upgrade_technology_hook
    def accelerator_upgrade(self): pass
    
    def detector_buy(self): pass
    
    def detector_remove(self): pass
    
    @upgrade_technology_hook
    def detector_upgrade(self): pass
    
    @upgrade_technology_hook
    def datacentre_upgrade(self): pass
    
    def hr_hire(self): pass
    
    def hr_fire(self): pass
    
    def hr_adjust_salary(self): pass

    def pay_running_costs(self): pass
    
    def pay_salaries(self): pass

    def update_max_number_scientists(self):
        """
            Update the maximum number of scientists in the human resources manager.
            Invoked after technology upgrade.
        """
        self._hr_manager.max_scientists = sum([t.num_scientists for t in self.all_technology])
