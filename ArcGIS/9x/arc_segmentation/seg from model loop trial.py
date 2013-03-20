# ---------------------------------------------------------------------------
# seg from model.py
# Created on: ��� ���� 19 2007 11:38:16 ��
#   (generated by ArcGIS/ModelBuilder)
# ---------------------------------------------------------------------------
import sys
import os
import string
import imghdr
import Image
import win32com.client

gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

# Load required toolboxes...
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Segmentation.tbx")


# Script arguments...
InputWS = "C:\\data\\images"

# set the workspace
gp.workspace = InputWS

# Local variables...
Sigma = "0.5"
Min = "20"
K = "500"
seg = "C:\\data"
tmp = "C:\\data\\new"



#get a list of all rasters in the input workspace
rasters = gp.listrasters("*", "all")

#for each raster in the list
rasters.reset
img = rasters.next

try
    while img:
        # Process: Segmentation...
        gp.toolbox = "C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Segmentation.tbx"
        gp.Segmentation(Sigma, K, Min, img, tmp, seg)
        img = rasters.next