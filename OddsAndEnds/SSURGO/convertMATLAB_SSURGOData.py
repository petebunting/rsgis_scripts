#!/usr/bin/env python
#
# Script to convert MATLAB format processed SSURGO data
# used in AirMOSS processing to GDAL format
# 
# Dan Clewley (daniel.clewley@gmail.com)
# 25/02/2014
#
# Adapted from convertHDFSSURGOData.py
# 
# Lines for calculating band statistics taken from:
# http://www.jeremymsmith.us/davidson/NDVI.py

import sys, re
import gdal, osr
import numpy as np
from scipy import io
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inmat", type=str, help="Input data (MATLAB format)",required=True)
parser.add_argument("--claysand", action='store_true', default=False, help="Input is CL_SA layer")
parser.add_argument("--bulkdens", action='store_true', default=False, help="Input is BULKDE layer")
parser.add_argument("--depth", action='store_true', default=False, help="Input is DEPTH2TOP_DEPTH2BOT layer")
parser.add_argument("--src_nodataval", type=float, default=-9999, help="No data value for input (default is -9999)")
parser.add_argument("--dst_nodataval", type=float, default=None, help="No data value for output (default is same as input)")

args = parser.parse_args()    

inMATFile = args.inmat

if args.claysand:
    inputLayers = ['TEMP_CL','TEMP_SA']
elif args.depth:
    inputLayers = ['TEMP_DEPTH2BOT','TEMP_DEPTH2TOP']
elif args.bulkdens:
    inputLayers = ['TEMP_BULKDENS','TEMP_SI']
else:
    print('File type not recognised / provided')
    sys.exit()

numLayers = len(inputLayers)

# Read in data
print('Reading in data')
soildata = io.loadmat(inMATFile)

# GET GEOSPATIAL INFORMATION
geoTransform = []
for i in range(6):
    geoTransform.append(0.0)

# Set image size
inXSize = np.array(soildata[inputLayers[0]]).shape[2]
inYSize = np.array(soildata[inputLayers[0]]).shape[1]

minLon = np.min(soildata['lonsLGE'])
maxLon = np.max(soildata['lonsLGE'])
minLat = np.min(soildata['latsLGE'])
maxLat = np.max(soildata['latsLGE'])

# Get pixel resolution
pixelX = (maxLon - minLon) / float(inXSize)
pixelY = (minLat - maxLat) / float(inYSize)

geoTransform[0] = minLon # top left x 
geoTransform[1] = pixelX
geoTransform[2] = 0
geoTransform[3] = maxLat + (pixelY / 2.0)# top left y 
geoTransform[4] = 0
geoTransform[5] = pixelY

srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")

# Loop through input layers
for layer in range(numLayers):
    layerName = inputLayers[layer]
   
    outFileName = re.sub('\.mat','',inMATFile) + '_' +layerName + '_kea.kea'
    print('Saving ' + str(layer+1) + '/' + str(numLayers) + ': ' + layerName + ' to: ' + outFileName)

    numBands = soildata[layerName].shape[0]
    
    # Creat output image
    driver = gdal.GetDriverByName("KEA")
    metadata = driver.GetMetadata()
    newDataset = driver.Create(outFileName, inXSize, inYSize, numBands, gdal.GDT_Float32)
    newDataset.SetGeoTransform(geoTransform)
    newDataset.SetProjection(srs.ExportToWkt())

    for band in range(numBands):
        outData = soildata[layerName][band]

        if args.dst_nodataval is not None:
            outData = np.where(outData == args.src_nodataval,args.dst_nodataval,outData)

        newDataset.GetRasterBand(band+1).WriteArray(outData)
        # Calculate stats
        stat = newDataset.GetRasterBand(band+1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
        newDataset.GetRasterBand(band+1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band

    # Close dataset
    newDataset = None
