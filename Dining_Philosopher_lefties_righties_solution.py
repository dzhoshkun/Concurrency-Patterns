# Osama M. Afifi osama.egt@gmail.com -  27/Nov/2014
#
# The Dining Philosophers Problem solved using alternating lefties and righties
#
# This solution make odd positioned philosophers righties and even positioned lefties This guarantees no deadlock and
# make the solution as fair as possible with maximum philosophers even The Solution is completely fair with even
# number of philosophers but is slightly unfair when the number is odd where to righties sit next to each other (1st
# and last) This code is deadlock free if you can see anything else feel free to tell me.


from time import time

from utils import human_readable_timestamp

use_processes = False

if use_processes:
    from multiprocessing import Process as Environment, Semaphore, Queue
    call_statistics_queue = Queue()
else:
    from threading import Thread as Environment, Semaphore


n = 2  # for standard Dining Philosophers problem
forks = [Semaphore(1) for i in range(n)]
lifetime_in_sec = 2
call_statistics_filename = 'call-stats-'
if use_processes:
    call_statistics_filename += 'processes-'
else:
    call_statistics_filename += 'threads-'
call_statistics_filename += human_readable_timestamp() + '.csv'


def left(i):
    return i


def right(i):
    return (i + 1) % n


def get_forks(i):
    if i % 2 == 0:
        forks[right(i)].acquire()
        forks[left(i)].acquire()
    else:
        forks[left(i)].acquire()
        forks[right(i)].acquire()


def put_forks(i):
    if i % 2 == 0:
        forks[right(i)].release()
        forks[left(i)].release()
    else:
        forks[left(i)].release()
        forks[right(i)].release()


class Philosopher:

    def __init__(self, identifier):
        self._identifier = identifier

    def dine(self, dining_time_in_sec, report_call_stats):
        started_at_sec = time()
        num_thoughts = 0
        num_meals = 0
        while time() - started_at_sec < dining_time_in_sec:
            self.think()
            num_thoughts += 1
            get_forks(self._identifier)
            self.eat()
            num_meals += 1
            put_forks(self._identifier)
        call_stats = '%d, %d, %d\n' % (self._identifier, num_thoughts, num_meals)
        report_call_stats(call_stats)

    # do something useful in the following two functions
    def think(self):
        pass

    def eat(self):
        pass


if __name__ == '__main__':
    if use_processes:
        call_stats_callback = call_statistics_queue.put
    else:
        call_stats_callback = open(call_statistics_filename, 'a').write
    tasks = [Environment(target=Philosopher(i).dine, args=[lifetime_in_sec, call_stats_callback]) for i in range(n)]
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()

    if use_processes:
        with open(call_statistics_filename, 'w') as call_statistics_file:
            while not call_statistics_queue.empty():
                call_statistics_file.write(call_statistics_queue.get())
