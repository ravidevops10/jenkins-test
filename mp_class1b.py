#!/usr/bin/env python
# https://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma
# Eric H #1
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ApplyResult

# --------- see Stenven's solution above -------------
from copy_reg import pickle
from types import MethodType

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


# put process_obj() into another class and see what happens
class MyProc(object):
    def __init__(self):
        pass
# fails as class method
    def process_obj(self, index):
        print "object %d" % index
        return "results"
    def __del__(self):
        print MyProc.__name__, "Destructor"

class Myclass(object):

    def __init__(self, nobj, workers=cpu_count()):

        print "Constructor ..."
        # multi-processing
        pool = Pool(processes=workers)
        p = MyProc()
        async_results = [ pool.apply_async(p.process_obj, (i,)) for i in range(nobj) ]
        pool.close()
        # waiting for all results
        map(ApplyResult.wait, async_results)
        lst_results=[r.get() for r in async_results]
        print lst_results

    def __del__(self):
        print Myclass.__name__ , "... Destructor"

pickle(MethodType, _pickle_method, _unpickle_method)
Myclass(nobj=8, workers=3)
# problem !!! the destructor is called nobj times (instead of once)
