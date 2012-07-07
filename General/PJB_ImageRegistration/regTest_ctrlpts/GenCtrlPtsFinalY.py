#! /usr/bin/env python

import math

image1StartX = 0.0
image1StartY = 0.0
image2StartX = 9.0
image2StartY = 38.0
xStep = 8.0
yStep = 8.0
image1EndX = 500.0
image1EndY = 150.0
image2EndX = 508.0
image2EndY = 187.0
amplitude = 5
frequency = (math.pi / (image2EndY-image2StartY))*2
image1CurrentX = image1StartX
image1CurrentY = image1StartY
image2CurrentX = image2StartX
image2CurrentY = image2StartY
image2OutputX = 0.0

outputFile = '/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/AIRSARLiDAR_p142_Ynonlinear_ctrlpts.pts'
#outputFile = '/Users/pete/Desktop/Registration_Tests/tmpCtrl_pts/outputY_ctrl_pts.pts'

outFile = open(outputFile, 'w')
newline = str('\n')
tab = str('\t')

comment = '; Output control points '
outFile.write(str(comment))
outFile.write(newline)

while image1CurrentY < image1EndY:
	image2OutputX = amplitude * math.sin((image2CurrentY*frequency))
	while image1CurrentX < image1EndX:
		outStr = tab
		outStr = outStr + str(image1CurrentX)
		outStr = outStr + tab
		outStr = outStr + str(image1CurrentY)
		outStr = outStr + tab
		outStr = outStr + str((image2OutputX + image2CurrentX))
		outStr = outStr + tab
		outStr = outStr + str(image2CurrentY)
		
		outFile.write(outStr)
		outFile.write(newline)
		image1CurrentX = image1CurrentX + xStep
		image2CurrentX = image2CurrentX + xStep
	
	image1CurrentY = image1CurrentY + yStep
	image2CurrentY = image2CurrentY + yStep
	image1CurrentX = image1StartX
	image2CurrentX = image2StartX
	
