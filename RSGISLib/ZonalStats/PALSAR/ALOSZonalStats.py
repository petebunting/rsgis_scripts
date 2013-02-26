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
        self.gammaHH = 0
        self.gammaHV = 0
        self.topoHH = 0
        self.topoHV = 0
        self.inc = 0
        self.pix = 0
        
    def getPlot(self):
        return self.plot
    
    def getSigmaHH(self):
        return self.sigmaHH
    
    def getSigmaHV(self):
        return self.sigmaHV

    def getGammaHH(self):
        return self.gammaHH
    
    def getGammaHV(self):
        return self.gammaHV
        
    def getTopoHH(self):
        return self.gammaHH
    
    def getTopoHV(self):
        return self.gammaHV
        
    def getInc(self):
        return self.inc
    
    def getPix(self):
        return self.pix
        
    def getOutLine(self):
        outLine = str(self.sigmaHH) + ',' + str(self.sigmaHV) + ',' + str(self.gammaHH) + ',' + str(self.gammaHV) + ',' + str(self.topoHH) + ',' + str(self.topoHV) + ',' + str(self.inc) + ',' + str(self.pix)
        return outLine
    
    def getParameters(self, inLine):
        count = inLine.count(',')
        elements = inLine.split(',',count)
        
        #For transect data
        plotStr = str(elements[9])
        self.plot = re.sub('\s','',plotStr)
        self.sigmaHH = elements[14]
        self.sigmaHV = elements[15]
        self.gammaHH = elements[16]
        self.gammaHV = elements[17]
        self.topoHH = elements[18]
        self.topoHV = elements[19]
        self.inc = elements[20]
        pixStr = str(elements[21])
        pixStr = re.sub('\n','',pixStr)
        self.pix = pixStr

        # For plot data
#        plotStr = str(elements[20])
#        self.plot = re.sub('\s','',plotStr)
#        self.sigmaHH = elements[21]
#        self.sigmaHV = elements[22]
#        self.gammaHH = elements[23]
#        self.gammaHV = elements[24]
#        self.topoHH = elements[25]
#        self.topoHV = elements[26]
#        self.inc = elements[27]
#        pixStr = str(elements[28])
#        pixStr = re.sub('\n','',pixStr)
#        self.pix = pixStr   
