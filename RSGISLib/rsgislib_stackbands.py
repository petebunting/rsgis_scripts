#!/usr/bin/env python

# Stack selected files in a directory and name based on file name
# Daniel Clewley (daniel.clewley@googlemail.com)
# 17/03/2014


import os
import fnmatch
import argparse
import rsgislib
from rsgislib import imageutils

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
parser.add_argument("-o", "--outstack", type=str, required=True, help="Output stack file")
parser.add_argument("-ot",'--datatype',type=str, default='Float32',help="Data type")
args = parser.parse_args()   

# Get output extension from file
outFormat=getGDALFormat(args.outstack)

imageList = []
bandNamesList = []

fileList = os.listdir(args.indir)

replaceFileStrList = args.search.split('*')

for fName in fileList:
    if fnmatch.fnmatch(fName, args.search): # Match search string
        imageList.append(os.path.join(args.indir,fName))
        for replaceFileStr in replaceFileStrList:
            bandName = fName.replace(replaceFileStr,'')
        bandNamesList.append(bandName)

gdalformat = 'KEA'
dataType = rsgislib.TYPE_32FLOAT

# Stack bands
imageutils.stackImageBands(imageList, bandNamesList, args.outstack, None, 0, 'KEA', getRSGISLibDataType(args.datatype))

# Calculate stats
imageutils.popImageStats(args.outstack,True,0.,True)


