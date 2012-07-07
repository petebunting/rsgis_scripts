 #! /usr/bin/env python

#######################################
# A python script to plot deflate tests
# for spdlib paper.
#
# Email: petebunting@mac.com
# Date: 01/02/2012
# Version: 1.0
#######################################

import os.path
import sys
from datetime import datetime,timedelta
from math import *
import optparse
import matplotlib.pyplot as plt
import numpy as np

def readCSVFile(inFile, dataList, col):
	line = 0
	inFile.seek(0)
	for eachLine in inFile:
		eachLine = eachLine.strip()
		if (line != 0) and (eachLine != ""):
			split = eachLine.split(',', eachLine.count(','))
			dataList.append(float(split[col]))
		line = line + 1
		
ptReadFilePath = "PointReadTests.csv"
ptWriteFilePath = "PointWriteTests.csv"
waveReadFilePath = "WaveformReadTests.csv"
waveWriteFilePath = "WaveformWriteTests.csv"

deflateValsList = [0,1,2,3,4,5,6,7,8,9]
readPtTimeList = list()
writePtTimeList = list()
writePtSizeList = list()
readWaveTimeList = list()
writeWaveTimeList = list()
writeWaveSizeList = list()
readShufPtTimeList = list()
writeShufPtTimeList = list()
writeShufPtSizeList = list()
readShufWaveTimeList = list()
writeShufWaveTimeList = list()
writeShufWaveSizeList = list()

try:
	ptReadFile = open(ptReadFilePath.strip(), 'r')
	readCSVFile(ptReadFile, readShufPtTimeList, 1)
	readCSVFile(ptReadFile, readPtTimeList, 2)
	ptReadFile.close()
	
	ptWriteFile = open(ptWriteFilePath.strip(), 'r')
	readCSVFile(ptWriteFile, writeShufPtTimeList, 1)
	readCSVFile(ptWriteFile, writeShufPtSizeList, 2)
	readCSVFile(ptWriteFile, writePtTimeList, 3)
	readCSVFile(ptWriteFile, writePtSizeList, 4)
	ptWriteFile.close()
	
	waveReadFile = open(waveReadFilePath.strip(), 'r')
	readCSVFile(waveReadFile, readShufWaveTimeList, 1)
	readCSVFile(waveReadFile, readWaveTimeList, 2)
	waveReadFile.close()
	
	waveWriteFile = open(waveWriteFilePath.strip(), 'r')
	readCSVFile(waveWriteFile, writeShufWaveTimeList, 1)
	readCSVFile(waveWriteFile, writeShufWaveSizeList, 2)
	readCSVFile(waveWriteFile, writeWaveTimeList, 3)
	readCSVFile(waveWriteFile, writeWaveSizeList, 4)
	waveWriteFile.close()
except IOError, e:
	print '\nCould not open file:\n', e
	sys.exit()

#print deflateValsList
#print readShufPtTimeList
#print readPtTimeList
#print writeShufPtTimeList
#print writeShufPtSizeList
#print writePtTimeList
#print writePtSizeList
#print readShufWaveTimeList
#print readWaveTimeList
#print writeShufWaveTimeList
#print writeShufWaveSizeList
#print writeWaveTimeList
#print writeWaveSizeList

fig = plt.figure(figsize=(12, 12), dpi=80)

ax1_1 = fig.add_subplot(2,2,1)

lineNoShuffle = ax1_1.plot(deflateValsList, writePtTimeList, '-vg')
lineShuffle = ax1_1.plot(deflateValsList, writeShufPtTimeList, '-vb')

ax1_2 = ax1_1.twinx()

lineNoShuffleSize = ax1_2.plot(deflateValsList, writePtSizeList, '-og')
lineShuffleSize = ax1_2.plot(deflateValsList, writeShufPtSizeList, '-ob')

ax1_1.set_title("Write Points")
ax1_1.set_ylabel("Time (s)")

ax1_1Range = ax1_1.axis('tight')
out1_1Range = list()
out1_1Range.append(ax1_1Range[0])
out1_1Range.append(ax1_1Range[1])
out1_1Range.append(0)
out1_1Range.append(8)

ax1_2Range = ax1_2.axis('tight')
out1_2Range = list()
out1_2Range.append(ax1_2Range[0])
out1_2Range.append(ax1_2Range[1])
out1_2Range.append(0)
out1_2Range.append(30)

ax1_1.axis(out1_1Range)
ax1_2.axis(out1_2Range)



ax2_1 = fig.add_subplot(2,2,2)

ax2_1.plot(deflateValsList, writeWaveTimeList, '-vg')
ax2_1.plot(deflateValsList, writeShufWaveTimeList, '-vb')

ax2_2 = ax2_1.twinx()

ax2_2.plot(deflateValsList, writeWaveSizeList, '-og')
ax2_2.plot(deflateValsList, writeShufWaveSizeList, '-ob')

ax2_1.set_title("Write Waveforms")
ax2_2.set_ylabel("Size (MB)")

ax2_1Range = ax2_1.axis('tight')
out2_1Range = list()
out2_1Range.append(ax2_1Range[0])
out2_1Range.append(ax2_1Range[1])
out2_1Range.append(0)
out2_1Range.append(30)

ax2_2Range = ax2_2.axis('tight')
out2_2Range = list()
out2_2Range.append(ax2_2Range[0])
out2_2Range.append(ax2_2Range[1])
out2_2Range.append(20)
out2_2Range.append(100)

ax2_1.axis(out2_1Range)
ax2_2.axis(out2_2Range)



ax3 = fig.add_subplot(2,2,3)

ax3.plot(deflateValsList, readPtTimeList, '-vg')
ax3.plot(deflateValsList, readShufPtTimeList, '-vb')

ax3.set_title("Read Points")
ax3.set_xlabel("Deflate")
ax3.set_ylabel("Time (s)")

ax3Range = ax3.axis('tight')
out3Range = list()
out3Range.append(ax3Range[0])
out3Range.append(ax3Range[1])
out3Range.append(0.5)
out3Range.append(0.75)

ax3.axis(out3Range)


ax4 = fig.add_subplot(2,2,4)

ax4.plot(deflateValsList, readWaveTimeList, '-vg')
ax4.plot(deflateValsList, readShufWaveTimeList, '-vb')

ax4.set_title("Read Waveforms")
ax4.set_xlabel("Deflate")

ax4Range = ax4.axis('tight')
out4Range = list()
out4Range.append(ax4Range[0])
out4Range.append(ax4Range[1])
out4Range.append(1.5)
out4Range.append(4)

ax4.axis(out4Range)


lines = [lineNoShuffle,lineShuffle,lineNoShuffleSize,lineShuffleSize]
labels = ["No Shuffling (s)", "Shuffling (s)","No Shuffling (MB)", "Shuffling (MB)"]

plt.figlegend(lines, labels, 'upper left')

plt.savefig("Figure9_DeflateTests.pdf", format='PDF')

#plt.show()

