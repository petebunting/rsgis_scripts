#! /usr/bin/env python

import math

startX = 0.0
startY = 0
xStep = 7.0
yStep = 9.0
endX = 1000.0
endY = 1000.0
amplitude = 250.0
frequency = 0.01
currentX = startX
currentY = startY
outputY = 0

outputFile = '/Users/pete/Desktop/outputpts.pts'
outFile = open(outputFile, 'w')
newline = str('\n')

print outFile

while currentX < endX:
	outputY = amplitude * math.sin((currentX*frequency))
	while currentY < endY:
		outVal = currentX, currentY,	currentX, (outputY + currentY)
		outStr = str(outVal)
		outFile.write(outStr)
		outFile.write(newline)
		currentY = currentY + yStep	
	currentX = currentX + xStep
	currentY = startY
	
