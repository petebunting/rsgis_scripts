#! /usr/bin/env python

################################
# A python script to loop through a directory create ENVI
# header files
# For Lat-Long Coordinates
# Author: Dan Clewley 
# Email: ddc06@aber.ac.uk
# Date 13/11/2008
###############################

import os
import sys
import string
from GenerateENVIHeaderLatLong import GenerateENVIHeader

processdir = list()
dir = sys.argv[1]

dirlist = os.listdir(dir)

for dirname in dirlist:
	if dirname[0:3] == 'alp':
		processdir.append(dirname)
	
for processname in processdir:
	processdirpath = dir + '/' + processname + '/l1data/'
	
	obj = GenerateENVIHeader()		
	obj.run('spatial', processdirpath, '.utm')
