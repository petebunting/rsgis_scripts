# Code to gerate geotiff from HDF5 files
# Dan Clewley
# 20/08/12

# Lines for calculating band statistics taken from:
# http://www.jeremymsmith.us/davidson/NDVI.py

# Import required libraries
import sys
import h5py, gdal, osr
import numpy as np

# Get input and output files from the command line or hardcode
inHDF5File = sys.argv[1] #'/data/ssurgo_tonzi/ca067.h5'
outGEOTiff = sys.argv[2] #'/data/ca067_tif.tif'

# Read in data
soildata = h5py.File(inHDF5File)

# Set input layers available in HDF5 file, found by running:
#list(soildata)
# in interactive python mode after opening the HDF5 file.

inputLayers = ['K_o','K_sat','L_parameter','N_parameter','alpha','bulk_density_0.33bar', 'depth_to_bottom','depth_to_top','horizon_thickness','percent_clay','percent_sand','percent_silt','theta_res','theta_sat','water_retention_0.33bar','water_retention_15bar']

# Set the number of bands (for the output image)
numBands = len(inputLayers)

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

# Set projection to WGS84 - Lat / Long
srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")

# Creat output image
driver = gdal.GetDriverByName("GTiff") # Could put any gdal supported layers here
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
            # For each pixel there are 6 layers, I assumed only the first was actual data and the others were metadata
            # You can to pixel[required band] to alter this 
            if pixel[0] == -9999:
                outLine.append(0.)
            else:
                outLine.append(pixel[0])
        outArray.append(outLine)
    
    # Set output as numpy array (so it can be transposed if required)
    outArray = np.array(outArray)
    if outArray.shape[0] != inYSize: # Some data I had the lat/long and data arrays were rotated so it was neccesary to transpose
        outArray = np.transpose(outArray)

    newDataset.GetRasterBand(band+1).WriteArray(outArray)
    # Calculate stats
    stat = newDataset.GetRasterBand(band+1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
    newDataset.GetRasterBand(band+1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band
    # Set output name
    newDataset.GetRasterBand(band+1).SetDescription(layerName)

# Close dataset
newDataset = None
