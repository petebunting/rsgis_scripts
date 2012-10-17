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

class Rows2Cols (object):

    def parseTextFile(self, inputTextFile):
        textList = list()
        colLen = 0
        first = True
        for eachLine in inputTextFile:
            eachLine = eachLine.strip()
            commaSplit = eachLine.split(',', eachLine.count(','))
            lineList = list()
            for token in commaSplit:
                lineList.append(token.strip())
            if first:
                first = False
                colLen = len(lineList)
            elif colLen != len(lineList):
                print "ERROR!!!"
                print "colLen == ", colLen
                print "len(lineList) = ", len(lineList)
                print "eachLine: ", eachLine
                #sys.exit()
            textList.append(lineList)
        return textList, colLen
            
    def outputColsTextFile(self, outputTextFile, parsedFile, colLen):
        for i in range(colLen):
            print "i = ", i
            for row in parsedFile:
                outputTextFile.write(str(row[i]))
                outputTextFile.write(',')
            outputTextFile.write('\n')

    def run(self):
        inputTextFilePath = sys.argv[1]
        outputTextFilePath = sys.argv[2]
        if os.path.exists(inputTextFilePath):
            try:
                inputTextFile = open(inputTextFilePath, 'r')
                parsedFile, colLen = self.parseTextFile(inputTextFile)
                inputTextFile.close()
                
                print "Column Length: ", colLen
                
                outputTextFile = open(outputTextFilePath, 'w')
                self.outputColsTextFile(outputTextFile, parsedFile, colLen)
                outputTextFile.flush()
                outputTextFile.close()
                
            except IOError, e:
                print '\nCould not open file:\n', e
                return
        else:
            print 'File \'' + inputTextFilePath + '\' does not exist.'

if __name__ == '__main__':
    obj = Rows2Cols()
    obj.run()