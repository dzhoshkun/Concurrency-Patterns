from time import time


class Philosopher:

    def __init__(self, identifier, forks):
        self._identifier = identifier
        self._forks = forks

    def dine(self, dining_time_in_sec, report_call_stats):
        started_at_sec = time()
        num_thoughts = 0
        num_meals = 0
        while time() - started_at_sec < dining_time_in_sec:
            self.think()
            num_thoughts += 1
            self._forks.pick_up(self._identifier)
            self.eat()
            num_meals += 1
            self._forks.put_down(self._identifier)
        call_stats = '%d, %d, %d\n' % (self._identifier, num_thoughts, num_meals)
        report_call_stats(call_stats)

    # do something useful in the following two functions
    def think(self):
        pass

    def eat(self):
        pass
