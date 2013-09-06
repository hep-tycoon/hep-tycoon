import random
from time import time

from backend.hr import HR
from backend.ht_exceptions import BankruptcyException
from backend import level
from backend import settings
from backend import technology


def upgrade_technology_hook(original_function):
    def new_function(self, *args, **kwargs):
        result = original_function(self, *args, **kwargs)
        self.update_max_number_scientists()
        return result
    return new_function


class GameManager(object):
    """
        The core piece of code that manages the game.
    """
    def __init__(self, lab_name, accelerator_geometry, accelerator_particles):
        """
        """
        self.start_time = time()
        self.last_updated = time()
        self.last_month_start = time()

        self.lab_name = lab_name
        self.data_centre = technology.from_tech_tree('datacentres', 0)
        self.accelerator = technology.from_tech_tree(
            'accelerators',
            accelerator_geometry,
            accelerator_particles,
            0
        )
        self.funds = settings.INITIAL_FUNDS - self.accelerator.price
        self.hr_manager = HR()
        self.update_max_number_scientists()
        self.salary = 1000
        self.grant_bar = 0
        self.level = level.current_level()
        self.accelerator_running = False
        self.has_won = False
        self._events = []

    def event(self, *args):
        self._events.append(args)

    def events(self):
        res = self._events
        self._events = []
        return res

    @property
    def all_technology(self):
        return [self.accelerator, self.data_centre] + \
            self.accelerator.detectors

    @property
    def funds(self):
        return self._funds

    @funds.setter
    def funds(self, value):
        if value < 0:
            raise BankruptcyException()
        self._funds = value

    def accelerator_start(self):
        """
            Start the data-taking.
            Returns False if the accelerator is already running.
        """
        self.process_events()
        self.accelerator_running = True

    def accelerator_stop(self):
        """
            Stop the data-taking and store the collected data in the data
            storage.
            Returns the number of collected data sets and the mean purity.
        """
        self.process_events()
        self.accelerator_running = False

    @upgrade_technology_hook
    def accelerator_upgrade(self):
        self.accelerator_stop()
        self.funds -= self.accelerator.upgrade_cost
        self.accelerator = self.accelerator.upgrade_from_tech_tree()

    @upgrade_technology_hook
    def detector_buy(self, slug):
        self.funds -= self.accelerator.add_detector(
            technology.from_tech_tree("detectors", slug, 0)
        )

    @upgrade_technology_hook
    def detector_remove(self, slug):
        self.funds -= self.accelerator.remove_detector(slug)

    @upgrade_technology_hook
    def detector_upgrade(self, slug):
        self.funds -= self.accelerator.upgrade_detector(slug)

    @upgrade_technology_hook
    def datacentre_upgrade(self):
        self.funds -= self.data_centre.upgrade_cost
        self.data_centre = self.data_centre.upgrade_from_tech_tree()

    def hr_hire(self, n):
        return self.hr_manager.hire(self.salary, n)

    def hr_fire(self, n):
        self.hr_manager.fire(n)

    def hr_adjust_salary(self, salary):
        self.salary = salary
        self.hr_manager.adjust_salary(salary)

    def pay_running_costs(self):
        totalCost = sum([tech.running_costs for tech in self.all_technology])
        if not self.accelerator_running:
            totalCost -= self.accelerator.running_costs
        self.funds -= totalCost

    def pay_salaries(self):
        self.funds -= self.hr_manager.sum_salary()

    def grant_bar_add(self, gnt):
        self.grant_bar += gnt
        if level.has_more_levels() and self.grant_bar > self.level.publication_target:
            lvl = level.pop_level()
            self.level = level.current_level()
            self.grant_bar -= lvl.publication_target
            self.funds += lvl.grant
            discovery = random.choice(lvl.discoveries)
            discovery["granted"] = lvl.grant
            self.event("grant", discovery)

    def process_events(self):
        elapsed = (time() - self.last_updated)
        for _ in xrange(int(elapsed)):
            total_quality = 0
            for scientist in self.hr_manager.scientists:
                if self.data_centre.empty():
                    scientist.reset_last_published()
                elif scientist.can_work():
                    total_quality += scientist.publish(self.data_centre.retrieve())
            self.grant_bar_add(total_quality*settings.GRANT_BAR_CONSTANT)

            if self.accelerator_running:
                data = self.accelerator.run(1)
                self.data_centre.store(data)
            self.last_updated += 1

        if not self.has_won and not level.has_more_levels():
            self.event("win")
            self.has_won = True

        # Month duration in real time
        month_time = (60 * 60 * 24 * 30) / settings.TIME_CONVERSION
        elapsed_months = (time() - self.last_month_start) / month_time
        for _ in xrange(int(elapsed_months)):
            self.pay_salaries()
            self.pay_running_costs()
            self.last_month_start += month_time

    def update_max_number_scientists(self):
        """
            Update the maximum number of scientists in the human resources
            manager. Invoked after technology upgrade.
        """
        self.hr_manager.max_scientists = sum(
            [t.num_scientists for t in self.all_technology]
        )
