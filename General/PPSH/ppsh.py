#!/usr/bin/env python

#####################################################
# Parallel Python Shell Script                      #
# Reads a list of commands and excecutes            #
# on multiple cores using Parallel python           #
# http://www.parallelpython.com/                    #
#                                                   #
# Known Issues:                                     #
# The output of the command will only be printed    #
# after the command has excecuted                   #
#                                                   #
# Dan Clewley 18/01/12                              #
#                                                   #
#####################################################

import pp, subprocess, sys

numArgs = len(sys.argv)
if numArgs >= 3:
    commandFile = sys.argv[1]
    nCores = int(sys.argv[2].strip())
    job_server = pp.Server(nCores)

elif numArgs == 2:
    commandFile = sys.argv[1]
    job_server = pp.Server()
else:
    print '''Parallel Python Shell Script
Usage:
    ppsh <script.sh> <nCores>
'''
    exit()

commandList = open(commandFile,'r')

def runCommand(command):
    out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (stdout, stderr) = out.communicate()
    print stdout

jobs = []

for command in commandList:
    jobs.append(job_server.submit(runCommand,(command,),modules=("subprocess",)))

for job in jobs:
    job()

