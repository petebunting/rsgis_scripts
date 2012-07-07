###################################
# TopoCorrect1_5.py               #
# A python script to loop through #
# ALOS scenes and topographically #
# correct using existing script   #
# Dan Clewley                     #
# 23/05/2011                      #
###################################  

import os.path
import sys

inDIR = sys.argv[1]

dirList = os.listdir(inDIR)

for directory in dirList:
    if os.path.isdir(os.path.join(inDIR,directory)):
        os.chdir(os.path.join(inDIR,directory))
        replaceCMD = "sed 's/lev1/lev1_5/g' TopoCorrect.csh > TopoCorrect_1_5.csh"
        os.system(replaceCMD)
        runCMD = 'csh TopoCorrect_1_5.csh'
        os.system(runCMD)