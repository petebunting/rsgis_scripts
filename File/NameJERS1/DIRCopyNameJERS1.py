#! /usr/bin/env python

################################
# A python script to copy JERS-1 data to a directory,
# rename and tar.gz 
# 
# Author: Dan Clewley 
# Email: ddc06@aber.ac.uk
# Date 14/02/2009
###############################

import os
import sys
import string

from NameJERS1 import NameJERS

inDir = sys.argv[1].strip()
outDir =  sys.argv[2].strip()

print 'Copying from ' + inDir + ' to ' + outDir

processlist = list()

dirlist = os.listdir(inDir)

for filename in dirlist:
	# Check for .LAB extension
        fname = os.path.splitext(filename)[0]
        ext =  os.path.splitext(filename)[1]
        if(ext == '.LAB'):
            processlist.append(fname)
            print fname
        
# Copy files from input DIR to output DIR
copycmd = 'cp -r ' + inDir + '/* ' + outDir + '/'
permisionscmd = 'chmod -R a+wrx ' + outDir + '/*'
os.system(copycmd)
os.system(permisionscmd)

for processname in processlist:
    print 'Renaming ' + processname
    obj = NameJERS()
    obj.run(outDir, processname)
