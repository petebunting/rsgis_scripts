from mpi4py import MPI
import argparse
import numpy
from arcsilib.arcsiutils import ARCSIEnum
import sys

# Define MPI message tags
mpiTags = ARCSIEnum('READY', 'DONE', 'EXIT', 'START')

arcsiStages = ARCSIEnum('ARCSIPART1', 'ARCSIPART2', 'ARCSIPART3', 'ARCSIPART4')

# Initializations and preliminaries
mpiComm = MPI.COMM_WORLD    # get MPI communicator object
mpiSize = mpiComm.size      # total number of processes
mpiRank = mpiComm.rank      # rank of this process
mpiStatus = MPI.Status()    # get MPI status object


print("Rank: " + str(mpiRank))
if (__name__ == '__main__') and (mpiRank == 0):
    
    paramsLst = numpy.arange(100)
    
    paramsLstTmp = []
    nTasks = len(paramsLst)
    taskIdx = 0
    completedTasks = 0
    while completedTasks < nTasks:
        print("completedTasks = ", completedTasks)
        print("nTasks = ", nTasks)
        rtnParamsObj = mpiComm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=mpiStatus)
        source = mpiStatus.Get_source()
        tag = mpiStatus.Get_tag()
        print("Source: ", source)
        if tag == mpiTags.READY:
            # Worker is ready, so send it a task
            if taskIdx < nTasks:
                mpiComm.send([arcsiStages.ARCSIPART1, paramsLst[taskIdx]], dest=source, tag=mpiTags.START)
                print("Sending task %d to worker %d" % (taskIdx, source))
                taskIdx += 1
            #else:
            #    mpiComm.send(None, dest=source, tag=mpiTags.EXIT)
        elif tag == mpiTags.DONE:
            print("Got data from worker %d" % source)
            paramsLstTmp.append(rtnParamsObj)
            completedTasks += 1
        elif tag == tags.EXIT:
            print("Worker %d exited." % source)
            closedWorkers += 1
            #raise ARCSIException("MPI worker was closed - worker was still needed so there is a bug here somewhere... Please report to mailing list.")
    paramsLst = paramsLstTmp
    print(paramsLst)
    
    
    paramsLstTmp = []
    nTasks = len(paramsLst)
    taskIdx = 0
    completedTasks = 0
    while completedTasks < nTasks:
        print("completedTasks = ", completedTasks)
        print("nTasks = ", nTasks)
        rtnParamsObj = mpiComm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=mpiStatus)
        source = mpiStatus.Get_source()
        tag = mpiStatus.Get_tag()
        print("Source: ", source)
        if tag == mpiTags.READY:
            # Worker is ready, so send it a task
            if taskIdx < nTasks:
                mpiComm.send([arcsiStages.ARCSIPART4, paramsLst[taskIdx]], dest=source, tag=mpiTags.START)
                print("Sending task %d to worker %d" % (taskIdx, source))
                taskIdx += 1
            #else:
            #    mpiComm.send(None, dest=source, tag=mpiTags.EXIT)
        elif tag == mpiTags.DONE:
            print("Got data from worker %d" % source)
            paramsLstTmp.append(rtnParamsObj)
            completedTasks += 1
        elif tag == tags.EXIT:
            print("Worker %d exited." % source)
            closedWorkers += 1
            #raise ARCSIException("MPI worker was closed - worker was still needed so there is a bug here somewhere... Please report to mailing list.")
    
    for workerID in range(mpiSize):
        if workerID > 0:
            mpiComm.send(None, dest=workerID, tag=mpiTags.EXIT)            
    
else:
    print("ELSE not main: ", mpiRank)
    
    # Worker processes execute code below
    while True:
        mpiComm.send(None, dest=0, tag=mpiTags.READY)
        tskData = mpiComm.recv(source=0, tag=MPI.ANY_TAG, status=mpiStatus)
        tag = mpiStatus.Get_tag()
        paramsObj = None
        
        print(tskData)
        print(tag)

        if tag == mpiTags.START:
            # Do work!
            if tskData[0] == arcsiStages.ARCSIPART1:
                print('PART #1')
                paramsObj = tskData[1] * 10
            elif tskData[0] == arcsiStages.ARCSIPART2:
                print('PART #2')
                paramsObj = tskData[1] * 20
            elif tskData[0] == arcsiStages.ARCSIPART3:
                print('PART #3')
                paramsObj = tskData[1] * 30
            elif tskData[0] == arcsiStages.ARCSIPART4:
                print('PART #4')
                paramsObj = tskData[1] * 40
            else:
                raise ARCSIException("Don't recognise processing stage")

            mpiComm.send(paramsObj, dest=0, tag=mpiTags.DONE)
        elif tag == mpiTags.EXIT:
            break
    mpiComm.send(None, dest=0, tag=mpiTags.EXIT)
    


