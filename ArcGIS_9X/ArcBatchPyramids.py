#! /usr/bin/env python

#######################################
# ArcBatchPyramids.py 
#
# Version 1.0:
# A script to create image pyramids for a
# directory of raster images. 
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 18/12/2007
# Version: 1.0
#######################################

import win32com.client, string,win32api


def createImagePyramid(raster, gp):
    try:
        gp.AddMessage("Building pyramid for raster " + raster)
        gp.BuildPyramids_management(raster)            
        gp.AddMessage("Pyramids were successfully built for " + raster)
    except Exception, ErrorDesc:
        gp.AddMessage("Error: pyramids could not be built for " + raster)


def iterateFilesToBuildPyramids(rasterList, gp):
    splitRasterList = str(rasterList).split(';')
    for raster in splitRasterList:
        if raster.startswith("'") and raster.endswith("'"):
            raster = raster[1:-1]
        createImagePyramid(raster, gp)

if __name__ == '__main__':
    gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
    rasterList = gp.GetParameterAsText(0)
    iterateFilesToBuildPyramids(rasterList, gp)