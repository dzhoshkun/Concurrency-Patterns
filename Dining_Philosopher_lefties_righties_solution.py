# Osama M. Afifi osama.egt@gmail.com -  27/Nov/2014
#
# The Dining Philosophers Problem solved using alternating lefties and righties
#
# This solution make odd positioned philosophers righties and even positioned lefties This guarantees no deadlock and
# make the solution as fair as possible with maximum philosophers even The Solution is completely fair with even
# number of philosophers but is slightly unfair when the number is odd where to righties sit next to each other (1st
# and last) This code is deadlock free if you can see anything else feel free to tell me.


from time import time, strftime

use_processes = False

if use_processes:
    from multiprocessing import Process as Environment, Semaphore, Queue
    call_statistics_queue = Queue()
else:
    from threading import Thread as Environment, Semaphore


def human_readable_timestamp_string():
    return strftime('%Y-%m-%d-%H-%M-%S')


n = 5  # for standard Dining Philosophers problem
forks = [Semaphore(1) for i in range(n)]
lifetime_in_sec = 5
call_statistics_filename = 'call-stats-'
if use_processes:
    call_statistics_filename += 'processes-'
else:
    call_statistics_filename += 'threads-'
call_statistics_filename += human_readable_timestamp_string() + '.csv'


def dining_philosopher(i):
    started_at_sec = time()
    num_thoughts = 0
    num_meals = 0
    while time() - started_at_sec < lifetime_in_sec:
        think()
        num_thoughts += 1
        get_forks(i)
        eat()
        num_meals += 1
        put_forks(i)
    call_statistics = '%d, %d, %d' % (i, num_thoughts, num_meals)
    if use_processes:
        call_statistics_queue.put(call_statistics)
    else:
        with open(call_statistics_filename, 'a') as call_statistics_file:
            call_statistics_file.write(call_statistics + '\n')


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
    tasks = [Environment(target=dining_philosopher, args=[i]) for i in range(n)]
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()

    if use_processes:
        with open(call_statistics_filename, 'w') as call_statistics_file:
            while not call_statistics_queue.empty():
                call_statistics_file.write(call_statistics_queue.get() + '\n')
