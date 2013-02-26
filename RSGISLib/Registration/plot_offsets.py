
# Adapted from demo http://matplotlib.org/examples/pylab_examples/quiver_demo.html

from osgeo import gdal  
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

startX = 1200
startY = 750
imgSize = 100

dataset = gdal.Open('/Users/danclewley/Documents/Temp/PALSAR_Reg/pan_palsar_offsets_sub.kea', GA_ReadOnly)
imageDS = gdal.Open('S27E149_09_sl_HV_aeq_sub.kea',GA_ReadOnly)

band1 = dataset.GetRasterBand(1)  
band2 = dataset.GetRasterBand(2)
imageData = imageDS.GetRasterBand(1)

xOffsets =  band1.ReadAsArray()
yOffsets =  band2.ReadAsArray()
image = imageData.ReadAsArray()

plt.imshow(image[startX:startX+imgSize,startY:startY+imgSize])
plt.quiver(xOffsets[startX:startX+imgSize,startY:startY+imgSize], yOffsets[startX:startX+imgSize,startY:startY+imgSize])

plt.savefig('offsets.pdf', format='PDF') 

plt.savefig('/Users/danclewley/Documents/Temp/PALSAR_Reg/Offsets.pdf',format='PDF')