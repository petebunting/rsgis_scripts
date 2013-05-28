#! /usr/bin/env python

###########################################################
# subsetImage2Image.py
# A script to subset and reproject an image to a base image
# using gdalwarp.
#
# Dan Clewley (daniel.clewley@gmail.com) - 15/02/2013
###########################################################

import os, sys
import osgeo.gdal as gdal

def getGDALFormat(fileName):
    """ Get GDAL format, based on filename """
    gdalStr = ''
    extension = os.path.splitext(fileName)[-1] 
    if extension == '.env':
        gdalStr = 'ENVI'
    elif extension == '.kea':
        gdalStr = 'KEA'
    elif extension == '.tif':
        gdalStr = 'GTiff'
    elif extension == '.img':
        gdalStr = 'HFA'
    elif extension == '.pix':
        gdalStr = 'PCIDSK'
    else:
        raise Exception('Type not recognised')
    
    return gdalStr

if len(sys.argv) < 4:
    print(''' The correct number of parameters was not provided.
== subsetImage2Image.py ==

Subsets and reprojects an image (inImage) to the same size and
projection of a base image (baseImage).

Usage:
    python subsetImage2Image.py baseImage inImage outImage [-print]

-print : Don't run, only print gdal_translate options.

''')
    exit()

inBaseFile = sys.argv[1]
inLargeImage = sys.argv[2]
outSubsetImage = sys.argv[3]

dummyRun = False

if len(sys.argv) == 5:
    if sys.argv[4] == '-print':
        dummyRun = True


# Get output format from name
outGDALFormat = getGDALFormat(outSubsetImage)

# Get information from image
dataset = gdal.Open(inBaseFile, gdal.GA_ReadOnly )
projection = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
xSize = dataset.RasterXSize
ySize = dataset.RasterYSize

# Get bounding box
minX = geotransform[0]
maxY = geotransform[3]
pixSizeX = geotransform[1]
pixSizeY = geotransform[5]
maxX = minX + (xSize * pixSizeX)
minY = maxY + (ySize * pixSizeY)

# Create gdalwarp command
ofStr = ' -of ' + outGDALFormat + ' '
bbStr = ' -te %s %s %s %s '%(minX, minY, maxX, maxY) 
resStr = ' -tr %s %s '%(pixSizeX, pixSizeY)
projectionStr = ''' -t_srs '%s' ''' %(projection)
overwriteStr = ' -overwrite ' # Overwrite output if it exists
additionalOptions = ' ' # Additional options
warpOptions = ofStr + bbStr + resStr + projectionStr + overwriteStr + additionalOptions

warpCMD = 'gdalwarp ' + warpOptions + inLargeImage + ' ' + outSubsetImage
if dummyRun:
    print(warpCMD)
else:
    os.system(warpCMD)

