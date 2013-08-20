# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# calcPointClusterAreas.py
# Dan Clewley (clewley@usc.edu) - 20/08/2013
#
# ---------------------------------------------------------------------------

# Import arcpy module
import os, sys, glob
try:
	import arcpy
	from arcpy import env
except ImportError:
	print("Could not open python libraries, check PYTHONPATH")
	sys.exit()

if len(sys.argv) != 4:
	print '''Not enough parameters provided.
Usage:
	python calcPointClusterAreas.py inDIR convexHullDIR boundingBoxDIR
'''
	exit()

inDIR = sys.argv[1]
convexHullDIR = sys.argv[2]
boundingBoxDIR = sys.argv[3]

# Change directory and set workspace (so we can use relative paths)
os.chdir(inDIR)
env.workspace = inDIR.replace('\\','/')

shpFileList = glob.glob(inDIR + '/*shp')

for inSHPFile in shpFileList:
	print inSHPFile
	baseName = os.path.split(inSHPFile)[-1].replace('.shp','')
	outConvexSHP = os.path.join(convexHullDIR,baseName + '_convexhull.shp')
	outBBSHP = os.path.join(boundingBoxDIR,baseName + '_boundingbox.shp')
	outConvexDBF = os.path.join(convexHullDIR,baseName + '_convexhull.dbf')
	outBBDBF = os.path.join(boundingBoxDIR,baseName + '_boundingbox.dbf')
	
	arcpy.MinimumBoundingGeometry_management(inSHPFile, outConvexSHP, \
                                         "CONVEX_HULL", "ALL")

										 
	arcpy.MinimumBoundingGeometry_management(inSHPFile, outBBSHP, \
                                         "ENVELOPE", "ALL")
										 
	# Calculate areas
	
	arcpy.AddField_management(outConvexDBF, "Area", "DOUBLE")
	arcpy.CalculateField_management(outConvexDBF, "Area", 
                                '!shape.area@squaremeters!', "PYTHON_9.3")
								
	arcpy.AddField_management(outBBDBF, "Area", "DOUBLE")
	arcpy.CalculateField_management(outBBDBF, "Area", 
                                '!shape.area@squaremeters!', "PYTHON_9.3")

