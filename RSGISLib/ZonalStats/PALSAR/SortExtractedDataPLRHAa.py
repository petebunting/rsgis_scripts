#!/usr/bin/env python

####################################
####################################
## SortExtractedData.py           ##
## Script to sort zonal stats     ##
## data into single spreadsheet   ##
##                                ##
## Author: Dan Clewley            ##
## Email: ddc06@aber.ac.uk        ##
## Date 28/04/2010                ##
####################################
####################################

import os, sys, re
from ALOSZonalStatsPLRHAa import ALOSZonalStats

class SortExtractedData (object):

    def readInPlotData (self, inFileName, plots, plotsData):
        # Read plot data in to two lists.
        # 'plots' containing only the plot name and 
        # 'plotsData' containing the entire line
        inFile = open(inFileName,'r')
        
        for line in inFile:
            count = line.count(',')
            elements = line.split(',',count)
                        
            plots.append(elements[0]) # Add plotname to list
            
            line = re.sub('\n','',line) 
            plotsData.append(line)    # Add complete line to seperate list

        inFile.close()
        
    def findExtension(self, filename, ext):
        # Check for file extension
        # Allows for dots within file name
        count = filename.count('.')
        elements = filename.split('.',count)
        if elements[count] == ext:
            return True
        else:
            return False
            
    def readInZonalStats(self, inZonalStatsFile, zonalStatsData):
        # Read zonal stats file to 'ALOSZonalStats' object
        inFile = open(inZonalStatsFile,'r')

        for line in inFile:
            statsPar = ALOSZonalStats()
            statsPar.getParameters(line)
            zonalStatsData.append(statsPar)
        inFile.close()
    
    def generateHeaderRow(self, fileName):
        # Create names for output column headings
        sceneName = re.sub('\.csv','',fileName)
        headerRow = ''
        headerRow = headerRow + sceneName + '_sigma0HH,'
        headerRow = headerRow + sceneName + '_sigma0HV,'
        headerRow = headerRow + sceneName + '_sigma0VV,'
        headerRow = headerRow + sceneName + '_gamma0HH,'
        headerRow = headerRow + sceneName + '_gamma0HV,'
        headerRow = headerRow + sceneName + '_gamma0VV,'
        headerRow = headerRow + sceneName + '_topoHH,'
        headerRow = headerRow + sceneName + '_topoHV,'
        headerRow = headerRow + sceneName + '_topoVV,'
        headerRow = headerRow + sceneName + '_alpha,'
        headerRow = headerRow + sceneName + '_anisotropy,'
        headerRow = headerRow + sceneName + '_entropy,'
        headerRow = headerRow + sceneName + '_inc,'
        headerRow = headerRow + sceneName + '_pix'
        
        return headerRow
    
    def addMatchingPlots(self, plots, plotsData, zonalStatsData, sceneName):
        # Loop through plot / transect data and find matching plots in zonal stats for that scene.
        # If the scene doesn't cover a plot a blank line is written.
        # Zeros could be written instead
        blankLine = ',,,,,,,,,,,,,'
        #blankLine = ',0,0,0,0,0,0,0,0'
        
        for i in range(len(plots)): # Loop through plots
            if i == 0:
                # Add header row
                headerRow = self.generateHeaderRow(sceneName)
                plotsDataLine = plotsData[0]
                plotsDataLine = plotsDataLine + ',' + headerRow
                plotsData[0] = plotsDataLine
            
            else:
                plotName = plots[i]
                found = False
                for zonalStatsElement in zonalStatsData:       
                    #print 'zonalStatsElement.getPlot() = ' + zonalStatsElement.getPlot()
                    #print 'plotName = ' + plotName
                    if zonalStatsElement.getPlot() == plotName:
                        plotsDataLine = plotsData[i]
                        plotsDataLine = plotsDataLine + ',' + zonalStatsElement.getOutLine()
                        plotsData[i] = plotsDataLine
                        found = True
                        break
                        
                if found == False:
                        plotsDataLine = plotsData[i]
                        plotsDataLine = plotsDataLine + blankLine
                        plotsData[i] = plotsDataLine
                
    def writeOutData(self, plotsData, outFileName):
        # Loop through plots data and save out to text file
        outFile = open(outFileName, 'w')
        for i in range(len(plotsData)):
            outLine = plotsData[i] + '\n'
            outFile.write(outLine)
        
    def run(self, inFileName, inDIR, outFileName):
        # Read in inFile containing plot data
        plots = list()
        plotsData = list()
        
        self.readInPlotData(inFileName, plots, plotsData)
        
        # Loop through inDIR
        filelist = list()
        fileList = os.listdir(inDIR)
        
        for filename in fileList:
            #zonalStatsData = list()
            zonalStatsData = []
            if self.findExtension(filename, 'csv'):
                # Add matching plots
                fileNamePath = inDIR + '/' + filename
                print 'Processing ' + filename
                self.readInZonalStats(fileNamePath, zonalStatsData)
                self.addMatchingPlots(plots, plotsData, zonalStatsData, filename)
                
            del zonalStatsData
        
        # Write out Data
        self.writeOutData(plotsData, outFileName)
    
    def help(self):
        print 'python SortExtractedData <inFileName> <inDIR> <outFileName>'
        
if __name__ == '__main__':
    obj = SortExtractedData()
    numArgs = len(sys.argv)

    if numArgs == 4:
        inFileName = sys.argv[1]
        inDIR = sys.argv[2]
        outFileName = sys.argv[3]
        obj.run(inFileName, inDIR, outFileName)
    else:
        obj.help()
