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
# Purpose:  Submit jobs to slurm.
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 11/06/2016
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

class CreateSlurmSubScripts (object):
    
    def startWithHash(self, line):
        foundHash = False
        for i in range(len(line)):
            if line[i] == '#':
                foundHash = True
        return foundHash
    
    def createOutputFiles(self, inputFile, outputFile, outputBase, memMbs, time, name, logsPath):
        outCmdsFile = open(outputFile, 'w+')
        logsPath = os.path.abspath(logsPath)
        inputFileList = open(inputFile, 'r')
        outFileCount = 1
        for eachLine in inputFileList:
            if (eachLine.strip() != "") and (not self.startWithHash(eachLine)):
                outFilePath = outputBase + str("_") + str(outFileCount) + str(".slurm")
                outFile = open(outFilePath, 'w')
                outFile.write("#!/bin/bash --login\n")
                outFile.write("#SBATCH --job-name=" + name + "_" + str(outFileCount) + str("\n"))
                outFile.write("#SBATCH --output=" + os.path.join(logsPath, str("%J.out\n")))
                outFile.write("#SBATCH --error=" + os.path.join(logsPath, str("%J.err\n")))
                outFile.write("#SBATCH --mem-per-cpu=" + str(memMbs) + "\n")
                outFile.write("#SBATCH --time=" + time + "\n");
                outFile.write("#SBATCH --ntasks=1\n")
                
                outFile.write(eachLine)
                
                outFile.write("\n\n")
                
                outFile.flush()
                outFile.close()
                
                command = str("sbatch ") + outFilePath
                print(command)
                outCmdsFile.write(command + "\n")
                outFileCount+=1
        outCmdsFile.flush()
        outCmdsFile.close()
            
    
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", dest="inputFile", type=str, help="Input list of commands (1 per line)")
        parser.add_argument("-f", "--outfile", dest="outputFile", type=str, help="Output file which lists the slurm commands.")
        parser.add_argument("-o", "--output", dest="outputFileBase", type=str, help="Output base name and path")
        parser.add_argument("-m", "--memory", dest="memoryMbs", type=str, help="The amount of memory in MBs.")
        parser.add_argument("-t", "--time", dest="timeStr", type=str, help="The time limit for the jobs (D-HH:MM).")
        parser.add_argument("-n", "--name", dest="processName", type=str, help="The name of the process.")
        parser.add_argument("-p", "--path", dest="logsPath", type=str, help="The path where the log files will be outputted.")

        args = parser.parse_args()    

        if args.inputFile is None:
            print("No list of commands has been inputted.")
            parser.print_help()
            sys.exit()
            
        if args.outputFile is None:
            print("No output file destination provided.")
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
        
        if args.timeStr is None:
            print("The time (in minutes) must be set.")
            parser.print_help()
            sys.exit()
            
        if args.processName is None:
            print("A process name must be provided.")
            parser.print_help()
            sys.exit()
            
        self.createOutputFiles(args.inputFile, args.outputFile, args.outputFileBase, args.memoryMbs, args.timeStr, args.processName, args.logsPath)

if __name__ == '__main__':
    obj = CreateSlurmSubScripts()
    obj.run()



