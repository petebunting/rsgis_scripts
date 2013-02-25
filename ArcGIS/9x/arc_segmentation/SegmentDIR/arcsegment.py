#####################################################
## NAME: arcsegment
## Source Name: arcsegment.py
## Author: Peter Bunting
## Email: pjb00@aber.ac.uk
## Usage: 
## Description:  
## Date: 22 June 2007
## Updated: 22 June 2007
#####################################################

import sys
import os
import string
import imghdr
import Image
import win32com.client

gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
gp.AddMessage('Started got GP')

segmentLocation = gp.GetParameterAsText(0)
sigma = gp.GetParameterAsText(1)
k = gp.GetParameterAsText(2)
min = gp.GetParameterAsText(3)
inputDIR = gp.GetParameterAsText(4)
outputDIR = gp.GetParameterAsText(5)
tmpDIR = gp.GetParameterAsText(6)

gp.AddMessage('segmentLocation: '+segmentLocation)
gp.AddMessage('sigma: '+sigma)
gp.AddMessage('k: '+k)
gp.AddMessage('min: '+min)
gp.AddMessage('inputDIR: '+inputDIR)
gp.AddMessage('outputDIR: '+outputDIR)
gp.AddMessage('tmpDIR: '+tmpDIR)

gp.AddMessage('Working directory: '+inputDIR)
fileList = os.listdir(inputDIR)
gp.AddMessage(str(fileList))
for filename in fileList:
	gp.AddMessage('filename: '+filename)
	filenameSplit = filename.split('.', 2)
	gp.AddMessage('filenameSplit: '+str(filenameSplit))
	if len(filenameSplit) == 2:
		if filenameSplit[1] == 'jpg':
			gp.AddMessage('SEGMENT!')
			imageFile = inputDIR+filename
			gp.AddMessage('Converting Image!')
			im = Image.open(inputDIR+'\\'+filename)
			im.save(tmpDIR+'\\tmp.ppm', 'ppm')
			imageFile = tmpDIR + '\\tmp.ppm'
			command = segmentLocation + '\\segment ' + str(sigma) + ' ' + str(k) + ' ' + str(min) + ' ' + imageFile + ' ' + tmpDIR+'\\tmp_output.ppm'
			gp.AddMessage('Running: ' + command)
			os.system(command)
			gp.AddMessage('Finished Segmentation..')
			outFileName = outputDIR + '\\' + filenameSplit[0] + '_segment.png'
			gp.AddMessage('Output File Name: ' + outFileName)
			im = Image.open(tmpDIR+'\\tmp_output.ppm')
			im.save(outFileName)
			os.remove(tmpDIR+'\\tmp_output.ppm')
			os.remove(tmpDIR+'\\tmp.ppm')

