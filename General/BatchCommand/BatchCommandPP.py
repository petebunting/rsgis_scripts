#! /usr/bin/env python

#######################################
# BatchCommand.py
# A command to batch commands for all
# Files in a directory with a given extension
# Dan Clewley
# 19/02/2012
#######################################

import os, sys, optparse, subprocess, pp

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
        print stdout

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


# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-c","--command", dest="command", default=None, help="Command line to use, last two inputs of the command should be left blank for input and output file")
    p.add_option("-e","--ext", dest="extension", default=None, help="Input file extension (e.g., \'env\')") 
    p.add_option("-s","--suffix", dest="suffix", default=None, help="Suffix for output files, including extension (e.g., \'_tif.tif\')")
    p.add_option("-i","--inputDIR", dest="inDIR", default=None, help="Input directory. Can use '.' for current directory")
    p.add_option("-o","--outputDIR", dest="outDIR", default=None, help="Output directory. Can use '.' for current directory")
    p.add_option("-r","--reverse", dest="reverse", default=False, help="Reverse - command takes output first, then input")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.command is None:
        p.print_help()
        print "Command must be set"
        sys.exit()

    if self.extension is None:
        p.print_help()
        print "Extension must be set"
        sys.exit()

    if self.suffix is None:
        p.print_help()
        print "Suffix must be set"
        sys.exit()

    if self.inDIR is None:
        p.print_help()
        print "Input directory must be set"
        sys.exit()

    if self.outDIR is None:
        p.print_help()
        print "Output directory must be set"
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = BatchRunCommand()
    obj.runCommand(cmdargs.command, cmdargs.inDIR, cmdargs.outDIR, cmdargs.extension, cmdargs.suffix, cmdargs.reverse)
