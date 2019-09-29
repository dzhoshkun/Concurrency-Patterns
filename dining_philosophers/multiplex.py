from dining_philosophers import Forks


class Multiplex(Forks):
    """
    Original implementation by: Osama M. Afifi osama.egt@gmail.com - 27/Nov/2014

    The Dining Philosophers Problem solved using Multiplex.

    The Classic dining philosophers problem solved using a multiplex initialized with n-1 to avoid deadlocks.
    Starvation though can occur in this solution frequently by making a philosopher starve and switching between the
    others. For example: Philosopher 0 waits, and 1 and 3 eat, then they put down their forks; and 2 and 4 eat, and so
    on which makes philosopher 0 starve without eating. This code is deadlock free, if you can see anything else feel
    free to tell me.
    """

    def __init__(self, num_philosophers, semaphore_type):
        super().__init__(num_philosophers, semaphore_type)
        # initialize a multiplex allowing num_philosophers-1 philosophers to get their forks,
        # leaving one out to avoid deadlock
        self._multiplex = semaphore_type(num_philosophers - 1)

    def pick_up(self, identifier):
        self._multiplex.acquire()
        self._semaphores[self.right(identifier)].acquire()
        self._semaphores[self.left(identifier)].acquire()

    def put_down(self, identifier):
        self._semaphores[self.right(identifier)].release()
        self._semaphores[self.left(identifier)].release()
        self._multiplex.release()
