#! /usr/bin/env python

############################################################################
# Copyright (c) 2012 Pete Bunting, Aberystwyth University
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
# Purpose:  Submit jobs to bsub.
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 02/08/2012
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
#############################################################################

import os.path
import sys
from time import strftime
import argparse

class Submit2QSubPBS (object):
    
    def startWithHash(self, line):
        foundHash = False
        for i in range(len(line)):
            if line[i] == '#':
                foundHash = True
        return foundHash
    
    def createOutputFiles(self, inputFile, outputBase, memory, time, name, workingDIR):
        inputFileList = open(inputFile, 'r')
        outFileCount = 1
        for eachLine in inputFileList:
            if (eachLine.strip() != "") and (not self.startWithHash(eachLine)):
                outFile = open(outputBase + str("_") + str(outFileCount) + str(".pbs"), 'w')
                outFile.write("#!/bin/bash --login\n")            
                outFile.write("#PBS -N " + name + "_" + str(outFileCount) + str("\n"))
                outFile.write("#PBS -e " + name + "_" + str(outFileCount) + str(".err\n"))
                outFile.write("#PBS -o " + name + "_" + str(outFileCount) + str(".log\n"))
                outFile.write("#PBS -l  nodes=1:ppn=1\n")
                outFile.write("#PBS -l vmem=" + str(memory) + str("gb\n"))
                outFile.write("#PBS -l walltime=" + str(time) + str("\n"))
                outFile.write("#PBS -j oe\n\n")
                
                outFile.write("cd " + workingDIR + str("\n\n"))
                
                outFile.write(eachLine)
                
                outFile.write("\n\n")
                
                outFile.flush()
                outFile.close()
                
                command = str("qsub ") + outputBase + str("_") + str(outFileCount) + str(".pbs")
                print(command)
                os.system(command)
                outFileCount+=1
            
    
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", dest="inputFile", type=str, help="Input list of commands (1 per line)")
        parser.add_argument("-o", "--output", dest="outputFileBase", type=str, help="Output base name and path")
        parser.add_argument("-m", "--memory", dest="memoryGbs", type=str, help="The amount of memory in Gbs.")
        parser.add_argument("-t", "--time", dest="time", type=str, help="The time limit for the jobs (HH:MM:ss). 1 hour = 1:00:00.")
        parser.add_argument("-n", "--name", dest="processName", type=str, help="The name of the process.")
        parser.add_argument("-d", "--workdir", dest="workingDIR", type=str, help="The working directory.")
        
        args = parser.parse_args()    

        if args.inputFile is None:
            print("No list of commands has been inputted.")
            parser.print_help()
            sys.exit()
            
        if args.outputFileBase is None:
            print("No output base name and path has been provided.")
            parser.print_help()
            sys.exit()

        if args.memoryGbs is None:
            print("The memory amount must be set.")
            parser.print_help()
            sys.exit()
        
        if args.time is None:
            print("The time (in minutes) must be set.")
            parser.print_help()
            sys.exit()
            
        if args.processName is None:
            print("A process name must be provided.")
            parser.print_help()
            sys.exit()
            
        if args.workingDIR is None:
            print("A working directory must be provided.")
            parser.print_help()
            sys.exit()
            
        self.createOutputFiles(args.inputFile, args.outputFileBase, args.memoryGbs, args.time, args.processName, args.workingDIR)

if __name__ == '__main__':
    obj = Submit2QSubPBS()
    obj.run()
