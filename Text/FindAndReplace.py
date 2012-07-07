import sys
import string
import re

inFileName = sys.argv[1].strip()
outFileName = sys.argv[2].strip()

inFile = open(inFileName, 'r') 
outFile = open(outFileName,'w')

i = 0
for eachLine in parFile:
    # For header row
    if(i == 0):
        outFile.write(eachLine)
    
    # Find and replace using regular expressions
    # re.sub( ' find ', 'replace with', 'string to search,)
    else:
        newline = re.sub('\s\s+\n', '\n', eachLine) # Replace two or more spaces at the end of  line with a new line
        newline = re.sub('\s\s+', ' : ', newline) # Replace two or more spaces in the middle of a line with a colon
        newParFile.write(newline)
    i = i + 1
                        
inFile.close()
outFile.close()