#! /usr/bin/env python
#############################################
# A script to recursivly find files with a given search
# string and mosaic using RGISLib.
#
# Dan Clewley (clewley@usc.edu) 12/08/2013
# 
# Line encoding example from:
# http://stackoverflow.com/questions/15817420/python-subprocess-and-type-str-doesnt-support-the-buffer-api
#############################################


import os, sys, subprocess
from time import strftime
import rsgislib
from rsgislib import imageutils
import argparse
import locale

# Get encoding (for line endings)
encoding=locale.getdefaultlocale()[1]

def getRSGISLibDataType(gdaltype):
    gdaltype = gdaltype.lower()
    if gdaltype == 'byte' or gdaltype == 'int8':
        return rsgislib.TYPE_8INT
    elif gdaltype == 'int16':
        return rsgislib.TYPE_16INT
    elif gdaltype == 'int32':
        return rsgislib.TYPE_32INT
    elif gdaltype == 'int64':
        return rsgislib.TYPE_64INT
    elif gdaltype == 'uint8':
        return rsgislib.TYPE_8UINT
    elif gdaltype == 'uint16':
        return rsgislib.TYPE_16UINT
    elif gdaltype == 'uint32':
        return rsgislib.TYPE_32UINT
    elif gdaltype == 'uint64':
        return rsgislib.TYPE_64UINT
    elif gdaltype == 'float32':
        return rsgislib.TYPE_32FLOAT
    elif gdaltype == 'float64':
        return rsgislib.TYPE_64FLOAT
     
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
parser.add_argument("-i", "--indir", type=str, required=True, help="Input directory to recursively search")
parser.add_argument("-s", "--search", type=str, required=True, help="Search string, e.g., '*kea'")
parser.add_argument("-o", "--outmosaic", type=str, required=True, help="Output mosaic file")
parser.add_argument("-ot", dest='datatype',type=str, default='Float32',help="Data type")
parser.add_argument("--backgroundval", dest='datatype',type=float, default=0,help="Background Value (Default 0)")
parser.add_argument("--skipval", dest='datatype',type=float, default=0,help="Value to be skipped (nodata values) in the input images (Default 0)")
parser.add_argument("--skipband", dest='datatype',type=int, default=1,help="Band to check for skip val (Default 1)")
parser.add_argument("--minpix", action='store_true', default=False, help="Use minimum pixel in overlap areas (default, use last in)")
parser.add_argument("--maxpix", action='store_false',default=False, help="User maximum pixel in overlap areas (default, use last in)")
args = parser.parse_args()    

overlapBehaviour = 0

if args.minpix:
    overlapBehaviour = 1

if args.maxpix:
    overlapBehaviour = 2

# Get output extension from input file
outFormat=getGDALFormat(args.outmosaic)

# Recursively find all files in the input directory using specified search string
command='find ' + args.indir + ' -name \'' + args.search + '\''
out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(stdout, stderr) = out.communicate()
# Check which python version we're using
if sys.version_info[0] > 2:
    fileList = stdout.decode(encoding).split()
else:
    fileList = stdout[:-1].split('\n')

fileCount=len(fileList)

print('Found %i files'%fileCount)

print('Creating mosaic...')
t = rsgislib.RSGISTime()
t.start(True)
imageutils.createImageMosaic(fileList, args.outmosaic, args.backgroundval, args.skipval, args.skipband, overlapBehaviour, outFormat, getRSGISLibDataType(args.datatype))
t.end()

# Create pyramids
print('\nCalculating stats and pyramids...')
t.start(True)
imageutils.popImageStats(args.outmosaic,True,0.,True)
t.end()
print('Finished')

