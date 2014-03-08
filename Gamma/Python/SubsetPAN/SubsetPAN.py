#! /usr/bin/env python

#######################################
# A class to subset a PAN based on
# gamma image coordinates
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 16/04/2010
# Version: 1.2
# 
# 1.1
# Added quiet option so messages are printed
# when running from command line but
# not within other scripts
# Dan Clewley - 25/02/2011
#
# 1.2
# Use GDAL to convert corner coordinates to target projection
# Re-projection now only performed once.
#
#######################################

import os
import subprocess
import sys, re

try:
    from osgeo import osr
except ImportError:
    print('Need GDAL (built with Python bindings) to perform coordinate transform')

class SubsetPAN (object):
        
    def __init__(self):
        self.quiet = True # Display minimal messages (default)
        
    def setOutputMessages(self):
        self.quiet = False # Display output
    
    def checkFile(self, testFile):
        if(os.path.isfile(testFile)):
            return True
        else:
            print('Could not find ' + testFile)
            raise BaseException
    
    def getCorners(self, gammaCornerFile, outCorners):
        if(os.path.isfile(gammaCornerFile)):
            #print 'Found parameters file'
            try:
                gammaCorners = open(gammaCornerFile, 'r') 
                for eachLine in gammaCorners:
                    eachLine = re.sub('\s\s+',':',eachLine)
                    eachLine = re.sub('::+',':',eachLine)
                    #print eachLine
                    count = eachLine.count(':')
                    elements = eachLine.split(':',count)
                    
                    if elements[0].strip() == 'min. latitude (deg.)':
                        outCorners.append(float(elements[1].strip()) - 0.1)
                        outCorners.append(float(elements[3].strip()) + 0.1)
                    elif elements[0].strip() == 'min. longitude (deg.)':
                        outCorners.append(float(elements[1].strip()) - 0.1)                
                        outCorners.append(float(elements[3].strip()) + 0.1)
                            
                gammaCorners.close()
            except IOError as e:
                print('\nCould not open corners file: ', e)
                raise IOError(e)
        else:
            raise BaseException            

    def convertCoordinates(self, inCoords, outProjFile):
        """ Convert coordinates from Lat/Long (WGS-84) to 
            projection defined by WKT file.
            Takes list of coordinates as tuples.
        """
        # Set source spatial reference system
        
        srcSRS = osr.SpatialReference()
        srcSRS.ImportFromEPSG(4326)
        
        # Read in WKT file
        outProjWKTFile = open(outProjFile,'r')
        outProjWKT = outProjWKTFile.read()
        outProjWKTFile.close()
        
        # Set destination spatial reference system
        dstSRS = osr.SpatialReference()
        dstSRS.ImportFromWkt(outProjWKT)
        
        # Transform coordinates
        ctr = osr.CoordinateTransformation(srcSRS, dstSRS)
        outCoordsTuple = ctr.TransformPoints(inCoords)

        # Convert to list
        outCoords = []
        for coord in outCoordsTuple:
            outCoords.append([coord[0],coord[1]])
            
        return outCoords
    
    def createSubset(self, srtmName, srtmSubName, corners, outProjFile, targetRes=30):
            
        # Buffer corners by 100 * targetRes

        corners[0][0] = corners[0][0] - 100*targetRes # xmin
        corners[0][1] = corners[0][1] - 100*targetRes # ymin
        corners[1][0] = corners[1][0] + 100*targetRes # xmax
        corners[1][1] = corners[1][1] + 100*targetRes # ymax

        if self.quiet:
            subCMD = 'gdalwarp -t_srs %s -te %s  %s %s %s -tr %s %s -of ENVI -ot UInt16 -r cubic -overwrite %s %s > /dev/null' % (outProjFile, corners[0][0], corners[0][1], corners[1][0], corners[1][1], targetRes, targetRes, srtmName, srtmSubName)
        else:
            subCMD = 'gdalwarp -t_srs %s -te %s  %s %s %s -tr %s %s -of ENVI -ot UInt16 -r cubic -overwrite %s %s' % (outProjFile, corners[0][0], corners[0][1], corners[1][0], corners[1][1], targetRes, targetRes, srtmName, srtmSubName)
            print(subCMD)
        subprocess.call(subCMD,shell=True)  
    
    def run(self, inSRTMFile, outSRTMSub, gammaCornerFile, outProjFile, targetRes=30):
        # Check files
        self.checkFile(inSRTMFile)
        self.checkFile(gammaCornerFile)
        self.checkFile(outProjFile)
        
        # Get corners from corners file
        outCorners = []
        self.getCorners(gammaCornerFile,outCorners)
        
        outCornersTuple = [(outCorners[2], outCorners[0]), (outCorners[3], outCorners[1])]
        
        # Get corners in target projection
        cornersDSR = self.convertCoordinates(outCornersTuple, outProjFile)
        
        # Subset PAN
        self.createSubset(inSRTMFile, outSRTMSub, cornersDSR, outProjFile, targetRes)
        

    def help(self):
        print('python SubsetPAN.py <inSRTMFile> <outSRTMSub> <gammaCornerFile> <outProjFile> <target res>')
        
if __name__ == '__main__':
    obj = SubsetPAN()
    numArgs = len(sys.argv)
    if numArgs == 6:
        inSRTMFile = sys.argv[1].strip()
        outSRTMSub = sys.argv[2].strip()
        gammaCornerFile = sys.argv[3].strip()
        outProjFile = sys.argv[4].strip()
        targetRes = float(sys.argv[5].strip())
        obj.setOutputMessages()
        obj.run(inSRTMFile, outSRTMSub, gammaCornerFile, outProjFile, targetRes)
    else:
        obj.help()
