#! /usr/bin/env python

#######################################
# A class to subset a DEM based on
# gamma image coordinates
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 16/04/2010
# Version: 1.1
# 
# Update added quiet option so messages are printed
# when running from command line but
# not within other scripts
# Dan Clewley - 25/02/2011
#######################################

import os.path
import sys, re

class SubsetDEM (object):
        
    def __init__(self):
        self.quiet = True # Display minimal messages (default)
        
    def setOutputMessages(self):
        self.quiet = False # Display output
    
    def checkFile(self, testFile):
        if(os.path.isfile(testFile)):
            return True
        else:
            print 'Could not find ' + testFile
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
            except IOError, e:
                print '\nCould not open corners file: ', e
                raise IOError(e)
        else:
            raise BaseException            

    def createSubset(self, srtmName, srtmSubName, corners, projFile, res):
        dataSizeDeg = str(0.000277777777782)
        if res == 5:
            dataSizeDeg = str(0.00007524)
            
        if self.quiet:
            subCMD = 'gdalwarp -t_srs %s -te %s  %s %s %s -tr %s %s -of ENVI -ot UInt16 %s %s > temp_log.txt' % (projFile, corners[2], corners[0], corners[3], corners[1], dataSizeDeg, dataSizeDeg, srtmName, srtmSubName)
        else:
            subCMD = 'gdalwarp -t_srs %s -te %s  %s %s %s -tr %s %s -of ENVI -ot UInt16 %s %s > temp_log.txt' % (projFile, corners[2], corners[0], corners[3], corners[1], dataSizeDeg, dataSizeDeg, srtmName, srtmSubName)
            print subCMD
        os.system(subCMD)
        
    def reProjectReSample(self, srtmSubName, reProjSRTM, projFile):
        if self.quiet:
            subCMD = 'gdalwarp -t_srs %s -tr 12.5 12.5 -order 3 -r bilinear -of ENVI -ot UInt16 %s %s > temp_log.txt' % (projFile, srtmSubName, reProjSRTM)
        else:
            subCMD = 'gdalwarp -t_srs %s -tr 12.5 12.5 -order 3 -r bilinear -of ENVI -ot UInt16 %s %s' % (projFile, srtmSubName, reProjSRTM)
            print subCMD
        os.system(subCMD)          
    
    def run(self, inSRTMFile, outSRTMSub, gammaCornerFile, llProjFile, utmProjFile, res=30):
        # Check files
        self.checkFile(inSRTMFile)
        self.checkFile(gammaCornerFile)
        self.checkFile(llProjFile)
        self.checkFile(utmProjFile)
        
        tempSRTM = outSRTMSub + 'temp'
        tempSRTMhdr = tempSRTM + '.hdr'
        # Remove existing output files
        try:
            os.remove(outSRTMSub)
            if self.quiet == False:
                print 'replacing existing file: ' + outSRTMSub
        except OSError, e:
            if self.quiet == False:
                print 'saving to ' + outSRTMSub
            
        try:
            os.remove(tempSRTM)
            if self.quiet == False:
                print 'replacing existing file: ' + tempSRTM
        except OSError, e:
            if self.quiet == False:
                print 'saving temp file: ' + tempSRTM + ', will remove after'
        
        # Get corners from corners file
        outCorners = []
        self.getCorners(gammaCornerFile, outCorners)
        
        # Subset DEM
        self.createSubset(inSRTMFile, tempSRTM, outCorners, llProjFile, res)
        
        # Reproject and resample DEM
        self.reProjectReSample(tempSRTM, outSRTMSub, utmProjFile)
        
        # Remove temp DEM
        try:
            os.remove(tempSRTM)
            if self.quiet == False:
                print 'removing temp file: ' + tempSRTM
            try:
                os.remove(tempSRTMhdr)
            except OSError, e:
            	if self.quiet == False:
            	   print 'can\'t remove temp header file: ' + tempSRTM + '.env'
        except OSError, e:
            if self.quiet == False:
                print 'can\'t remove temp file: ' + tempSRTM

    def help(self):
        print 'python SubsetDEM.py <inSRTMFile> <outSRTMSub> <gammaCornerFile> <llProjFile> <utmProjFile>'
        
if __name__ == '__main__':
    obj = SubsetDEM()
    numArgs = len(sys.argv)
    if numArgs == 6:
        inSRTMFile = sys.argv[1].strip()
        outSRTMSub = sys.argv[2].strip()
        gammaCornerFile = sys.argv[3].strip()
        llProjFile = sys.argv[4].strip()
        utmProjFile = sys.argv[5].strip()
        obj.setOutputMessages()
        obj.run(inSRTMFile, outSRTMSub, gammaCornerFile, llProjFile, utmProjFile)
    else:
        obj.help()
