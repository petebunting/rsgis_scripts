#! /usr/bin/env python

############################################################################
# Copyright (c) 2013 Dr. Peter Bunting, Aberystwyth University
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
# Purpose:  A class to submit jobs to loadleveler
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 19/04/2013
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

class Submit2Loadleveler (object):
    
    def startWithHash(self, line):
        foundHash = False
        for i in range(len(line)):
            if line[i] == '#':
                foundHash = True
        return foundHash
    
    def createOutputFiles(self, inputFile, outputBase, memory, time, name):
        inputFileList = open(inputFile, 'r')
        outFileCount = 1
        for eachLine in inputFileList:
            if (eachLine.strip() != "") and (not self.startWithHash(eachLine)):
                outFile = open(outputBase + str("_") + str(outFileCount) + str(".ll"), 'w')
                
                outFile.write("#@ class = default\n")
                outFile.write("#@ group = nesi\n")
                outFile.write("#@ notification = never\n")
                outFile.write("#@ account_no = landcare\n")
                outFile.write("#@ wall_clock_limit = " + time + "\n");
                outFile.write("#@ resources = ConsumableMemory(" + memory + "mb) ConsumableVirtualMemory(" + memory + "mb)\n")
                outFile.write("#@ job_type = serial\n")
                outFile.write("#@ job_name = " + name + "_" + str(outFileCount) + str("\n"))
                outFile.write("#@ output = $(job_name).$(jobid).$(stepid).out\n")
                outFile.write("#@ error = $(job_name).$(jobid).$(stepid).err\n")
                outFile.write("#@ environment = COPY_ALL\n")
                outFile.write("#@ queue\n\n")
                
                outFile.write("ulimit -v " + str(int(memory)*1024)  + " -m " + str(int(memory)*1024)  + "\n\n")
                
                outFile.write(eachLine)
                
                outFile.write("\n\n")
                
                outFile.flush()
                outFile.close()
                
                command = str("llsubmit ") + outputBase + str("_") + str(outFileCount) + str(".ll")
                print(command)
                os.system(command)
                outFileCount+=1
            
    
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", dest="inputFile", type=str, help="Input list of commands (1 per line)")
        parser.add_argument("-o", "--output", dest="outputFileBase", type=str, help="Output base name and path")
        parser.add_argument("-m", "--memory", dest="memoryMbs", type=str, help="The amount of memory in MBs.")
        parser.add_argument("-t", "--time", dest="timeMins", type=str, help="The time limit for the jobs.")
        parser.add_argument("-n", "--name", dest="processName", type=str, help="The name of the process.")

        args = parser.parse_args()    

        if args.inputFile is None:
            print("No list of commands has been inputted.")
            parser.print_help()
            sys.exit()
            
        if args.outputFileBase is None:
            print("No output base name and path has been provided.")
            parser.print_help()
            sys.exit()

        if args.memoryMbs is None:
            print("The memory amount must be set.")
            parser.print_help()
            sys.exit()
        
        if args.timeMins is None:
            print("The time (in minutes) must be set.")
            parser.print_help()
            sys.exit()
            
        if args.processName is None:
            print("A process name must be provided.")
            parser.print_help()
            sys.exit()
            
        self.createOutputFiles(args.inputFile, args.outputFileBase, args.memoryMbs, args.timeMins, args.processName)

if __name__ == '__main__':
    obj = Submit2Loadleveler()
    obj.run()
