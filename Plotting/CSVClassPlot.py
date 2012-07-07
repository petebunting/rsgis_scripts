#! /usr/bin/env python

############################################################################
# Copyright (c) 2009 Dr. Peter Bunting, Aberystwyth University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# Purpose:  The generation of scatter plots and frequency histograms from
#           an inputted CSV file where the first column is the class.
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 22/09/2009
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
#############################################################################

import os.path
import sys
from pylab import *
import matplotlib.pyplot as plt

def checkforHash(line):
    foundHash = False
    for i in range(len(line)):
        if line[i] == '#':
            foundHash = True
    return foundHash

def stringTokenizer(line, delimiter):
    tokens = list()
    token = str()
    for i in range(len(line)):
        if line[i] == delimiter:
            tokens.append(token)
            token = str()
        else:
            token = token + line[i]
    tokens.append(token)
    return tokens

class CSVClassPlot (object):

    def readColoursCSV(self, inputFile):
        colours = list()
        dataFile = open(inputFile, 'r')
        for eachLine in dataFile:
            comment = checkforHash(eachLine)
            if comment == False:
                tokens = stringTokenizer(eachLine, ',')
                if len(tokens) == 5:
                    colour = list()
                    colour.append(str(tokens[0].strip()))
                    colour.append(float(tokens[1].strip()))
                    colour.append(float(tokens[2].strip()))
                    colour.append(float(tokens[3].strip()))
                    colour.append(float(tokens[4].strip()))
                    colours.append(colour)
                else:
                    raise Exception('Not enough tokens in a line: Should be 5 Class, R, G, B, A')
        dataFile.close()
        return colours
    
    def readClassnames(self, inputFile):
        classnames = list()
        dataFile = open(inputFile, 'r')
        for eachLine in dataFile:
            comment = checkforHash(eachLine)
            if comment == False:
                tokens = stringTokenizer(eachLine, ',')
                classnames.append(str(tokens[0].strip()))
        dataFile.close()
        return classnames
        
    def readClassnamesIgnoreFirstLine(self, inputFile):
        classnames = list()
        dataFile = open(inputFile, 'r')
        first = True
        for eachLine in dataFile:
            comment = checkforHash(eachLine)
            if comment == False:
                if first:
                    first = False
                else:
                    tokens = stringTokenizer(eachLine, ',')
                    classnames.append(str(tokens[0].strip()))
        dataFile.close()
        return classnames
        
    def readVariableNames(self, inputCSV):
        dataFile = open(inputCSV, 'r')
        line = dataFile.readline()
        tokens = stringTokenizer(line, ',')
        variables = list()
        first = True
        for token in tokens:
            if first:
                first = False
            else:
                variables.append(token.strip())
        dataFile.close()
        return variables
        
    def readCSVFileVariables(self, inputCSV, numVariables):
        data = list()
        dataFile = open(inputCSV, 'r')
        first = True
        numVariables = numVariables + 1 # The class column
        for eachLine in dataFile:
            comment = checkforHash(eachLine)
            if comment == False:
                if first:
                    first = False
                else:
                    tokens = stringTokenizer(eachLine, ',')
                    if len(tokens) == numVariables:
                        dataElement = list()
                        firstElement = True
                        for token in tokens:
                            if firstElement:
                                dataElement.append(str(token.strip()))
                                firstElement = False
                            else:
                                dataElement.append(float(token.strip()))
                        data.append(dataElement)
                    else:
                        raise Exception('Not enough tokens in a inputCSV line')
        dataFile.close()
        return data
   
    def getVariableIndex(self, variables, variable):
        for i in range(len(variables)):
            if variable == variables[i]:
                return i
        return -1
                
    def getData1(self, data, xlist, ylist, classname, xVarIdx, yVarIdx):
        classcount = 0
        for item in data:
            if item[0] == classname:
                classcount = classcount + 1
                xlist.append(item[xVarIdx+1])
                ylist.append(item[yVarIdx+1])
        return classcount
        
    def getData2(self, data, datalist, classname, varIdx):
        classcount = 0
        for item in data:
            if item[0] == classname:
                classcount = classcount + 1
                datalist.append(item[varIdx+1])
        return classcount
    
    def getDataRow(self, data, classname, xData, yData):
        for item in data:
            if item[0] == classname:
                for i in range(len(item)):
                    if i != 0:
                        xData.append(i-1)
                        yData.append(item[i])
                break
   
    def addColours(self, colours, ptColourList, classname, count):
        colour = list()
        found = False
        for eachColour in colours:
            if eachColour[0] == classname:
                colour.append(eachColour[1])
                colour.append(eachColour[2])
                colour.append(eachColour[3])
                colour.append(eachColour[4])
                found = True
                break
        if found:
            for i in range(count):
                ptColourList.append(colour)
        else:
            raise Exception('Did not find colour')
            
    def getColour(self, colours, classname):
        colour = list()
        found = False
        for eachColour in colours:
            if eachColour[0] == classname:
                colour.append(eachColour[1])
                colour.append(eachColour[2])
                colour.append(eachColour[3])
                colour.append(eachColour[4])
                found = True
                break
        if found:
            return colour
        else:
            raise Exception('Did not find colour')
   
    def plotData(self, x, y, pointSize, colours, titleText, xText, yText):
        figure()
        scatter(x, y, s=pointSize, edgecolor=colours, facecolor=colours)
        axis('tight')
        title(titleText)
        xlabel(xText)
        ylabel(yText)
        show()
        
    def plotDataToFile(self, x, y, pointSize, colours, titleText, xText, yText, outFile):
        figure()
        scatter(x, y, s=pointSize, edgecolor=colours, facecolor=colours)
        axis('tight')
        title(titleText)
        xlabel(xText)
        ylabel(yText)
        plt.savefig(outFile, format='PDF')
        
        
    def freqHistData(self, data, colour, titleText, xText, binwidth):
        figure()
        hist(data,bins=binwidth, edgecolor=colour, facecolor=colour)
        axis('tight')
        title(titleText)
        xlabel(xText)
        ylabel("Frequency")
        show()
        
    def freqHistDataToFile(self, data, colour, titleText, xText, binwidth, outFile):
        figure()
        hist(data,bins=binwidth, edgecolor=colour, facecolor=colour)
        axis('tight')
        title(titleText)
        xlabel(xText)
        ylabel("Frequency")
        plt.savefig(outFile, format='PDF')    
    
    
    def createScatter(self, colours, variables, data, classesStr, var1, var2, outputImg):
        classes = stringTokenizer(classesStr, ',')
        x = list()
        y = list()
        ptColours = list()
        xVarIdx = self.getVariableIndex(variables, var1)
        yVarIdx = self.getVariableIndex(variables, var2)
        
        print var1, ' has index ', xVarIdx
        print var2, ' has index ', yVarIdx
        
        for classname in classes:
            count = self.getData1(data, x, y, classname, xVarIdx, yVarIdx)
            print 'There are ', count, ' ', classname
            self.addColours(colours, ptColours, classname, count)
        
        title = str(classes) + str(" ") + str(var1) + str(" v ") + str(var2)
        
        self.plotDataToFile(x, y, 20, ptColours, title, var1, var2, outputImg) 
    
    def runScatterI(self, inputCSV, outputImg, colourCSV, classesStr, var1, var2):
        colours = self.readColoursCSV(colourCSV)
        variables = self.readVariableNames(inputCSV)
        data = self.readCSVFileVariables(inputCSV, len(variables))
        self.createScatter(colours, variables, data, classesStr, var1, var2, outputImg)
       
        
    def runScatterA(self, inputCSV, outputDIR, colourCSV):
        colours = self.readColoursCSV(colourCSV)
        variables = self.readVariableNames(inputCSV)
        classnames = self.readClassnames(colourCSV)
        data = self.readCSVFileVariables(inputCSV, len(variables))
        outputImg = str("")
        classes = str("")
        for i in range(len(classnames)):
            for j in range(len(classnames)):
                if j > i:
                    classes = str(classnames[i]) + str(",") + str(classnames[j])
                    for n in range(len(variables)):
                        for m in range(len(variables)):
                            if m > n:
                                outputImg = outputDIR + str(classnames[i]) + str("_") + str(classnames[j]) + str("_") + str(variables[n]) + str("_") + str(variables[m]) + str(".pdf")
                                self.createScatter(colours, variables, data, classes, variables[n], variables[m], outputImg)
    
    
    def createFreqHist(self, colours, variables, data, classname, variable, binwidth, outputImg):
        varIdx = self.getVariableIndex(variables, variable)
        datalist = list()
        count = self.getData2(data, datalist, classname, varIdx)
        colour = self.getColour(colours, classname)        
        print "Processing Variable", variable, " for ", classname, " for which there are ", count, " inputs\n"
        titleText = str("Frequency Histogram ") + str(classname) + str(" ") + str(variable)
        xText = str(classname) + str(" ") + str(variable)
        self.freqHistDataToFile(datalist, colour, titleText, xText, binwidth, outputImg)
    
    def runFreqhI(self, inputCSV, outputImg, colourCSV, classStr, var, binwidth):
        colours = self.readColoursCSV(colourCSV)
        variables = self.readVariableNames(inputCSV)
        data = self.readCSVFileVariables(inputCSV, len(variables))
        self.createFreqHist(colours, variables, data, classStr, var, binwidth, outputImg)
                            
    def runFreqhA(self, inputCSV, outputDIR, colourCSV, binwidth):
        colours = self.readColoursCSV(colourCSV)
        variables = self.readVariableNames(inputCSV)
        data = self.readCSVFileVariables(inputCSV, len(variables))
        classnames = self.readClassnames(colourCSV)
        outputImg = str("")
        for classname in classnames:
            for variable in variables:
                outputImg = outputDIR + str(classname) + str("_") + str(variable) + str(".pdf")
                self.createFreqHist(colours, variables, data, classname, variable, binwidth, outputImg)
    
    def createLinePlot(self, data, colours, classes, outputPDF):
        figure()
        classnames = stringTokenizer(classes, ',')
        for classname in classnames:
            xData = list()
            yData = list()
            self.getDataRow(data, classname, xData, yData)
            colour = self.getColour(colours, classname)
            plot(yData, xData, color=colour, linestyle='solid', marker='o', markerfacecolor=colour, markersize=8)
        axis('tight')
        titleText = str("Line plot of ") + str(classnames)
        title(titleText)
        xlabel("Percentage Frequency")
        ylabel("Height")
        #show()   
        plt.savefig(outputPDF, format='PDF')
    
    def runLineI(self, inputCSV, outputPDF, coloursCSV, classes):
        colours = self.readColoursCSV(coloursCSV)
        variables = self.readVariableNames(inputCSV)
        data = self.readCSVFileVariables(inputCSV, len(variables))
        self.createLinePlot(data, colours, classes, outputPDF)
        
    def runLineA(self, inputCSV, outputDIR, coloursCSV):
        colours = self.readColoursCSV(coloursCSV)
        variables = self.readVariableNames(inputCSV)
        data = self.readCSVFileVariables(inputCSV, len(variables))
        classnames = self.readClassnamesIgnoreFirstLine(inputCSV)
        for classname in classnames:
            outputPDF = outputDIR + classname + "_lineplot.pdf"
            self.createLinePlot(data, colours, classname, outputPDF)
    
    def run(self):
        numArgs = len(sys.argv)
        if numArgs > 2:
            command = sys.argv[1].strip()
            
            if command == 'scatterI':
                if numArgs == 8:
                    inputCSV = sys.argv[2].strip()
                    outputPDF = sys.argv[3].strip()
                    coloursCSV = sys.argv[4].strip()
                    classesStr = sys.argv[5].strip()
                    variable1 = sys.argv[6].strip()
                    variable2 = sys.argv[7].strip()
                    self.runScatterI(inputCSV, outputPDF, coloursCSV, classesStr, variable1, variable2)
                else:
                    print 'Arguments incorrect for scatterI'
                    self.help()
            elif command == 'scatterA':
                if numArgs == 5:
                    inputCSV = sys.argv[2].strip()
                    outputDIR = sys.argv[3].strip()
                    coloursCSV = sys.argv[4].strip()
                    self.runScatterA(inputCSV, outputDIR, coloursCSV)
                else:
                    print 'Arguments incorrect for scatterA'
                    self.help()
            elif command == 'freqhI':
                if numArgs == 8:
                    inputCSV = sys.argv[2].strip()
                    outputPDF = sys.argv[3].strip()
                    coloursCSV = sys.argv[4].strip()
                    classStr = sys.argv[5].strip()
                    variable = sys.argv[6].strip()
                    binwidth = float(sys.argv[7].strip())
                    self.runFreqhI(inputCSV, outputPDF, coloursCSV, classStr, variable, binwidth)
                else:
                    print 'Arguments incorrect for freqhI'
                    self.help()
            elif command == 'freqhA':
                if numArgs == 6:
                    inputCSV = sys.argv[2].strip()
                    outputDIR = sys.argv[3].strip()
                    coloursCSV = sys.argv[4].strip()
                    binwidth = float(sys.argv[5].strip())
                    self.runFreqhA(inputCSV, outputDIR, coloursCSV, binwidth)
                else:
                    print 'Arguments incorrect for freqhA'
                    self.help()        
            elif command == 'lineI':
                if numArgs == 6:
                    inputCSV = sys.argv[2].strip()
                    outputPDF = sys.argv[3].strip()
                    coloursCSV = sys.argv[4].strip()
                    classes = sys.argv[5].strip()
                    self.runLineI(inputCSV, outputPDF, coloursCSV, classes)
                else:
                    print 'Arguments incorrect for freqhA'
                    self.help()
            elif command == 'lineA':
                if numArgs == 5:
                    inputCSV = sys.argv[2].strip()
                    outputDIR = sys.argv[3].strip()
                    coloursCSV = sys.argv[4].strip()
                    self.runLineA(inputCSV, outputDIR, coloursCSV)
                else:
                    print 'Arguments incorrect for freqhA'
                    self.help()
        else:
            self.help()
    
    def help(self):
        print 'CSVClassPlot.py script generates plots from CSV files where the '
        print 'first column is the class'
        print 'Usage (1): python CSVClassPlot.py scatterI <INPUT.csv> <OUTPUT_PDF> <COLOURS_CSV>'
        print ' <CLASS(ES (comma seperated)> <Variable 1> <Variable 2>'
        print 'Usage (2): python CSVClassPlot.py scatterA <INPUT.csv> <OUTPUT_PDF> <COLOURS_CSV>'
        print 'Usage (3): python CSVClassPlot.py freqhI <INPUT.csv> <OUTPUT_PDF> <COLOURS_CSV> <CLASS> <VARIABLE> <BIN_WIDTH>'
        print 'Usage (4): python CSVClassPlot.py freqhA <INPUT.csv> <OUTPUT_DIR> <COLOURS_CSV> <BIN_WIDTH>'
        print 'Usage (5): python CSVClassPlot.py lineI <INPUT.csv> <OUTPUT_PDF> <COLOURS_CSV> <CLASS(ES - comma seperated)>'
        print 'Usage (6): python CSVClassPlot.py lineA <INPUT.csv> <OUTPUT_DIR> <COLOURS_CSV>'
        
        
if __name__ == '__main__':
    obj = CSVClassPlot()
    obj.run()
    
