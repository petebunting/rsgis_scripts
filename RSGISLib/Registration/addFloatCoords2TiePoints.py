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
import numpy as np
import csv

if len(sys.argv) != 4:
    print '''Not enough parameters provided.
Usage:
    python addFloatCoords2TiePoints.py inImageFile inTiePointFile.csv outTiePointFile.csv
'''
    exit()

inImageFile = sys.argv[1]
inGCPFile = sys.argv[2]
outGCPFile = sys.argv[3]

# Get information from image
dataset = gdal.Open(inImageFile, gdal.GA_ReadOnly )
projection = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
xSize = dataset.RasterXSize
ySize = dataset.RasterYSize

# Get geoinfo from image
minX = geotransform[0]
maxY = geotransform[3]
pixSizeX = geotransform[1]
pixSizeY = geotransform[5]
maxX = minX + (xSize * pixSizeX)
minY = maxY + (ySize * pixSizeY)

try:
    inGCPs = np.genfromtxt(inGCPFile, delimiter=',', comments='#')
except IOError:
    print 'ERROR: In text file contains no points!'
    exit()

try:
    floatXCoords = minX + (inGCPs[:,2] * pixSizeX) 
    floatYCoords = maxY + (inGCPs[:,3] * pixSizeY) 
    
    # Calculate differences
    diffX = floatXCoords - inGCPs[:,0]
    diffY = floatYCoords - inGCPs[:,1]
    
    diffXPix = diffX / pixSizeX
    diffYPix = diffY / pixSizeY
    
    phaseDiffPix = np.arctan(abs(diffYPix) / abs(diffXPix)) * 180. / np.pi
    
    phaseDiffPix = np.where(np.logical_and(diffXPix < 0, diffYPix < 0) ,phaseDiffPix + 180.,phaseDiffPix)
    phaseDiffPix = np.where(np.logical_and(diffXPix < 0, diffYPix > 0) ,phaseDiffPix + 90, phaseDiffPix)
    phaseDiffPix = np.where(np.logical_and(diffXPix > 0, diffYPix < 0) ,phaseDiffPix + 270, phaseDiffPix)
        
        
    
    powerDiffPix = np.sqrt((diffXPix + diffYPix)**2)
    
    sqDiffX = (inGCPs[:,0] - floatXCoords)**2
    sqDiffY = (inGCPs[:,1] - floatYCoords)**2
    
    rmseX = np.sqrt(np.average(sqDiffX))
    rmseY = np.sqrt(np.average(sqDiffY))
    
    print 'RMSE (map units): x', rmseX, ', y', rmseY
    print 'RMSE (pixels): x', rmseX / pixSizeX, ', y', rmseY / np.abs(pixSizeY)
    
    # Write data out to CSV file
    outGCPs = csv.writer(open(outGCPFile,'w'))
    
    outGCPs.writerow(['baseE','baseN','floatE','floatN','diffE','diffN','diffXPix','diffYPix','powerPixDiff','phasePixDiff'])
    
    for i in range(inGCPs.shape[0]):
        outGCPs.writerow([inGCPs[i,0],inGCPs[i,1],floatXCoords[i], floatYCoords[i], diffX[i], diffY[i], diffXPix[i],diffYPix[i], powerDiffPix[i], phaseDiffPix[i]])

except IndexError:
    print 'ERROR: Not enough columns in infile'


