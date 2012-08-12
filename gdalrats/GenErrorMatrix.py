#!/usr/bin/env python

import sys
from rios import rat
import numpy as np
import optparse

class GenerateErrorMatrix (object):

    def sumDiagonal(self, errMatrix, classes):
        sumVal = 0
        for i in range(classes.size):
            sumVal += errMatrix[i,i]
        return sumVal

    def exportErrorMatrixAsTex(self, outputFile, classes, errMatrix):
        try:
            outputTextFile = open(outputFile, 'w')

            outputTextFile.write("\\documentclass[14pt]{amsart}\n")
            outputTextFile.write("\\usepackage{geometry}\n")
            outputTextFile.write("\\geometry{a3paper}\n")
            outputTextFile.write("\\geometry{landscape}\n")
            outputTextFile.write("\\usepackage{graphicx}\n")
            outputTextFile.write("\\usepackage{amssymb}\n")
            outputTextFile.write("\\usepackage{epstopdf}\n")
            outputTextFile.write("\\usepackage{colortbl}\n")
            outputTextFile.write("\\usepackage[table]{xcolor}\n")

            outputTextFile.write("\\begin{document}\n")

            outputTextFile.write("\\begin{table}[htdp]\n")
            outputTextFile.write("\\caption{Error Matrix}\n")
            outputTextFile.write("\\begin{center}\n")

            strLine = "\\begin{tabular}{|c"
            for i in range(classes.size):
                strLine = strLine + str("|c")
            strLine = strLine + str("|c|}\n")
            outputTextFile.write(strLine)
            outputTextFile.write("\\hline\n")

            strLine = ""
            for i in range(classes.size):
                strLine = strLine + str("&\\cellcolor{gray!50}\\textbf{") + str(classes[i]) + str("}")
            strLine = strLine + str("&\\cellcolor{gray!50}\\textbf{User}\\\\ \n")
            outputTextFile.write(strLine)
            outputTextFile.write("\\hline\n")

            for i in range(classes.size):
                strLine = str("\\cellcolor{gray!50}\\textbf{") + str(classes[i]) + str("}")
                for j in range(classes.size):
                    if i == j:
                        strLine = strLine + str("&\\cellcolor{red!50}") + str(errMatrix[i,j])
                    else:
                        strLine = strLine + str("&") + str(errMatrix[i,j])
                if errMatrix[i,i] == 0:
                    strLine = strLine + str("&\\textbf{0}\\\\ \n")
                else:
                    strLine = strLine + str("&\\textbf{") + str(round((errMatrix[i,i]/sum(errMatrix[i,...]))*100,2)) + str("}\\\\ \n")
                outputTextFile.write(strLine)
                outputTextFile.write("\\hline\n")

            strLine = str("\\cellcolor{gray!50}\\textbf{Prod}")
            for i in range(classes.size):
                if errMatrix[i,i] == 0:
                    strLine = strLine + str("&\\textbf{0}")
                else:
                    strLine = strLine + str("&\\textbf{") + str(round((errMatrix[i,i]/sum(errMatrix[...,i]))*100,2)) + str("}")
            strLine = strLine + str("&\\cellcolor{red!50}\\textbf{") + str(round((self.sumDiagonal(errMatrix, classes)/sum(errMatrix.flatten()))*100,2)) + str("}\\\\ \n")
            outputTextFile.write(strLine)
            outputTextFile.write("\\hline\n")

            outputTextFile.write("\\end{tabular}\n")
            outputTextFile.write("\\end{center}\n")
            outputTextFile.write("\\label{tab:ErrMatrix}\n")
            outputTextFile.write("\\end{table}\n")
            outputTextFile.write("\\end{document}\n")

            outputTextFile.flush()
            outputTextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return

        print "Exporting as LaTeX file"

    def exportErrorMatrixAsASCII(self, outputFile, classes, errMatrix):
        print "Exporting as ASCII file"
        try:
            outputTextFile = open(outputFile, 'w')

            strLine = ""
            for i in range(classes.size):
                strLine = strLine + str(",") + str(classes[i])
            strLine = strLine + str("\n")
            outputTextFile.write(strLine)

            for i in range(classes.size):
                strLine = str(classes[i])
                for j in range(classes.size):
                    strLine = strLine + str(",") + str(errMatrix[i,j])
                strLine = strLine + str("\n")
                outputTextFile.write(strLine)

            outputTextFile.flush()
            outputTextFile.close()
        except IOError, e:
            print '\nCould not open file:\n', e
            return

    def buildErrorMatrix(self, errMatrix, classes, refCol, classCol):
        print "Building Error Matrix."
        refColSize = refCol.size
        classColSize = classCol.size

        if refColSize != classColSize:
            print "The reference and classified columns do not have the same number of features."
            return

        refVal = 0
        refValIdx = 0
        classVal = 0
        classValIdx = 0
        for idx in range(refColSize):
            refVal = refCol[idx]
            classVal = classCol[idx]
            refValIdx = np.where(classes==refVal)[0]
            classValIdx = np.where(classes==classVal)[0]
            errMatrix[refValIdx, classValIdx] += 1


    def run(self, cmdargs):
        refCol = rat.readColumn(cmdargs.inputFile, cmdargs.referenceCol)
        classCol = rat.readColumn(cmdargs.inputFile, cmdargs.classifiedCol)

        classes = np.unique(refCol)

        print "Classes (", classes.size, "): ", classes

        errMatrix = np.zeros((classes.size, classes.size))

        self.buildErrorMatrix(errMatrix, classes, refCol, classCol)

        self.exportErrorMatrixAsASCII(cmdargs.outputFile, classes, errMatrix)

        if cmdargs.outputTexFile is not None:
            self.exportErrorMatrixAsTex(cmdargs.outputTexFile, classes, errMatrix)


# Command arguments
class CmdArgs:
    def __init__(self):
        p = optparse.OptionParser()
        p.add_option("-i","--input", dest="inputFile", default=None, help="Input GDAL image with RAT.")
        p.add_option("-o","--output", dest="outputFile", default=None, help="Output ASCII file.")
        p.add_option("-t","--tex", dest="outputTexFile", default=None, help="Output Tex file.")
        p.add_option("-r","--ref", dest="referenceCol", default=None, help="Reference column.")
        p.add_option("-c","--class", dest="classifiedCol", default=None, help="Classified column.")
        (options, args) = p.parse_args()
        self.__dict__.update(options.__dict__)

        if self.inputFile is None:
            p.print_help()
            print "Input filename must be provided."
            sys.exit()

        if self.outputFile is None:
            p.print_help()
            print "Output filename must be provided."
            sys.exit()

        if self.referenceCol is None:
            p.print_help()
            print "Reference column must be provided."
            sys.exit()

        if self.classifiedCol is None:
            p.print_help()
            print "Classified column must be provided."
            sys.exit()

if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = GenerateErrorMatrix()
    obj.run(cmdargs)
