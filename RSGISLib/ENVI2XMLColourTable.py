############################################
# Script to read in ENVI density slice     #
# and print XML to screen                  #
############################################

import sys
import string
import re

if len(sys.argv) < 2:
	print('''
A script to produce XML for use within RSGISLib for colouring
images. Takes ENVI density slice file as input

Usage:
python ENVI2XMLColourTable.py [enviDensitySliceFile]

''')
	sys.exit()

inFileName = sys.argv[1].strip()

inFile = open(inFileName, 'r') 

i = 0
for eachLine in inFile:
    # For header row
    if(i == 0):
        print('<rsgis:command algor=\"imageutils\" option=\"colourimage\" image=\"Input Image\" output="Output Image\">')
        
    # Find and replace using regular expressions
    # re.sub( ' find ', 'replace with', 'string to search,)
    else:
        newline = re.sub('\s\n', '\n', eachLine) # Replace space spaces at the end of  line with a new line
        newline = re.sub('\s+', ',', newline) # Replace spaces in the middle of a line with a colon
    # Split Lines
        count = newline.count(',')
        #print count
        elements = newline.split(',', count)
        print('\t<rsgis:colour name=\"Class_' + str(i) + '\" id=\"' + str(i) + '\" band=\"1\" lower=\"' + elements[1] + '\" upper=\"' + elements[2] + '\" red=\"' + elements[3] + '\" green=\"' + elements[4] + '\" blue=\"' + elements[5] + '\" />')
        
    i = i + 1

print('</rsgis:command>')
                        
inFile.close()
