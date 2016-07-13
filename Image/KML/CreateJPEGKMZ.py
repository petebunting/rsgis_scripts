#! /usr/bin/env python

##############################################################################
# CreateJPEGKMZ.py
# A class to read EXIF data from geotageged JPEG files and 
# create a KMZ File containing a quick look PNG
# 
# Function for reading EXIF data modified from one 
# proposed on http://stackoverflow.com/questions/765396/exif-manipulation-library-for-python
# 
# Author: Dan Clewley
# Email: daniel.clewley@gmail.com
# Date: 06/06/2012
# Version: 1.1
#
# 13/07/2016
# Updated code and made compatible with Python 3.
# Requires pillow library.
##############################################################################

from __future__ import print_function
import argparse
import csv
import os
import glob
import sys
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS

def createKMZFile(inImageFile, outDIR, outXY=None):
    """
    Create a KMZ file from a geotagged photo
    """
    imageBaseName = os.path.basename(inImageFile)
    imageBaseName = os.path.splitext(imageBaseName)[0]
    # Replace spaces
    imageBaseName = imageBaseName.replace(' ', '_')
    inPhoto = Image.open(inImageFile)
    info = inPhoto._getexif()
    photoInfo = {}
    for tag, value in list(info.items()):
        decoded = TAGS.get(tag, tag)
        photoInfo[decoded] = value
        
    try:
        if photoInfo["GPSInfo"][2][0][1] == 0:
            print("No GeoInfo for: {}".format(inImageFile),
                  file=sys.stderr)
    except KeyError:
        print("No Geotags for : " + inImageFile)
    else:
       
        # Get coordinated from photo   
        northSouth = photoInfo["GPSInfo"][1]
        northingDeg = photoInfo["GPSInfo"][2][0][0] / photoInfo["GPSInfo"][2][0][1]
        northingMin = photoInfo["GPSInfo"][2][1][0] / photoInfo["GPSInfo"][2][1][1]
        northingSec = float(photoInfo["GPSInfo"][2][2][0]) / float(photoInfo["GPSInfo"][2][2][1])
        
        eastWest = photoInfo["GPSInfo"][3]
        eastingDeg= photoInfo["GPSInfo"][4][0][0] / photoInfo["GPSInfo"][4][0][1]
        eastingMin = photoInfo["GPSInfo"][4][1][0] / photoInfo["GPSInfo"][4][1][1]
        eastingSec = float(photoInfo["GPSInfo"][4][2][0]) / float(photoInfo["GPSInfo"][4][2][1])
        
        eastingDD = eastingDeg + (eastingMin / 60.) + (eastingSec / 3600.)
        nortingDD = northingDeg + (northingMin / 60.) + (northingSec / 3600.)
        
        northSouthStr = ''
        if northSouth == 'S':
            northSouthStr = '-'
            
        eastWestStr = ''
        if eastWest == 'W':
            eastWestStr = '-'
        
        eastingDDStr = eastWestStr + str(eastingDD)
        nortingDDStr = northSouthStr+ str(nortingDD)
        
        # Write out to text file
        if outXY is not None:
            outXY.writerow([imageBaseName, eastingDDStr, nortingDDStr])
        
        if outDIR is not None:
            os.chdir(outDIR) # Change into input directory (for zipping files)
            # Create quicklook image (using imagemagick)
            qlImage = imageBaseName + '_ql.png'
            convertCommand = ['convert',
                              '-thumbnail', '600',
                              inImageFile,
                              os.path.join(outDIR, qlImage)]
            subprocess.check_call(convertCommand)
            outKMLName = imageBaseName + '_kml.kml'
            outKMLFile = os.path.join(outDIR, outKMLName)
            outKML = open(outKMLFile, 'w')
            
            outKMLText = '''
<kml xmlns="http://earth.google.com/kml/2.2">
<Document id="{0}">
  <name>{0}</name>
  <Snippet></Snippet>
  <Snippet></Snippet>
    <Placemark>
      <name>{0}</name>
      <description>
    <a href="file://{1}">
    <img style="width: 600px" alt="Photo" src="{2}"/></a>
      </description><Snippet></Snippet>
        <Point>
            <coordinates>{3},{4}</coordinates>
        </Point>
    </Placemark>
</Document></kml>
            '''.format(imageBaseName, inImageFile,
                       qlImage, eastingDDStr, nortingDDStr)
            
            outKML.write(outKMLText)
            outKML.close()
        
            # Create KML archive
            zipCommand = ['zip', '-r', 
                          imageBaseName + '.kmz',
                          qlImage, outKMLName]
            subprocess.check_call(zipCommand)
            os.remove(qlImage)
            os.remove(outKMLName)

            print(' Saved to: {}.kmz'.format(imageBaseName))

def processAllInDIR(inDIR, outDIR, outXYFile=None):
    """
    Process all JPEG files within a directory
    """
    # If an output CSV file is provided open
    # a CSV writer.
    if outXYFile is not None:
        outXYHandler = open(outXYFile, 'w')
        outCSV = csv.writer(outXYHandler)
        outCSV.writerow(['Photo' ,'Easting', 'Northing'])
    else:
        outCSV = None

    # Convert to absolute paths
    inDIR = os.path.abspath(inDIR)
    if outDIR is not None:
        outDIR = os.path.abspath(outDIR)

    jpegList = glob.glob(os.path.join(inDIR, '*.[Jj][Pp][Gg]'))

    for i, image in enumerate(jpegList):
        print('{}/{}'.format(i+1, len(jpegList)))
        createKMZFile(image, outDIR, outCSV)

    if outXYFile is not None:
        print('Saved coordinates to: {}'.format(outXYFile))
        outXYHandler.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', nargs=1, type=str,
                        help='Input directory containing JPEGS')
    parser.add_argument('--outkmz',
                        required=False,
                        help='Output KML directory')
    parser.add_argument('--outcsv',
                        required=False,
                        help='Output CSV file')
    args = parser.parse_args()

    processAllInDIR(args.inputdir[0], args.outkmz, args.outcsv)
