#! /usr/bin/env python

#######################################
# model.py 
#
# Adapted from GDALCalcNDVI
#
# Version 1.0:
# A script using the GDAL Library to 
# create a new image contains the NDVI
# of the original image
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 17/12/2007
# Version: 1.0
#######################################

import gdal, sys, os, struct
from gdalconst import *

class ImageProcessing (object):

    def createOutputImage(self, outFilename, inDataset):
        driver = gdal.GetDriverByName( "GTiff" )
        metadata = driver.GetMetadata()
        if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
            print 'Driver GTiff supports Create() method.'
        if metadata.has_key(gdal.DCAP_CREATECOPY) and metadata[gdal.DCAP_CREATECOPY] == 'YES':
            print 'Driver GTiff supports CreateCopy() method.'
        newDataset = driver.Create(outFilename, inDataset.RasterXSize, inDataset.RasterYSize, 1, gdal.GDT_Float32)
        newDataset.SetGeoTransform(inDataset.GetGeoTransform())
        newDataset.SetProjection(inDataset.GetProjection())
        return newDataset


    def runModel(self, filePath, outFilePath):
        dataset = gdal.Open( filePath, GA_ReadOnly )
        if dataset is None:
            print "The dataset could not openned"
            sys.exit(-1)
        print "IMAGE OPENED!"
    
        outDataset = self.createOutputImage(outFilePath, dataset)
        if outDataset is None:
            print 'Could not create output image'
            sys.exit(-1)
        print 'Output Image Created'
    
        band_1 = dataset.GetRasterBand(1) # Get Band_1
        band_2 = dataset.GetRasterBand(2) # Get Band_2

        
        numLines = band_1.YSize
        for line in range(numLines):
            outputLine = ''
            band_1_scanline = band_1.ReadRaster( 0, line, band_1.XSize, 1, band_1.XSize, 1, gdal.GDT_Float32 )
            band_1_tuple = struct.unpack('f' * band_1.XSize, band_1_scanline)
            
            band_2_scanline = band_2.ReadRaster( 0, line, band_2.XSize, 1, band_2.XSize, 1, gdal.GDT_Float32 )
            band_2_tuple = struct.unpack('f' * band_2.XSize, band_2_scanline)
            
            for i in range(len(band_1_tuple)):
                # YOUR CODE GOES HERE!
                
                #band_1_tuple[i] # Pixel Value for band 1
                #band_2_tuple[i] # Pixel Value for band 2
                
                for a in range(len(15)):
                	for b in range(len(15)):
                		print a
                		print b
                		# DO SOMETHING
                		
                
                                
                outputValue = 0 # THIS IS THE VALUE WHICH WILL BE OUTPUTTED IN THE OUTPUT IMAGE
                #YOUR CODE ENDS HERE!
                outputLine = outputLine + struct.pack('f', outputValue)
            outDataset.GetRasterBand(1).WriteRaster(0, line, band_1.XSize, 1, outputLine, buf_xsize=band_1.XSize, buf_ysize=1, buf_type=gdal.GDT_Float32)
            del outputLine
        print 'Model Calculated and Outputted to File'

    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 3:
            filePath = sys.argv[1]  
            outFilePath = sys.argv[2]
            if os.path.exists(filePath):
                self.runModel(filePath, outFilePath)
            else:
                print 'The file does not exist.'
        else:
            print 'Incorrect number of arguments provided.'

if __name__ == '__main__':
    obj = ImageProcessing()
    obj.run()