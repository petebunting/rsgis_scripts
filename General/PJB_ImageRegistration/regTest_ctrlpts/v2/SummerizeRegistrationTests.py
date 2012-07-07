#! /usr/bin/env python

import sys
import os
import gc
from CompareCtrlPts import CompareCtrlPts
from RegSummery import Summery 
from RegParam import RegistrationParameter 

class RegistrationSummeries (object):
    'Class for summeries the registration tests.'
    refBase = ''
    regBase = ''
    outPlots = ''
    summeryOut = ''
    summeryFileStr = ''
    imageFormat = ''
    spotSize = 20
    experiment = ''
    
    def openFile4Read(self, inputPath):
        return open(inputPath, 'r', -1)
        
    def createExtraDirs(self):
        os.chdir(self.outPlots)
        if not os.path.isdir('final'):
            os.mkdir('final')
        if not os.path.isdir('steps'):
            os.mkdir('steps')
    
    def checkforSemiColons(self, line):
        foundSemiColon = False
        for i in range(len(line)):
            #print  line[i],
            if line[i] == ';':
                foundSemiColon = True
        return foundSemiColon
    
    def getString(self, line):
        #print 'Line: ', line
        strStart = 0
        strOut = ''
        for i in range(len(line)):
            #print  line[i],
            if line[i] == '\'':
                if strStart == 0:
                    strStart = strStart + 1
                elif strStart > 1:
                    strStart = strStart + 1
                    break;
            elif strStart == 1: 
                strOut = strOut + line[i]
        return strOut
    
    # Parse the Control points file into a List.
    def parseParamFile(self, paramsFile, paramList):
        os.chdir('/')
        counter = 0
        for eachLine in paramsFile:
            semiColon = self.checkforSemiColons(eachLine)
            if semiColon == False:
                if counter == 0:
                    self.refBase = self.getString(eachLine.strip())
                    if not os.path.exists(self.refBase):
                        print 'Reference Base does not exist: \'', self.refBase, '\''
                        #self.help()
                    else:        
                        if not os.path.isdir(self.refBase):
                            print 'Reference Base is not a directory: \'', self.refBase, '\''
                            #self.help()
                        else:
                            print 'Reference Base is OK.'
                elif counter == 1:
                    self.regBase = self.getString(eachLine.strip())
                    if not os.path.exists(self.regBase):
                        print 'Registration Base does not exist: \'', self.regBase, '\''
                        #self.help()
                    else:        
                        if not os.path.isdir(self.regBase):
                            print 'Registration Base is not a directory: \'', self.regBase, '\''
                            #self.help()
                        else:
                            print 'Registration Base is OK.'
                elif counter == 2:
                    self.outPlots = self.getString(eachLine.strip())
                    if not os.path.exists(self.outPlots):
                        print 'Plots Base does not exist: ', self.outPlots, '\''
                        #self.help()
                    else:        
                        if not os.path.isdir(self.outPlots):
                            print 'Plots Base is not a directory: \'', self.outPlots, '\''
                            #self.help()
                        else:
                            print 'Output Plots Base is OK.'
                elif counter == 3:
                    self.summeryOut = self.getString(eachLine.strip())
                    if not os.path.exists(self.summeryOut):
                        print 'Summery output does not exist: \'', self.summeryOut, '\''
                        #self.help()
                    else:        
                        if not os.path.isdir(self.summeryOut):
                            print 'Plots Base is not a Directory: \'', self.summeryOut, '\''
                            #self.help()
                        else:
                            print 'Summery Output Base is OK.'
                elif counter == 4:
                    self.summeryFileStr = self.getString(eachLine.strip())
                elif counter == 5:
                    self.experiment = self.getString(eachLine.strip())
                elif counter == 6:
                    imageFormat = self.getString(eachLine.strip())
                elif counter == 7:
                    self.spotSize = int(self.getString(eachLine.strip()))
                else:
                    tmpParam = RegistrationParameter()
                    tmpParam.createParamFromLine(eachLine)
                    paramList.append(tmpParam)  
                    #print 'Found param: [', tmpParam.reference_file, ', ', tmpParam.registration_base, ']'
                counter = counter + 1
    
    
    def producePlots(self, paramList, summeryList, minor, start, end):
        
        fileList = os.listdir(self.regBase)
        basePointsFilepath = ''
        regPoints = ''
        regPointsFilepath = ''
        regPointsTitle = ''
        plotFilepath = ''
        summery = []
        tmpSummery = Summery()
        baseFound = False
        counter = 1
        print 'Start: ', start, ' End: ', end
        for i in range(len(fileList)):
            compareCtrlPts = CompareCtrlPts()
            regPoints = fileList[i]
            if os.path.splitext(regPoints)[1] == '.txt':
                print 'CurrentFile: ', regPoints
                baseFound = False
                for j in range(len(paramList)):
                    if regPoints.count(paramList[j].registration_base, 0, len(regPoints)) == 1:
                        basePointsFilepath = self.refBase + paramList[j].reference_file
                        baseFound = True
                        #print 'Found BASE!!: ', paramList[j].registration_base
                        break;
                        
                if baseFound == False:
                    print 'BUGGER!!! No base file found!!'
                    return
                        
                regPointsTitle = os.path.splitext(regPoints)[0]
                plotFilepath = self.outPlots + regPointsTitle
                regPointsFilepath = self.regBase + regPoints
                #print 'BASE Points: ', basePointsFilepath
                #print 'Reg Points: ', regPointsFilepath
                #print 'Plot output: ', plotFilepath
                
                print 'Counter: ', counter
                
                
                if regPointsFilepath.count('nodesLevel', 0, len(regPointsFilepath)) == 1:
                    if minor == 0:
                        if (counter >= start) and (counter < end):
                            plotFilepath = self.outPlots + 'steps/' + regPointsTitle
                            summery = compareCtrlPts.run(basePointsFilepath, regPointsFilepath, plotFilepath, self.imageFormat, self.spotSize, [1,1,0,0])
                            tmpSummery = Summery()
                            tmpSummery.createSummery(summery, regPointsTitle)
                            summeryList.append(tmpSummery)
                            print 'Complete ', regPointsTitle
                        counter = counter + 1
                else:
                    if (counter >= start) and (counter < end):
                        plotFilepath = self.outPlots + 'final/' + regPointsTitle
                        summery = compareCtrlPts.run(basePointsFilepath, regPointsFilepath, plotFilepath, self.imageFormat, self.spotSize, [1,1,1,0])
                        tmpSummery = Summery()
                        tmpSummery.createSummery(summery, regPointsTitle)
                        summeryList.append(tmpSummery)
                        print 'Complete ', regPointsTitle
                    counter = counter + 1
                    
                if counter < start:
                    print 'Ignoring ', regPointsTitle
                elif counter >= end:
                    print 'Finished Counter: ', counter
                    return
            del compareCtrlPts
            gc.collect()
            
    def outputSummery(self, summeryList):
        fileOutput = self.summeryOut + self.summeryFileStr
        summeryFile = open(fileOutput, 'w')
        summeryFile.write('title, \t min, \t mean, \t max, \t stddev \n')
        
        for i in range(len(summeryList)):
            summeryFile.write(summeryList[i].toString())
        
        summeryFile.close()
    
    def run(self):
        
        paramList = list()
        summeryList = list()
        
        numArgs = len(sys.argv)
        if numArgs == 5:
            filePath = sys.argv[1]
            minor = int(sys.argv[2])
            start = int(sys.argv[3])
            end = int(sys.argv[4])
            if not os.path.exists(filePath):
                print 'Filepath does not exist'
                self.help()
            else:
                print filePath, ' is OK.'        
                if not os.path.isfile(filePath):
                    print 'Filepath is not a file!'
                    self.help()
                else:
                    file = self.openFile4Read(filePath)
                    self.parseParamFile(file, paramList)
                    self.createExtraDirs()
                    self.producePlots(paramList, summeryList, minor, start, end)
                    self.outputSummery(summeryList)
        else:
            self.help()
        
    def help(self):
        print 'HELP: Registration Summeries'
        print 'python SummerizeRegstrationTests.py <parametersfile.txt> <int steps>'
        
        print 'Parameters file:'
        print 'Comments start with ; and are ignored (Lines only)'
        print 'Line 1: Path to reference files'
        print 'Line 2: Path to registration input files'
        print 'Line 3: Path to output plots directory'
        print 'Line 4: Path to summery output directory'
        print 'Line 5: Image file format'
        print 'Line 6: Plot spot size'
        print '<reference file> <registration file base>'
        
        print 'Process steps: 1 - YES'


if __name__ == '__main__':
    
    obj = RegistrationSummeries()
    obj.run()
