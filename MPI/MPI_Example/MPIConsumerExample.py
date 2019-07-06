#!/usr/bin/env python
import numpy as np
import time
from mpi4py import MPI
from basic import consumer, do_something, nr_dim, nr_instances

READY, START, DONE, EXIT = 0, 1, 2, 3
comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
status = MPI.Status()

def consumer_daemon():
    name = MPI.Get_processor_name()
    while True:
        comm.send(None, dest=0, tag=READY)
        task = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()

        if tag == START:
            instances = task
            global_vector = np.zeros(nr_dim)
            for instance in instances:
                global_vector += consumer()
            comm.send(global_vector, dest=0, tag=DONE)
        elif tag == EXIT:
            break
    comm.send(None, dest=0, tag=EXIT)

def producer():
    instances = range(nr_instances)
    L = len(instances)
    fence = L/ (size - 1)
    arguments = [(instances[i*fence:(L if i+1==size-1 else (i+1)*fence)]) for i in xrange(size - 1)]
    for i in xrange(1, size):
        comm.send(arguments[i-1], dest=i, tag=START)
    finished = 0
    global_vector = np.zeros(nr_dim)
    while finished < size - 1:
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()
        if tag == DONE:
            global_vector += data
            finished += 1
    do_something(global_vector)

if __name__=="__main__":
    if rank == 0:
        for i in xrange(5):
            producer()
            print("iter %d is done." % i)
        for i in xrange(1, size):
            comm.send(None, dest=i, tag=EXIT)
    else:
        consumer_daemon()