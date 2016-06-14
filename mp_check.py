from __future__ import print_function

import multiprocessing
import time

def worker():
    name = multiprocessing.current_process().name
    print (name, 'Starting')
    i = 0
    for i in range(20000000): i += 1
    print (name, 'Exiting')

if __name__ == '__main__':
    t = time.time
    workers = [ multiprocessing.Process(target=worker) for w in range(3) ]
    start = t()
    [w.start() for w in workers]
    [w.join() for w in workers]
    end = t()
    delta = end-start
    print("Summary: start time",start,"\n\tend ",end,"\n\telapsed",delta)

