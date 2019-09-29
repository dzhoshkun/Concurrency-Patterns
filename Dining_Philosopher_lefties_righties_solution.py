# Osama M. Afifi osama.egt@gmail.com -  27/Nov/2014
#
# The Dining Philosophers Problem solved using alternating lefties and righties
#
# This solution make odd positioned philosophers righties and even positioned lefties This guarantees no deadlock and
# make the solution as fair as possible with maximum philosophers even The Solution is completely fair with even
# number of philosophers but is slightly unfair when the number is odd where to righties sit next to each other (1st
# and last) This code is deadlock free if you can see anything else feel free to tell me.

from dining_philosophers import Forks
from dining_philosophers import Philosopher
from utils import human_readable_timestamp


if __name__ == '__main__':

    use_processes = False

    if use_processes:
        from multiprocessing import Process as Environment, Semaphore, Queue
        call_statistics_queue = Queue()
    else:
        from threading import Thread as Environment, Semaphore

    num_philosophers = 2
    lifetime_in_sec = 2
    call_statistics_filename = 'call-stats-'
    if use_processes:
        call_statistics_filename += 'processes-'
    else:
        call_statistics_filename += 'threads-'
    call_statistics_filename += human_readable_timestamp() + '.csv'

    if use_processes:
        call_stats_callback = call_statistics_queue.put
    else:
        call_stats_callback = open(call_statistics_filename, 'a').write

    forks = Forks(num_philosophers, Semaphore)
    tasks = [
        Environment(target=Philosopher(i, forks).dine, args=[lifetime_in_sec, call_stats_callback])
        for i in range(num_philosophers)]
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()

    if use_processes:
        with open(call_statistics_filename, 'w') as call_statistics_file:
            while not call_statistics_queue.empty():
                call_statistics_file.write(call_statistics_queue.get())
