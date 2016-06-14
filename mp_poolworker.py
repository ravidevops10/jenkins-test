#!/usr/bin/env python
# https://stackoverflow.com/questions/9038711/python-pool-with-worker-processes
#
import multiprocessing as mp
from multiprocessing import Pool, Process, Manager
import time


class Worker(Process):
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue= queue

    def run(self):
        print 'Worker {} started'.format(mp.current_process().name)
        # do some initialization here

        print 'Computing things!'
        for data in iter( self.queue.get, None ):
           time.sleep(.3)
           print 'Computing {}: {} '.format(mp.current_process().name,data*data)


if __name__ == "__main__":
   request_queue = Manager().Queue()
   for i in range(4):
       Worker( request_queue ).start()
   for data in range(10):
       request_queue.put( data )
   # Sentinel objects to allow clean shutdown: 1 per worker.
   for i in range(4):
       request_queue.put( None )
