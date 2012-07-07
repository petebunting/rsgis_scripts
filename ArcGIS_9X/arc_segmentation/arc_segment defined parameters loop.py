#####################################################
## NAME: Perform_segment
## Source Name: Perform_segment.py
## Version: ArcGIS 9.X
## Author: Peter Bunting
## Email: pjb00@aber.ac.uk
## Usage: 
## Description:  
## Date: 29 May 2007
## Updated: 29 May 2007
#####################################################

import sys
import os
import string
import imghdr
import Image
import win32com.client

gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

# Load required toolboxes...
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Conversion Tools.tbx")
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")

sigma = "1"
k = "100"
min = "1000"

# Script arguments...
InputWS = "C:\data\images"

# set the workspace
gp.workspace = InputWS

#get a list of all rasters in the input workspace
rasters = gp.listrasters("*", "all")

#for each raster in the list

rasters.reset
inRaster = rasters.next()

try:
    while inRaster:
        inRasterSafe = inRaster.replace('\\', '\\\\', inRaster.count('\\'))

        inRasterSplit = os.path.split(inRaster)

        gp.AddMessage('In dir: ' + inRasterSplit[0])
        gp.AddMessage('Using Image (safe): ' + inRasterSplit[1])

        os.chdir(inRasterSplit[0])

        imageFile = inRaster

        gp.AddMessage('Converting image to ppm format')
        im = Image.open(inRasterSplit[1])
        os.chdir(workspace)
        im.save('tmp.ppm', 'ppm')
        imageFile = workspace + '\\test.ppm'
            

        command = segmentLocation + '\\segment.exe ' + sigma + ' ' + k + ' ' + min + ' ' + workspace + '\\tmp.ppm ' + workspace + '\\tmp_output.ppm'
    
        gp.AddMessage('COMMAND: ' + command)
    
        os.system(command)

        os.chdir(inRasterSplit[0])

        filenameInput = inRasterSplit[1].split('.', 2)

        outFileName = filenameInput[0] + '_segment.png'

        gp.AddMessage('Output File Name: ' + outFileName)

        im = Image.open(workspace + '\\tmp_output.ppm')
        im.save(outFileName)
        gp.AddMessage('Saved PNG')
    
        fullPath2PNG = inRasterSplit[0]+ '\\' + outFileName
        gp.AddMessage('Image: ' + fullPath2PNG)

        output_shp = inRasterSplit[0]+ '\\' + filenameInput[0] + '_segment_shp.shp'
        gp.AddMessage('Shapefile: ' + output_shp)

        inRaster = rasters.next()