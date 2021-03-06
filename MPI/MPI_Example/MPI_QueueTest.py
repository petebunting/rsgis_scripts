#!/usr/bin/env python
"""Demonstrate the task-pull paradigm for high-throughput computing
using mpi4py. Task pull is an efficient way to perform a large number of
independent tasks when there are more tasks than processors, especially
when the run times vary for each task. 
This code is over-commented for instructional purposes.
This example was contributed by Craig Finch (cfinch@ieee.org).
Inspired by http://math.acadiau.ca/ACMMaC/Rmpi/index.html
"""
from __future__ import print_function

from mpi4py import MPI
import glob
import os.path
import rsgislib
import rsgislib.imageutils
import rsgislib.imagefilter

def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START')

# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object

if rank == 0:
    tiledImg = False
    if not tiledImg:
        inImg = "/scratch/pete.bunting/Sen2UKARD/Outputs/UKSentinel2A_20170505/SEN2_20170505_lat60lon202_T30VWM_osgb_vmsk_sharp_rad_toa.kea"
        baseImg = "/home/pete.bunting/mpitest/tiles/SEN2_20170505_tile"
        rsgislib.imageutils.createTiles(inImg, baseImg, 1000, 1000, 50, False, 'KEA', rsgislib.TYPE_16UINT, 'kea')
        tiledImg = True
        
    tileFiles = glob.glob(baseImg+'*.kea')
    resultsFiles = []
    
    # Master process executes code below
    tasks = len(tileFiles)
    task_index = 0
    num_workers = size - 1
    closed_workers = 0
    print("Master starting with %d workers" % num_workers)
    while closed_workers < num_workers:
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        tag = status.Get_tag()
        if tag == tags.READY:
            # Worker is ready, so send it a task
            if task_index < tasks:
                comm.send(tileFiles[task_index], dest=source, tag=tags.START)
                print("Sending task %d to worker %d" % (task_index, source))
                task_index += 1
            else:
                comm.send(None, dest=source, tag=tags.EXIT)
        elif tag == tags.DONE:
            print('Result: \'' + data + '\'')
            resultsFiles.append(data)
            print("Got data from worker %d" % source)
        elif tag == tags.EXIT:
            print("Worker %d exited." % source)
            closed_workers += 1
    
    outImg = "SEN2_20170505_lat60lon202_T30VWM_osgb_vmsk_sharp_rad_toa_median.kea"
    rsgislib.imageutils.createCopyImage(inImg, outImg, 10, 0, 'KEA', rsgislib.TYPE_16UINT)
    rsgislib.imageutils.includeImagesWithOverlap(outImg, resultsFiles, 50)

    print("Master finishing")
else:
    # Worker processes execute code below
    name = MPI.Get_processor_name()
    print("I am a worker with rank %d on %s." % (rank, name))
    while True:
        comm.send(None, dest=0, tag=tags.READY)
        tskImg = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()
        
        if tag == tags.START:
            outImg = os.path.join('/home/pete.bunting/mpitest/medTiles', os.path.splitext(os.path.basename(tskImg))[0]+'_med.kea')
            rsgislib.imagefilter.applyMedianFilter(tskImg, outImg, 3, "KEA", rsgislib.TYPE_16UINT)
            comm.send(outImg, dest=0, tag=tags.DONE)
        elif tag == tags.EXIT:
            break

    comm.send(None, dest=0, tag=tags.EXIT)


