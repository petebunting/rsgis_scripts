 #! /usr/bin/env python

#######################################
# A python script to plot time-series
# soil moisture information and save
# as PDF
#
# Used as part of SoilSCAPE website
#
# Email: daniel.clewley@gmail.com
# Date: 28/08/2012
# Version: 1.0
#######################################

import sys, os, csv
#os.environ['MPLCONFIGDIR'] = '/var/www/webmapping/datadownloads'
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as matdate
from time import time, struct_time, mktime, strptime, gmtime
from datetime import datetime
import calendar
from scipy import signal
# Turn of warnings for polyfit
import warnings
warnings.simplefilter('ignore', np.RankWarning)

class createPlotFromCSV (object):
    ''' Creates plots from CSV data for soil moisture sensors.
Data is assumed to have the following format.
'uniqueID','bsID','lcID','edID','measFlags', 'year','month','day','hour','minute','second','S1_depthcm','S2_depthcm','S3_depthcm','S1_depthcm_raw','S2_depthcm_raw','S3_depthcm_raw'
'''
    def padZeros(self, inInt, digits=2):
        ''' Function to add zerors before number '''
        inStr = str(inInt)
        outStr = ''
        if digits == 2:
            outStr = inStr
            if len(inStr) == 1:
                outStr = '0' + inStr
        if digits == 3:
            outStr = inStr
            if len(inStr) == 1:
                outStr = '00' + inStr
            elif len(inStr) == 2:
                outStr = '0' + inStr
        return outStr

    def polyFitSmooth(self, inX, inY, polyOrder):
        ''' Fit polynominal and return value for centre coefficent.
Used in Savitzky-Golay Smoothing '''
        
        coefficients = np.polyfit(inX,inY,polyOrder)
        
        fittedPoly = np.poly1d(coefficients)
        dfPoly = fittedPoly.deriv()
        
        outPos = int(inX.shape[0] / 2.)

        outYVal = fittedPoly(inX[outPos])
        outdYVal = dfPoly(inX[outPos])
        
        return outYVal, outdYVal

    def plotData(self, inDataFile, outPlot, applyFilter='No', filterParameters=None):
        inData = csv.reader(open(inDataFile, 'rU'))
        dateTime = []
        dateTimeLabel = list()
        dateTimeLabelPos = list()

        # Set up arrays to hold data        
        sensor1 = []
        sensor2 = []
        sensor3 = []
        
        # Set depth labels to default values
        depth1 = 'shallowest'
        depth2 = 'middle'
        depth3 = 'deepest'

        headerRow = True
        previousDay = 0

        minTimeEpoch = 32503680000 # initialise at 01/01/3000
        maxTimeEpoch = 0

        # Itterate through input file
        for line in inData:
            if headerRow:
                if(line[11].count('_') >= 1):
                    s1Split = line[11].split('_',line[11].count('_')) # Split into S1 and depthcm
                    depth1 = s1Split[1].replace('cm',' cm') # Add space before 'cm'
                if(line[12].count('_') >= 1):
                    s2Split = line[12].split('_',line[12].count('_')) # Split into S2 and depthcm
                    depth2 = s2Split[1].replace('cm',' cm') # Add space before 'cm'
                if(line[13].count('_') >= 1):
                    s3Split = line[13].split('_',line[13].count('_')) # Split into S3 and depthcm
		    if s3Split[1] != '999cm': # Check for nodata value
                    	depth3 = s3Split[1].replace('cm',' cm') # Add space before 'cm'
                headerRow = False
            else:
                mTimeTS = struct_time((int(line[5]),int(line[6]),int(line[7]),int(line[8]),int(line[9]),int(line[10]),0,0,0))
                mTimeEpoch = calendar.timegm(mTimeTS)
                dateTime.append(mTimeEpoch)

                sensor1.append(float(line[11]))
                sensor2.append(float(line[12]))
                sensor3.append(float(line[13]))

        edIDStr = 'ED#' + str(line[3]) # Get enddevice number
        
        dateTimeNP = np.array(dateTime) - 1340000000 # Offset values (to reduce the risk of overflow in polyfit)
        if applyFilter == 'SG':
            # Savitzky-Golay filtering of data
            filterSize = filterParameters['filterSize']
            polyOrder = filterParameters['polyOrder']

            # Convert to numpy arrays and copy
            sensor1 = np.array(sensor1)
            sensor2 = np.array(sensor2)
            sensor3 = np.array(sensor3)
        
            sensor1SG = sensor1
            sensor2SG = sensor2
            sensor3SG = sensor3

            blockSize = (filterSize * 2) + 1 # Set total size of the data block to use
            numMeasurements = sensor1.shape[0]
            for i in range(numMeasurements):
                blockStart = i - filterSize
                blockEnd = i + filterSize
            
                if blockStart < 0:
                    blockStart = 0
                elif blockEnd >= numMeasurements:
                    blockEnd = numMeasurements - 1
                
                timeSub = dateTimeNP[blockStart:blockEnd]
                s1Sub = sensor1[blockStart:blockEnd]
                s2Sub = sensor2[blockStart:blockEnd]
                s3Sub = sensor3[blockStart:blockEnd]
            
                # Get fitted value and first order derivative
                s1SGVal, s1dSGVal = self.polyFitSmooth(timeSub, s1Sub, polyOrder)
                s2SGVal, s2dSGVal  = self.polyFitSmooth(timeSub, s2Sub, polyOrder)
                s3SGVal, s3dSGVal  = self.polyFitSmooth(timeSub, s3Sub, polyOrder)

                sensor1SG[i] = s1SGVal
                sensor2SG[i] = s2SGVal
                sensor3SG[i] = s3SGVal
            
            sensor1 = sensor1SG
            sensor2 = sensor2SG
            sensor3 = sensor3SG

        if applyFilter == 'MED':
            filterSize = filterParameters['filterSize']

            # Convert to numpy arrays and copy
            sensor1 = np.array(sensor1)
            sensor2 = np.array(sensor2)
            sensor3 = np.array(sensor3)
            
            sensor1 = signal.medfilt(sensor1, filterSize)
            sensor2 = signal.medfilt(sensor2, filterSize)
            sensor3 = signal.medfilt(sensor3, filterSize)

        # Set up tick labels
        timeTickInterval = (max(dateTime) - min(dateTime)) / 10 # One day interval
        if timeTickInterval > 0:
            dateTimeLabelPosSec = np.arange(min(dateTime), max(dateTime), timeTickInterval)
            dateTimeLabel = []
            dateTimeLabelPosHours = []
        else:
            raise Exception('Diffference between minimum and maximum dates is zero')

        twiceDaily = False
        if timeTickInterval < (3600*12): # If interval is less than a day
            twiceDaily = True

        am = True
        # Create labels
        for epochTime in dateTimeLabelPosSec:
            timeTS = gmtime(epochTime)
            if twiceDaily == True and am == True: # If twice a day and am, round to midnight
                timeTSRound = struct_time((timeTS[0],timeTS[1],timeTS[2],0,0,0,timeTS[6],timeTS[7],timeTS[8]))
                epochTimeRound = calendar.timegm(timeTSRound)
                am = False
            elif twiceDaily == True and am == False: # If twice a day and pm, round to noon
                timeTSRound = struct_time((timeTS[0],timeTS[1],timeTS[2],12,0,0,timeTS[6],timeTS[7],timeTS[8]))
                epochTimeRound = calendar.timegm(timeTSRound)
                am = True
            else:
                timeTSRound = struct_time((timeTS[0],timeTS[1],timeTS[2],0,0,0,timeTS[6],timeTS[7],timeTS[8]))
                epochTimeRound = calendar.timegm(timeTSRound)

            labelStr = self.padZeros(timeTSRound[3],2) + ':' + self.padZeros(timeTSRound[4],2) + '\n' + str(timeTSRound[0]) + '/' + str(timeTSRound[1]) + '/' + str(timeTSRound[2])
            dateTimeLabel.append(labelStr)
            dateTimeLabelPosHours.append(epochTimeRound)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        # Set x and y limit for axis (want the same for all plots)
        ax.set_ylabel('Soil moisture (%)')
        ax.set_xlabel('Sampling time')
        ax.plot(dateTime, sensor1)
        ax.plot(dateTime, sensor2)
        ax.plot(dateTime, sensor3)
        ax.set_ylim((0,50))
        ax.legend(('Sensor 1 (' + depth1 + ')','Sensor 2 (' + depth2 + ')','Sensor 3 (' + depth3 + ')'),loc='upper right')
        plt.xticks(dateTimeLabelPosHours, dateTimeLabel, rotation=50)
        plt.title(edIDStr)
        plt.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.25)
        if outPlot.find('.pdf') > 0:
            plt.savefig(outPlot, format='PDF')
        elif outPlot.find('.png') > 0:
            plt.savefig(outPlot, format='PNG',dpi=300)
        else:
            print 'Outplot file must end in PNG or PDF'

    def help(self):
        print '''soilSCAPE_plotData.py
Plot soil moisture data downloaded from soilscape.usc.edu and save the output as a PDF / PNG
Data may be filtered prior to plotting.
Available filters:
    SG - Savitzky-Golay
    MED - Median
Usage:
  python createPlotFromCSV.py inCSV.csv outPDF.pdf / outPNG.png [Filter]
'''

if __name__=='__main__':
    obj = createPlotFromCSV()
    if len(sys.argv) == 3:
        inCSVFile = sys.argv[1]
        outPlotFile = sys.argv[2]
        obj.plotData(inCSVFile, outPlotFile)
    elif len(sys.argv) >= 4:
        inCSVFile = sys.argv[1]
        outPlotFile = sys.argv[2]
        applyFilter = sys.argv[3].strip()
        if applyFilter == 'SG':
            filterParameters = {'filterSize':9, 'polyOrder':3}
        elif applyFilter == 'MED':
            filterParameters = {'filterSize':9}
        else:
            print 'Filter not recognised, not using'
            applyFilter = 'NO'
            filterParameters = None
        obj.plotData(inCSVFile, outPlotFile, applyFilter, filterParameters)
    else:
        obj.help()
