 #! /usr/bin/env python

#######################################
# A python script to read in a text file
# of rainfall data for summer and winter
# within the UK and display as a plot.
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 28/08/2007
# Version: 1.0
#######################################

import os.path
import sys

class Cols2Rows (object):
 
	def parseTextFile(self, inputTextFile, x, y, z):
		for eachLine in inputTextFile:
			print eachLine
			commaSplit = eachLine.split(',', eachLine.count(','))
			i = 0
			for token in commaSplit:
				print str(i) + ': token = ' + str(token.strip())
				if i == 0:
					x.append(token.strip())
				elif i == 1:
					y.append(token.strip())
				elif i == 2:
					z.append(token.strip())
				i += 1
			
	
	def outputColsTextFile(self, outputTextFile, x, y, z):
		for i in range(len(x)):
			outputTextFile.write(str(x[i]))
			outputTextFile.write(',')
		outputTextFile.write('\n')
		for i in range(len(y)):
			outputTextFile.write(str(y[i]))
			outputTextFile.write(',')
		outputTextFile.write('\n')
		for i in range(len(y)):
			outputTextFile.write(str(z[i]))
			outputTextFile.write(',')
		outputTextFile.write('\n')
	
	def run(self):
		inputTextFilePath = sys.argv[1]
		outputTextFilePath = sys.argv[2]
		if os.path.exists(inputTextFilePath):
			x = list()
			y = list()
			z = list()
			try:
				inputTextFile = open(inputTextFilePath, 'r')
				self.parseTextFile(inputTextFile, x, y, z)
				inputTextFile.close()
			except IOError, e:
				print '\nCould not open file:\n', e
				return
			#print 'x: ' + str(x)
			#print 'y: ' + str(y)
			#print 'z: ' + str(z)
			try:
				outputTextFile = open(outputTextFilePath, 'w')
				self.outputColsTextFile(outputTextFile, x, y, z)
				outputTextFile.flush()
				outputTextFile.close()
			except IOError, e:
				print '\nCould not open file:\n', e
				return
		else:
			print 'File \'' + inputTextFilePath + '\' does not exist.'
	
if __name__ == '__main__':
	obj = Cols2Rows()
	obj.run()
	