#!/usr/bin/env python

import sys

def readCSVFile(csvFilePath):
    colourParams = list()
    inFile = open(csvFilePath, 'r')
    idx = 0
    for line in inFile:
        line = line.strip()
        tokens = line.split(',')
        if len(tokens) == 4:
            colourParams.append(list())
            colourParams[idx].append(tokens[3])
            colourParams[idx].append(tokens[0])
            colourParams[idx].append(tokens[1])
            colourParams[idx].append(tokens[2])
            idx += 1
        else:
            print "ERROR: \'", tokens, "\'"
            print line
    inFile.close()
    return colourParams


def generateColourPy(outFilePath, inParams, inRatFilePath):
    outFile = open(outFilePath, 'w')
    outFile.write("#!/usr/bin/env python\n")
    outFile.write("\nimport sys\n")
    outFile.write("from rios import rat\n")
    outFile.write("import numpy as np\n")
    outFile.write("import osgeo.gdal as gdal\n")
    outFile.write("\ndef colourLevel4(LCCSs):\n")
    outFile.write("    # Create Output Arrays\n")
    outFile.write("    redColours = np.empty_like(LCCSs, dtype=np.int)\n")
    outFile.write("    redColours[...] = 0\n")
    outFile.write("    greenColours = np.empty_like(LCCSs, dtype=np.int)\n")
    outFile.write("    greenColours[...] = 0\n")
    outFile.write("    blueColours = np.empty_like(LCCSs, dtype=np.int)\n")
    outFile.write("    blueColours[...] = 0\n")
    outFile.write("    alphaColours = np.empty_like(LCCSs, dtype=np.int)\n")
    outFile.write("    alphaColours[...] = 255\n")
    outFile.write("\n    # NA\n")
    outFile.write("    redColours = np.where(LCCSs == \"NA\", 0, redColours)\n")
    outFile.write("    greenColours = np.where(LCCSs == \"NA\", 0, greenColours)\n")
    outFile.write("    blueColours = np.where(LCCSs == \"NA\", 0, blueColours)\n")
    outFile.write("    alphaColours = np.where(LCCSs == \"NA\", 255, alphaColours)\n")
    
    
    for param in inParams:
        redStr = str("\n    redColours = np.where(LCCSs == \"") + str(param[0]) + str("\", ") + str(param[1]) + str(", redColours)\n")
        blueStr = str("    greenColours = np.where(LCCSs == \"") + str(param[0]) + str("\", ") + str(param[2]) + str(", greenColours)\n")
        greenStr = str("    blueColours = np.where(LCCSs == \"") + str(param[0]) + str("\", ") + str(param[3]) + str(", blueColours)\n")
        alphaStr = str("    alphaColours = np.where(LCCSs == \"") + str(param[0]) + str("\", 255, alphaColours)\n")
        
        outFile.write(redStr)
        outFile.write(blueStr)
        outFile.write(greenStr)
        outFile.write(alphaStr)
        
        
    outFile.write("    return redColours, greenColours, blueColours, alphaColours\n")
    outFile.write("\n# Input file.\n")
    inputFileLine = str("fname = \"") + inRatFilePath + str("\"\n")
    outFile.write(inputFileLine)
    outFile.write("ratDataset = gdal.Open( fname, gdal.GA_Update )\n")
    
    outFile.write("\nprint \"Import Columns.\"\n")
    outFile.write("LCCSs = rat.readColumn(ratDataset, \"LCCS\")\n")
    outFile.write("\nprint \"Classifying Level 4\"\n")
    outFile.write("red, green, blue, alpha = colourLevel4(LCCSs)\n")
    outFile.write("rat.writeColumn(ratDataset, \"Red\", red)\n")
    outFile.write("rat.writeColumn(ratDataset, \"Green\", green)\n")
    outFile.write("rat.writeColumn(ratDataset, \"Blue\", blue)\n")
    outFile.write("rat.writeColumn(ratDataset, \"Alpha\", alpha)\n")
    outFile.flush()
    outFile.close()


################################################
#
# YOU NEED TO UPDATE THESE VARIABLES!!!
#
################################################
csvFilePath = "/Users/pete/Desktop/Colour_scheme_LCCS-1_updated.csv"
outFilePath = "/Users/pete/Desktop/test_output.py"
inRatFilePath = "/some/random/file.kea"

# Read CSV file
colourParams = readCSVFile(csvFilePath)
# Generate the python script to colour the classes
generateColourPy(outFilePath, colourParams, inRatFilePath)
    
    
