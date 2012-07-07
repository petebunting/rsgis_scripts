 #! /usr/bin/env python

#######################################
# A python script to plot the averaged
# columns data.
#
# Email: petebunting@mac.com
# Date: 01/02/2012
# Version: 1.0
#######################################

import os.path
import sys
from math import *
import optparse
import matplotlib.pyplot as plt
import matplotlib.dates as matdate
import numpy as np

class PlotData (object):

    def readCSVFile(self, inFile, dataList):
        for eachLine in inFile:
            eachLine = eachLine.strip()
            if eachLine != "":
                split = eachLine.split(',', eachLine.count(','))
                for val in split:
                    dataList.append(float(val))


    def plotData(self, outputFile, titleText, xLabelText, yLabelText, yVals, xVals):
		fig = plt.figure(figsize=(15, 10), dpi=120)
		ax = fig.add_subplot(111)
		
		ax.plot(xVals, yVals, 'k-', label='Mean', zorder=10)
		
		axRange = plt.axis('tight')
		
		plt.grid(color='k', linestyle='--', linewidth=0.5)
		plt.title(titleText)
		plt.xlabel(xLabelText)
		plt.ylabel(yLabelText)
		
		plt.savefig(outputFile, format='PDF')
		
    def createDataSummaries(self, dataList, yVals):       
        dataList.sort(reverse=True)
        
        #print dataList
        
        totalArea = np.sum(dataList)
        
        #print "Total: ", totalArea
        
        thresholds = list()
        thresholds.append(totalArea * 0.1)
        thresholds.append(totalArea * 0.2)
        thresholds.append(totalArea * 0.3)
        thresholds.append(totalArea * 0.4)
        thresholds.append(totalArea * 0.5)
        thresholds.append(totalArea * 0.6)
        thresholds.append(totalArea * 0.7)
        thresholds.append(totalArea * 0.8)
        thresholds.append(totalArea * 0.9)

        cSum = 0.0
        count = 0
        for thres in thresholds:
            cSum = 0.0
            count = 0
            for val in dataList:
                cSum += val
                count = count + 1
                if cSum > thres:
                    yVals.append(count)
                    break
        yVals.append(len(dataList)) 

    def run(self, cmdargs):
        xDataValsList = list()
        yDataValsList = list()

        for strVal in cmdargs.yDataStrVals:
            xDataValsList.append(float(strVal.strip()))

        for fileName in cmdargs.inputs:
            try:
                inputTextFile = open(fileName.strip(), 'r')
                dataList = list()
                self.readCSVFile(inputTextFile, dataList)
                dataSum = list()
                self.createDataSummaries(dataList, dataSum)
                yDataValsList.append(dataSum[int(cmdargs.percentage4Disp)])
                inputTextFile.close()
            except IOError, e:
                print '\nCould not open file:\n', e
                return

        self.plotData(cmdargs.outputFile, cmdargs.title, cmdargs.xAxis, cmdargs.yAxis, yDataValsList, xDataValsList)


# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output PDF file.")
    p.add_option("-t","--title", dest="title", default="Title", help="Plot title.")
    p.add_option("-x","--xaxis", dest="xAxis", default="X Axis", help="Plot x-axis label.")
    p.add_option("-y","--yaxis", dest="yAxis", default="Y Axis", help="Plot y-axis label.")
    p.add_option("-p","--percentage", dest="percentage4Disp", default="5", help="Percentage to be displayed in plot.")
    p.add_option("-i","--input", action="append", dest="inputs", default=None, help="Input files in order they will be plotted.")
    p.add_option("-d","--yData", action="append", dest="yDataStrVals", default=None, help="Values for along the y-axis.")



    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.outputFile is None:
        p.print_help()
        print "output filename must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = PlotData()
    obj.run(cmdargs)
