#!/usr/bin/env python

import sys
from osgeo import gdal
import argparse

# Set up options
parser = argparse.ArgumentParser('setthematic.py')
parser.add_argument("inimage", nargs=1,type=str, help="Input Image")
parser.add_argument("-b","--band", type=int, default=None, help="Set band to set as thematic (default=all bands)", required=False)

args = parser.parse_args() 

inImage = args.inimage[0]

ds = gdal.Open(inImage, gdal.GA_Update)

if args.band is not None:
    band = ds.GetRasterBand(args.band)
    band.SetMetadataItem('LAYER_TYPE', 'thematic')
    
else:
    for bandnum in range(ds.RasterCount):
        band = ds.GetRasterBand(bandnum + 1)
        band.SetMetadataItem('LAYER_TYPE', 'thematic')

ds = None

