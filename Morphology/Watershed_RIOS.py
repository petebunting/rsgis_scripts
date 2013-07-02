#/usr/bin/ python

import numpy as np
from scipy import ndimage
import scipy.ndimage.filters as filters
import scipy.ndimage.morphology as morphology

import sys

import optparse

from rios.imagereader import ImageReader
from rios.imagewriter import ImageWriter

inputs = list()
inputs.append("/Users/pete/Temp/Hyperforest/Kersselaerspleyn_LiDAR_05m_pmfgrd_chmNN_median5_morphgrad_minima.env")
inputs.append("/Users/pete/Temp/Hyperforest/Kersselaerspleyn_LiDAR_05m_pmfgrd_chmNN_median5_morphgrad.env")

outfile = "/Users/pete/Temp/Hyperforest/Kersselaerspleyn_LiDAR_05m_pmfgrd_chmNN_median5_watershed.img"

reader = ImageReader(inputs, windowxsize=1000, windowysize=1000, overlap=100)
writer = None
# read through each block and apply scaling
# and write into output file
for (info, blocks) in reader:
    block1,block2 = blocks
    seeds = np.int32(block1)
    grad = np.uint16(block2)

    out = np.expand_dims(ndimage.watershed_ift(grad[0], seeds[0]),0)

    if writer is None:
        writer = ImageWriter(outfile, info=info, firstblock=out)
    else:
        writer.write(out)
    print info.getPercent(), '%\r',
print '100%\r',

writer.close(calcStats=False)
