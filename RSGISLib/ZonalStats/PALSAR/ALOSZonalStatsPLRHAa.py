#!/usr/bin/env python

###############################
# ALOSZonalStats.py           #
# Class to store extracted    #
# ALOS Zonal stats            #
#                             #
# Author: Dan Clewley         #
# Email: ddc06@aber.ac.uk     #
# Date 28/04/2010             #  
###############################

import os, sys, re

class ALOSZonalStats (object):
    
    def __init__(self):
        self.plot = ''
        self.sigmaHH = 0
        self.sigmaHV = 0
        self.sigmaVV = 0
        self.gammaHH = 0
        self.gammaHV = 0
        self.gammaVV = 0
        self.topoHH = 0
        self.topoHV = 0
        self.topoVV = 0
        self.alpha = 0
        self.anisotropy = 0
        self.entropy = 0
        self.inc = 0
        self.pix = 0
        
    def getPlot(self):
        return self.plot
    
    def getSigmaHH(self):
        return self.sigmaHH
    
    def getSigmaHV(self):
        return self.sigmaHV

    def getSigmaVV(self):
        return self.sigmaVV

    def getGammaHH(self):
        return self.gammaHH
    
    def getGammaHV(self):
        return self.gammaHV

    def getGammaVV(self):
        return self.gammaVV
        
    def getTopoHH(self):
        return self.gammaHH
    
    def getTopoHV(self):
        return self.gammaHV
        
    def getTopoVV(self):
        return self.gammaVV
        
    def getAlpha(self):
        return self.alpha
    
    def getAnisotropy(self):
        return self.anisotropy
        
    def getEntropy(self):
        return self.entropy
        
    def getInc(self):
        return self.inc
    
    def getPix(self):
        return self.pix
        
    def getOutLine(self):
        outLine = str(self.sigmaHH) + ',' + str(self.sigmaHV) + ',' + str(self.sigmaVV) + ',' + str(self.gammaHH) + ',' + str(self.gammaHV) + ',' + str(self.gammaVV) + ',' + str(self.topoHH) + ',' + str(self.topoHV) + ',' + str(self.topoVV) + ',' + str(self.alpha) + ',' + str(self.anisotropy) + ',' + str(self.entropy) + ',' + str(self.inc) + ',' + str(self.pix)
        return outLine
    
    def getParameters(self, inLine):
        count = inLine.count(',')
        elements = inLine.split(',',count)
        
        #For transect data
#        plotStr = str(elements[9])
#        self.plot = re.sub('\s','',plotStr)
#        self.sigmaHH = elements[14]
#        self.sigmaHV = elements[15]
#        self.sigmaVV = elements[16]
#        self.gammaHH = elements[17]
#        self.gammaHV = elements[18]
#        self.gammaVV = elements[19]
#        self.topoHH = elements[20]
#        self.topoHV = elements[21]
#        self.topoVV = elements[22]
#        self.inc = elements[23]
#        pixStr = str(elements[24])
#        pixStr = re.sub('\n','',pixStr)
#        self.pix = pixStr

        # For plot data
        plotStr = str(elements[20])
        self.plot = re.sub('\s','',plotStr)
        self.sigmaHH = elements[21]
        self.sigmaHV = elements[22]
        self.sigmaVV = elements[23]
        self.gammaHH = elements[24]
        self.gammaHV = elements[25]
        self.gammaVV = elements[26]
        self.topoHH = elements[27]
        self.topoHV = elements[28]
        self.topoVV = elements[29]
        self.alpha = elements[30]
        self.anisotropy = elements[31]
        self.entropy = elements[32]
        self.inc = elements[33]
        pixStr = str(elements[34])
        pixStr = re.sub('\n','',pixStr)
        self.pix = pixStr   
