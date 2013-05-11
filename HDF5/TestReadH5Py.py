 #! /usr/bin/env python

#######################################
#
#
# Email: petebunting@mac.com
# Date: 04/04/2013
# Version: 1.0
#######################################

import numpy as np
import h5py
import sys
import matplotlib.pyplot as plt

def plot(data, x, y):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(data[...,x], data[...,y])
    plt.show()




def run():
    file = 'OriginalMoscaic_sample.hdf'
    if not h5py.is_hdf5(file):
        print "It was not a hdf5 file."
        sys.exit()
    
    f = h5py.File(file,'r')

    dset = f['/DATA/DATA']
    
    plot(dset, 1, 2)
    
    f.close()
    
if __name__ == '__main__':
    run()