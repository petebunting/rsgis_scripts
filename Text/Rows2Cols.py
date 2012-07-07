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

    def parseTextFile(self, inputTextFile, x, y, z):
        line = 0
        for eachLine in inputTextFile:
            commaSplit = eachLine.split(',', eachLine.count(','))
            for token in commaSplit:
                if line == 0:
                    x.append(token.strip())
                elif line == 1:
                    y.append(token.strip())
                elif line == 2:
                    z.append(token.strip())
            line += 1

    def outputColsTextFile(self, outputTextFile, x, y, z):
        for i in range(len(x)):
            outputTextFile.write(str(x[i]))
            outputTextFile.write(',')
            outputTextFile.write(str(y[i]))
            outputTextFile.write(',')
            outputTextFile.write(str(z[i]))
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
    obj = Rows2Cols()
    obj.run()

