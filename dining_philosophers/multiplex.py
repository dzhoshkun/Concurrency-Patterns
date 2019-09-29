from abc import ABC

from dining_philosophers import Forks


class Multiplex(Forks, ABC):

    def __init__(self, num_philosophers, semaphore_type):
        super().__init__(num_philosophers, semaphore_type)
