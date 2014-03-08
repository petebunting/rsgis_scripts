#!/usr/bin/env python
# A script to colour an image with range 0 - 50 %
# using RSGISLib
# Designed for SM raster images.
# 
# Dan Clewley (clewley@usc.edu)
# 11/11/2013
#

import subprocess, argparse, os
import tempfile as tempfile
import osgeo.gdal as gdal

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

def colourImage(inImage, outImage, band=1, outKMZ=None):
    """ Colour image using RSGISLib and optionally export as KMZ
    """
    gdalFormat = getGDALFormat(outImage)
    
    outXMLStr = '''<?xml version="1.0" encoding="UTF-8" ?>
    <!--
        Description:
            XML File for execution within RSGISLib
        Created by Dan Clewley on Wed Nov 14 10:04:09 2012.
        Copyright (c) 2012 USC. All rights reserved.
    -->
    
    <!-- Colour up soil moisture surfaces. Colour scheme RdYiBi from http://colorbrewer2.org/ -->
    
    <rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">
    
        <rsgis:command algor="imageutils" option="colourimage" 
            image="{0}" 
            output="{1}" 
            format="{2}" datatype="Byte">
            <rsgis:colour name="class_name_1" id="1"  band="{3}" lower="0" upper="0.05" red="165" green="0" blue="38" />
            <rsgis:colour name="class_name_2" id="2"  band="{3}" lower="0.05" upper="0.1" red="215" green="48" blue="39" />
            <rsgis:colour name="class_name_3" id="3"  band="{3}" lower="0.1" upper="0.15" red="244" green="109" blue="67" />
            <rsgis:colour name="class_name_3" id="4"  band="{3}" lower="0.15" upper="0.2" red="253" green="174" blue="97" />
            <rsgis:colour name="class_name_3" id="5"  band="{3}" lower="0.2" upper="0.25" red="254" green="224" blue="144" />
            <rsgis:colour name="class_name_3" id="6"  band="{3}" lower="0.25" upper="0.3" red="224" green="243" blue="248" />
            <rsgis:colour name="class_name_3" id="7"  band="{3}" lower="0.3" upper="0.35" red="171" green="217" blue="233" />
            <rsgis:colour name="class_name_3" id="8"  band="{3}" lower="0.35" upper="0.4" red="116" green="173" blue="209" />
            <rsgis:colour name="class_name_3" id="9"  band="{3}" lower="0.4" upper="0.45" red="69" green="117" blue="180" />
            <rsgis:colour name="class_name_3" id="10" band="{3}" lower="0.45" upper="0.5" red="49" green="54" blue="149" />
        </rsgis:command>
    
    </rsgis:commands>'''.format(inImage, outImage, gdalFormat, band)
            
    # Create temp XML File
    (osHandle, outXMLName) = tempfile.mkstemp(suffix='.xml')
    outFile = open(outXMLName, 'w')
    
    # Write out XML
    outFile.write(outXMLStr)
    outFile.close()
    
    subprocess.call('rsgisexe -x ' + outXMLName, shell=True)
    os.remove(outXMLName)
     
    if outKMZ is not None:
        print('Creating KMZ file...')
        subprocess.call('gdal_translate -of KMLSUPEROVERLAY {0} {1}'.format(outImage, outKMZ),shell=True)
    
    

# Get input parameters
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inimage", type=str, help="Input image",required=True)
parser.add_argument("-o", "--outimage", type=str, help="Output image", required=True)
parser.add_argument("-k", "--outkmz", type=str, default=None, help="Output KMZ file (optional)")
parser.add_argument("-b", "--band", type=int, default=1, help="Band (default = 1)")
parser.add_argument("-a", "--allbands", action='store_true', default=False, help="Run for all bands")
args = parser.parse_args()    

if not args.allbands:
     colourImage(args.inimage, args.outimage, args.band, args.outkmz)
else:
        
    outimageBase = os.path.splitext(args.outimage)[0]
    outimageExt = os.path.splitext(args.outimage)[1]

    if args.outkmz is not None:
        outKMZBase = os.path.splitext(args.outkmz)[0]
        outKMZExt = os.path.splitext(args.outkmz)[1]

    dataset = gdal.Open(args.inimage, gdal.GA_ReadOnly)
            
    # Loop through number of bands in image
    nBands = dataset.RasterCount
        
            
    for i in range(nBands):
        band = i + 1
        bandName = dataset.GetRasterBand(band).GetDescription()
        if bandName == "":
            bandName = 'b' + str(band)
        else:
            bandName = bandName.replace(' ','_')
    
        outImage = outimageBase + '_' + bandName + outimageExt
    
        if args.outkmz:
            outKMZ = outKMZBase + '_' + bandName + outKMZExt
        else:
            outKMZ = None
    
        colourImage(args.inimage, outImage, band, outKMZ)
          
    


