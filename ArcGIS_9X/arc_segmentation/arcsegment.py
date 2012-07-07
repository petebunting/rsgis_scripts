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

import segment
import win32com.client

gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

usrSegmentDIR = sys.argv[1]
usrSigma = sys.argv[2]
usrK = sys.argv[3]
usrMin = sys.argv[4]
usrInputDIR = sys.argv[5]
usrOutputDIR = sys.argv[6]
tmpOutputDIR = sys.argv[7]

outputArcObj = outputArc()
segmentObj = segment()
segmentObj.segmentDir(usrSegmentDIR, 
                      usrSigma, 
                      usrK,
                      usrMin, 
                      usrInputDIR,
                      usrOutputDIR,
                      tmpOutputDIR,
                      outputArcObj)

class outputArc (object):

	def printMessage(self, outText):
    	gp.AddMessage(outText)