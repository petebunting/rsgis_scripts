import sys
import string
import re

inFileName = sys.argv[1].strip()
outFileName = sys.argv[2].strip()

print 'Infile = ' + inFileName
print 'Outfile = ' + outFileName

inFile = open(inFileName, 'r') 
outFile = open(outFileName,'w')

i = 0
for eachLine in inFile:
    # For header row
    if(i == 0):
        outFile.write(eachLine)
    elif(i == 1):
        outFile.write(eachLine)
    
    else:
        # Split Lines
        count = eachLine.count(',')
        elements = eachLine.split(',', count)
        # Maths expression
        newDensity = float(elements[1]) / 10000
        newLine = elements[0] + ',' + str(newDensity) + ',' + elements[2]
        outFile.write(newLine)
    i = i + 1
                        
inFile.close()
outFile.close()

print 'Done'