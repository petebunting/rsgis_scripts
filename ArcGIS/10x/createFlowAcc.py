# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# createFlowAcc.py
# Dan Clewley (daniel.clewley@gmail.com) - 22/02/2013
#
# ---------------------------------------------------------------------------

# Import arcpy module
import os, sys
sys.path.append("C:/Program Files/ArcGIS/Desktop10.1/Python/arcpy")
import arcpy

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

if len(sys.argv) != 4:
	print '''Not enough parameters provided.
Usage:
	python createFlowAcc.py inDEM outDIR outBaseName
'''
    exit()

inDEM = sys.argv[1]
outDIR = sys.argv[2]
outFileBase = sys.argv[3]

# Local variables:
outFill = os.path.join(outDIR, outFileBase + '_fill.tif')
outDirection = os.path.join(outDIR, outFileBase + '_flow_direction.tif')
Output_drop_raster = ""
outAccumulation =  os.path.join(outDIR, outFileBase + '_flow_accumulation.tif')

# Process: Fill
print 'Filling gaps in DEM'
arcpy.gp.Fill_sa(inDEM, outFill, "")

# Process: Flow Direction
print 'Creating flow direction raster'
arcpy.gp.FlowDirection_sa(outFill, outDirection, "NORMAL", Output_drop_raster)

# Process: Flow Accumulation
print 'Creating flow accumulation raster'
arcpy.gp.FlowAccumulation_sa(outDirection, outAccumulation, "", "FLOAT")
