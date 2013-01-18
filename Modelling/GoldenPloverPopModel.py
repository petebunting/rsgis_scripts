#!/usr/bin/env python

############################################################################
# Copyright (c) 2013
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
# Purpose:  To generate a map legend from an inputted GDAL file where
#           the RAT contains a list of classes and colours.

# Authors: Heather Crump and Pete Bunting
# Email: petebunting@mac.com
# Date: 13/01/2012
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
#############################################################################

import sys
import optparse
import math as math

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

class GoldenPloverPopModel (object):

    def parseParameterFile(self, inputFile):
        paramsStr = "## Input Parameters to the model.\n"
        parameterFile = open(inputFile, 'r')
        params = dict()
        for line in parameterFile:
            line = line.strip()
            paramsStr += "# " + line + "\n"
            paramVals = line.split("=", 1)
            if paramVals[0] == "numOfYears":
                params[paramVals[0]] = int(paramVals[1])
            elif paramVals[0] == "initalAdultPairPop":
                params[paramVals[0]] = int(paramVals[1])
            elif paramVals[0] == "winterSurvivalRate":
                params[paramVals[0]] = float(paramVals[1])
            elif paramVals[0] == "averageEggsPerPair":
                params[paramVals[0]] = float(paramVals[1])
            elif paramVals[0] == "averageFledgelingsPerPair":
                params[paramVals[0]] = float(paramVals[1])
            elif paramVals[0] == "predatorControl":
                if paramVals[1].lower() == "false":
                    params[paramVals[0]] = False
                elif paramVals[1].lower() == "true":
                    params[paramVals[0]] = True
                else:
                    print "predatorControl must be either True or False."
                    sys.exit()
            elif paramVals[0] == "numOfFledgelings":
                params[paramVals[0]] = int(paramVals[1])
            elif paramVals[0] == "numOfFledgelingsYearOld":
                params[paramVals[0]] = int(paramVals[1])
            elif paramVals[0] == "fledgelingsSurvivePredatorsCtrl":
                params[paramVals[0]] = float(paramVals[1])
            elif paramVals[0] == "fledgelingsSurvivePredatorsNoCtrl":
                params[paramVals[0]] = float(paramVals[1])
            else:
                params[paramVals[0]] = paramVals[1]
        return params, paramsStr            
    
    def runGPModel(self, params):
        print "Running Model"
        # Local Variables.
        numOfAdultsPairs = params['initalAdultPairPop']
        numOfFledgelingsYearOld = params['numOfFledgelingsYearOld']
        numOfFledgelings = params['numOfFledgelings']
        numOfEggs = 0
        
        # Output Lists. 
        numOfAdultsPairsOut = list()
        numYearOldFledgelingsOut = list()
        numOfEggsOut = list()
        numOfFledgelingsOut = list()
        numOfFledgelingsB4PredOut = list()
        
        for year in range(params['numOfYears']):
            numOfAdultsPairsOut.append(numOfAdultsPairs)
            numYearOldFledgelingsOut.append(numOfFledgelingsYearOld)
            numOfFledgelingsOut.append(numOfFledgelings)
            
            numOfAdultsPairs += (numOfFledgelingsYearOld/2)
            numOfFledgelingsYearOld = numOfFledgelings
            
            # Winter Survival
            numOfAdultsPairs=int(numOfAdultsPairs*params['winterSurvivalRate'])
            numOfFledgelingsYearOld=int(numOfFledgelingsYearOld*params['winterSurvivalRate'])
            
            # Numbers of Eggs to hatch
            numOfEggs = int(numOfAdultsPairs * params['averageEggsPerPair'])
            numOfEggsOut.append(numOfEggs)
            
            # Number of Eggs to Fledgeling
            numOfFledgelings = int(numOfAdultsPairs * params['averageFledgelingsPerPair'])
            numOfFledgelingsB4PredOut.append(numOfFledgelings)
            
            if params['predatorControl']:
                numOfFledgelings=int(numOfFledgelings*params['fledgelingsSurvivePredatorsCtrl'])
            else:
                numOfFledgelings=int(numOfFledgelings*params['fledgelingsSurvivePredatorsNoCtrl'])
                
        return numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut
            
        
    def writeResultsFile(self, outputFile, paramStr, params, numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut):
        print "Writing to " + outputFile
        outFile = open(outputFile, 'w')
        outFile.write(paramStr)
        outFile.write("\n\n## Output Results.\n")
        yearStrs = "Year"
        numOfAdultsStrs = "NumberOfAdultsPairs"
        numOfYearOldFledgesStrs = "NumberOfYearOldFledgelings"
        numOfFledgesStrs = "NumberOfFledgelings"
        numOfFledgesB4PredStrs = "NumberOfFledgelingsB4Preds"
        numOfEggsStrs = "NumberOfEggs"
        for year in range(params['numOfYears']):
            yearStrs += "," + str(year)
            numOfAdultsStrs += "," + str(numOfAdultsPairsOut[year])
            numOfYearOldFledgesStrs += "," + str(numYearOldFledgelingsOut[year])
            numOfFledgesStrs += "," + str(numOfFledgelingsOut[year])
            numOfFledgesB4PredStrs += "," + str(numOfFledgelingsB4PredOut[year])
            numOfEggsStrs += "," + str(numOfEggsOut[year])
        
        yearStrs += "\n"
        numOfAdultsStrs += "\n"
        numOfYearOldFledgesStrs += "\n"
        numOfFledgesStrs += "\n"
        numOfFledgesB4PredStrs += "\n"
        numOfEggsStrs += "\n"
        
        outFile.write(yearStrs)
        outFile.write(numOfAdultsStrs)
        outFile.write(numOfFledgesStrs)
        outFile.write(numOfFledgesB4PredStrs)
        outFile.write(numOfFledgesStrs)
        outFile.write(numOfEggsStrs)
        
        outFile.close()
        
    def writeRScript(self, outputFile, params, numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut):
        print "Write to " + outputFile
        
    def plots(self, outputFile, params, numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut):        
        if module_exists("matplotlib.pyplot"):
            print "Matplotlib is available."
            import matplotlib.pyplot as plt
            years = range(params['numOfYears'])
            
            fig1 = plt.figure(figsize=(15, 5), dpi=150)
            plt.plot(years, numOfAdultsPairsOut)
            plt.title("Number of pairs per year predicted by model")
            plt.xlabel("Year")
            plt.ylabel("Number Of Pairs")
            plt.savefig((outputFile+"_adultpairs.pdf"), format='PDF')
            
            fig2 = plt.figure(figsize=(15, 5), dpi=150)
            plt.plot(years, numYearOldFledgelingsOut)
            plt.title("Number of pairs per year predicted by model")
            plt.xlabel("Year")
            plt.ylabel("Number Of Pairs")
            plt.savefig((outputFile+"_numYearOldFledgelings.pdf"), format='PDF')
            
            fig3 = plt.figure(figsize=(15, 5), dpi=150)
            plt.plot(years, numOfEggsOut)
            plt.title("Number of pairs per year predicted by model")
            plt.xlabel("Year")
            plt.ylabel("Number Of Pairs")
            plt.savefig((outputFile+"_numOfEggs.pdf"), format='PDF')
            
            fig4 = plt.figure(figsize=(15, 5), dpi=150)
            plt.plot(years, numOfFledgelingsOut)
            plt.title("Number of pairs per year predicted by model")
            plt.xlabel("Year")
            plt.ylabel("Number Of Pairs")
            plt.savefig((outputFile+"_numOfFledgelings.pdf"), format='PDF')
            
            fig5 = plt.figure(figsize=(15, 5), dpi=150)
            plt.plot(years, numOfFledgelingsB4PredOut)
            plt.title("Number of pairs per year predicted by model")
            plt.xlabel("Year")
            plt.ylabel("Number Of Pairs")
            plt.savefig((outputFile+"_numOfFledgelingsB4Pred.pdf"), format='PDF')
            
        else:
            print "Matplotlib is not available and therefore the plot cannot be created."
        
    def run(self, cmdargs):
        print "Parse Input File."
        params, paramsStr = self.parseParameterFile(cmdargs.inputFile)
        print params
        print "Run the model"
        numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut = self.runGPModel(params)
        print "Write the results to an output file"
        self.writeResultsFile(cmdargs.outputFile, paramsStr, params, numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut)
        if cmdargs.rFile is not None:
            print "Write the results to an R script"
            self.writeRScript(cmdargs.outputFile, params, numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut)
        if cmdargs.plotFile is not None:
            print "Write the number of adult to a plot"
            self.plots(cmdargs.plotFile, params, numOfAdultsPairsOut, numYearOldFledgelingsOut, numOfEggsOut, numOfFledgelingsOut, numOfFledgelingsB4PredOut)
        

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input parameter file.")
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output results file.")
    p.add_option("-r","--rplot", dest="rFile", default=None, help="Output R script to plot the result.")
    p.add_option("-p","--plot", dest="plotFile", default=None, help="Output a plot of the number of adult GPs.")

    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "An input parameter file should be provided."
        sys.exit()

    if self.outputFile is None:
        p.print_help()
        print "Output results file."
        sys.exit()
        
if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = GoldenPloverPopModel()
    obj.run(cmdargs)
