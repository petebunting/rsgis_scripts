# Code to gerate geotiff from HDF5 files
# Dan Clewley
# 20/08/12

# Lines for calculating band statistics taken from:
# http://www.jeremymsmith.us/davidson/NDVI.py

import sys
import h5py, gdal, osr
import numpy as np

inHDF5File = sys.argv[1] #'/home/danclewley/Documents/Temp/ssurgo_tonzi/ca067.h5'
outGEOTiff = sys.argv[2] #'/home/danclewley/Documents/Temp/ssurgo_tonzi/ca067_tif.tif'

inputLayers = ['K_o','K_sat','L_parameter','N_parameter','alpha','bulk_density_0.33bar', 'depth_to_bottom','depth_to_top','horizon_thickness','percent_clay','percent_sand','percent_silt','theta_res','theta_sat','water_retention_0.33bar','water_retention_15bar']

numBands = len(inputLayers)

# Read in data
soildata = h5py.File(inHDF5File)

# List available datasets
#list(soildata)

# Get geospatial information
geoTransform = []
for i in range(6):
    geoTransform.append(0.0)

inXSize = np.array(soildata[inputLayers[0]]).shape[0]
inYSize = np.array(soildata[inputLayers[0]]).shape[1]

minLon = np.min(soildata['lons'])
maxLon = np.max(soildata['lons'])
minLat = np.min(soildata['lats'])
maxLat = np.max(soildata['lats'])

geoTransform[0] = minLon # top left x 
geoTransform[1] = (maxLon - minLon) / float(inXSize)
geoTransform[2] = 0
geoTransform[3] = maxLat # top left y 
geoTransform[4] = 0
geoTransform[5] = (minLat - maxLat) / float(inYSize)

srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")

# Creat output image
driver = gdal.GetDriverByName("KEA")
metadata = driver.GetMetadata()
newDataset = driver.Create(outGEOTiff, inXSize, inYSize, numBands, gdal.GDT_Float32)
newDataset.SetGeoTransform(geoTransform)
newDataset.SetProjection(srs.ExportToWkt())

for band in range(numBands):
    layerName = inputLayers[band]
    
    print 'Saving ' + str(band+1) + '/' + str(numBands) + ': ' + layerName    

    outArray = []

    for line in soildata[layerName]:
        outLine = []
        for pixel in line:
            if pixel[0] == -9999:
                outLine.append(0.)
            else:
                outLine.append(pixel[0])
        outArray.append(outLine)

    outArray = np.array(outArray)
    if outArray.shape[0] != inYSize:
        outArray = np.transpose(outArray)

    newDataset.GetRasterBand(band+1).WriteArray(outArray)
    # Calculate stats
    stat = newDataset.GetRasterBand(band+1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
    newDataset.GetRasterBand(band+1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band
    # Set output name
    newDataset.GetRasterBand(band+1).SetDescription(layerName)

# Build overview images
newDataset.BuildOverviews()
# Close dataset
newDataset = None
