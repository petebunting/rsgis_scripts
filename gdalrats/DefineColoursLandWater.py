#!/usr/bin/env python

import sys
from rios import rat
import numpy as np
import osgeo.gdal as gdal
import optparse

def collapseClasses(inputFile):
    ratDataset = gdal.Open(inputFile, gdal.GA_Update)
    Red = rat.readColumn(ratDataset, "Red")
    Green = rat.readColumn(ratDataset, "Green")
    Blue = rat.readColumn(ratDataset, "Blue")
    
    # Water
    Red[0] = 135
    Green[0] = 206
    Blue[0] = 255
    
    # Land
    Red[1] = 34
    Green[1] = 139
    Blue[1] = 34
    
    rat.writeColumn(ratDataset, "Red", Red)
    rat.writeColumn(ratDataset, "Green", Green)
    rat.writeColumn(ratDataset, "Blue", Blue)


# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input file.")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "Input filename must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    collapseClasses(cmdargs.inputFile)