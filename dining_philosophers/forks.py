class Forks:

    def __init__(self, num_philosophers, semaphore_type):
        self._semaphores = [semaphore_type(1) for _ in range(num_philosophers)]

    def left(self, identifier):
        return identifier

    def right(self, identifier):
        return (identifier + 1) % len(self._semaphores)

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
