#!/usr/bin/env python
#
# Script to read JPL format AirMOSS data (HDF5)
# and write out as GDAL format.
#
# Usage:
# python convertAirMOSS2GDAL.py in.h5 out.tif
#
# Dan Clewley (clewley@usc.edu)
# 11/11/2013
#
# Lines for calculating band statistics taken from:
# http://www.jeremymsmith.us/davidson/NDVI.py
#
# Copyright 2014 Daniel Clewley. All rights reserved.
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

import sys, re, os
import h5py, gdal, osr
import numpy as np
import argparse

def getGDALFormatFromExt(fileName):
    """ Get GDAL format, based on filename """
    gdalStr = ''
    extension = os.path.splitext(fileName)[-1] 
    if extension == '.env':
        gdalStr = 'ENVI'
    elif extension == '.kea':
        gdalStr = 'KEA'
    elif extension == '.tif' or extension == '.tiff':
        gdalStr = 'GTiff'
    elif extension == '.img':
        gdalStr = 'HFA'
    elif extension == '.pix':
        gdalStr = 'PCIDSK'
    else:
        raise Exception('Type not recognised')
    
    return gdalStr

# Get input parameters
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inimage", type=str, help="Input image",required=True)
parser.add_argument("-o", "--outimage", type=str, help="Output image", required=True)
args = parser.parse_args() 


inHDF5File = args.inimage
outFileName = args.outimage

inputLayers = ['HHHH','VVVV','HVHV']

numLayers = len(inputLayers)

# Read in data
indata = h5py.File(inHDF5File)

# GET GEOSPATIAL INFORMATION
geoTransform = []
for i in range(6):
    geoTransform.append(0.0)

# Set image size
inXSize = np.array(indata[inputLayers[0]]).shape[1]
inYSize = np.array(indata[inputLayers[0]]).shape[0]

minLon = indata.attrs['northwest longitude'] 
maxLat = indata.attrs['northwest latitude']

# Get pixel resolution
pixelX = indata.attrs['longitude spacing']
pixelY = indata.attrs['latitude spacing']

geoTransform[0] = minLon # top left x 
geoTransform[1] = pixelX
geoTransform[2] = 0
geoTransform[3] = maxLat # top left y 
geoTransform[4] = 0
geoTransform[5] = pixelY

srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")

print('Saving to {}'.format(outFileName))

numBands = numLayers
    
# Creat output image
gdalDriver = getGDALFormatFromExt(outFileName)
driver = gdal.GetDriverByName(gdalDriver)
metadata = driver.GetMetadata()
newDataset = driver.Create(outFileName, inXSize, inYSize, numBands, gdal.GDT_Float32)
newDataset.SetGeoTransform(geoTransform)
newDataset.SetProjection(srs.ExportToWkt())

# Loop through input layers
for layer in range(numLayers):
    layerName = inputLayers[layer]
    
    outData = np.array(indata[layerName])
    outData = np.where(outData < -9998,0,outData)

    # Write out data
    newDataset.GetRasterBand(layer+1).WriteArray(outData)
    
    # Set layer name
    newDataset.GetRasterBand(layer+1).SetDescription(layerName)
    # Calculate stats
    stat = newDataset.GetRasterBand(layer+1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
    newDataset.GetRasterBand(layer+1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band

# Close dataset
newDataset = None
