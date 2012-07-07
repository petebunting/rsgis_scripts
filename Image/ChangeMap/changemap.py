#! /usr/bin/env python

#######################################
# changemap.py 
#
# Adapted from GDALCalcNDVI
#
# Version 1.0:
# A script using the GDAL Library to 
# create a change image from two
# classifications.
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 17/12/2007
# Version: 1.0
# Modified by Dan Clewley for mapping change in Omo valley
# 11/11/2008
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

		changecode = [[8,9,1,1,9,9,9,3,10,10,4,4,4,2,2],[4,8,10,1,1,9,9,3,10,10,2,5,8,2,2],[4,6,8,1,1,9,9,3,1,1,2,5,6,2,2],[4,6,4,8,2,2,2,3,10,10,2,5,6,2,2],[4,6,4,1,8,2,2,3,10,10,2,5,6,2,2],[4,6,4,4,4,8,7,3,1,10,7,5,6,2,2],[4,6,4,4,4,7,8,3,1,1,7,5,6,2,2],[4,6,4,4,4,7,7,8,2,2,7,5,6,2,2],[4,6,4,10,10,2,2,3,8,1,2,5,6,2,2],[4,6,4,10,10,2,2,3,2,8,2,5,6,2,2],[4,6,4,1,1,7,7,7,1,1,8,5,6,10,2],[4,6,4,1,1,1,1,3,1,1,1,8,6,1,2],[4,8,4,1,1,1,1,3,1,1,6,5,8,10,2],[4,4,4,1,1,1,1,3,1,1,10,5,6,8,2],[4,4,4,1,1,1,1,3,1,1,6,5,6,1,8]]
		
		numLines = band_1.YSize
		for line in range(numLines):
			outputLine = ''
			band_1_scanline = band_1.ReadRaster( 0, line, band_1.XSize, 1, band_1.XSize, 1, gdal.GDT_Float32 )
			band_1_tuple = struct.unpack('f' * band_1.XSize, band_1_scanline)
			
			band_2_scanline = band_2.ReadRaster( 0, line, band_2.XSize, 1, band_2.XSize, 1, gdal.GDT_Float32 )
			band_2_tuple = struct.unpack('f' * band_2.XSize, band_2_scanline)
			
			for i in range(len(band_1_tuple)):
				# YOUR CODE GOES HERE!
				
				band_1_code = int(band_1_tuple[i]) - 1# Pixel Value for band 1
				band_2_code = int(band_2_tuple[i]) - 1# Pixel Value for band 2
				#print str(i) + ': [' + str(band_1_code) + ',' + str(band_2_code) + ']',

				if band_1_code >= 15 or band_2_code >= 15:
					outputValue = 0
				elif band_1_code == -1 or band_2_code == -1:
					outputValue = 0
				
				else:				
					outputValue = changecode[band_2_code][band_1_code] # THIS IS THE VALUE WHICH WILL BE OUTPUTTED IN THE OUTPUT IMAGE
				#YOUR CODE ENDS HERE!
				#print str(outputValue)
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
			print 'changemap.py [input - stacked classifications] [output - changemap] '

if __name__ == '__main__':
	obj = ImageProcessing()
	obj.run()