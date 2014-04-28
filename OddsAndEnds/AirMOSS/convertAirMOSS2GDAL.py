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
import warnings
warnings.simplefilter('ignore', RuntimeWarning) # Ignore warnings.

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
parser.add_argument("--gamma0",action='store_true',default=False, help="Output as gamma0 (default sigma0)", required=False)
parser.add_argument("--dB",action='store_true',default=False, help="Convert to dB", required=False)
parser.add_argument("--layer",action='append',default=None,required=False, help="Datalayers to export \
(if not using standard parameters). Choose any combination of, HHHH, HHHV, \
HHVV,HVHV,HVVV,VVVV,height,incidence_angle,slope")

args = parser.parse_args() 

inHDF5File = args.inimage
outFileName = args.outimage

if args.layer is None:
    inputLayers = ['HHHH','VVVV','HVHV']
else:
    inputLayers = []
    for layerName in args.layer:
        inputLayers.append(layerName)

numLayers = len(inputLayers)

# Read in data
indata = h5py.File(inHDF5File)

# GET GEOSPATIAL INFORMATION
geoTransform = []
for i in range(6):
    geoTransform.append(0.0)

# Set image size
try:
    inXSize = np.array(indata[inputLayers[0]]).shape[1]
    inYSize = np.array(indata[inputLayers[0]]).shape[0]
except KeyError:
    print('Could not find first layer: ',inputLayers[0])
    print('Available layers are:')
    for key in indata.keys():
        print('\t' + key)
    sys.exit()

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

if args.gamma0:
    localInc = indata['incidence_angle']

# Loop through input layers
for layer in range(numLayers):
    layerName = inputLayers[layer]
    print(' Saving ' + layerName)
    
    try:
        outData = np.array(indata[layerName])
        outData = np.where(outData < -9998,0,outData)

        if args.gamma0 and (layerName.find('H') or layerName.find('V')):
            outData = outData / np.cos(localInc)

        if args.dB and (layerName.find('H') or layerName.find('V')):
            outData = np.where(outData > 0,10*np.log10(outData),np.nan)

        # Write out data
        newDataset.GetRasterBand(layer+1).WriteArray(outData)
        
        # Set layer name
        newDataset.GetRasterBand(layer+1).SetDescription(layerName)
        # Calculate stats
        stat = newDataset.GetRasterBand(layer+1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
        newDataset.GetRasterBand(layer+1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band
    except KeyError:
        print('Could not find layer in H5 file')
        print('Available layers are:')
        for key in indata.keys():
            print('\t' + key)
    except Exception as err:
        print(err)

# Close dataset
newDataset = None
