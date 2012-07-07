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

    def __init__(self, sceneDIR, mode):
        self.sceneDIR = sceneDIR
        self.scenename = self.removeFilePathUNIX(sceneDIR)
        self.mode = mode
        self.dataOwner = "Richard Lucas / Dan Clewley"
        self.dataContact = "rml@aber.ac.uk / ddc06@aber.ac.uk"
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
ALOS PALSAR %s data

Processed to Level 1.5 (georeffernced product)
Using BatchGamma%s.py
All SAR processing using GAMMA, with CSH scripts included
in directory.

Products:
*.utm - Georeffernced sigma0 data
*.gamma.utm - Georefferenced gamma0 data
*.topo.utm - Georefferenced topographicaly corrected data (Using the method of Castel et al. 2001)
*.inc - Local incidence angle image
*.pix - Local pixel area (relative to 'flat' projection of pixel)

Process Date: %s
Contact: %s
Email: %s
        
        ''' % (self.scenename, self.mode,  self.mode, self.importTime, self.dataOwner, self.dataContact)
        
        return metatxt
        
    def writeMetaText(self):
        outFileName = self.sceneDIR + '/au_process_readme.txt'
        outFile = open(outFileName, 'w')
        outFile.write(self.createMetaText())
        outFile.close()
        
if __name__ == '__main__':
    # Test program
    obj = BatchGammaMeta("/Users/danclewley/Desktop/Test/", "FBD")
    obj.writeMetaText()
