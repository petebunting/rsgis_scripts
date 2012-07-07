#! /usr/bin/env python

################################
# A python script to loop through a directory create ENVI
# header files
# Author: Dan Clewley 
# Email: ddc06@aber.ac.uk
# Date 13/11/2008
###############################

import os, sys, string
from CreateSARQuickLook import CreateQuickLook

processdir = list()
dir = sys.argv[1]

dirlist = os.listdir(dir)

for dirname in dirlist:
	if dirname[0:4] == 'alps':
		processdir.append(dirname)

for processname in processdir:
	processdirpath = dir + '/' + processname + '/'

	obj = CreateQuickLook()
	obj.run(processdirpath, processdirpath, 'utm')
