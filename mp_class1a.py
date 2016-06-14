#!/usr/bin/env python
# https://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma
# Eric H #2
# Overriding __call__ restricts class to only being able to use 1 method
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ApplyResult

class Myclass(object):

    def __init__(self, nobj, workers=cpu_count()):

        print "Constructor ..."
        # multiprocessing
        pool = Pool(processes=workers)
        async_results = [ pool.apply_async(self, (i,)) for i in range(nobj) ]
        pool.close()
        # waiting for all results
        map(ApplyResult.wait, async_results)
        lst_results=[r.get() for r in async_results]
        print lst_results

    def __call__(self, i):
        return self.process_obj(i)

    def __del__(self):
        print "... Destructor"

    def process_obj(self, i):
        print "obj %d" % i
        return "result"

Myclass(nobj=8, workers=3)
# problem !!! the destructor is called nobj times (instead of once), 
# **and** results are empty !
