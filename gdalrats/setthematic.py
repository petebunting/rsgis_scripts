#!/usr/bin/env python

import sys
from osgeo import gdal

ds = gdal.Open(sys.argv[1], gdal.GA_Update)
for bandnum in range(ds.RasterCount):
    band = ds.GetRasterBand(bandnum + 1)
    band.SetMetadataItem('LAYER_TYPE', 'thematic')

