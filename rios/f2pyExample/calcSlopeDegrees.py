#! /usr/bin/env python
####################################################################################
# calcSlopeDegrees.py
#
# A Python script to calculate slope from a DEM, where the horizontal spacing is in degrees
# latitude and longitude.
#
# Requires RIOS (https://bitbucket.org/chchrsc/rios/) to read image
#
# The base slope calculation is in Python. If Numba (http://numba.pydata.org)
# is available this is used to improve speed.
# For the best speed a Fortran function (slope.f) is available to perform the slope calculation.
# This must be compiled using:
#
# f2py -c slope.f -m slope
# 
# Dan Clewley (daniel.clewley@gmail.com) - 26/06/2013
#
# Adapted from EASI code by Jane Whitcomb
#
#
# Copyright 2014 Daniel Clewley & Jane Whitcomb.
# 
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
####################################################################################

import sys,os
from rios import imagereader
from rios.imagewriter import ImageWriter

import numpy as np
from math import sqrt

useFortranSlope=True

try:
    import slope
except ImportError:
    useFortranSlope=False

try:
    from numba import autojit
    if useFortranSlope:
        print('Numba is available - using Fortran module instead')
    else:
        print('Fortran module not available - using Numba instead')
except ImportError:
    if not useFortranSlope:
        print('Warning: Could not import Numba or Fortran slope module - will be about 50 x slower!')
    else:
        print('Fortran module is available')
    # have to define our own autojit so Python doesn't complain
    def autojit(func):
        return func

@autojit
def slopePython(inBlock, inXSize, inYSize, zScale):

    """ Calculate slope using Python.
        If Numba is available will make use of autojit function
        to provide similar speed to Fortran module. if not will fall
        back to pure Python - which will be slow.
    """
    
    outBlock = np.zeros_like(inBlock, dtype=np.float32)

    for x in range(1,inBlock.shape[2]-1):
        for y in range(1, inBlock.shape[1]-1):
            # Get pixel size (offset by one due to overlap)
            dx = 2 * inXSize[y,x]
            dy = 2 * inYSize[y,x]
            # Calculate difference in elevation
            dzx = (inBlock[0,y,x-1] - inBlock[0,y,x+1])*zScale
            dzy = (inBlock[0,y-1,x] - inBlock[0,y+1,x])*zScale
    
            # Find normal vector to the plane
            nx = -1 * dy * dzx
            ny = -1 * dx * dzy
            nz = dx * dy
    
            slopeRad = np.arccos(nz / sqrt(nx**2 + ny**2 + nz**2))
            slopeDeg = (180. / np.pi) * slopeRad
    
            outBlock[0,y,x] = slopeDeg
   
    return outBlock

def calcSlope(inBlock, inXSize, inYSize, zScale = 1):
    """ Calculates slope for a block of data
        Blocks of data are provided giving the size for
        each pixel
    """

    if useFortranSlope:
        # If fortran class could be imported use this
        outBlock = slope.slope(inBlock[0], inXSize, inYSize, zScale)
        # Add third dimension (required by rios)
        outBlock = outBlock.reshape(1, outBlock.shape[0], outBlock.shape[1])
        # Cast to 32 bit float (rather than 64 bit numpy default)
        outBlock = outBlock.astype(np.float32)

    else:
        # Otherwise run through loop in python (which will be slower)
        outBlock = slopePython(inBlock, inXSize, inYSize, zScale)

    return(outBlock)

def getPixelSize(lat, latsize, lonsize):
    """ Get the pixel size (in m) based on latitude and
        pixel size in degrees
    """

    # Set up parameters for elipse
    # Semi-major and semi-minor for WGS-84 ellipse
    ellipse = [6378137.0, 6356752.314245]
    
    radlat = np.deg2rad(lat)
    
    Rsq = (ellipse[0]*np.cos(radlat))**2+(ellipse[1]*np.sin(radlat))**2
    Mlat = (ellipse[0]*ellipse[1])**2/(Rsq**1.5)
    Nlon = ellipse[0]**2/np.sqrt(Rsq)
    xsize = np.pi/180*np.cos(radlat)*Nlon*lonsize
    ysize = np.pi/180*Mlat*latsize

    return xsize, ysize
    
if len(sys.argv) < 3:
    print('''ERROR: Not enough parameters provided.
Usage:
calcSlopeDegrees.py inImage outImage [--nostats]''')
    sys.exit()

inImage = sys.argv[1]
outImage = sys.argv[2]

calcStats = True
if (len(sys.argv) == 4) and (sys.argv[3] == '--nostats'):
    calcStats = False

reader = imagereader.ImageReader(inImage, overlap=1)

writer = None

print("Starting...")

for (info, inBlock) in reader:

    # Get percent complete
    sys.stdout.write("\r %i Percent Complete"%(int(info.getPercent())))

    # Get coordinates for block
    xCoords, yCoords = info.getBlockCoordArrays()

    # Convert to pixel sizes
    xres, yres = info.getPixelSize()
    xSize, ySize = getPixelSize(yCoords, xres, yres)

    outBlock = calcSlope(inBlock, xSize, ySize, 1)

    # Check if writer exists, create one if not.
    if writer is None:
        writer = ImageWriter(outImage, info=info, firstblock=outBlock) 
    else:
        writer.write(outBlock)

sys.stdout.write("\r 100 Percent Complete\n")

if calcStats:
    # Close and calculate stats (for faster display)
    print("Writing stats...")
    writer.close(calcStats=True)
else:
    writer.close(calcStats=False)
print("Done")


