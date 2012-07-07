#! /usr/bin/env python

############################################################################
# Copyright (c) 2009 Dr. Peter Bunting, Aberystwyth University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# Purpose:  The generation a row summary for each class.
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 22/09/2009
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
#############################################################################

import os.path
import sys

def checkforHash(line):
    foundHash = False
    for i in range(len(line)):
        if line[i] == '#':
            foundHash = True
    return foundHash

def stringTokenizer(line, delimiter):
    tokens = list()
    token = str()
    for i in range(len(line)):
        if line[i] == delimiter:
            tokens.append(token)
            token = str()
        else:
            token = token + line[i]
    tokens.append(token)
    return tokens

class SummaryRows (object):
    
    def readVariableNames(self, inputCSV):
        dataFile = open(inputCSV, 'r')
        line = dataFile.readline()
        tokens = stringTokenizer(line, ',')
        variables = list()
        first = True
        for token in tokens:
            if first:
                first = False
            else:
                variables.append(token.strip())
        dataFile.close()
        return variables
    
    def readCSVFileVariables(self, inputCSV, numVariables):
        data = list()
        dataFile = open(inputCSV, 'r')
        first = True
        numVariables = numVariables + 1 # The class column
        for eachLine in dataFile:
            comment = checkforHash(eachLine)
            if comment == False:
                if first:
                    first = False
                else:
                    tokens = stringTokenizer(eachLine, ',')
                    if len(tokens) == numVariables:
                        dataElement = list()
                        firstElement = True
                        for token in tokens:
                            if firstElement:
                                dataElement.append(str(token.strip()))
                                firstElement = False
                            else:
                                dataElement.append(float(token.strip()))
                        data.append(dataElement)
                    else:
                        raise Exception('Not enough tokens in a inputCSV line')
        dataFile.close()
        return data

    def getClassnames(self, data):
        classnames = list()
        for item in data:
            found = False
            for classname in classnames:
                if item[0] == classname:
                    found = True
            if not found:
                classnames.append(item[0])
        return classnames
            
    def getDataSummary(self, data, classname):
    	summary = list()
    	count = 0;
    	total = 0;
    	first = True
    	for item in data:
    		if first:
    			first = False
    			firstItem = True
    			for i in range(len(item)):
    				if firstItem:
    					firstItem = False
    					summary.append(classname)
    				else:
    					summary.append(0)    					
    		if item[0] == classname:
    			firstItem = True
    			for i in range(len(item)):
    				if firstItem:
    					firstItem = False
    				else:
    					summary[i] = summary[i] + item[i]
    					total = total + item[i];
    			count = count + 1
    	first = True
    	for i in range(len(summary)):
    		if first:
    			first = False
    		else:
    			summary[i] = (summary[i]/total)*100
    	return summary
            
    def createOutput(self, data, outputCSV, classnames, variables):
    	outFile = open(outputCSV, 'w')
    	outFile.write("class")
    	for var in variables:
    		outFile.write(",")
    		outFile.write(var)
    	outFile.write("\n")
    	for classname in classnames:
    		summary = self.getDataSummary(data, classname)
    		first = True
    		for item in summary:
    			if first:
    				outFile.write(str(item))
    				first = False
    			else:
    				outFile.write(",")
    				outFile.write(str(item))
    		outFile.write("\n")
    		print summary
    	outFile.flush()
    	outFile.close()
    
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 3:
            inputCSV = sys.argv[1].strip()
            outputCSV = sys.argv[2].strip()
            
            variables = self.readVariableNames(inputCSV)
            data = self.readCSVFileVariables(inputCSV, len(variables))
            classnames = self.getClassnames(data)
            self.createOutput(data, outputCSV, classnames, variables)
            print classnames
        else:
            self.help()
    
    def help(self):
        print 'CSVClassPlot.py script generates a summary row for each class in the input CSV file\n'
        print 'Usage (1): python summaryrows.py <INPUT.csv> <OUTPUT_CSV>'
        
if __name__ == '__main__':
    obj = SummaryRows()
    obj.run()
    
