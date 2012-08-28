# Code to gerate geotiff from HDF5 files
# Dan Clewley
# 20/08/12

# Lines for calculating band statistics taken from:
# http://www.jeremymsmith.us/davidson/NDVI.py

import sys, re
import h5py, gdal, osr
import numpy as np

inHDF5File = sys.argv[1]

inputLayers = ['K_o','K_sat','L_parameter','N_parameter','alpha','bulk_density_0.33bar', 'depth_to_bottom','depth_to_top','horizon_thickness','percent_clay','percent_sand','percent_silt','theta_res','theta_sat','water_retention_0.33bar','water_retention_15bar']

numBands = len(inputLayers)

# Read in data
soildata = h5py.File(inHDF5File)

# GET GEOSPATIAL INFORMATION
geoTransform = []
for i in range(6):
    geoTransform.append(0.0)

# Set image size
inXSize = np.array(soildata[inputLayers[0]]).shape[0]
inYSize = np.array(soildata[inputLayers[0]]).shape[1]

minLon = np.min(soildata['lons'])
maxLon = np.max(soildata['lons'])
minLat = np.min(soildata['lats'])
maxLat = np.max(soildata['lats'])

# Get pixel resolution
pixelX = (maxLon - minLon) / float(inXSize)
pixelY = (minLat - maxLat) / float(inYSize)

geoTransform[0] = minLon # top left x 
geoTransform[1] = pixelX
geoTransform[2] = 0
geoTransform[3] = maxLat + (pixelY / 2.0)# top left y 
geoTransform[4] = 0
geoTransform[5] = pixelY

inXSize = np.array(soildata[inputLayers[0]]).shape[0]
inYSize = np.array(soildata[inputLayers[0]]).shape[1]

srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")

# Loop through input layers
for band in range(numBands):
    layerName = inputLayers[band]
   
    outFileName = re.sub('\.h5','',inHDF5File) + '_' +layerName + '_kea.kea'
    print 'Saving ' + str(band+1) + '/' + str(numBands) + ': ' + layerName + ' to: ' + outFileName

    numBands = len(soildata[layerName][0][0])
    
    # Creat output image
    driver = gdal.GetDriverByName("KEA")
    metadata = driver.GetMetadata()
    newDataset = driver.Create(outFileName, inXSize, inYSize, numBands, gdal.GDT_Float32)
    newDataset.SetGeoTransform(geoTransform)
    newDataset.SetProjection(srs.ExportToWkt())

    outArray = []
    for i in range(numBands):
        outArray.append([])

    for line in soildata[layerName]:
        outLine = []
        for i in range(numBands):
            outLine.append([])

        for pixel in line:
            for i in range(numBands):
                if pixel[i] == -9999:
                    outLine[i].append(0.)
                else:
                    outLine[i].append(pixel[i])

        for i in range(numBands):
           outArray[i].append(outLine[i])

    for i in range(numBands):
        outArray[i] = np.array(outArray[i])

    if outArray[0].shape[0] != inYSize:
        for i in range(numBands):
            outArray[i] = np.transpose(outArray[i])
    
    for band in range(numBands):
        newDataset.GetRasterBand(band+1).WriteArray(outArray[band])
        # Calculate stats
        stat = newDataset.GetRasterBand(band+1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
        newDataset.GetRasterBand(band+1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band

    # Close dataset
    newDataset = None
