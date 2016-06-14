#!/usr/bin/env python
# http://stackoverflow.com/questions/3288595/multiprocessing-using-pool-map-on-a-function-defined-in-a-class
# user753720
from multiprocessing import Pool
import itertools

#--util.py----------------------------------------------------------------------------------------------------
def add(a, b): return a+b
   
def eval_func_tuple(f_args):
   """Takes a tuple of a function and args, evaluates and returns result"""
   return f_args[0](*f_args[1:])  
#^^^^^^^^^util.py^^^^
pool = Pool()
class Example(object):
    def __init__(self, my_add): 
        self.f = my_add  
    def add_lists(self, list1, list2):
        # The following line will now work
        return pool.map(eval_func_tuple, 
            itertools.izip(itertools.repeat(self.f), list1, list2)) 

if __name__ == '__main__':
    myExample = Example(add)
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]
    print myExample.add_lists(list1, list2)  
