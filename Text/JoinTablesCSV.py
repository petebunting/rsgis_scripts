#!/usr/bin/env python

#####################################
# JoinTables.py                     #
# A script to join two csv files    #
# based on a common attribute.      #
# Similar to the 'Join' feature in  #
# ArcMap                            #
#                                   #
# Author: Dan Clewley               #
# Email: ddc06@aber.ac.uk           #
# Date 30/04/2010                   #
# Version 1.1                       #
# Updated to use csv.reader         #
#####################################

import os, sys, re
import csv

class JoinTables (object):
    
    def readInData (self, inFileName, featureList, dataList, searchFeature):
        # read in refference data
        inFile = csv.reader(open(inFileName,'rU'))
        
        for line in inFile:
            featureList.append(line[searchFeature])
            dataList.append(line)

    def loopThroughData(self, refFeatureList, refDataList, matchFeatureList, matchDataList):        
        for i in range(len(refDataList)): # Loop through plots
            if i == 0:
                # Add header row
                refDataListLine = refDataList[0]
                refDataListLine = refDataListLine + matchDataList[0]
                refDataList[0] = refDataListLine
            
            else:
                found = False
                for j in range(len(matchDataList)):
                    if matchFeatureList[j] == refFeatureList[i]:
                        refDataListLine = refDataList[i]
                        refDataListLine = refDataListLine + matchDataList[j]
                        refDataList[i] = refDataListLine
                        found = True
                        break
    
    def writeOutData(self, data, outFileName):
        outFile = csv.writer(open(outFileName, 'w'))
        for i in range(len(data)):
            outFile.writerow(data[i])
    
    def run(self, inRefFileName, inMatchFileName, outFileName, refSearchFeature, matchSearchFeature):
        refFeatureList = list()
        refDataList = list()
        matchFeatureList = list()
        matchDataList = list()
        
        print('Matching column: ', matchSearchFeature, ' with: ',  refSearchFeature, ' in refference data')
        
        # Read in refference data
        print('Reading in data')
        self.readInData (inRefFileName, refFeatureList, refDataList, refSearchFeature)
        self.readInData (inMatchFileName, matchFeatureList, matchDataList, matchSearchFeature)
        
        # Match Features
        print('Matching Features')
        self.loopThroughData(refFeatureList, refDataList, matchFeatureList, matchDataList)
        
        # Write out data
        print('Saving data to: ' + outFileName)
        self.writeOutData(refDataList, outFileName)
        
    def help(self):
        print('python JoinTables.py <inRefFileName> <inMatchFileName> <outFileName> <refSearchFeature> <matchSearchFeature>')
    
if __name__ == '__main__':
    obj = JoinTables()
    numArgs = len(sys.argv)

    if numArgs == 6:
        inRefFileName = sys.argv[1]
        inMatchFileName = sys.argv[2]
        outFileName = sys.argv[3]
        refSearchFeatureStr = sys.argv[4].strip()
        matchSearchFeatureStr = sys.argv[5].strip()
        
        refSearchFeature = int(refSearchFeatureStr)
        matchSearchFeature = int(matchSearchFeatureStr)
        
        obj.run(inRefFileName, inMatchFileName, outFileName, refSearchFeature, matchSearchFeature)
    else:
        obj.help()
    
    