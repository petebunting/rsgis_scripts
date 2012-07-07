#! /usr/bin/env python

################################
# A python script to copy JERS-1 data to a directory,
# rename and tar.gz 
# 
# Author: Dan Clewley 
# Email: ddc06@aber.ac.uk
# Date 14/02/2009
###############################

# Called using:
# pyhton DIRCopyNameJERS1outParFile.py [inDIR] [outDIR] [outParFile] [new / append]

import os
import sys
import string

from NameJERS1outParFile import NameJERSoutParFile

inDir = sys.argv[1].strip()
outDir =  sys.argv[2].strip()
outParFile = sys.argv[3].strip()
parAppend = sys.argv[4].strip()

# Check is writing parameters to new file or existing file
if(parAppend == 'new'):
    print 'Writing parameters to new text file: ' + outParFile
    outPar = open(outParFile, 'w')
    header = 'OutName,OrderNumber,JAXAName,ProcessingLevel,PathRow,Date,CenterLat,CenterLong\n'
    outPar.write(header)
    outPar.close()
elif(parAppend == 'append'):
    print 'Writing to exising file: ' + outParFile
else:
    print 'Please select new or append'

print 'Copying from ' + inDir + ' to ' + outDir

processlist = list()

dirlist = os.listdir(inDir)

i = 0
for filename in dirlist:
	# Check for .LAB extension
        fname = os.path.splitext(filename)[0]
        ext =  os.path.splitext(filename)[1]
        if(ext == '.LAB'):
			i = i + 1
			processlist.append(fname)
        

j = 1

for processname in processlist:
    # Copy files from input DIR to output DIR
    print 'Copying ' + processname + '\n'
    print '\t file ' + str(j) + ' of ' + str(i)
    
    copycmd = 'cp -r ' + inDir + '/' + processname + '* ' + outDir + '/'
    permisionscmd = 'chmod -R a+wrx ' + outDir + '/' + 'SCENE*'
    os.system(copycmd)
    os.system(permisionscmd)

    print 'Renaming ' + processname
    obj = NameJERSoutParFile()
    obj.run(outDir, processname, outParFile)
    
    j = j + 1
