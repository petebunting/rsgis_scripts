#!/usr/bin/env python
"""
"""

import argparse
import os.path

def findMissingFiles(baseFile, changesFile, outputFile):
    filesDict = dict()
    rBaseFile = open(baseFile, "r")
    for baseLine in rBaseFile:
        baseLine = baseLine.strip()
        baseName = os.path.basename(baseLine)
        #print(baseName)
        filesDict[baseName] = baseLine
    rBaseFile.close()
    
    countMiss = 0
    wOutFile = open(outputFile, 'w')
    rChangesFile = open(changesFile, "r")
    for changeLine in rChangesFile:
        changeLine = changeLine.strip()
        changeName = os.path.basename(changeLine)
        #print(changeName)
        if not changeName in filesDict:
            wOutFile.write(changeLine + '\n')
            countMiss = countMiss + 1
    rChangesFile.close() 
    wOutFile.flush()
    wOutFile.close()
    print("There were " + str(countMiss) + " missing file")

if __name__ == "__main__":
    # Read config file from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', "--base", help="The base file from which the missing will be identified.")
    parser.add_argument('-c', "--changes", help="The file from which the missing will be identified.")
    parser.add_argument('-o', "--output", help="The output file listing the missing file.")
    args = parser.parse_args() 
    
    findMissingFiles(args.base, args.changes, args.output)
    
