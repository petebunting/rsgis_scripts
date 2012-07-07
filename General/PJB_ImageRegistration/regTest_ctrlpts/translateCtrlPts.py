#! /usr/bin/env python

import math

image1StartX = 0.0
image1StartY = 0.0
image2StartX = 0.0
image2StartY = 0.0
xStep = 20.0
yStep = 20.0
image1EndX = 497.0
image1EndY = 150.0
image2EndX = 500.0
image2EndY = 150.0
image1CurrentX = image1StartX + xStep
image1CurrentY = image1StartY + yStep
image2CurrentX = image2StartX + xStep
image2CurrentY = image2StartY + yStep


outputFile = '/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_16x18y_correct_LiDAR_ctrlpts.pts'
#outputFile = '/Users/pete/Desktop/Registration_Tests/tmpCtrl_pts/output_ctrl_pts.pts'

outFile = open(outputFile, 'w')
newline = str('\n')
tab = str('\t')

comment = '; Output control points '
outFile.write(str(comment))
outFile.write(newline)

while image1CurrentY < image1EndY:
	
	while image1CurrentX < image1EndX:
		outStr = tab
		outStr = outStr + str(image1CurrentX)
		outStr = outStr + tab
		outStr = outStr + str(image1CurrentY)
		outStr = outStr + tab
		outStr = outStr + str(image2CurrentX)
		outStr = outStr + tab
		outStr = outStr + str(image2CurrentY)
		
		outFile.write(outStr)
		outFile.write(newline)
		image1CurrentX = image1CurrentX + xStep + 1
		image2CurrentX = image2CurrentX + xStep + 1
		
	image1CurrentY = image1CurrentY + yStep + 1
	image2CurrentY = image2CurrentY + yStep + 1
	image1CurrentX = image1StartX + xStep
	image2CurrentX = image2StartX + yStep
	
