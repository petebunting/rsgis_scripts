#! /usr/bin/env python
# catFilesWithHeader.py
#
# A script to join multiple files to a single
# file. Takes header from first file only.
#
# Dan Clewley (daniel.clewley@gmail.com)
# 03/04/2013
#

import os, sys, glob

if len(sys.argv) < 3:
    print '''Not enough parameters provided.
Usage:
    python catFilesWithHeader.py inSearch outFileName
e.g.,
    python catFilesWithHeader.py '/data/text*.txt' /joined/all.txt
'''
    exit()    

inSearch=sys.argv[1]
outFileName=sys.argv[2]

# Open outfile 
outFile = open(outFileName,'w')

print ' --'
print inSearch
print '--'

fileList = glob.glob(inSearch)

firstFile = True
fileCount = 0

for inFileName in fileList:
    fileCount+=1
    inFile = open(inFileName,'rU')
    if firstFile:
        outFile.write(inFile.next())
        firstFile = False
    else:
        inFile.next()
    for line in inFile:
        outFile.write(line)
    inFile.close()
    
outFile.close()

print 'Wrote ' + str(fileCount) + ' files to:'
print ' ' + outFileName
    
