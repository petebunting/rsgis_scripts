#! /usr/bin/env python
#############################################
# A script to recursivly find files with a given search
# string and create an XML file to mosaic, for execution 
# in RGISLib.
#
# Dan Clewley (clewley@usc.edu) 24/05/2013
# 
# Line encoding example from:
# http://stackoverflow.com/questions/15817420/python-subprocess-and-type-str-doesnt-support-the-buffer-api
#############################################


import os, sys, subprocess
from time import strftime
import argparse
import locale

# Get encoding (for line endings)
encoding=locale.getdefaultlocale()[1]

def getGDALFormat(fileName):
    """ Get GDAL format, based on filename """
    gdalStr = ''
    extension = os.path.splitext(fileName)[-1] 
    if extension == '.env':
        gdalStr = 'ENVI'
    elif extension == '.kea':
        gdalStr = 'KEA'
    elif extension == '.tif':
        gdalStr = 'GTiff'
    elif extension == '.img':
        gdalStr = 'HFA'
    else:
        raise Exception('Type not recognised')
    
    return gdalStr

# Get input parameters
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indir", type=str, help="Input directory to recursively search")
parser.add_argument("-s", "--search", type=str, help="Search string, e.g., '*kea'")
parser.add_argument("-o", "--outmosaic", type=str, help="Output mosaic file")
parser.add_argument("-x", "--xml", type=str, help="XML file")
parser.add_argument("-ot", dest='datatype',type=str, default='Float32',help="Data type")
args = parser.parse_args()    

if args.indir == None:
    print('No input directory provided')
    parser.print_help()
    exit()

if args.search == None:
    print('No search string provided')
    parser.print_help()
    exit()

if args.outmosaic == None:
    print('No out mosaic provided')
    parser.print_help()
    exit()

if args.xml == None:
    print('No output XML provided')
    parser.print_help()
    exit()

# Get output extension from input file
outFormat=getGDALFormat(args.outmosaic)

# Get username (for XML file)
try:
    user=os.environ['USER']
except AttributeError:
    user='User'

# Get time
timeStr = strftime('%a %b %m %H:%M:%S %Y.')

outXMLFile = open(args.xml, 'w')
outXML = '''<?xml version="1.0" encoding="UTF-8" ?>
<!--
    Description:
        XML File for execution within RSGISLib
    Created by %s on %s.
    Copyright (c) 2013 USC. All rights reserved.
-->

<rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">

    <!-- Create Mosaic -->
    <rsgis:command algor="imageutils" option="mosaic" 
     output="%s"
     format="%s" datatype="%s" proj="IMAGE" 
     setSkipBand="1" nodata="0" skipValue="0" overlapBehaviour="max" >
'''%(user,timeStr,args.outmosaic,outFormat, args.datatype)

# Recursively find all files in the input directory using specified search string
command='find ' + args.indir + ' -name \'' + args.search + '\''
print(command)
out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(stdout, stderr) = out.communicate()
fileList = stdout.decode(encoding).split()

fileCount=0
# Add XML string for each file
for file in fileList:
    outXML = outXML+'''\t\t<rsgis:image file="%s" />\n'''%(file)
    fileCount+=1

outXML=outXML+'''
    </rsgis:command>
    
    <!-- Calculate stats and generate pyramids (for faster display) -->
    <rsgis:command algor="imageutils" option="popimgstats" image="%s" ignore="0" pyramids="yes" />

</rsgis:commands>'''%(args.outmosaic)

outXMLFile.write(outXML)

# Close XML file
outXMLFile.close()

print('Found %i files'%fileCount)
print('Run mosaic using:\n\trsgisexe -x ' + args.xml)



