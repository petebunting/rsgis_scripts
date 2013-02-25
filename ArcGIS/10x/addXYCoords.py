# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# addXYCoords.py
# Dan Clewley (daniel.clewley@gmail.com) - 25/02/2013
#
# ---------------------------------------------------------------------------

# Import arcpy module
import os, sys, glob
sys.path.append("C:/Program Files/ArcGIS/Desktop10.1/Python/arcpy")
import arcpy
from arcpy import env

if len(sys.argv) != 2:
	print '''Not enough parameters provided.
Usage:
	python addXYCoors.py inDIR
'''
	exit()

inDIR = sys.argv[1]

# Change directory and set workspace (so we can use relative paths)
os.chdir(inDIR)
env.workspace = inDIR.replace('\\','/')

shpFileList = glob.glob(inDIR + '/*shp')

for shpfile in shpFileList:
	print shpfile
	arcpy.AddXY_management(shpfile)
