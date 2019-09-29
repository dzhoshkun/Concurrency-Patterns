# Osama M. Afifi osama.egt@gmail.com -  27/Nov/2014
#
# The Dining Philosophers Problem solved using alternating lefties and righties
#
# This solution make odd positioned philosophers righties and even positioned lefties This guarantees no deadlock and
# make the solution as fair as possible with maximum philosophers even The Solution is completely fair with even
# number of philosophers but is slightly unfair when the number is odd where to righties sit next to each other (1st
# and last) This code is deadlock free if you can see anything else feel free to tell me.


# use only one of the following lines for the corresponding multi-tasking execution environment:
from threading import Thread as Environment, Semaphore
# from multiprocessing import Process as Environment, Semaphore

from time import time

n = 5  # for standard Dining Philosophers problem
forks = [Semaphore(1) for i in range(n)]
lifetime_in_sec = 5


def dining_philosphers(i):
    started_at_sec = time()
    while time() - started_at_sec < lifetime_in_sec:
        think()
        get_forks(i)
        eat()
        put_forks(i)


# do something useful in the following two functions
def think():
    pass


def eat():
    pass


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


if __name__ == '__main__':
    tasks = [Environment(target=dining_philosphers, args=[i]) for i in range(n)]
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()
