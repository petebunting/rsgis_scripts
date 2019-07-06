#hello_mpi.py
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print("hello world from process %d/%d“ %(rank,size)")
