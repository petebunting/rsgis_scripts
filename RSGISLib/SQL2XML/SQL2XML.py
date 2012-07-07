 #! /usr/bin/env python

#######################################
# A python script to read in a text file
# of SQL statements formatted name;sql 
# and convert this to the standard rsgis
# XML format for SQL based classification
# and to escape an problematic characters.
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 16/03/2009
# Version: 1.0
#######################################

import os.path
import sys

class SQL2XML (object): 
 
	def parseTextFile(self, inputTextFile, name, sql):
		line = 0
		for eachLine in inputTextFile:
			if eachLine[0] != '#':
				split = eachLine.split(';', eachLine.count(';'))
				if len(split) == 2:
					name.append(split[0].strip())
					sql.append(split[1].strip())
				else:
					print 'Syntax Error: ', eachLine
	
	def outputXMLTextFile(self, outputTextFile, name, sql):
		for i in range(len(name)):
			outputTextFile.write('<rsgis:class name=\"')
			outputTextFile.write(str(name[i]))
			outputTextFile.write('\" ')
			outputTextFile.write('sql=\"')
			outputTextFile.write(str(sql[i]))
			outputTextFile.write('\" />\n')
	
	def replaceSQLChars(self, sql):
		for i in range(len(sql)):
			sql[i] = sql[i].replace('&', '&amp;')
			sql[i] = sql[i].replace('\"', '&quot;')
			sql[i] = sql[i].replace('\'', '&apos;')
			sql[i] = sql[i].replace('<', '&lt;')
			sql[i] = sql[i].replace('>', '&gt;')
			
	def run(self):
		inputTextFilePath = sys.argv[1]
		outputTextFilePath = sys.argv[2]
		if os.path.exists(inputTextFilePath):
			name = list()
			sql = list()
			try:
				inputTextFile = open(inputTextFilePath, 'r')
				self.parseTextFile(inputTextFile, name, sql)
				inputTextFile.close()
			except IOError, e:
				print '\nCould not open file:\n', e
				return
			
			self.replaceSQLChars(sql)
			
			try:
				outputTextFile = open(outputTextFilePath, 'w')
				self.outputXMLTextFile(outputTextFile, name, sql)
				outputTextFile.flush()
				outputTextFile.close()
			except IOError, e:
				print '\nCould not open file:\n', e
				return
		else:
			print 'File \'' + inputTextFilePath + '\' does not exist.'
	
if __name__ == '__main__':
	obj = SQL2XML()
	obj.run()
	