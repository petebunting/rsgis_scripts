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
from datetime import datetime,timedelta
from math import *
import optparse
import matplotlib.pyplot as plt
import matplotlib.dates as matdate

class PlotAverageData (object):

    def readCSVFile(self, inFile, dateStrList, minList, maxList, meanList, medianList, stddevList, meanSDP1List, meanSDM1List,sumList):
        line = 0
        for eachLine in inFile:
            eachLine = eachLine.strip()
            if (line != 0) and (eachLine != ""):
                split = eachLine.split(',', eachLine.count(','))
                dateStrList.append(split[0])
                minList.append(float(split[2]))
                maxList.append(float(split[3]))
                meanList.append(float(split[4]))
                medianList.append(float(split[5]))
                stddevList.append(float(split[6]))
                meanSDP1List.append(float(split[7]))
                meanSDM1List.append(float(split[8]))
                sumList.append(float(split[9]))
            line = line + 1

    def convertStrDateToDates(self, dateStrList, dateList, summary):
        for strVal in dateStrList:
            if summary == 'year':
                dateYear = datetime.strptime(strVal, "%Y")
                dateYear = dateYear + timedelta(365)
                dateList.append(dateYear)
            elif summary == 'month':
                dateMonth = datetime.strptime(strVal, "%m/%Y")
                dateMonth = dateMonth + timedelta(28)
                dateList.append(dateMonth)
            elif summary == 'week':
                split = strVal.split('/', strVal.count(''))
                days = int(split[0])*7
                dateObj = datetime.strptime(split[1], "%Y") + timedelta(days=int(split[0])*7)
                dateList.append(dateObj)
            elif summary == 'day':
                dateList.append(datetime.strptime(strVal, "%d/%m/%Y"))
            else:
                print "Summary needs to be one of the following: year | month | week | day."
                sys.exit()

    def plotData(self, outputFile, summary, titleText, xLabelText, yLabelText, dateList, minList, maxList, meanList, medianList, stddevList, meanSDP1List, meanSDM1List, sumList, plotMean, plotMedian, plotStdDev, plotRange, plotSum, startDateDefined, startDate, endDateDefined, endDate):
        plotDateVals = list()
        plotDateVals.append(list())
        plotMeanVals = list()
        plotMeanVals.append(list())
        plotMedianVals = list()
        plotMedianVals.append(list())
        plotMinVals = list()
        plotMinVals.append(list())
        plotMaxVals = list()
        plotMaxVals.append(list())
        plotMeanSDP1Vals = list()
        plotMeanSDP1Vals.append(list())
        plotMeanSDM1Vals = list()
        plotMeanSDM1Vals.append(list())
        plotSumVals = list()
        plotSumVals.append(list())

        fig = plt.figure(figsize=(15, 5), dpi=80)
        ax = fig.add_subplot(111)


        numVals = len(dateList)
        dataIdx = 0

        nextDate = None

        yearDelta = timedelta(366)
        monthDelta = timedelta(31)
        weekDelta = timedelta(7)
        dayDelta = timedelta(1)

        startDateTreatment = datetime.strptime("01/10/2007", "%d/%m/%Y")
        endDateTreatment = datetime.strptime("30/06/2008", "%d/%m/%Y")

        #ax.axvspan(startDateTreatment, endDateTreatment, facecolor='k', edgecolor='k', alpha=0.5, hatch='x', fill=False, linestyle='dashed', zorder=-100)


        for i in range(numVals):
            if i == 0:
                plotDateVals[dataIdx].append(dateList[i])
                plotMeanVals[dataIdx].append(meanList[i])
                plotMedianVals[dataIdx].append(medianList[i])
                plotMinVals[dataIdx].append(minList[i])
                plotMaxVals[dataIdx].append(maxList[i])
                plotMeanSDP1Vals[dataIdx].append(meanSDP1List[i])
                plotMeanSDM1Vals[dataIdx].append(meanSDM1List[i])
                plotSumVals[dataIdx].append(sumList[i])
            else:
                if (dateList[i] > nextDate):
                    plotDateVals.append(list())
                    plotMeanVals.append(list())
                    plotMedianVals.append(list())
                    plotMinVals.append(list())
                    plotMaxVals.append(list())
                    plotMeanSDP1Vals.append(list())
                    plotMeanSDM1Vals.append(list())
                    plotSumVals.append(list())

                    if plotSum:
                        ax.plot_date(plotDateVals[dataIdx], plotSumVals[dataIdx], 'k-', label='Sum', zorder=10)
                    if plotMean:
                        ax.plot_date(plotDateVals[dataIdx], plotMeanVals[dataIdx], 'k-', label='Mean', zorder=10)
                    if plotMedian:
                        if plotMean:
                            ax.plot_date(plotDateVals[dataIdx], plotMedianVals[dataIdx], 'k--', label='Median', zorder=9)
                        else:
                            ax.plot_date(plotDateVals[dataIdx], plotMedianVals[dataIdx], 'k-', label='Median', zorder=10)
                    if plotRange:
                        ax.fill_between(plotDateVals[dataIdx], plotMinVals[dataIdx], plotMaxVals[dataIdx], alpha=0.2, linewidth=1.0, facecolor='b', edgecolor=[0.70,0.70,0.70], label='Range', zorder=-1)
                    if plotStdDev:
                        ax.fill_between(plotDateVals[dataIdx], plotMeanSDP1Vals[dataIdx], plotMeanSDM1Vals[dataIdx], alpha=0.4, linewidth=1.0, facecolor='g', edgecolor=[0.70,0.70,0.70], label='1 Std Dev', zorder=1)
                    dataIdx = dataIdx + 1

                plotDateVals[dataIdx].append(dateList[i])
                plotMeanVals[dataIdx].append(meanList[i])
                plotMedianVals[dataIdx].append(medianList[i])
                plotMinVals[dataIdx].append(minList[i])
                plotMaxVals[dataIdx].append(maxList[i])
                plotMeanSDP1Vals[dataIdx].append(meanSDP1List[i])
                plotMeanSDM1Vals[dataIdx].append(meanSDM1List[i])
                plotSumVals[dataIdx].append(sumList[i])

            if (summary == 'year'):
                nextDate = dateList[i] + yearDelta
            elif (summary == 'month'):
                nextDate = dateList[i] + monthDelta
            elif (summary == 'week'):
                nextDate = dateList[i] + weekDelta
            elif (summary == 'day'):
                nextDate = dateList[i] + dayDelta

        if plotSum:
            ax.plot_date(plotDateVals[dataIdx], plotSumVals[dataIdx], 'k-', label='Sum', zorder=10)
        if plotMean:
            ax.plot_date(plotDateVals[dataIdx], plotMeanVals[dataIdx], 'k-', label='Mean', zorder=10)
        if plotMedian:
            if plotMean:
                ax.plot_date(plotDateVals[dataIdx], plotMedianVals[dataIdx], 'k--', label='Median', zorder=10)
            else:
                ax1.plot_date(plotDateVals[dataIdx], plotMedianVals[dataIdx], 'k-', label='Median', zorder=9)
        if plotRange:
            ax.fill_between(plotDateVals[dataIdx], plotMinVals[dataIdx], plotMaxVals[dataIdx], alpha=0.2, linewidth=1.0, facecolor='b', edgecolor=[0.70,0.70,0.70], label='Range', zorder=-1)
        if plotStdDev:
            ax.fill_between(plotDateVals[dataIdx], plotMeanSDP1Vals[dataIdx], plotMeanSDM1Vals[dataIdx], alpha=0.4, linewidth=1.0, facecolor='g', edgecolor=[0.70,0.70,0.70], label='1 Std Dev', zorder=1)

        axRange = plt.axis('tight')
        #print "axRange: ", axRange
        #print "datetime.utcnow(): ", matdate.date2num(datetime.utcnow())

        outRange = list()
        outRange.append(axRange[0])
        outRange.append(axRange[1])
        outRange.append(axRange[2])
        outRange.append(axRange[3])

        if startDateDefined:
            outRange[0] = matdate.date2num(startDate)
        if endDateDefined:
            outRange[1] = matdate.date2num(endDate)

        plt.axis(outRange)

        heightOff = (outRange[3])*0.9

        monthDelta = timedelta(90)
        if matdate.date2num(matdate.num2date(outRange[0])+monthDelta) < matdate.date2num(startDateTreatment):
            ax.axvline(x=startDateTreatment, linewidth=2, color='r', linestyle='--', zorder=-100)
            ax.text(startDateTreatment-monthDelta, heightOff, "Pre", color='r', fontsize='large', fontweight='bold')
        elif matdate.date2num(matdate.num2date(outRange[0])) < matdate.date2num(endDateTreatment-(monthDelta*2)):
            ax.text(endDateTreatment-(monthDelta*2), heightOff, "During", color='r', fontsize='large', fontweight='bold')
        ax.axvline(x=endDateTreatment, linewidth=2, color='r', linestyle='--', zorder=-100)
        ax.text(endDateTreatment+monthDelta, heightOff, "Post", color='r', fontsize='large', fontweight='bold')

        plt.grid(color='k', linestyle='--', linewidth=0.5)
        plt.title(titleText)
        plt.xlabel(xLabelText)
        plt.ylabel(yLabelText)
        #plt.legend(shadow=True, fancybox=True)

        plt.savefig(outputFile, format='PDF')

    def barPlotSumData(self, outputFile, summary, titleText, xLabelText, yLabelText, dateList, sumList, startDateDefined, startDate, endDateDefined, endDate):
        plotDateVals = list()
        plotDateVals.append(list())
        plotSumVals = list()
        plotSumVals.append(list())

        fig = plt.figure(figsize=(15, 5), dpi=80)
        ax = fig.add_subplot(111)


        numVals = len(dateList)
        dataIdx = 0

        nextDate = None

        yearDelta = timedelta(366)
        monthDelta = timedelta(31)
        weekDelta = timedelta(7)
        dayDelta = timedelta(1)

        startDateTreatment = datetime.strptime("01/10/2007", "%d/%m/%Y")
        endDateTreatment = datetime.strptime("30/06/2008", "%d/%m/%Y")

        barWidth = 1
        if summary == 'year':
            barWidth=matdate.date2num(datetime.strptime("2001/01/01", "%Y/%m/%d"))-matdate.date2num(datetime.strptime("2000/01/01", "%Y/%m/%d"))
        elif (summary == 'month'):
            barWidth=matdate.date2num(datetime.strptime("2000/02/01", "%Y/%m/%d"))-matdate.date2num(datetime.strptime("2000/01/01", "%Y/%m/%d"))
        elif (summary == 'week'):
            barWidth=matdate.date2num(datetime.strptime("2000/01/07", "%Y/%m/%d"))-matdate.date2num(datetime.strptime("2000/01/01", "%Y/%m/%d"))
        elif (summary == 'day'):
            barWidth=matdate.date2num(datetime.strptime("2000/01/02", "%Y/%m/%d"))-matdate.date2num(datetime.strptime("2000/01/01", "%Y/%m/%d"))

        for i in range(numVals):
            if i == 0:
                plotDateVals[dataIdx].append(dateList[i])
                plotSumVals[dataIdx].append(sumList[i])
            else:
                if (dateList[i] > nextDate):
                    plotDateVals.append(list())
                    plotSumVals.append(list())

                    ax.bar(plotDateVals[dataIdx], plotSumVals[dataIdx], width=barWidth, color='grey', label='Sum', zorder=10)
                    dataIdx = dataIdx + 1

                plotDateVals[dataIdx].append(dateList[i])
                plotSumVals[dataIdx].append(sumList[i])

            if (summary == 'year'):
                nextDate = dateList[i] + yearDelta
            elif (summary == 'month'):
                nextDate = dateList[i] + monthDelta
            elif (summary == 'week'):
                nextDate = dateList[i] + weekDelta
            elif (summary == 'day'):
                nextDate = dateList[i] + dayDelta

        ax.bar(plotDateVals[dataIdx], plotSumVals[dataIdx], width=barWidth, color='grey', label='Sum', zorder=10, )

        axRange = plt.axis('tight')
        #print "axRange: ", axRange
        #print "datetime.utcnow(): ", matdate.date2num(datetime.utcnow())

        outRange = list()
        outRange.append(axRange[0])
        outRange.append(axRange[1])
        outRange.append(axRange[2])
        outRange.append(axRange[3])

        if startDateDefined:
            outRange[0] = matdate.date2num(startDate)
        if endDateDefined:
            outRange[1] = matdate.date2num(endDate)

        plt.axis(outRange)

        heightOff = (outRange[3])*0.9

        monthDelta = timedelta(90)
        if matdate.date2num(matdate.num2date(outRange[0])+monthDelta) < matdate.date2num(startDateTreatment):
            ax.axvline(x=startDateTreatment, linewidth=2, color='r', linestyle='--', zorder=-100)
            ax.text(startDateTreatment-monthDelta, heightOff, "Pre", color='r', fontsize='large', fontweight='bold')
        elif matdate.date2num(matdate.num2date(outRange[0])) < matdate.date2num(endDateTreatment-(monthDelta*2)):
            ax.text(endDateTreatment-(monthDelta*2), heightOff, "During", color='r', fontsize='large', fontweight='bold')
        ax.axvline(x=endDateTreatment, linewidth=2, color='r', linestyle='--', zorder=-100)
        ax.text(endDateTreatment+monthDelta, heightOff, "Post", color='r', fontsize='large', fontweight='bold')

        plt.grid(color='k', linestyle='--', linewidth=0.5)
        plt.title(titleText)
        plt.xlabel(xLabelText)
        plt.ylabel(yLabelText)
        #plt.legend(shadow=True, fancybox=True)

        plt.savefig(outputFile, format='PDF')

    def run(self, cmdargs):
        dateStrList = list()
        minList = list()
        maxList = list()
        meanList = list()
        medianList = list()
        stddevList = list()
        meanSDP1List = list()
        meanSDM1List = list()
        sumList = list()
        try:
            inputTextFile = open(cmdargs.inputFile.strip(), 'r')
            self.readCSVFile(inputTextFile, dateStrList, minList, maxList, meanList, medianList, stddevList, meanSDP1List, meanSDM1List, sumList)
            inputTextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return

        dateList = list()
        self.convertStrDateToDates(dateStrList, dateList, cmdargs.summary.strip())

        startDateDefined = False
        startDate = datetime.strptime("01/01/2001", "%d/%m/%Y")
        if cmdargs.startDate != "":
            startDateDefined = True
            startDate = datetime.strptime(cmdargs.startDate, "%d/%m/%Y")

        endDateDefined = False
        endDate = datetime.strptime("01/01/2001", "%d/%m/%Y")
        if cmdargs.endDate != "":
            endDateDefined = True
            endDate = datetime.strptime(cmdargs.endDate, "%d/%m/%Y")
        if not cmdargs.barPlot:
            self.plotData(cmdargs.outputFile.strip(), cmdargs.summary.strip(), cmdargs.title, cmdargs.xAxis, cmdargs.yAxis, dateList, minList, maxList, meanList, medianList, stddevList, meanSDP1List, meanSDM1List, sumList, cmdargs.mean, cmdargs.median, cmdargs.stddev, cmdargs.range, cmdargs.sum, startDateDefined, startDate, endDateDefined, endDate)
        else:
            self.barPlotSumData(cmdargs.outputFile.strip(), cmdargs.summary.strip(), cmdargs.title, cmdargs.xAxis, cmdargs.yAxis, dateList, sumList, startDateDefined, startDate, endDateDefined, endDate)

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input CSV file.")
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output PDF file.")
    p.add_option("-s","--summary", dest="summary", default="", help="Data Summary (year | month | week | day).")
    p.add_option("-t","--title", dest="title", default="Title", help="Plot title.")
    p.add_option("-x","--xaxis", dest="xAxis", default="X Axis", help="Plot x-axis label.")
    p.add_option("-y","--yaxis", dest="yAxis", default="Y Axis", help="Plot y-axis label.")
    p.add_option("", "--mean", action="store_true", dest="mean", default=False, help="Plot mean values")
    p.add_option("", "--median", action="store_true", dest="median", default=False, help="Plot median values")
    p.add_option("", "--stddev", action="store_true", dest="stddev", default=False, help="Plot standard deviation values")
    p.add_option("", "--range", action="store_true", dest="range", default=False, help="Plot range values")
    p.add_option("", "--sum", action="store_true", dest="sum", default=False, help="Plot sum values")
    p.add_option("", "--bar", action="store_true", dest="barPlot", default=False, help="Plot a bar graph of the summed values")
    p.add_option("", "--start", dest="startDate", default="", help="Start Date")
    p.add_option("", "--end", dest="endDate", default="", help="End Date")

    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "Input filename must be set."
        sys.exit()

    if self.outputFile is None:
        p.print_help()
        print "output filename must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = PlotAverageData()
    obj.run(cmdargs)
