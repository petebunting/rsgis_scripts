#! /usr/bin/env python

#######################################
# A script to change a find and replace
# in a file name
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 28/03/2011
#######################################

import os, sys, string
import re

numArgs = len(sys.argv)
if numArgs != 4:
    print '''

A python script to change filenames in a directory based on regular expressions
Usage:
python reFindandReplaceFileName.py [inDIR] [find RE] [replace RE]

eg.,

python reFindandReplaceFileName.py /data/ '\.ptxt' '\.csv'
    
'''
    exit()

inDIR = sys.argv[1]
findString = str(sys.argv[2])
replaceString = str(sys.argv[3])

fileList = os.listdir(inDIR)

for fileName in fileList:        
    newFileName = re.sub(findString, replaceString, fileName)

    if fileName != newFileName:
        mvcmd = 'mv ' + inDIR + '/' + fileName + ' ' + inDIR + '/' + newFileName
        os.system(mvcmd)
    
