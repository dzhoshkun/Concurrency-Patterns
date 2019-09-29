from abc import ABC, abstractmethod


class Forks(ABC):

    def __init__(self, num_philosophers, semaphore_type):
        self._semaphores = [semaphore_type(1) for _ in range(num_philosophers)]

    def left(self, identifier):
        return identifier

    def right(self, identifier):
        return (identifier + 1) % len(self._semaphores)

    @abstractmethod
    def pick_up(self, identifier):
        raise NotImplementedError

    @abstractmethod
    def put_down(self, identifier):
        raise NotImplementedError
