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

	def removeHDRExtension(self, name):
		outName = name
		count = name.find('.hdr', 0, len(name))
		if not count == -1:
			outName = name.replace('.hdr', '', name.count('.hdr'))
		return outName

	def removeHDRExtensionUpper(self, name):
		outName = name
		count = name.find('.HDR', 0, len(name))
		if not count == -1:
			outName = name.replace('.HDR', '', name.count('.HDR'))
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

	def convertfiles(self, inFilePath, fileList, outFilePath):
		hdr = '.HDR'
		tif = '.tif'
		inFilePath = inFilePath.strip()
		outFilePath = outFilePath.strip()
		command_gdal = 'gdal_translate'
		command_ot = '-ot UINT16'
		command_of = '-of GTIFF'
		command_b = '-b'
		command = ''
		for file in fileList:
			hdrmatch = file.find(hdr, 0, len(file))
			if hdrmatch > 0:
				print file
				enviFileName = self.removeHDRExtensionUpper(file)
				for i in range(4):
					print i
					if i == 0:
						command = command_gdal + ' ' + command_ot + ' ' + command_of + ' ' + command_b + ' ' + str(i+1) + ' ' + inFilePath + enviFileName + ' ' + outFilePath + enviFileName + '_GREEN' + tif
					elif i == 1:
						command = command_gdal + ' ' + command_ot + ' ' + command_of + ' ' + command_b + ' ' + str(i+1) + ' ' + inFilePath + enviFileName + ' ' + outFilePath + enviFileName + '_RED' + tif
					elif i == 2:
						command = command_gdal + ' ' + command_ot + ' ' + command_of + ' ' + command_b + ' ' + str(i+1) + ' ' + inFilePath + enviFileName + ' ' + outFilePath + enviFileName + '_NIR' + tif
					elif i == 3:
						command = command_gdal + ' ' + command_ot + ' ' + command_of + ' ' + command_b + ' ' + str(i+1) + ' ' + inFilePath + enviFileName + ' ' + outFilePath + enviFileName + '_SWIR' + tif
					else:
						print 'IGNORING'
					print command
					os.system(command)
			
			
	def run(self):
		numArgs = len(sys.argv)
		inFilePath = ''
		outFilePath = ''
		
		if numArgs >= 3:
			inFilePath = sys.argv[1]
			outFilePath = sys.argv[2]
			if os.path.exists(inFilePath) and os.path.isdir(inFilePath) and os.path.exists(outFilePath) and os.path.isdir(outFilePath):
				print 'File paths are OK'
				fileList = os.listdir(inFilePath)
				self.convertfiles(inFilePath, fileList, outFilePath)
			else:
				print 'Check file paths.. Exiting...'
				self.help()
		else:
			self.help()

	def help(self):
		print 'You need HELP!'

if __name__ == '__main__':    
	obj = ConvertImagery()
	obj.run()