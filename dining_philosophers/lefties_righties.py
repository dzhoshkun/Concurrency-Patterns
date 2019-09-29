from dining_philosophers import Forks


class LeftiesRighties(Forks):
    """
    Original implementation by: Osama M. Afifi osama.egt@gmail.com - 27/Nov/2014

    The Dining Philosophers Problem solved using alternating lefties and righties.

    This solution make odd-positioned philosophers righties and even-positioned ones lefties. This guarantees no
    deadlock and the solution is as fair as possible with maximum philosophers even. The Solution is completely fair
    with even number of philosophers but is slightly unfair when the number is odd where to righties sit next to each
    other (1st and last). This code is deadlock free; if you can see anything else feel free to tell me.
    """

    def __init__(self, num_philosophers, semaphore_type):
        super().__init__(num_philosophers, semaphore_type)

    def pick_up(self, identifier):
        if identifier % 2 == 0:
            self._semaphores[self.right(identifier)].acquire()
            self._semaphores[self.left(identifier)].acquire()
        else:
            self._semaphores[self.left(identifier)].acquire()
            self._semaphores[self.right(identifier)].acquire()

    def put_down(self, identifier):
        if identifier % 2 == 0:
            self._semaphores[self.right(identifier)].release()
            self._semaphores[self.left(identifier)].release()
        else:
            self._semaphores[self.left(identifier)].release()
            self._semaphores[self.right(identifier)].release()
