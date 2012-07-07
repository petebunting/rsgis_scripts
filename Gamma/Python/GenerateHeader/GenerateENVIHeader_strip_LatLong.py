#! /usr/bin/env python

#######################################
# A class automatically generate ENVI
# header files from the GAMMA outputted
# par parameter files.
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 06/03/2008
# Version: 1.0
#######################################

import os.path
import sys
import string

class GenerateENVIHeader (object):
	
	def checkFileExtension(self, filename, extension):
		foundExtension = False;
		filenamesplit = os.path.splitext(filename)
		fileExtension = filenamesplit[1].strip()
		if(fileExtension == extension):
			foundExtension = True
		return foundExtension
	
	def findFiles(self, filelist, directory, extension):
		if os.path.exists(directory):
			if os.path.isdir(directory):
				fileList = os.listdir(directory)
				for filename in fileList:
					#print filename
					if(os.path.isdir(os.path.join(directory,filename))):
						#print filename + ' is a directory.'
						self.findFiles(filelist, os.path.join(directory,filename), extension)
					elif(os.path.isfile(os.path.join(directory,filename))):
						#print filename + ' is a file.'
						if(self.checkFileExtension(filename, extension)):
							#print 'FOUND FILE - ADD TO LIST!'
							filelist.append(os.path.join(directory,filename))
					else:
						print filename + ' is NOT a file or directory!'
			else:
				print directory + ' is not a directory!'
		else:
			print directory + ' does not exist!'
	
	def stripdeg(self, instring):
		stringstrip = instring.split(' ')
		return stringstrip[0]
	
	def getALOSPAR_NoSpatial(self, parFilename, outputParameters):
		if(os.path.isfile(parFilename)):
			#print 'Found parameters file'
			try:
				parFile = open(parFilename, 'r') 
				for eachLine in parFile:
					print eachLine
					count = eachLine.count(':')
					print 'count = ' + str(count)
					if(count == 1):
						#print 'Two elements'
						elements = eachLine.split(':', count)
						elements[0] = elements[0].strip()
						elements[1] = elements[1].strip()
						print '1: \'' + elements[0] + '\' 2:\'' + elements[1] + '\''
						if(elements[0] == 'title'):
							outputParameters.append(elements[1])
						elif(elements[0] == 'sensor'):
							outputParameters.append(elements[1])
						elif(elements[0] == 'date'):
							outputParameters.append(elements[1])
						elif(elements[0] == 'range_samples'):
							outputParameters.append(elements[1])
						elif(elements[0] == 'azimuth_lines'):
							outputParameters.append(elements[1])
						elif(elements[0] == 'image_format'):
							outputParameters.append(elements[1])
				parFile.close()
			except IOError, e:
				print '\nCould not open file: ', e
				raise IOError(e)
		else:
			raise BaseException
	
	def generateENVIHeadersNoSpatial(self, filelist):
		for filename in filelist:
			print '\n\n'
			print filename
			outputFileName = os.path.splitext(filename)[0] +'.hdr'
			print outputFileName
			try:
				parameters = list()
				self.getALOSPAR_NoSpatial(filename+'.par', parameters)
				#print str(parameters)
				outputFile = open(outputFileName, 'w')
				outputFile.write( 'ENVI\n')
				outputFile.write( 'description = { Parameter File: ' + str(parameters[0]) + ' for sensor: ' + str(parameters[1]) + ' captured on: ' + str(parameters[2]) + '}\n' )
				outputFile.write( 'samples = ' + str(parameters[3]) + '\n' )
				outputFile.write( 'lines = ' + str(parameters[4]) + '\n')
				outputFile.write( 'bands   = 1\n' )
				outputFile.write( 'header offset = 0\n' )
				outputFile.write( 'file type = ENVI Standard\n' )
				#print 'Parameters[5]: \'' + str(parameters[5]) + '\''
				if(parameters[5] == 'FLOAT'):
					outputFile.write( 'data type = 4\n' )
				elif(parameters[5] == 'FCOMPLEX'):
					outputFile.write( 'data type = 6\n' )
				else:
					print 'Data type not recognised. Only FLOAT and FCOMPLEX supported.'
					sys.exit(-1)
				outputFile.write( 'interleave = bsq\n' )
				outputFile.write( 'sensor type = Unknown\n' )
				outputFile.write( 'byte order = 1\n' )
				outputFile.write( 'wavelength units = Unknown\n' )
				if(parameters[5] == 'FCOMPLEX'):
					outputFile.write( 'complex function = Power\n')
				outputFile.write('\n\n')
				outputFile.flush()
				outputFile.close()
			except BaseException, e:
				print 'Could not retrieve ALOS parameters to generate ENVI Header\n'
				print e
	
	def findSpatialParamsFile(self, imageFile):
		#print str(imageFile)
		directory = os.path.dirname(imageFile)
		#print str(directory)
		fileList = os.listdir(directory)
		for filename in fileList:
			#print 'filename =' + filename
			if(os.path.isfile(os.path.join(directory,filename))):
				#print filename + ' is a file.'
				if(self.checkFileExtension(filename, '.par')):
					#print 'A Parameter file has been found!'
					#print os.path.splitext(filename)[0]
					if(self.checkFileExtension(os.path.splitext(filename)[0], '.dem')):
						#print 'Found DEM Parameters file'
						return os.path.join(directory,filename)
		raise IOError('DEM parameter file not found')			
	
	def getALOSPAR_Spatial(self, parFilename, outputParameters):
		if(os.path.isfile(parFilename)):
			#print 'Found parameters file'
			try:
				parFile = open(parFilename, 'r') 
				for eachLine in parFile:
					#print eachLine
					count = eachLine.count(':')
					#print 'count = ' + str(count)
					if(count == 1):
						#print 'Two elements'
						elements = eachLine.split(':', count)
						elements[0] = elements[0].strip()
						elements[1] = elements[1].strip()
						#print '1: \'' + elements[0] + '\' 2:\'' + elements[1] + '\''
						if(elements[0] == 'title'):
							outputParameters.append(elements[1])
						elif(elements[0] == 'width'):
							outputParameters.append(elements[1])
						elif(elements[0] == 'nlines'):
							outputParameters.append(elements[1])						
						elif(elements[0] == 'corner_lat'):
							stripelement = self.stripdeg(elements[1])
							outputParameters.append(str(stripelement))
						elif(elements[0] == 'corner_lon'):
							stripelement = self.stripdeg(elements[1])
							outputParameters.append(str(stripelement))
						elif(elements[0] == 'post_lat'):
							stripelement = self.stripdeg(elements[1])
							outputParameters.append(str(stripelement))
						elif(elements[0] == 'post_lon'):
							stripelement = self.stripdeg(elements[1])
							outputParameters.append(str(stripelement))
						elif(elements[0] == 'ellipsoid_name'):
							if(elements[1] == 'WGS 84'):
								outputParameters.append('WGS-84')
							else:
								outputParameters.append(elements[1])	
						#elif(elements[0] == 'projection_name'):
						#	outputParameters.append(elements[1])
						#elif(elements[0] == 'projection_zone'):
						#	outputParameters.append(elements[1])
						
				parFile.close()
			except IOError, e:
				print '\nCould not open file: ', e
				raise IOError(e)
		else:
			raise BaseException
	
	def generateENVIHeaderSpatial(self, filelist):
		try:
			for filename in filelist:
				print filename
				parfile = self.findSpatialParamsFile(filename)
				print parfile
				outputFileName = os.path.splitext(filename)[0] +'.utm.hdr'
				print outputFileName
				parameters = list()
				self.getALOSPAR_Spatial(parfile, parameters)
				outputFile = open(outputFileName, 'w')
				outputFile.write( 'ENVI\n')
				outputFile.write( 'description = {\n')
				outputFile.write( '\t' + filename + '}\n')
				outputFile.write( 'samples = ' + parameters[1] + '\n')
				outputFile.write( 'lines = ' + parameters[2] + '\n')
				outputFile.write( 'bands = 1\n')
				outputFile.write( 'header offset = 0\n')
				outputFile.write( 'data type = 4\n')
				outputFile.write( 'interleave = bsq\n')
				outputFile.write( 'sensor type = Unknown\n')
				outputFile.write( 'byte order = 1\n')
				outputFile.write( 'map info = {Geographic Lat/Lon, 1.5000, 1.5000, ' + str(parameters[4]) + ', ' + str(parameters[3]) + ', '+ str(parameters[6]) + ', '+ str(parameters[6]) + ', ' + str(parameters[7]) + ', units=Degrees}\n' )
				outputFile.write( 'wavelength units = Unknown\n')

		except IOError, e:
			print 'IOError Occurred: ' + str(e)
			
	def run(self, spatial, directory, extension):
		filelist = list()
		self.findFiles(filelist, directory, extension)
		if(str(spatial) == 'spatial'):
			self.generateENVIHeaderSpatial(filelist)
		else:
			self.generateENVIHeaderSpatial(filelist)
		

if __name__ == '__main__':
	obj = GenerateENVIHeader()
	spatial = sys.argv[1].strip()
	directory = sys.argv[2].strip()
	extension = sys.argv[3].strip()
	obj.run(spatial, directory, extension)