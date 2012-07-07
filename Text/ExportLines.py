 #! /usr/bin/env python

#######################################
# A python script for exporting selected
# lines of a text file.
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 01/12/2011
# Version: 1.0
#######################################

from time import localtime, strftime
import os, sys, optparse


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def main(cmdargs):
    print "Input File: \'", cmdargs.inputFile.strip(), "\'"
    print "Output File: \'", cmdargs.outputFile.strip(), "\'"

    numLines = file_len(cmdargs.inputFile.strip())

    print "Num Lines: ", numLines

    # Open input file
    inFileObj = open(cmdargs.inputFile.strip(), 'r')
    # Open file for output
    outFileObj = asciiObj = open(cmdargs.outputFile, 'w')

    start = 0
    end = numLines

    if not cmdargs.start == None:
        start = int(cmdargs.start)
        if start >= numLines:
            print "Start needs to be less than the number of point."
            sys.exit()

    if not cmdargs.end == None:
        end = int(cmdargs.end)
        if end > numLines:
            numInt = numLines

    if start > end:
        print "Start needs to be less than the end."
        sys.exit()

    print "start: ", start
    print "end: ", end

    if cmdargs.first:
        print "Including header line"

    for i, line in enumerate(inFileObj):
        if cmdargs.first and (i == 0):
            outFileObj.write(line)
        elif i > end:
            break
        elif i >= start:
            outFileObj.write(line)


    inFileObj.close()
    outFileObj.close()




# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--inputFile", dest="inputFile", default=None, help="Input file ASC.")
    p.add_option("-o","--outputFile", dest="outputFile", default=None, help="Output XYZI file.")
    p.add_option("-s","--start", dest="start", default=None, help="Start point to be processed.")
    p.add_option("-e","--end", dest="end", default=None, help="End point to be processed.")
    p.add_option("-f", "--first", action="store_true", dest="first", default=False, help="Include first line in output (i.e., header).")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if (self.inputFile is None) or (self.outputFile is None):
        p.print_help()
        print "Input and output filenames must be set."
        sys.exit()


# Run the script
if __name__ == "__main__":
    print strftime("Start: %a, %d %b %Y %H:%M:%S", localtime())
    cmdargs = CmdArgs()
    main(cmdargs)
    print strftime("End: %a, %d %b %Y %H:%M:%S", localtime())

