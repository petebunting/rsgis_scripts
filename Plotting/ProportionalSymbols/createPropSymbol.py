 #! /usr/bin/env python

#######################################
# createPropSymbol.py
#
# A python class to create a nested proportional symbol showing three values.
#
# Used as part of the SoilSCAPE website to create symbols used in open layers to 
# display soil moisture. 
# See http://soilscape.usc.edu/drupal/?q=node/24
#
# Requires:
# - imagemagick - http://www.imagemagick.org
#
# Created by Daniel Clewley (The University of Southern California)
# Copyright 2012 Daniel Clewley. All rights reserved.
#
# Email: daniel.clewley@gmail.com
# Date: 21/01/2013
# Version: 1.0
# 
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#######################################

import os, sys

# Set Scale factor, used to scale values to provide the required size, in pixels
scaleFactor = 10

def createSMSymbol(outDIR, outSymbolName, val1, val2, val3):

    # Set up files
    sensor1File = os.path.join(outDIR, 's1.png')
    sensor2File = os.path.join(outDIR, 's2.png')
    sensor3File = os.path.join(outDIR, 's3.png')
    tempStack = os.path.join(outDIR, 'temp_stack.png')
    outSymbol = os.path.join(outDIR, outSymbolName)
    
    # Create symbols
    command1 = '''convert -resize %i -channel rgba -alpha on s1_yellow_circle_base.png %s'''%(val1 * scaleFactor, sensor1File)
    command2 = '''convert -resize %i -channel rgba -alpha on s2_orange_circle_base.png %s'''%(val2 * scaleFactor, sensor2File)
    command3 = '''convert -resize %i -channel rgba -alpha on s3_red_circle_base.png %s'''%(val3 * scaleFactor, sensor3File)
    
    os.system(command1)
    os.system(command2)
    os.system(command3)
    
    # Sort sensors symbols according to soil moisture. 3 - largest, 1 smallest
    sensorDict = {sensor1File: val1, sensor2File: val2,sensor3File: val3}
    sortedFiles = sorted(iter(sensorDict.items()), key=lambda k_v: (k_v[1],k_v[0]))
    
    symbol3 = sortedFiles[2][0]
    symbol2 = sortedFiles[1][0]
    symbol1 = sortedFiles[0][0]
    
    stackCommand1 = 'composite -gravity center ' + symbol2 + ' ' + symbol3 + ' ' + tempStack
    stackCommand2 = 'composite -gravity center ' + symbol1 + ' ' + tempStack + ' ' + outSymbol
    os.system(stackCommand1)
    os.system(stackCommand2)
    
    # Remove temp files
    tempFiles = [sensor1File, sensor2File, sensor3File, tempStack]
    
    for tfile in tempFiles:
        os.remove(tfile)

if len(sys.argv) < 6:
    print('''Not enough parameters provided.
Usage:
   python createPropSymbol.py outDIR outSymbolName.png Val1 (yellow) Val2 (orange) Val3 (red)
''')
    exit()
else:
    outDIR = sys.argv[1]
    outSymbolName = sys.argv[2]
    val1 = int(sys.argv[3])
    val2 = int(sys.argv[4])
    val3 = int(sys.argv[5])
    
    createSMSymbol(outDIR, outSymbolName, val1, val2, val3)