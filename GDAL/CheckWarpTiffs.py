#!/usr/bin/env python

import osgeo.gdal as gdal
import optparse
import os

def warpImage(inputFile, outputFile, outputDIR):
    dataset = gdal.Open(inputFile, gdal.GA_ReadOnly)
    if not dataset is None:
    
        geotransform = dataset.GetGeoTransform()
        if not geotransform is None:
            #print 'Origin = (',geotransform[0], ',',geotransform[3],')'
            #print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
            print 'Rotation = (',geotransform[2], ',',geotransform[4],')'
            
            outFileUsed = ""
            cmd = ""
            if (geotransform[2] == 0) and (geotransform[4] == 0):
                cmd = str("gdal_translate -of GTIFF -a_srs ./osgb36.wkt -co \"COMPRESS=DEFLATE\" -co \"TILED=YES\" ") + inputFile + str(" ") + outputDIR + str("/") + inputFile
                outFileUsed = inputFile
            else:
                cmd = str("gdalwarp -overwrite -r cubic -s_srs ./osgb36.wkt -multi -wt Float32 -of GTIFF -co \"COMPRESS=DEFLATE\" -co \"TILED=YES\" ") + inputFile + str(" ") +  outputDIR + str("/") + outputFile
                outFileUsed = outputFile
            print "Command: ", cmd
            os.system(cmd)
            setNoData(outputDIR + str("/") + outFileUsed, 0.0)
            cmd = "gdaladdo -r average " + outputDIR + str("/") + outFileUsed + " 2 4 8 16 32" 
            print "Command: ", cmd
            os.system(cmd)
        else:
            print "Could not find a geotransform for image file ", inputFile
    else:
        print "Could not open the input image file: ", inputFile

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
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output file name.")
    p.add_option("-d","--outdir", dest="outputDIR", default=None, help="Output directory.")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "Input filename must be set."
        sys.exit()
        
    if self.outputFile is None:
        p.print_help()
        print "Output filename must be set."
        sys.exit()
        
    if self.outputDIR is None:
        p.print_help()
        print "Output directory must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    warpImage(cmdargs.inputFile, cmdargs.outputFile, cmdargs.outputDIR)



