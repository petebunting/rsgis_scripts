#!/usr/bin/env python

############################################################################
# Copyright (c) 2013 Dr. Peter Bunting
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
# Purpose:  To generate a map legend from an inputted GDAL file where
#           the RAT contains a list of classes and colours.

# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 13/01/2012
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
#############################################################################

import sys
import numpy
import optparse
import csv
import math as math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class GenerateClassLegend (object):

    def readClassesColours(self, inputCSV):
        namesColoursList = list()
        try:
            with open(inputCSV, 'rb') as csvfile:
                csvData = csv.reader(csvfile, delimiter=',')
                for row in csvData:
                    classList = list()
                    classList.append(row[0].strip())
                    classList.append(row[1])
                    classList.append(row[2])
                    classList.append(row[3])
                    namesColoursList.append(classList)
        except Exception, e:
            print "Error: ", str(e)
            sys.exit()
        return namesColoursList

    def generateLegend(self, outFileName, outImageFormat, numRows, numCols, classNamesColoursList, fontFile):
        try:
            classNamesColoursListCols = list()
            classNamesColoursListCol = list()
            i = 1
            maxNumChars = 0
            first = True
            for classNameColours in classNamesColoursList:
                if first:
                    maxNumChars = len(classNameColours[0])
                    first = False
                elif len(classNameColours[0]) > maxNumChars:
                    maxNumChars = len(classNameColours[0])
                if (i % numRows) == 0:
                    classNamesColoursListCol.append(classNameColours)
                    classNamesColoursListCols.append(classNamesColoursListCol)
                    classNamesColoursListCol = list()
                else:
                    classNamesColoursListCol.append(classNameColours)
                i+=1
            if len(classNamesColoursListCol) > 0:
                classNamesColoursListCols.append(classNamesColoursListCol)
                
                   
            print "Longest Class Name has " + str(maxNumChars) + " characters."
            
            #print "len(classNamesColoursListCols): ", len(classNamesColoursListCols)
            #for classNamesColoursListCol in classNamesColoursListCols:
            #    print "len(classNamesColoursListCol): ", len(classNamesColoursListCol)
            #    for classNameColours in classNamesColoursListCol:
            #        print classNameColours
            
            imBorder = 5
            recWidth = 100
            recHeight = 50
            numPxlsPerChar = 21
            imColWidth = ((maxNumChars * numPxlsPerChar) + recWidth) + imBorder
            imRowHeight = recHeight + imBorder
            imXSize = (numCols * imColWidth) + (imBorder*2)
            imYSize = (numRows * imRowHeight) + (imBorder*2)
            
            print "New output image has size: [" + str(imXSize) + "," + str(imYSize) + "]."
            
            im = Image.new ("RGB", (imXSize, imYSize), "white" )
            draw = ImageDraw.Draw(im)
            fontObj = ImageFont.truetype(fontFile, 36)
            
            col = 0
            for classNamesColoursListCol in classNamesColoursListCols:
                row = 0
                for classNameColours in classNamesColoursListCol:
                    xMin = imBorder+(col*imColWidth)
                    yMin = imBorder+(row*imRowHeight)
                    xMax = xMin + recWidth
                    yMax = yMin + recHeight
                    colour=str("rgb(")+str(classNameColours[1])+str(",")+str(classNameColours[2])+str(",")+str(classNameColours[3])+str(")")
                    draw.rectangle([(xMin, yMin), (xMax, yMax)], outline="rgb(0,0,0)", fill=colour)
                    draw.text((xMax+imBorder, yMin+imBorder), classNameColours[0], fill="rgb(0,0,0)", font=fontObj)
                    row += 1
                col += 1
            
            del fontObj
            del draw
            im.save(outFileName, outImageFormat)
            
        except Exception, e:
            print "Error: ", str(e)
            sys.exit()
        
    def run(self, cmdargs):
        classNamesColoursList = self.readClassesColours(cmdargs.inputCSV)
        print "-------------------------"
        print "Class: [Red, Green, Blue]"
        print "-------------------------"
        for classNameColours in classNamesColoursList:
            print str(classNameColours[0]) + ": [" + str(classNameColours[1]) + ","  + str(classNameColours[2]) + "," + str(classNameColours[3]) + "]"
        print "-------------------------"
                
        numCols = 0
        numRows = 0
        if cmdargs.numOfColumns != 0:
            numCols = cmdargs.numOfColumns
            if numCols == 1:
                numRows = len(classNamesColoursList)
            else:
                numRows = int(math.ceil(float(len(classNamesColoursList)) / float(numCols)))
        elif cmdargs.numOfRows != 0:
            numRows = cmdargs.numOfRows
            if numRows == 1:
                numCols = len(classNameColours)
            else:
                numCols = int(math.ceil(float(len(classNamesColoursList)) / float(numRows)))
        else:
            print "Error: Neither the number of rows or number of columns was speciified"
            sys.exit()
        
        print "The legend with have " + str(numCols) + " columns and " + str(numRows) + " rows."

        self.generateLegend(cmdargs.outputImage, cmdargs.outputFormat, int(numRows), int(numCols), classNamesColoursList, cmdargs.fontFile)

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputCSV", default=None, help="Input CSV file (Name, Red, Green, Blue)")
    p.add_option("-o","--output", dest="outputImage", default=None, help="Output image file")
    p.add_option("-f","--format", dest="outputFormat", default="PNG", help="Output image file format")
    p.add_option("-r","--rows", dest="numOfRows", default=0, help="Number of rows in legend")
    p.add_option("-c","--cols", dest="numOfColumns", default=0, help="Number of columns in legend")
    p.add_option("","--font", dest="fontFile", default=0, help="A font file (TTF).")

    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputCSV is None:
        p.print_help()
        print "Input CSV file (Name, Red, Green, Blue) must be provided."
        sys.exit()

    if self.outputImage is None:
        p.print_help()
        print "Output filename must be set."
        sys.exit()
        
    if self.fontFile is None:
        p.print_help()
        print "A TTF font file must be specified."
        sys.exit()
        
    if (self.numOfRows == 0) and (self.numOfColumns == 0):
        self.numOfColumns = 1
        print "Neither the number of rows or columns has been specified so just creating 1 column."
        
    if (self.numOfRows != 0) and (self.numOfColumns != 0):
        p.print_help()
        print "Both the number of rows and columns have been specified only one can be used."
        sys.exit()

if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = GenerateClassLegend()
    obj.run(cmdargs)

