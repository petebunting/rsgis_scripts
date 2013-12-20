#!/usr/bin/env python
#
# Script to read JPL format AirMOSS data (HDF5)
# and write out as KEA format
#
# Dan Clewley (clewley@usc.edu)
# 19/12/2013
#
# Modified from code to gerate geotiff from HDF5 files
# Dan Clewley
# 20/08/12
#
# Lines for calculating band statistics taken from:
# http://www.jeremymsmith.us/davidson/NDVI.py

import sys, re
import h5py, gdal, osr
import numpy as np

if len(sys.argv) < 2:
    print('Error: No input file provided')
    sys.exit()
inHDF5File = sys.argv[1]

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

outFileName = re.sub('\.h5','',inHDF5File) + '_kea.kea'
print('Saving to {}'.format(outFileName))

numBands = numLayers
    
# Creat output image
driver = gdal.GetDriverByName("KEA")
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
