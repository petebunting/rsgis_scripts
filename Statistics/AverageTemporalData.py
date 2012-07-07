 #! /usr/bin/env python

#######################################
# A python script to average columns of
# data by time (weekly, monthly, yearly)
#
# Email: petebunting@mac.com
# Date: 13/09/2011
# Version: 1.0
#######################################

import os.path
import sys
import datetime
from datetime import timedelta
from math import *
import optparse

class AverageData (object):

    def calcMinMax(self, numbers):
        min = 0
        max = 0
        if len(numbers) > 0:
            first = True
            for number in numbers:
                if first:
                    min = number
                    max = number
                    first = False
                else:
                    if number < min:
                        min = number
                    elif number > max:
                        max = number
        return min, max

    def calcMean(self, numbers):
        mean = 0
        if len(numbers) > 0:
            sum = 0.0
            for number in numbers:
                sum += number
            mean = sum/len(numbers)
        return mean

    def calcSum(self, numbers):
        sum = 0.0
        if len(numbers) > 0:
            for number in numbers:
                sum += number
        return sum

    def calcStdDev(self, numbers, mean):
        stddev = 0
        if len(numbers) > 1:
            deviation = 0.0
            singleDev = 0.0
            for number in numbers:
                singleDev = number-mean
                deviation += (singleDev**2)
            stddev = sqrt(deviation/(len(numbers)-1))
        return stddev

    def calcMedian(self, numbers):
        median = 0
        if len(numbers) == 1:
            median = numbers[0]
        elif len(numbers) > 0:
            numbers = sorted(numbers)
            idx = int(len(numbers)/2)
            median = numbers[idx]
        return median

    def parseTextFile(self, inputTextFile, dataList, delimiter, dateCol, ignoreLines, dataCol, dateFormat):
        lineCount = 0
        for eachLine in inputTextFile:
            if lineCount >= ignoreLines:
                lineSplit = eachLine.split(delimiter, eachLine.count(delimiter))
                if len(lineSplit) > dateCol and len(lineSplit) > dataCol:
                    try:
                        dateStr = lineSplit[dateCol]
                        dateObj = datetime.date(2004, 1, 1)
                        if dateFormat == 'slashDay':
                            dateSplit = dateStr.split('/', dateStr.count('/'))
                            dateObj = datetime.date(int(dateSplit[2].strip()), int(dateSplit[1].strip()), int(dateSplit[0].strip()))
                        elif dateFormat == 'txtMonth':
                            dateSplit = dateStr.split('-', dateStr.count('-'))
                            dayVal = int(dateSplit[0].strip())
                            yearVal = int(dateSplit[2].strip())+2000
                            monthStr = dateSplit[1].strip()
                            monthVal = 0
                            if monthStr == 'Jan':
                                monthVal = 1
                            elif monthStr == 'Feb':
                                monthVal = 2
                            elif monthStr == 'Mar':
                                monthVal = 3
                            elif monthStr == 'Apr':
                                monthVal = 4
                            elif monthStr == 'May':
                                monthVal = 5
                            elif monthStr == 'Jun':
                                monthVal = 6
                            elif monthStr == 'Jul':
                                monthVal = 7
                            elif monthStr == 'Aug':
                                monthVal = 8
                            elif monthStr == 'Sep':
                                monthVal = 9
                            elif monthStr == 'Oct':
                                monthVal = 10
                            elif monthStr == 'Nov':
                                monthVal = 11
                            elif monthStr == 'Dec':
                                monthVal = 12
                            else:
                                print 'Do not recognise month string: "', monthStr, '"'
                                sys.exit(-1)
                            dateObj = datetime.date(yearVal, monthVal, dayVal)
                        else:
                            print 'Date format is not recognised.'
                            sys.exit(-1)

                        val = float(lineSplit[dataCol].strip())
                        tupVals = (dateObj, val)
                        dataList.append(tupVals)
                    except ValueError, e:
                        print 'Ignoring: ', eachLine,
                else:
                    print 'Line being ignored as column not available.'
                    print eachLine
                    print str(len(lineSplit)), ' tokens were found using "', delimiter, '" as delimiter.'
            lineCount = lineCount + 1


    def averageDataOverTime(self, dataList, outputFile, averageTime):
        if len(dataList) > 0:
            sorted(dataList, key=lambda dataVal: dataVal[0])
            #print dataList
            if averageTime == 'year':
                print 'Averaging over a year'
                outputFile.write('Year,Count,Min,Max,Mean,Median,StdDev,p1StdDev,m1StdDev,Sum\n')
                first = True
                currentYear = dataList[0][0].year
                dataValues = list()
                for i in range(len(dataList)):
                    if currentYear == dataList[i][0].year:
                        dataValues.append(dataList[i][1])
                    else:
                        sum = self.calcSum(dataValues)
                        min, max = self.calcMinMax(dataValues)
                        mean = self.calcMean(dataValues)
                        median = self.calcMedian(dataValues)
                        stddev = self.calcStdDev(dataValues, mean)
                        p1StdDev = mean + stddev
                        m1StdDev = mean - stddev
                        outStr = str((dataList[i-1][0]).strftime("%Y"))+','+str(len(dataValues))+','+str(min)+','+str(max)+','+str(mean)+','+str(median)+','+str(stddev)+','+str(p1StdDev)+','+str(m1StdDev)+','+str(sum)+'\n'
                        outputFile.write(outStr)
                        currentYear = dataList[i][0].year
                        dataValues = list()
                        dataValues.append(dataList[i][1])
            elif averageTime == 'month':
                print 'Averaging over a month'
                outputFile.write('Month/Year,Count,Min,Max,Mean,Median,StdDev,p1StdDev,m1StdDev,Sum\n')
                first = True
                currentYear = dataList[0][0].year
                currentMonth = dataList[0][0].month
                dataValues = list()
                for i in range(len(dataList)):
                    if currentYear == dataList[i][0].year and currentMonth == dataList[i][0].month:
                        dataValues.append(dataList[i][1])
                    else:
                        sum = self.calcSum(dataValues)
                        min, max = self.calcMinMax(dataValues)
                        mean = self.calcMean(dataValues)
                        median = self.calcMedian(dataValues)
                        stddev = self.calcStdDev(dataValues, mean)
                        p1StdDev = mean + stddev
                        m1StdDev = mean - stddev
                        outStr = str(dataList[i-1][0].strftime("%m/%Y"))+','+str(len(dataValues))+','+str(min)+','+str(max)+','+str(mean)+','+str(median)+','+str(stddev)+','+str(p1StdDev)+','+str(m1StdDev)+','+str(sum)+'\n'
                        outputFile.write(outStr)
                        currentYear = dataList[i][0].year
                        currentMonth = dataList[i][0].month
                        dataValues = list()
                        dataValues.append(dataList[i][1])
            elif averageTime == 'week':
                print 'Averaging over a week'
                outputFile.write('Week/Year,Count,Min,Max,Mean,Median,StdDev,p1StdDev,m1StdDev,Sum\n')
                first = True
                currentYear = dataList[0][0].year
                currentWeek = dataList[0][0].isocalendar()[1]
                dataValues = list()
                for i in range(len(dataList)):
                    if currentYear == dataList[i][0].year and currentWeek == dataList[i][0].isocalendar()[1]:
                        dataValues.append(dataList[i][1])
                    else:
                        sum = self.calcSum(dataValues)
                        min, max = self.calcMinMax(dataValues)
                        mean = self.calcMean(dataValues)
                        median = self.calcMedian(dataValues)
                        stddev = self.calcStdDev(dataValues, mean)
                        p1StdDev = mean + stddev
                        m1StdDev = mean - stddev
                        outStr = str(dataList[i-1][0].strftime("%W/%Y"))+','+str(len(dataValues))+','+str(min)+','+str(max)+','+str(mean)+','+str(median)+','+str(stddev)+','+str(p1StdDev)+','+str(m1StdDev)+','+str(sum)+'\n'
                        outputFile.write(outStr)
                        currentYear = dataList[i][0].year
                        currentWeek = dataList[i][0].isocalendar()[1]
                        dataValues = list()
                        dataValues.append(dataList[i][1])
            elif averageTime == 'day':
                print 'Averaging over a day'
                outputFile.write('Date,Count,Min,Max,Mean,Median,StdDev,p1StdDev,m1StdDev,Sum\n')
                first = True
                currentDay = dataList[0][0]
                dataValues = list()
                for i in range(len(dataList)):
                    if currentDay == dataList[i][0]:
                        dataValues.append(dataList[i][1])
                    else:
                        sum = self.calcSum(dataValues)
                        min, max = self.calcMinMax(dataValues)
                        mean = self.calcMean(dataValues)
                        median = self.calcMedian(dataValues)
                        stddev = self.calcStdDev(dataValues, mean)
                        p1StdDev = mean + stddev
                        m1StdDev = mean - stddev
                        outStr = str(dataList[i-1][0].strftime("%d/%m/%Y"))+','+str(len(dataValues))+','+str(min)+','+str(max)+','+str(mean)+','+str(median)+','+str(stddev)+','+str(p1StdDev)+','+str(m1StdDev)+','+str(sum)+'\n'
                        outputFile.write(outStr)
                        currentDay = dataList[i][0]
                        dataValues = list()
                        dataValues.append(dataList[i][1])
            else:
                print 'Averaging method not recognised.'
                sys.exit(-1)
        else:
            print 'No data values were extracted.'
            sys.exit(-1)

    def run(self, cmdargs):
        inputTextFilePath = cmdargs.inputFile.strip()
        outputTextFilePath = cmdargs.outputFile.strip()
        delimiter = cmdargs.delimiter.strip()
        dateCol = int(cmdargs.dateCol.strip())
        ignoreLines = int(cmdargs.ignoreLines.strip())
        dataCol = int(cmdargs.dataCol.strip())
        dateFormat = cmdargs.dateFormat.strip()
        averageTime = cmdargs.summary.strip()

        dataList = list()
        try:
            inputTextFile = open(inputTextFilePath, 'r')
            self.parseTextFile(inputTextFile, dataList, delimiter, dateCol, ignoreLines, dataCol, dateFormat)
            inputTextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return

        try:
            outputTextFile = open(outputTextFilePath, 'w')
            self.averageDataOverTime(dataList, outputTextFile, averageTime)
            outputTextFile.flush()
            outputTextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input file.")
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output file.")
    p.add_option("-d","--delimiter", dest="delimiter", default=",", help="Delimiter.")
    p.add_option("-c","--datecol", dest="dateCol", default="0", help="Date Column (starts at 0).")
    p.add_option("-l","--ignore", dest="ignoreLines", default="0", help="Number of lines to ignore.")
    p.add_option("-e","--datacol", dest="dataCol", default="2", help="Data Column (starts at 0).")
    p.add_option("-f","--dateformat", dest="dateFormat", default="slashDay", help="Date Format (slashDay | txtMonth).")
    p.add_option("-s","--summary", dest="summary", default="day", help="Data Summary (year | month | week | day).")
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
    obj = AverageData()
    obj.run(cmdargs)
