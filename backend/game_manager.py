import technology
from time import time
from hr import HR

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
        import settings
        """
        """
        self.start_time = time()
        self.lab_name = lab_name
        self.data_centre = technology.from_tech_tree('datacentres', 0)
        self.accelerator = technology.from_tech_tree('accelerators', accelerator_geometry, accelerator_particles, 0)
        self.funds = settings.INITIAL_FUNDS - self.accelerator.price
        self.hr_manager = HR(self.accelerator.num_scientists)
        self.accelerator_started = 0
        self.salary = 0

    @property
    def all_technology(self):
        return [self.accelerator, self.data_centre] + self.accelerator.detectors

    @property
    def accelerator_running(self):
        return self.accelerator_started != 0

    @property
    def funds(self):
        return self._funds

    @funds.setter
    def funds(self, value):
        from ht_exceptions import BankruptcyException
        if value < 0:
            raise BankruptcyException()
        self._funds = value

    def accelerator_start(self):
        """
            Start the data-taking.
            Returns False if the accelerator is already running.
        """
        if not self.accelerator_running:
            self.accelerator_started = time()
            return True
        return False

    def accelerator_stop(self):
        """
            Stop the data-taking and store the collected data in the data storage.
            Returns the number of collected data sets and the mean purity.
        """
        if self.accelerator_running:
            runtime = time() - self.accelerator_started
            self.accelerator_started = 0
            data = self.accelerator.run(runtime)
            n = len(data)
            mean_purity = sum([d.purity for d in data]) / n
            self.data_centre.store(data)
            return n, mean_purity
        return 0, 0

    @upgrade_technology_hook
    def accelerator_upgrade(self):
        self.accelerator = self.accelerator.upgrade_from_tech_tree()

    @upgrade_technology_hook
    def detector_buy(self, slug):
        self.accelerator.add_detector(technology.from_tech_tree("detectors", slug, 0))

    @upgrade_technology_hook
    def detector_remove(self, slug):
        self.accelerator.remove_detector(slug)

    @upgrade_technology_hook
    def detector_upgrade(self, slug):
        self.accelerator.upgrade_detector(slug)

    @upgrade_technology_hook
    def datacentre_upgrade(self):
        self.data_centre = self.data_centre.upgrade_from_tech_tree()
    
    def hr_hire(self, n):
        return self.hr_manager.hire(self.salary, n)
    
    def hr_fire(self, n):
        self.hr_manager.fire(n)
    
    def hr_adjust_salary(self, salary):
        self.salary = salary
        self.hr_manager.adjust_salary(salary)

    def pay_running_costs(self):
        totalCost = sum([tech.running_costs for tech in self.all_technology()])
        self.funds -= totalCost;
    
    def pay_salaries(self):
        self.funds -= hr_manager.sum_salary()

    def update_max_number_scientists(self):
        """
            Update the maximum number of scientists in the human resources manager.
            Invoked after technology upgrade.
        """
        self.hr_manager.max_scientists = sum([t.num_scientists for t in self.all_technology])

