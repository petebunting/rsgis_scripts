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

    def readCSVFile(self, inFile, dateStrList, minList, maxList, meanList, medianList, stddevList, meanSDP1List, meanSDM1List):
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

    def plotData(self, outputFile, summary, titleText, xLabelText, yLabelText1, yLabelText2, dateList1, minList1, maxList1, meanList1, medianList1, stddevList1, meanSDP1List1, meanSDM1List1, dateList2, minList2, maxList2, meanList2, medianList2, stddevList2, meanSDP1List2, meanSDM1List2, plotMean, plotMedian, plotStdDev, plotRange, startDateDefined, startDate, endDateDefined, endDate):
        plotDateVals1 = list()
        plotDateVals1.append(list())
        plotMeanVals1 = list()
        plotMeanVals1.append(list())
        plotMedianVals1 = list()
        plotMedianVals1.append(list())
        plotMinVals1 = list()
        plotMinVals1.append(list())
        plotMaxVals1 = list()
        plotMaxVals1.append(list())
        plotMeanSDP1Vals1 = list()
        plotMeanSDP1Vals1.append(list())
        plotMeanSDM1Vals1 = list()
        plotMeanSDM1Vals1.append(list())

        plotDateVals2 = list()
        plotDateVals2.append(list())
        plotMeanVals2 = list()
        plotMeanVals2.append(list())
        plotMedianVals2 = list()
        plotMedianVals2.append(list())
        plotMinVals2 = list()
        plotMinVals2.append(list())
        plotMaxVals2 = list()
        plotMaxVals2.append(list())
        plotMeanSDP1Vals2 = list()
        plotMeanSDP1Vals2.append(list())
        plotMeanSDM1Vals2 = list()
        plotMeanSDM1Vals2.append(list())

        fig = plt.figure(figsize=(15, 5), dpi=80)
        ax1 = fig.add_subplot(111)

        yearDelta = timedelta(366)
        monthDelta = timedelta(31)
        weekDelta = timedelta(7)
        dayDelta = timedelta(1)

        startDateTreatment = datetime.strptime("01/10/2007", "%d/%m/%Y")
        endDateTreatment = datetime.strptime("30/06/2008", "%d/%m/%Y")

        numVals = len(dateList1)
        dataIdx = 0
        nextDate = None
        for i in range(numVals):
            if i == 0:
                plotDateVals1[dataIdx].append(dateList1[i])
                plotMeanVals1[dataIdx].append(meanList1[i])
                plotMedianVals1[dataIdx].append(medianList1[i])
                plotMinVals1[dataIdx].append(minList1[i])
                plotMaxVals1[dataIdx].append(maxList1[i])
                plotMeanSDP1Vals1[dataIdx].append(meanSDP1List1[i])
                plotMeanSDM1Vals1[dataIdx].append(meanSDM1List1[i])
            else:
                if (dateList1[i] > nextDate):
                    plotDateVals1.append(list())
                    plotMeanVals1.append(list())
                    plotMedianVals1.append(list())
                    plotMinVals1.append(list())
                    plotMaxVals1.append(list())
                    plotMeanSDP1Vals1.append(list())
                    plotMeanSDM1Vals1.append(list())

                    if plotMean:
                        ax1.plot_date(plotDateVals1[dataIdx], plotMeanVals1[dataIdx], 'k-', label='Mean', zorder=10)
                    if plotMedian:
                        if plotMean:
                            ax1.plot_date(plotDateVals1[dataIdx], plotMedianVals1[dataIdx], 'k--', label='Median', zorder=9)
                        else:
                            ax1.plot_date(plotDateVals1[dataIdx], plotMedianVals1[dataIdx], 'k-', label='Median', zorder=10)
                    if plotRange:
                        ax1.fill_between(plotDateVals1[dataIdx], plotMinVals1[dataIdx], plotMaxVals1[dataIdx], alpha=0.2, linewidth=1.0, facecolor='b', edgecolor=[0.70,0.70,0.70], label='Range', zorder=-1)
                    if plotStdDev:
                        ax1.fill_between(plotDateVals1[dataIdx], plotMeanSDP1Vals1[dataIdx], plotMeanSDM1Vals1[dataIdx], alpha=0.4, linewidth=1.0, facecolor='g', edgecolor=[0.70,0.70,0.70], label='1 Std Dev', zorder=1)
                    dataIdx = dataIdx + 1

                plotDateVals1[dataIdx].append(dateList1[i])
                plotMeanVals1[dataIdx].append(meanList1[i])
                plotMedianVals1[dataIdx].append(medianList1[i])
                plotMinVals1[dataIdx].append(minList1[i])
                plotMaxVals1[dataIdx].append(maxList1[i])
                plotMeanSDP1Vals1[dataIdx].append(meanSDP1List1[i])
                plotMeanSDM1Vals1[dataIdx].append(meanSDM1List1[i])

            if (summary == 'year'):
                nextDate = dateList1[i] + yearDelta
            elif (summary == 'month'):
                nextDate = dateList1[i] + monthDelta
            elif (summary == 'week'):
                nextDate = dateList1[i] + weekDelta
            elif (summary == 'day'):
                nextDate = dateList1[i] + dayDelta

        if plotMean:
            ax1.plot_date(plotDateVals1[dataIdx], plotMeanVals1[dataIdx], 'k-', label='Mean', zorder=10)
        if plotMedian:
            if plotMean:
                ax1.plot_date(plotDateVals1[dataIdx], plotMedianVals1[dataIdx], 'k--', label='Median', zorder=10)
            else:
                ax1.plot_date(plotDateVals1[dataIdx], plotMedianVals1[dataIdx], 'k-', label='Median', zorder=9)
        if plotRange:
            ax1.fill_between(plotDateVals1[dataIdx], plotMinVals1[dataIdx], plotMaxVals1[dataIdx], alpha=0.2, linewidth=1.0, facecolor='b', edgecolor=[0.70,0.70,0.70], label='Range', zorder=-1)
        if plotStdDev:
            ax1.fill_between(plotDateVals1[dataIdx], plotMeanSDP1Vals1[dataIdx], plotMeanSDM1Vals1[dataIdx], alpha=0.4, linewidth=1.0, facecolor='g', edgecolor=[0.70,0.70,0.70], label='1 Std Dev', zorder=1)

        ax2 = ax1.twinx()
        numVals = len(dateList2)
        dataIdx = 0
        nextDate = None
        for i in range(numVals):
            if i == 0:
                plotDateVals2[dataIdx].append(dateList2[i])
                plotMeanVals2[dataIdx].append(meanList2[i])
                plotMedianVals2[dataIdx].append(medianList2[i])
                plotMinVals2[dataIdx].append(minList2[i])
                plotMaxVals2[dataIdx].append(maxList2[i])
                plotMeanSDP1Vals2[dataIdx].append(meanSDP1List2[i])
                plotMeanSDM1Vals2[dataIdx].append(meanSDM1List2[i])
            else:
                if (dateList2[i] > nextDate):
                    plotDateVals2.append(list())
                    plotMeanVals2.append(list())
                    plotMedianVals2.append(list())
                    plotMinVals2.append(list())
                    plotMaxVals2.append(list())
                    plotMeanSDP1Vals2.append(list())
                    plotMeanSDM1Vals2.append(list())

                    if plotMean:
                        ax2.plot_date(plotDateVals2[dataIdx], plotMeanVals2[dataIdx], 'b-', label='Mean', zorder=10)
                    if plotMedian:
                        if plotMean:
                            ax2.plot_date(plotDateVals2[dataIdx], plotMedianVals2[dataIdx], 'b--', label='Median', zorder=9)
                        else:
                            ax2.plot_date(plotDateVals2[dataIdx], plotMedianVals2[dataIdx], 'b-', label='Median', zorder=10)
                    if plotRange:
                        ax2.fill_between(plotDateVals2[dataIdx], plotMinVals2[dataIdx], plotMaxVals2[dataIdx], alpha=0.2, linewidth=1.0, facecolor='m', edgecolor=[0.70,0.70,0.70], label='Range', zorder=-1)
                    if plotStdDev:
                        ax2.fill_between(plotDateVals2[dataIdx], plotMeanSDP1Vals2[dataIdx], plotMeanSDM1Vals2[dataIdx], alpha=0.4, linewidth=1.0, facecolor='y', edgecolor=[0.70,0.70,0.70], label='1 Std Dev', zorder=1)
                    dataIdx = dataIdx + 1

                plotDateVals2[dataIdx].append(dateList2[i])
                plotMeanVals2[dataIdx].append(meanList2[i])
                plotMedianVals2[dataIdx].append(medianList2[i])
                plotMinVals2[dataIdx].append(minList2[i])
                plotMaxVals2[dataIdx].append(maxList2[i])
                plotMeanSDP1Vals2[dataIdx].append(meanSDP1List2[i])
                plotMeanSDM1Vals2[dataIdx].append(meanSDM1List2[i])

            if (summary == 'year'):
                nextDate = dateList2[i] + yearDelta
            elif (summary == 'month'):
                nextDate = dateList2[i] + monthDelta
            elif (summary == 'week'):
                nextDate = dateList2[i] + weekDelta
            elif (summary == 'day'):
                nextDate = dateList2[i] + dayDelta

        if plotMean:
            ax2.plot_date(plotDateVals2[dataIdx], plotMeanVals2[dataIdx], 'b-', label='Mean', zorder=10)
        if plotMedian:
            if plotMean:
                ax2.plot_date(plotDateVals2[dataIdx], plotMedianVals2[dataIdx], 'b--', label='Median', zorder=10)
            else:
                ax2.plot_date(plotDateVals2[dataIdx], plotMedianVals2[dataIdx], 'b-', label='Median', zorder=9)
        if plotRange:
            ax2.fill_between(plotDateVals2[dataIdx], plotMinVals2[dataIdx], plotMaxVals2[dataIdx], alpha=0.2, linewidth=1.0, facecolor='m', edgecolor=[0.70,0.70,0.70], label='Range', zorder=-1)
        if plotStdDev:
            ax2.fill_between(plotDateVals2[dataIdx], plotMeanSDP1Vals2[dataIdx], plotMeanSDM1Vals2[dataIdx], alpha=0.4, linewidth=1.0, facecolor='y', edgecolor=[0.70,0.70,0.70], label='1 Std Dev', zorder=1)

        ax1Range = ax1.axis('tight')
        out1Range = list()
        out1Range.append(ax1Range[0])
        out1Range.append(ax1Range[1])
        out1Range.append(ax1Range[2])
        out1Range.append(ax1Range[3])

        ax2Range = ax2.axis('tight')
        out2Range = list()
        out2Range.append(ax2Range[0])
        out2Range.append(ax2Range[1])
        out2Range.append(ax2Range[2])
        out2Range.append(ax2Range[3])

        if startDateDefined:
            out1Range[0] = matdate.date2num(startDate)
            out2Range[0] = matdate.date2num(startDate)
        if endDateDefined:
            out1Range[1] = matdate.date2num(endDate)
            out2Range[1] = matdate.date2num(endDate)

        ax1.axis(out1Range)
        ax2.axis(out2Range)

        heightOff = (out1Range[3])*0.9

        monthDelta = timedelta(90)
        if matdate.date2num(matdate.num2date(out1Range[0])+monthDelta) < matdate.date2num(startDateTreatment):
            ax1.axvline(x=startDateTreatment, linewidth=2, color='r', linestyle='--', zorder=-100)
            ax1.text(startDateTreatment-monthDelta, heightOff, "Pre", color='r', fontsize='large', fontweight='bold', zorder=20)
        elif matdate.date2num(matdate.num2date(out1Range[0])) < matdate.date2num(endDateTreatment-(monthDelta*2)):
            ax1.text(endDateTreatment-(monthDelta*2), heightOff, "During", color='r', fontsize='large', fontweight='bold', zorder=20)
        ax1.axvline(x=endDateTreatment, linewidth=2, color='r', linestyle='--', zorder=-100)
        ax1.text(endDateTreatment+monthDelta, heightOff, "Post", color='r', fontsize='large', fontweight='bold', zorder=20)

        plt.grid(color='k', linestyle='--', linewidth=0.5)
        plt.title(titleText)
        plt.xlabel(xLabelText)
        ax1.set_ylabel(yLabelText1)
        ax2.set_ylabel(yLabelText2)
        #plt.ylabel(yLabelText)
        #plt.legend(shadow=True, fancybox=True)

        plt.savefig(outputFile, format='PDF')

    def run(self, cmdargs):
        dateStrList1 = list()
        minList1 = list()
        maxList1 = list()
        meanList1 = list()
        medianList1 = list()
        stddevList1 = list()
        meanSDP1List1 = list()
        meanSDM1List1 = list()
        dateStrList2 = list()
        minList2 = list()
        maxList2 = list()
        meanList2 = list()
        medianList2 = list()
        stddevList2 = list()
        meanSDP1List2 = list()
        meanSDM1List2 = list()
        try:
            input1TextFile = open(cmdargs.inputFile1.strip(), 'r')
            self.readCSVFile(input1TextFile, dateStrList1, minList1, maxList1, meanList1, medianList1, stddevList1, meanSDP1List1, meanSDM1List1)
            input1TextFile.close()

            input2TextFile = open(cmdargs.inputFile2.strip(), 'r')
            self.readCSVFile(input2TextFile, dateStrList2, minList2, maxList2, meanList2, medianList2, stddevList2, meanSDP1List2, meanSDM1List2)
            input2TextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return

        dateList1 = list()
        self.convertStrDateToDates(dateStrList1, dateList1, cmdargs.summary.strip())
        dateList2 = list()
        self.convertStrDateToDates(dateStrList2, dateList2, cmdargs.summary.strip())

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

        self.plotData(cmdargs.outputFile.strip(), cmdargs.summary.strip(), cmdargs.title, cmdargs.xAxis, cmdargs.yAxis1, cmdargs.yAxis2, dateList1, minList1, maxList1, meanList1, medianList1, stddevList1, meanSDP1List1, meanSDM1List1, dateList2, minList2, maxList2, meanList2, medianList2, stddevList2, meanSDP1List2, meanSDM1List2, cmdargs.mean, cmdargs.median, cmdargs.stddev, cmdargs.range, startDateDefined, startDate, endDateDefined, endDate)

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("","--input1", dest="inputFile1", default=None, help="Input CSV file.")
    p.add_option("","--input2", dest="inputFile2", default=None, help="Input CSV file.")
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output PDF file.")
    p.add_option("-s","--summary", dest="summary", default="", help="Data Summary (year | month | week | day).")
    p.add_option("-t","--title", dest="title", default="Title", help="Plot title.")
    p.add_option("","--xaxis", dest="xAxis", default="X Axis", help="Plot x-axis label.")
    p.add_option("","--yaxis1", dest="yAxis1", default="Y Axis 1", help="Plot y-axis 1 label.")
    p.add_option("","--yaxis2", dest="yAxis2", default="Y Axis 2", help="Plot y-axis 2 label.")
    p.add_option("", "--mean", action="store_true", dest="mean", default=False, help="Plot mean values")
    p.add_option("", "--median", action="store_true", dest="median", default=False, help="Plot median values")
    p.add_option("", "--stddev", action="store_true", dest="stddev", default=False, help="Plot standard deviation values")
    p.add_option("", "--range", action="store_true", dest="range", default=False, help="Plot range values")
    p.add_option("", "--start", dest="startDate", default="", help="Start Date")
    p.add_option("", "--end", dest="endDate", default="", help="End Date")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile1 is None:
        p.print_help()
        print "Input1 filename must be set."
        sys.exit()

    if self.inputFile2 is None:
        p.print_help()
        print "Input2 filename must be set."
        sys.exit()

    if self.outputFile is None:
        p.print_help()
        print "output filename must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = PlotAverageData()
    obj.run(cmdargs)
