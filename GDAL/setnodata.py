#!/usr/bin/env python

import osgeo.gdal as gdal
import optparse
import os
import sys

def setNoData(inputFile, noDataVal):
    dataset = gdal.Open(inputFile, gdal.GA_Update)
    if not dataset is None:
        for i in range(dataset.RasterCount):
            print "Setting No data (" + str(noDataVal) + ") for band " + str(i+1)
            band = dataset.GetRasterBand(i+1)
            band.SetNoDataValue(noDataVal)
    else:
        print "Could not open the input image file: ", inputFile

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input file.")
    p.add_option("-n","--nodata", dest="noData", default=0, help="No data value.")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "Input filename must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    setNoData(cmdargs.inputFile, float(cmdargs.noData))



