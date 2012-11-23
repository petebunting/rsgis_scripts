#!/usr/bin/env python

import sys
from rios import rat
import numpy as np
import osgeo.gdal as gdal
import optparse
import os
from RATGenConfuseMatrix import GenConfusionMatrixFromRAT

class GenErrCompTable (object):

    def checkFileExtension(self, filename, extension):
        foundExtension = False;
        filenamesplit = os.path.splitext(filename)
        fileExtension = filenamesplit[1].strip()
        if(fileExtension == extension):
            foundExtension = True
        return foundExtension

    def findFiles(self, filelist, directory, extension):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                fileList = os.listdir(directory)
                for filename in fileList:
                    if(os.path.isdir(os.path.join(directory,filename))):
                        self.findFiles(filelist, os.path.join(directory,filename), extension)
                    elif(os.path.isfile(os.path.join(directory,filename))):
                        if(self.checkFileExtension(filename, extension)):
                            filelist.append(os.path.join(directory,filename))
                    else:
                        print filename + ' is NOT a file or directory!'
            else:
                print directory + ' is not a directory!'
        else:
            print directory + ' does not exist!'


    def run(self, cmdargs):
        # Get variables from command line
        inputDIRPath = cmdargs.inputdir.strip()
        fileExt = cmdargs.extension.strip()
        outputFilePath = cmdargs.outputFile.strip()
        predColName = cmdargs.predictedCol.strip()
        knownColName = cmdargs.knownCol.strip()
    
        inFileList = list()
        self.findFiles(inFileList, inputDIRPath, fileExt)
        
        errMatrixFuncs = GenConfusionMatrixFromRAT()
        outputFile = open(outputFilePath, 'w')
        outputFile.write('File,Users,Prods,Kappa,Overall\n')
        for file in inFileList:
            print file
            # Open the GDAL dataset 
            ratDataset = gdal.Open(file, gdal.GA_ReadOnly)
            
            # Check the GDAL dataset was correctly opened
            if ratDataset is None:
                print "The image dataset could not opened."
                sys.exit()
            
            # Read the two columns
            predCol = rat.readColumn(ratDataset, predColName)
            knownCol = rat.readColumn(ratDataset, knownColName)
            histogram = rat.readColumn(ratDataset, "Histogram")
            
            # Find the unique class names
            classes = np.append(predCol, knownCol)
            classes = np.unique(classes)
        
            # Create the blank data structures
            numClasses = len(classes)
            errMatrix = list()
            userErr = list()
            prodErr = list()
            overallErr = 0
            kappa = 0
            classAreas=list()
            for i in range(numClasses):
                row = list()
                for j in range(numClasses):
                    row.append(0)
                errMatrix.append(row)
                userErr.append(0)
                prodErr.append(0)
                classAreas.append(0)
            
            for i in range(len(knownCol)):
                idx = errMatrixFuncs.findColIdx(classes, knownCol[i])
                classAreas[idx] += histogram[i]
            
            totalArea = np.sum(classAreas)
            for i in range(numClasses):
                classAreas[i] = float(classAreas[i])/float(totalArea)
            
            # Populate the error matrix
            errMatrixFuncs.popErrMatrix(errMatrix, classes, predCol, knownCol, classAreas)
            
            # Populate the user error fields
            errMatrixFuncs.popUserErrorVals(errMatrix, classes, userErr)
            
            # Populate the producer error fields
            errMatrixFuncs.popProdErrorVals(errMatrix, classes, prodErr)
            
            # Calculate the overall error
            overallErr = errMatrixFuncs.calcOverallErr(errMatrix, classes)
            
            # Calculate kappa
            kappa = errMatrixFuncs.calcKappa(errMatrix, classes)
        
            basefile = os.path.basename(file)
            basename = os.path.splitext(basefile)[0]
            line = str(basename) + str(",") + str(round(np.mean(userErr),2)) + str(",") + str(round(np.mean(prodErr),2)) + str(",") + str(round(kappa*100, 2)) + str(",") + str(round(overallErr,2)) +  str("\n")
            outputFile.write(line)
        outputFile.flush()
        outputFile.close()


# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputdir", default=None, help="Input directory.")
    p.add_option("-e","--ext", dest="extension", default=None, help="File extension of the files of interest.")
    p.add_option("-o","--output", dest="outputFile", default=None, help="Output file.")
    p.add_option("-p","--predicted", dest="predictedCol", default="", help="Predicted Column Name.")
    p.add_option("-k","--known", dest="knownCol", default="", help="Known Column Name.")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputdir is None:
        p.print_help()
        print "Input directory path must be set."
        sys.exit()
        
    if self.extension is None:
        p.print_help()
        print "Input file extension path must be set."
        sys.exit()

    if self.outputFile is None:
        p.print_help()
        print "Output filename must be set."
        sys.exit()
        
    if self.predictedCol is None:
        p.print_help()
        print "Predicited column name must be set."
        sys.exit()

    if self.knownCol is None:
        p.print_help()
        print "Known column name must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = GenErrCompTable()
    obj.run(cmdargs)