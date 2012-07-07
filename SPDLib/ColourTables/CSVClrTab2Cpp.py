 #! /usr/bin/env python

#######################################
# A python script to read in a CSV file
# with a colour table and produce the C++
# code to be used with the SPD Points Viewer.
#
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 11/01/2012
# Version: 1.0
#######################################

import os.path
import sys
import optparse

class CSVClrTab2CPP (object):

    def parseCSVFileToList(self, inFile, redVals, greenVals, blueVals):
        for eachLine in inFile:
            commaSplit = eachLine.split(',', eachLine.count(','))
            col = 0
            for token in commaSplit:
                if col == 0:
                    redVals.append(int(token.strip()))
                elif col == 1:
                    greenVals.append(int(token.strip()))
                elif col == 2:
                    blueVals.append(int(token.strip()))
                col = col + 1

    def outputCPPSPDClrTab(self, outFile, redVals, greenVals, blueVals):
        outFile.write("SPDPointsViewerColourTable* createColourTab()\n{\n")
        outFile.write("    float rgbVals[256][3] = {\n")
        for i in range(len(redVals)):
            outFile.write("        {")
            outFile.write(str(redVals[i]))
            outFile.write(',')
            outFile.write(str(greenVals[i]))
            outFile.write(',')
            outFile.write(str(blueVals[i]))
            if i != len(redVals)-1:
                outFile.write('},\n')
            else:
                outFile.write('}};\n\n')

        outFile.write("    SPDPointsViewerColourTable *colourTab = new SPDPointsViewerColourTable();\n")
        outFile.write("    colourTab->setName(\"NAME\");\n")
        outFile.write("    for(unsigned int i = 0; i < 256; ++i)\n")
        outFile.write("    {\n")
        outFile.write("        ClrVals clrVal;\n")
        outFile.write("        clrVal.val = i;\n")
        outFile.write("        clrVal.red = rgbVals[i][0]/255;\n")
        outFile.write("        clrVal.green = rgbVals[i][1]/255;\n")
        outFile.write("        clrVal.blue = rgbVals[i][2]/255;\n")
        outFile.write("        colourTab->addColorValPair(clrVal);\n")
        outFile.write("    }\n")
        outFile.write("    return colourTab;\n")
        outFile.write("}\n")

    def run(self, cmdargs):
        redVals = list()
        greenVals = list()
        blueVals = list()
        try:
            inputTextFile = open(cmdargs.inputFile, 'r')
            self.parseCSVFileToList(inputTextFile, redVals, greenVals, blueVals)
            inputTextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return

        try:
            outputTextFile = open(cmdargs.outputFile, 'w')
            self.outputCPPSPDClrTab(outputTextFile, redVals, greenVals, blueVals)
            outputTextFile.flush()
            outputTextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return


# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","", dest="inputFile", default=None, help="Input CSV file.")
    p.add_option("-o","", dest="outputFile", default=None, help="Output cpp code.")
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


# Run the script
if __name__ == "__main__":
    cmdargs = CmdArgs()
    mainClass = CSVClrTab2CPP()
    mainClass.run(cmdargs)
