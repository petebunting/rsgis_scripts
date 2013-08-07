# A script to calculate slope from an image in degres
#
# Dan Clewley (daniel.clewley@gmail.com) - 26/06/2013
#
# Adapted from EASI code by Jane Whitcomb
#

import sys,os
from rios import imagereader
from rios.imagewriter import ImageWriter

import numpy as np
from math import sqrt
from scipy import stats

useFortranSlope=True
try:
    import slope
except ImportError:
    useFortranSlope=False
    print("Couldn't import fortran slope class - will be about 50 x slower!")

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
    
if len(sys.argv) != 3:
    print('''ERROR: Not enough parameters provided.
Usage:
calcSlopeDegrees.py inImage outImage''')
    sys.exit()

inImage = sys.argv[1]
outImage = sys.argv[2]

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

# Close and calculate stats (for faster display)
print("Writing stats...")
writer.close(calcStats=True)
print("Done")


