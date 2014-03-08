#! /usr/bin/env python

#######################################
# A class to generate a readme file
# for ALOS data processed with
# BatchGamma
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 24/02/2011
# Version: 1.0
#######################################

import sys
from datetime import date

class BatchGammaMeta (object):

    def __init__(self, sceneDIR, dataOwner, dataContact):
        self.sceneDIR = sceneDIR
        self.scenename = self.removeFilePathUNIX(sceneDIR)
        self.dataOwner = dataOwner
        self.dataContact = dataContact
        d = date.today()
        self.importTime = str(d.strftime("%d/%m/%y"))
        
    def removeFilePathUNIX(self, name):
        name = name.strip()
        count = name.count('/')
        nameSegments = name.split('/', count)
        outName = nameSegments[count]
        if outName == '': # For / at the end of DIR path
            outName = nameSegments[count-1]
        if outName == '': # For // at the end of DIR path
            outName = nameSegments[count-2]
        return outName
    
    def createMetaText(self):
        metatxt = '''
%s
ALOS PALSAR data

Processed to Level 1.5.

All SAR processing using GAMMA (http://www.gamma-rs.ch/), with CSH scripts included in directory.

Products:
*.utm - Georeffernced sigma0 data
*.topo.utm - Georefferenced topographicaly corrected data (using the method of Castel et al. 2001)
*.inc - Local incidence angle image
*.pix - Local pixel area (relative to 'flat' projection of pixel)
*.png - Quick look images (stretched)

Process Date: %s
Contact: %s
Email: %s
        
        ''' % (self.scenename, self.importTime, self.dataOwner, self.dataContact)
        
        return metatxt
        
    def writeMetaText(self):
        outFileName = self.sceneDIR + '/processing_readme.txt'
        outFile = open(outFileName, 'w')
        outFile.write(self.createMetaText())
        outFile.close()
        
if __name__ == '__main__':
    # Test program
    obj = BatchGammaMeta("/home/danclewley/Desktop/", "Dan Clewley / Richard Lucas", "ddc06@aber.ac.uk")
    obj.writeMetaText()
