#! /usr/bin/env python

################################
# A script to tar and move data
# 
# Author: Dan Clewley 
# Email: ddc06@aber.ac.uk
# Date 23/06/2011
###############################

import os
import sys
import string

inDIR = sys.argv[1].strip() 
outDIR = sys.argv[2].strip() 

processlist = list()

dirlist = os.listdir(inDIR)

os.chdir(inDIR)
i = 1
j = 0

processList = []

for filename in dirlist:
    if os.path.isdir(filename):
        processList.append(filename)
        j = j + 1

for filename in processList:
        print 'Processing file ' + str(i) + ' of ' + str(j)
        tarcmd = 'tar -czf ' + filename + '.tar.gz ' + filename + '/'
        mvcmd = 'mv ' + filename + '.tar.gz ' + outDIR
        #print tarcmd
        #print mvcmd
        os.system(tarcmd)
        os.system(mvcmd)
        i = i + 1

