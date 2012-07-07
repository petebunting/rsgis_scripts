#! /usr/bin/env python

#######################################
# ConvertImagery.py
# A python script to convert remote
# imagery to GeoTIFF unsigned 16 bit.
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 12/12/2007
# Version: 1.0
#######################################

import os
import sys

class ConvertImagery (object):

	def removeExtension(self, name, ext):
		outName = name
		count = name.find(ext.lower(), 0, len(name.lower()))
		if not count == -1:
			outName = name.replace(ext.lower(), '', name.count(ext.lower()))
		return outName
		
	def removeFilePathUNIX(self, name):
		name = name.strip()
		count = name.count('/')
		nameSegments = name.split('/', count)
		return nameSegments[count]
		
	def removeFilePathWINS(self, name):
		name = name.strip()
		count = name.count('\\')
		nameSegments = name.split('\\', count)
		return nameSegments[count]

	def convertfiles(self, inFilePath, fileList, outFilePath, ext):
		tif = '.tif'
		inFilePath = inFilePath.strip()
		outFilePath = outFilePath.strip()
		command_gdal = 'gdal_translate'
		command_ot = '-ot Float32'
		command_of = '-of GTIFF'
		command = ''
		for file in fileList:
			extmatch = file.find(ext, 0, len(file))
			if extmatch > 0:
				print file
				inFilename = file
				baseFile = self.removeExtension(file, ext)
				if ext == '.hdr':
				    inFilename = baseFile
				command = command_gdal + ' ' + command_ot + ' ' + command_of + ' ' + inFilePath + inFilename + ' ' + outFilePath + baseFile + "_tif" + tif
				print command
				os.system(command)
			
			
	def run(self):
		numArgs = len(sys.argv)
		inFilePath = ''
		outFilePath = ''
		
		if numArgs >= 4:
			inFilePath = sys.argv[1]
			outFilePath = sys.argv[2]
			inputExtension = sys.argv[3]
			if os.path.exists(inFilePath) and os.path.isdir(inFilePath) and os.path.exists(outFilePath) and os.path.isdir(outFilePath):
				print 'File paths are OK'
				fileList = os.listdir(inFilePath)
				self.convertfiles(inFilePath, fileList, outFilePath, inputExtension)
			else:
				print 'Check file paths.. Exiting...'
				self.help()
		else:
			self.help()

	def help(self):
		print 'python ConvertImageryTIFF.py <inputDIR> <outputDIR> <input_Extension>'

if __name__ == '__main__':    
	obj = ConvertImagery()
	obj.run()