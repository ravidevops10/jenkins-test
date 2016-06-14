#!/usr/bin/env python
# https://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma
# torek
import multiprocessing
import os

def call_it(instance, name, args=(), kwargs=None):
    "indirect caller for instance methods and multiprocessing"
    if kwargs is None:
        kwargs = {}
    return getattr(instance, name)(*args, **kwargs)

class Klass(object):
    def __init__(self, nobj, workers=multiprocessing.cpu_count()):
        print "Constructor (in pid=%d)..." % os.getpid()
        self.count = 1
        pool = multiprocessing.Pool(processes = workers)
        async_results = [pool.apply_async(call_it,
            args = (self, 'process_obj', (i,))) for i in range(nobj)]
        pool.close()
        map(multiprocessing.pool.ApplyResult.wait, async_results)
        lst_results = [r.get() for r in async_results]
        print lst_results

    def __del__(self):
        self.count -= 1
        print "... Destructor (in pid=%d) count=%d" % (os.getpid(), self.count)

    def process_obj(self, index):
        print "object %d" % index
        return "results"

Klass(nobj=8, workers=3)
