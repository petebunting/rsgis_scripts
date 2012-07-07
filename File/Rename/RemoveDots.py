#! /usr/bin/env python

#######################################
# A script to remove dots in a filename
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 12/05/2009
#######################################

import os, sys, string

processdir = list()
inDIR = sys.argv[1]

# Find Gamma0 Files
fileList = os.listdir(inDIR)

for fileName in fileList:
    count = fileName.count('.')
    elements = fileName.split('.', count)
    newFileName = ""
    i = 0
    if count > 0:
        while i < count - 1:
            newFileName = newFileName + elements[i] + '_'
            i = i + 1
        newFileName = newFileName + elements[count - 1]
        newFileName = newFileName + '.' + elements[count]
        print newFileName
        
        mvcmd = 'mv ' + inDIR + '/' + fileName + ' ' + inDIR + '/' + newFileName
        os.system(mvcmd)
    