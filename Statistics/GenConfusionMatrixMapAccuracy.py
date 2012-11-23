#!/usr/bin/env python

import sys
import os
from rios import rat
import numpy as np
import osgeo.gdal as gdal
import optparse

class GenErrorMatrixFromMapAccuracy (object):

    def exportToTex(self, outputFilePath, errMatrix, classes, userVals, prodVals, overallErr, kappa):
        try:
            for i in range(len(classes)):
                classes[i] = classes[i].replace('&', '\&')
        
            # Open File
            outputFile = open(outputFilePath, 'w')
            
            # Write latex header to file
            outputFile.write('\\documentclass[12pt]{amsart}\n')
            outputFile.write('\\usepackage{geometry}\n')
            outputFile.write('\\geometry{a1paper}\n')
            outputFile.write('\\geometry{landscape}\n')
            outputFile.write('\\usepackage{graphicx}\n')
            outputFile.write('\\usepackage{amssymb}\n')
            outputFile.write('\\usepackage{epstopdf}\n')
            outputFile.write('\\usepackage{colortbl}\n')
            outputFile.write('\\usepackage[table]{xcolor}\n')
            outputFile.write('\\begin{document}\n')
            # Create the latex table
            outputFile.write('\\begin{table}[htdp]\n')
            caption = str("\\caption{Error Matrix. Av. User Error: ") + str(round(np.mean(userVals),2)) + str("\% Av. Prod Error: ") + str(round(np.mean(prodVals))) + str("\% Kappa: ") + str(round((kappa*100),2)) +  str("\%}\n")
            outputFile.write(caption)
            outputFile.write('\\begin{center}\n')
            tabularLine = '\\begin{tabular}{|c|'
            for classVal in classes:
                tabularLine =  tabularLine + 'c|'
            tabularLine =  tabularLine + 'c|}\n'
            outputFile.write(tabularLine)
            outputFile.write('\\hline\n')
            
            # Create table column titles
            titleLine = ''
            for classVal in classes:
                titleLine =  titleLine + '&\\cellcolor{gray!50}\\rotatebox{90}{\\mbox{\\textbf{' + str(classVal) + '}}}'
            titleLine =  titleLine + '&\\cellcolor{gray!50}\\textbf{User}\\\\\n'
            outputFile.write(titleLine)
            outputFile.write('\\hline\n')
            
            # Create main table body
            yIdx = 0
            for classValY in classes:
                line = '\\cellcolor{gray!50}\\textbf{' + str(classValY) + '}'
                xIdx = 0
                for classValX in classes:
                    if classValY == classValX:
                        line = line + '&\\cellcolor{red!50}' + str(round(errMatrix[yIdx][xIdx]*100,4))
                    else:
                        line = line + '&' + str(round(errMatrix[yIdx][xIdx]*100,4))
                    xIdx = xIdx + 1    
                line = line + '&\\textbf{' + str(round(userVals[yIdx],2)) + '\%}\\\\\n'
                yIdx = yIdx + 1
                outputFile.write(line)
                outputFile.write('\\hline\n')
            
            # Add bottom (producers) row
            line = '\\cellcolor{gray!50}\\textbf{Prod}'
            for val in prodVals:
                line = line + '&\\textbf{' + str(round(val,2)) + '\%}'
            line = line + '&\\textbf{' + str(round(overallErr,2)) + '\%}\\\\\n'
            outputFile.write(line)
            outputFile.write('\\hline\n')
            
            # End the table and document
            outputFile.write('\\end{tabular}\n')
            outputFile.write('\\end{center}\n')
            outputFile.write('\\label{tab:ErrMatrix}\n')
            outputFile.write('\\end{table}\n')
            outputFile.write('\\end{document}\n')
            
            # Close and flush output file
            outputFile.flush()
            outputFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return
    
    def findColIdx(self, classes, val):
        i = 0
        found = False
        for classVal in classes:
            if classVal == val:
                found = True
                break
            i = i + 1
        if not found:
            print "CLASSES: ", classes
            print "Could not find column index for value \'" + str(val) + "\'"
            sys.exit()
        return i
        
    def popErrMatrix(self, errMatrix, classes, predCol, knownCol, classAreas):        
        for i in range(len(predCol)):
            predIdx = self.findColIdx(classes, predCol[i])
            knownIdx = self.findColIdx(classes, knownCol[i])
            errMatrix[predIdx][knownIdx] = errMatrix[predIdx][knownIdx] + 1
            
        for i in range(len(classes)):
            totUserErr = np.sum(errMatrix[i])
            for j in range(len(classes)):
                if totUserErr == 0:
                    errMatrix[i][j] = 0
                else:
                    errMatrix[i][j] = (float(errMatrix[i][j])/float(totUserErr)) * classAreas[i]
    
    def popUserErrorVals(self, errMatrix, classes, userErr):
        for i in range(len(classes)):
            totUserErr = np.sum(errMatrix[i])
            if totUserErr == 0:
                userErr[i] = 0
            else:
                userErr[i] = (float(errMatrix[i][i])/float(totUserErr))*100
            
    def popProdErrorVals(self, errMatrix, classes, prodErr):
        for i in range(len(classes)):
            totProdErr = 0
            for j in range(len(classes)):
                totProdErr = totProdErr + errMatrix[j][i]
            if totProdErr == 0:
                prodErr[i] = 0.0
            else:
                prodErr[i] = (float(errMatrix[i][i])/float(totProdErr))*100
    
    def calcOverallErr(self, errMatrix, classes):
        sumCorrect = 0
        for i in range(len(classes)):
            sumCorrect = sumCorrect + errMatrix[i][i]
            
        return float(sumCorrect)*100
        
    def calcKappa(self, errMatrix, classes):
        sumDataPts = np.sum(errMatrix)
        if sumDataPts == 0:
            return 0.0
                
        prodErr = list()
        userErr = list()
        sumCorrect = 0
        for i in range(len(classes)):
            userErr.append(np.sum(errMatrix[i]))
            totProdErr = 0
            for j in range(len(classes)):
                totProdErr += errMatrix[j][i]
            prodErr.append(totProdErr)
            sumCorrect += errMatrix[i][i]
        
        sumUserProd = 0
        for i in range(len(classes)):
            sumUserProd += (prodErr[i] * userErr[i])
        
        sumDataPtsSqd = sumDataPts * sumDataPts
        
        return ((float(sumDataPts) * float(sumCorrect)) - float(sumUserProd))/(float(sumDataPtsSqd) - float(sumUserProd))
        
    def parseDATFile(self, inputTextFile, predCol, knownCol):
        for line in inputTextFile:
            line = line.strip()
            #print line
            tokens = line.split('\t')
            #print tokens
            predCol.append(tokens[3].strip())
            knownCol.append(tokens[4].strip())
    
    def run(self, cmdargs):
        # Get variables from command line
        inputFilePath = cmdargs.inputFile.strip()
        outputFilePath = cmdargs.outputFile.strip()
        outFileType = cmdargs.outType.strip()
        gdalRATImage = cmdargs.gdalRATImage.strip()
        classNamesCol = cmdargs.classNamesCol.strip()

        # Check output type is supported.
        if outFileType != 'tex':
            print "Currently, the only available output type is \'tex\'."
            sys.exit()
        
        predCol = list()
        knownCol = list()
        
        if os.path.exists(inputFilePath):
            try:
                inputTextFile = open(inputFilePath, 'r')
                self.parseDATFile(inputTextFile, predCol, knownCol)
                inputTextFile.close()
            except IOError, e:
                print '\nCould not open file:\n', e
                return
        
        #print predCol
        #print knownCol
        
        # Find the unique class names
        classes = np.append(predCol, knownCol)
        classes = np.unique(classes)
        #print "CLASSES:", classes
        
        # Open the GDAL dataset 
        ratDataset = gdal.Open(gdalRATImage, gdal.GA_ReadOnly)
        
        # Check the GDAL dataset was correctly opened
        if ratDataset is None:
            print "The image dataset could not opened."
            sys.exit()
            
        # Read the two columns
        gdalRATClassNames = rat.readColumn(ratDataset, classNamesCol)
        gdalRATHistogram = rat.readColumn(ratDataset, "Histogram")
        
        # Create the blank data structures
        numClasses = len(classes)
        errMatrix = list()
        userErr = list()
        prodErr = list()
        overallErr = 0
        kappa = 0
        classAreas = list()
        for i in range(numClasses):
            row = list()
            for j in range(numClasses):
                row.append(0)
            errMatrix.append(row)
            userErr.append(0)
            prodErr.append(0)
            classAreas.append(0)
        
        # Find Areas of each class
        for i in range(numClasses):
            for j in range(len(gdalRATClassNames)):
                if gdalRATClassNames[j].strip() == classes[i].strip():
                    classAreas[i] = gdalRATHistogram[j]
                    break;
                    
        
        totalArea = np.sum(classAreas)
        for i in range(numClasses):
            classAreas[i] = float(classAreas[i])/float(totalArea)
            print "Class '", classes[i], "' has a percentage of the total area of ", (round(classAreas[i],4) * 100), ' %'
                
        # Populate the error matrix
        self.popErrMatrix(errMatrix, classes, predCol, knownCol, classAreas)
        
        # Populate the user error fields
        self.popUserErrorVals(errMatrix, classes, userErr)
        
        # Populate the producer error fields
        self.popProdErrorVals(errMatrix, classes, prodErr)
        
        # Calculate the overall error
        overallErr = self.calcOverallErr(errMatrix, classes)
        
        # Calculate kappa
        kappa = self.calcKappa(errMatrix, classes)
        
        # Write the error matrix to the output file.
        if outFileType == 'tex':
            self.exportToTex(outputFilePath, errMatrix, classes, userErr, prodErr, overallErr, kappa)
        else:
            print "Currently, the only available output type is \'tex\'."
            sys.exit()
        

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input file.")
    p.add_option("-r","--rat", dest="gdalRATImage", default=None, help="Input GDAL Image file (With Histogram Column).")
    p.add_option("-c","--column", dest="classNamesCol", default=None, help="Column which contains the class names.")
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output file.")
    p.add_option("-t","--outtype", dest="outType", default="tex", help="Output type (tex | csv).")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "Input filename must be set."
        sys.exit()

    if self.outputFile is None:
        p.print_help()
        print "Output filename must be set."
        sys.exit()
        
    if self.gdalRATImage is None:
        p.print_help()
        print "GDAL image must be provided."
        sys.exit()
        
    if self.classNamesCol is None:
        p.print_help()
        print "Class names column must be provided."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = GenErrorMatrixFromMapAccuracy()
    obj.run(cmdargs)
    
    
    
    
    