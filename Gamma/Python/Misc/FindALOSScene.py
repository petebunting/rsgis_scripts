#!/usr/bin/env python

#####################
#  FindALOSScene.py #
#####################

import os, sys, re

inFileName = sys.argv[1]
outFileName = sys.argv[2]
searchDIR = sys.argv[3]

inFile = open(inFileName,'r')
outFile = open(outFileName,'w')

for eachLine in inFile:
    count = eachLine.count(',')
    elements = eachLine.split(',', count)
    
    #fileName = 'alpsba_031436930_47_1211307_20060828_bd_lev1.tar.gz' 
    
    fileName = re.sub('ALPSRP', '*',elements[0])
    #fileName2 = re.sub('\n', '',elements[42])
    
    outLine = re.sub('\n','',eachLine)
    
    print 'Searching for ' + fileName + '...'
    
    findFileCommand = 'find ' + searchDIR + ' -name \'' + fileName + '*.tar.gz\''
    print findFileCommand
    out = os.popen(findFileCommand)
    #print 'File Location: ' + re.sub('\n','',str(out.readline()))
    outLine = outLine + ',' + re.sub('\n','',str(out.readline()))
    #print 'Outline = ' + outLine
    out.close()
    
    #findFileCommand = 'find ' + searchDIR + ' -name \'' + fileName2 + '\''
    #print findFileCommand
    #out = os.popen(findFileCommand)
    #print 'out = ' + str(out.readline())
    #outLine = outLine + ',' + re.sub('\n','',str(out.readline()))
    #out.close()
    
    outFile.write(outLine + '\n')
    
inFile.close()
outFile.close()