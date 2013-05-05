#! /usr/bin/env python

#######################################
# BatchCommand.py
# A command to batch commands for all
# Files in a directory with a given extension
# Dan Clewley
# 19/02/2012
#######################################

import os, sys, argparse, subprocess

try:
    import pp
except ImportError:
    print('ERROR: ParallelPython module is not accessible. Use BatchCommand.py instead')
    exit()

class BatchRunCommand (object):
    def findExtension(self, filename, ext):
        count = filename.count('.')
        if ext == '' and count == 0:
            return True
        elements = filename.split('.',count)
        if elements[count] == ext:
            return True
        else:
            return False

    def runSingleCommand(self, command):
        import subprocess
        out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        print(stdout)
        print(stderr)

    def runCommand(self, command, inDIR, outDIR, ext, suffix, reverse):
        job_server = pp.Server()
        filelist = []
        fileList = os.listdir(inDIR)
        jobs = []
        
        for fileName in fileList:
            inFile = fileName
            if self.findExtension(fileName, ext):
                baseFile = os.path.splitext(fileName)[0]
                if ext == '.hdr':
                    inFile = baseFile
                inFilePath = os.path.join(inDIR,inFile)
                outFilePath = os.path.join(outDIR,baseFile + suffix)
                if reverse:
                    fullCommand = command + ' \"' + outFilePath + '\" \"' + inFilePath + '\"'
                else:  
                    fullCommand = command + ' \"' + inFilePath + '\" \"' + outFilePath + '\"'
                jobs.append(job_server.submit(self.runSingleCommand,(fullCommand,),modules=("subprocess",)))
        for job in jobs:
            job()  


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-c","--command", type=str, dest="command", default=None, help="Command line to use, last two inputs of the command should be left blank for input and output file")
    p.add_argument("-e","--ext", dest="extension", default=None, help="Input file extension (e.g., \'env\')") 
    p.add_argument("-s","--suffix", dest="suffix", default=None, help="Suffix for output files, including extension (e.g., \'_tif.tif\')")
    p.add_argument("-i","--inputDIR", dest="inDIR", default=None, help="Input directory. Can use '.' for current directory")
    p.add_argument("-o","--outputDIR", dest="outDIR", default=None, help="Output directory. Can use '.' for current directory")
    p.add_argument("-r","--reverse", dest="reverse", default=False, help="Reverse - command takes output first, then input")
    cmdargs = p.parse_args()

    if cmdargs.command is None:
        print("Command must be set")
        p.print_help()
        sys.exit()

    if cmdargs.extension is None:
        print("Extension must be set")
        p.print_help()
        sys.exit()

    if cmdargs.suffix is None:
        print("Suffix must be set")
        p.print_help()
        sys.exit()

    if cmdargs.inDIR is None:
        print("Input directory must be set")
        p.print_help()
        sys.exit()

    if cmdargs.outDIR is None:
        print("Output directory must be set")
        p.print_help()
        sys.exit()
