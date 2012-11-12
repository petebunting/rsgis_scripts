#!/usr/bin/env python

import sys
from rios import rat
import numpy as np
import osgeo.gdal as gdal
import optparse

class RATColumnUniqueVals (object):

    def run(self, cmdargs):
        # Get variables from command line
        inputFilePath = cmdargs.inputFile.strip()
        selectColumn = cmdargs.column.strip()
        
        # Open the GDAL dataset 
        ratDataset = gdal.Open(inputFilePath, gdal.GA_ReadOnly)
        
        # Check the GDAL dataset was correctly opened
        if ratDataset is None:
            print "The image dataset could not opened."
            sys.exit()
        
        # Read the two columns
        selectCol = rat.readColumn(ratDataset, selectColumn)
        
        # Find the unique class names
        classes = np.unique(selectCol)
        for className in classes:
            print className
        
# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input file.")
    p.add_option("-c","--column", dest="column", default=None, help="Selected Column.")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "Input filename must be set."
        sys.exit()

    if self.column is None:
        p.print_help()
        print "Column must be set."
        sys.exit()
        


if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = RATColumnUniqueVals()
    obj.run(cmdargs)
    
    
    
    
    