# check_running_vms.py
# A script to check running VirtualBox machines and restart
# machines if they are not running.
#
# 21/12/2012 - Dan Clewley (clewley@usc.edu)
#

import os, sys
import subprocess

machineCheckList = ['Windows XP']

def findMachine(machine, outList):
    ''' Search for machine in list of running Virtual
machines'''
    foundMachine = False
    for outLine in outList:
        if outLine.find('"' + machine + '"') > -1:
            foundMachine = True

    return foundMachine


command = 'VBoxManage list runningvms' # Command to check for running machines
out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(stdout, stderr) = out.communicate()
runningList = stdout.split('\n') # Convert to list (item for each line)


for machine in machineCheckList: # Iterate through machines in check list
    if findMachine(machine, runningList) == True:
        print machine + ' is running'
    else:
        # If machine is not running, start
        print machine + ' is not running, starting now'
        startCommand = 'VBoxManage startvm ' + '"' + machine + '"'
        out = subprocess.Popen(startCommand,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        print stdout
