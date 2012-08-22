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

import os, glob, re, sys, csv

class CreateJPEGKMZ(object):
    
    def createKMZFile(self, inDIR, image, inXYLocationsFile):
        os.chdir(inDIR) # Change into input directory (for zipping files)
        imageBaseName = re.sub('\.JPG','',image.upper())
        imageBaseName = re.sub('\.jpg','',imageBaseName)
        inImageFile = os.path.join(inDIR, image)
        
        foundGeo = False

        # Find lat long in XYLocationsFile
        inXYLocations = csv.reader(open(inXYLocationsFile,'rU'))
        for line in inXYLocations:
            if line[0].strip() == imageBaseName:
                foundGeo = True      

        if foundGeo == False:
            print "No GeoInfo for: " + inImageFile
        else:
            # Create quicklook image (using imagemagick)
            qlImage = imageBaseName + '_ql.png'
            convertCommand = 'convert ' + os.path.join(inDIR, image) + ' -resize 600 400 ' + os.path.join(inDIR, qlImage)
            os.system(convertCommand)
            
            eastingDDStr = str(line[2])
            nortingDDStr = str(line[1])
            
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

    def run(self, inDIR, inXYLocationsFile):
        os.chdir(inDIR)
        jpegList = glob.glob('*.JPG')
        if len(jpegList) == 0:
            jpegList = glob.glob('*.jpg')
        for image in jpegList:
            self.createKMZFile(inDIR, image, inXYLocationsFile)
    
    def help(self):
        print 'python CreateJPEGKMZ.py inDIR'

if __name__ == '__main__':
    obj = CreateJPEGKMZ()
    if len(sys.argv) >= 3:
        inDIR = sys.argv[1]
        inXYLocationsFile = sys.argv[2]
        obj.run(inDIR, inXYLocationsFile)
    else:
        obj.help()
    
