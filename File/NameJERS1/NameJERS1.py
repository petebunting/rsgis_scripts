#! /usr/bin/env python

#######################################
# A class to rename JERS-1 data
# copied from CD /  DVD
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 11/02/2009
#######################################

import os.path
import sys
import re

class NameJERS (object) :

    def getSceneName(self, parFilename):
        parFile = open(parFilename, 'r')
        
        for eachLine in parFile:
            #print eachLine
            eachLine = re.sub('\s\s+\n', '\n', eachLine) # Check for two or more spaces at the end of a line and remove
            eachLine = re.sub('\s\s+', ' : ', eachLine) # Check for two or more spaces in the middle of a line  and replace with ' : '
            count = eachLine.count(':')
            #print count
            elements = eachLine.split(':', count)
            
            if(count == 2):
                elements[0] = elements[0].strip()
                elements[1] = elements[1].strip()
                elements[2] = elements[2].strip()
            
                if(elements[0] == 'Granule ID'):
                    #print elements[0]
                    jaxaSceneName = elements[1]
                    #print 'Scene name: ' + jaxaSceneName
                
            elif(count == 3):
                elements[0] = elements[0].strip()
                elements[1] = elements[1].strip()
                elements[2] = elements[2].strip()
                elements[3] = elements[3].strip()
            
                if(elements[2] == 'W/O No.'):
                    orderNo = elements[3]
                    #print 'Order number: ' + orderNo
            
            elif(count == 7):
                elements[0] = elements[0].strip()
                elements[1] = elements[1].strip()
                elements[2] = elements[2].strip()
                elements[3] = elements[3].strip()
                elements[4] = elements[4].strip()
                elements[5] = elements[5].strip()
                elements[6] = elements[6].strip()
                elements[7] = elements[7].strip()
                
                if(elements[2] == 'Processing Level'):
                    processingLevel = elements[3]
                    processingLevel = re.sub('\.','_', processingLevel)
                    #print 'Processing Level: ' + processingLevel
                elif(elements[4] == 'Center Latitude'):
                    centerLat = elements[5]          
                elif(elements[4] == 'Center Longitude'):
                    centerLong = elements[5]
                elif(elements[2] == 'Map Projection'):
                    mapProjection = elements[3]
                elif(elements[0] == 'Obs. Date'):
                    obsdate = elements[1]
                    obsdate = re.sub('/','',obsdate)
                    #print 'Obs. Date: ' + obsdate
                elif(elements[4] == 'Number of Pixels'):
                    nPixels = elements[5]
                    #print 'Number of Pixels: ' + nPixels
                elif(elements[4] == 'Number of Lines'):
                    nLines = elements[5]
                    #print 'Number of Lines: ' + nLines
                elif(elements[2] == 'Multi Look'):
                    mLook = elements[3]
                elif(elements[0] == 'Path-Row'):
                    pathRow = elements[1]
                    pathRow = re.sub('-','',pathRow)
                    pathRow = re.sub('\s','',pathRow)
                    #print 'Path-Row: ' + pathRow
                elif(elements[2] == 'Pixel Spacing'):
                    pixelSpaceing = elements[3]
                                
        if(processingLevel == '0'):
            processingLevel = '1'
        
        sceneName = 'j1saba_' + pathRow + '_' + obsdate + '_lev' + processingLevel
        
        parFile.close()
        
        return sceneName
        
    def renameFolder(self, inDIR, folderName, sceneDIRName):
        oldFolder = inDIR + '/' + folderName
        newFolder = inDIR + '/' + sceneDIRName
        mvcmd = 'mv ' + oldFolder + ' ' + newFolder
        os.system(mvcmd)
        
    def renameMoveLAB(self, inDIR, folderName, sceneName):
        # Can reneme .LAB file to same name as folder
        oldLAB = inDIR + folderName + '.LAB'
        #newLAB = inDIR + sceneName + '.LAB'
        #renamecmd = 'mv ' + oldLAB + ' ' + newLAB
        #mvcmd = 'mv ' + newLAB + '  ' + inDIR + '/' + sceneName
        mvcmd = 'mv ' + oldLAB + '  ' + inDIR + '/' + sceneName
        #os.system(renamecmd)
        os.system(mvcmd)

    def getHeaderFileName(self, dirPath, folderName):
        sceneLABfile = dirPath + '/' + folderName + '.LAB'
        return sceneLABfile
        
    def tarFile(self, inDIR, sceneName):
        tarcmd = 'tar -czf ' + inDIR + '/' + sceneName + '.tar.gz  ' + inDIR + '/' + sceneName + '/'
        os.system(tarcmd)
    
    def run(self, inDIR, folderName):
        sceneLABfile = self.getHeaderFileName(inDIR, folderName)
        sceneName = self.getSceneName(sceneLABfile)
        self.renameFolder(inDIR, folderName, sceneName)
        self.renameMoveLAB(inDIR, folderName, sceneName)
        #self.tarFile(inDIR, sceneName)
        
if __name__ == '__main__':
    inDIR =  sys.argv[1].strip()
    folderName = sys.argv[2].strip()
    obj = NameJERS()
    obj.run(inDIR, folderName)
        
    