#!/usr/bin/env python
# http://stackoverflow.com/questions/3288595/multiprocessing-using-pool-map-on-a-function-defined-in-a-class
# Bob McElrath
from multiprocessing import Process, Pipe
from itertools import izip

def spawn(f):
    def fun(ppipe, cpipe,x):
        ppipe.close()
        cpipe.send(f(x))
        cpipe.close()
    return fun

def parmap(f,X):
    pipe=[Pipe() for x in X]
    proc=[Process(target=spawn(f),args=(p,c,x)) for x,(p,c) in izip(X,pipe)]
    [p.start() for p in proc]
    ret = [p.recv() for (p,c) in pipe]
    [p.join() for p in proc]
    return ret

if __name__ == '__main__':
    print parmap(lambda x:x**x,range(1,5))
