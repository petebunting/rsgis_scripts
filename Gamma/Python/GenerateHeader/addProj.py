#!/usr/bin/env python

# Add projection from WKT to image
#
# Dan Clewley (clewley@usc.edu) 11/02/2014

import osgeo.gdal as gdal
import argparse
import sys

def addProj(inWKTFileName, outFile):

    inWKTFile = open(inWKTFileName,'rU')
    inWKT = inWKTFile.read()
    inWKTFile.close()
    
    # Open the image file, in update mode
    outputDS = gdal.Open(outFile, gdal.GA_Update)

    # Set projection
    outputDS.SetProjection(inWKT)

    # Close image
    outputDS = None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True,
                        help="Specify the input image file.")
    parser.add_argument("--proj", type=str, required=True,
                        help="Specify the projection file")
    args = parser.parse_args()
        
    addProj(args.proj, args.image)



