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

i = 1
j = 0

delList = ['*.topo*','*.gamma*','*tif*', ]
processList = []

os.chdir(outDIR)

for filename in dirlist:
    if os.path.isdir(filename):
        processList.append(filename)
        j = j + 1

for filename in processList:
        print 'Processing file ' + str(i) + ' of ' + str(j)
        mvcmd = 'cp -r ' + inDIR + '/' + filename + ' ' + outDIR + '/'
        os.system(mvcmd)
        for item in delList:
            os.remove(outDIR + '/' + filename + '/' + item)
        tarcmd = 'tar -czf ' + filename + '.tar.gz ' + filename + '/'
        os.system(tarcmd)
        #delcmd = 're -fr ' + outDIR + '/' + filename 
        #os.system(delcmd)
        i = i + 1

