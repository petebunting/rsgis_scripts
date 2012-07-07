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
# Version: 1.0
##############################################################################

import os, glob, re, sys
from PIL import Image
from PIL.ExifTags import TAGS

class CreateJPEGKMZ(object):
    
    def createKMZFile(self, inDIR, image, outXY):
        os.chdir(inDIR) # Change into input directory (for zipping files)
        imageBaseName = re.sub('\.JPG','',image.upper())
        inImageFile = os.path.join(inDIR, image)
        inPhoto = Image.open(inImageFile)
        info = inPhoto._getexif()
        photoInfo = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            photoInfo[decoded] = value
        
        if photoInfo["GPSInfo"][2][0][1] == 0:
            print "No GeoInfo for: " + inImageFile
        else:
            # Create directory (to be zipped)

            # Create quicklook image
            qlImage = imageBaseName + '_ql.png'
            convertCommand = 'convert ' + os.path.join(inDIR, image) + ' -resize 600 400 ' + os.path.join(inDIR, qlImage)

            os.system(convertCommand)   
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
            outXY.write(imageBaseName + ',' + eastingDDStr + ',' + nortingDDStr + '\n')
            
            outKMLName = imageBaseName + '_kml.kml'
            outKMLFile = os.path.join(inDIR, outKMLName)
            outKML = open(outKMLFile, 'w')
            
            outKMLText = '''
<kml xmlns="http://earth.google.com/kml/2.2">
<Document id="%s">
  <name>%s</name>
  <Snippet></Snippet>
  <Snippet></Snippet>
    <Placemark>
      <name>%s</name>
      <description>
    <a href="../%s">
    <img style="width: 600px; height: 400px;" alt="Photo" src="%s"/></a>
      </description><Snippet></Snippet>
        <Point>
            <coordinates>%s,%s</coordinates>
        </Point>
    </Placemark>
</Document></kml>
            ''' %(imageBaseName, imageBaseName, imageBaseName, image, qlImage, eastingDDStr, nortingDDStr)
            
            outKML.write(outKMLText)
            outKML.close()
            
            # Create KML archive
            zipCommand = 'zip -r ' + imageBaseName + '.kmz ' + qlImage + ' ' + outKMLName
            os.system(zipCommand)
            os.remove(qlImage)
            os.remove(outKMLName)

    def run(self, inDIR, outXYFile):
        outXY = open(outXYFile, 'w')
        outXY.write('Photo,Easting,Northing\n')
        os.chdir(inDIR)
        jpegList = glob.glob('*.JPG')
        if len(jpegList) == 0:
            jpegList = glob.glob('*.jpg')
        for image in jpegList:
            self.createKMZFile(inDIR, image, outXY)
        outXY.close()
    
    def help(self):
        print 'python CreateJPEGKMZ.py inDIR'

if __name__ == '__main__':
    obj = CreateJPEGKMZ()
    if len(sys.argv) >= 3:
        inDIR = sys.argv[1]
        outXYFile = sys.argv[2]
        obj.run(inDIR, outXYFile)
    else:
        obj.help()
    
