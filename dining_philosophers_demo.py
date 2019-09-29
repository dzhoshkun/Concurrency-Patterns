from argparse import ArgumentParser, ArgumentTypeError

from dining_philosophers import Philosopher, Multiplex
from dining_philosophers import LeftiesRighties
from utils import human_readable_timestamp


def algorithm(arg):
    arg_ = arg.lower()
    if arg_ == 'lefties-righties':
        return LeftiesRighties, arg
    elif arg_ == 'multiplex':
        return Multiplex, arg
    raise ArgumentTypeError('Dining philosophers algorithm %s unknown' % arg)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    env_group = arg_parser.add_mutually_exclusive_group(required=True)
    env_group.add_argument('-p', '--processes', action='store_true', help='Run each philosopher as a different process')
    env_group.add_argument('-t', '--threads', action='store_true', help='Run each philosopher as a different thread')
    arg_parser.add_argument('-a', '--algorithm', type=algorithm,
                            help='Which solution algorithm to use, options are: lefties-righties, multiplex')
    arg_parser.add_argument('-n', '--philosophers', type=int, required=True, help='Number of philosophers')
    arg_parser.add_argument('-l', '--lifetime', type=float, required=True, help='Each philosopher\'s lifetime in secs')
    arg_parser.add_argument('-o', '--stats-filename', type=str, required=True,
                            help='Output filename prefix (human-readable timestamp appended) for saving call stats'
                                 ' in CSV format')
    args = arg_parser.parse_args()

    use_processes = args.processes
    if use_processes:
        from multiprocessing import Process as Environment, Semaphore, Queue
        call_statistics_queue = Queue()
    else:
        from threading import Thread as Environment, Semaphore

    num_philosophers = args.philosophers
    lifetime_in_sec = args.lifetime

    call_statistics_filename = args.stats_filename + '-'
    if use_processes:
        call_statistics_filename += 'processes-'
    else:
        call_statistics_filename += 'threads-'
    call_statistics_filename += args.algorithm[1] + '-'
    call_statistics_filename += human_readable_timestamp() + '.csv'
    if use_processes:
        call_stats_callback = call_statistics_queue.put
    else:
        call_stats_callback = open(call_statistics_filename, 'a').write

    forks = args.algorithm[0](num_philosophers, Semaphore)
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
