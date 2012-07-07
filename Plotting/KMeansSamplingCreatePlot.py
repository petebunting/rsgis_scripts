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

def readCSVFile(inFile, b1List, b2List, b3List, b4List):
    line = 0
    inFile.seek(0)
    for eachLine in inFile:
        eachLine = eachLine.strip()
        if eachLine != "":
            split = eachLine.split(',', eachLine.count(','))
            if line == 2:
                for val in split:
                    b1List.append(float(val))
            elif line == 3:
                for val in split:
                    b2List.append(float(val))
            elif line == 4:
                for val in split:
                    b3List.append(float(val))
            elif line == 5:
                for val in split:
                    b4List.append(float(val))

        line = line + 1


centresFileSampling1 = "KMeansCentresResample0.gmtxt"
centresFileSampling10 = "KMeansCentresResample10.gmtxt"
centresFileSampling100 = "KMeansCentresResample100.gmtxt"


centresSampling1_B1 = list()
centresSampling1_B2 = list()
centresSampling1_B3 = list()
centresSampling1_B4 = list()

centresSampling10_B1 = list()
centresSampling10_B2 = list()
centresSampling10_B3 = list()
centresSampling10_B4 = list()

centresSampling100_B1 = list()
centresSampling100_B2 = list()
centresSampling100_B3 = list()
centresSampling100_B4 = list()


try:
    sample1File = open(centresFileSampling1.strip(), 'r')
    readCSVFile(sample1File, centresSampling1_B1, centresSampling1_B2, centresSampling1_B3, centresSampling1_B4)
    sample1File.close()

    sample10File = open(centresFileSampling10.strip(), 'r')
    readCSVFile(sample10File, centresSampling10_B1, centresSampling10_B2, centresSampling10_B3, centresSampling10_B4)
    sample10File.close()

    sample100File = open(centresFileSampling100.strip(), 'r')
    readCSVFile(sample100File, centresSampling100_B1, centresSampling100_B2, centresSampling100_B3, centresSampling100_B4)
    sample100File.close()
except IOError, e:
    print '\nCould not open file:\n', e
    sys.exit()

print "centresSampling1_B1: ", centresSampling1_B1
print "centresSampling1_B2: ", centresSampling1_B2
print "centresSampling1_B3: ", centresSampling1_B3
print "centresSampling1_B4: ", centresSampling1_B4
print "\n"
print "centresSampling10_B1: ", centresSampling10_B1
print "centresSampling10_B2: ", centresSampling10_B2
print "centresSampling10_B3: ", centresSampling10_B3
print "centresSampling10_B4: ", centresSampling10_B4
print "\n"
print "centresSampling100_B1: ", centresSampling100_B1
print "centresSampling100_B2: ", centresSampling100_B2
print "centresSampling100_B3: ", centresSampling100_B3
print "centresSampling100_B4: ", centresSampling100_B4


axOutRange = list()
axOutRange.append(0)
axOutRange.append(255)
axOutRange.append(0)
axOutRange.append(255)

fig = plt.figure(figsize=(12, 12), dpi=80)

ax1 = fig.add_subplot(2,2,1)

sample1Scatter = ax1.scatter(centresSampling1_B3, centresSampling1_B2, c='k', marker='o')
sample10Scatter = ax1.scatter(centresSampling10_B3, centresSampling10_B2, c='k', marker='*')
sample100Scatter = ax1.scatter(centresSampling100_B3, centresSampling100_B2, c='k', marker='^')

ax1.set_title("KMeans Sampling Tests (NIR-RED)")
ax1.set_xlabel("Stretched NIR")
ax1.set_ylabel("Stretched Red")

ax1.axis(axOutRange)

ax2 = fig.add_subplot(2,2,2)

ax2.scatter(centresSampling1_B3, centresSampling1_B1, c='k', marker='o')
ax2.scatter(centresSampling10_B3, centresSampling10_B1, c='k', marker='*')
ax2.scatter(centresSampling100_B3, centresSampling100_B1, c='k', marker='^')

ax2.set_title("KMeans Sampling Tests (NIR-Green)")
ax2.set_xlabel("Stretched NIR")
ax2.set_ylabel("Stretched Green")

ax2.axis(axOutRange)


ax3 = fig.add_subplot(2,2,3)

ax3.scatter(centresSampling1_B3, centresSampling1_B4, c='k', marker='o')
ax3.scatter(centresSampling10_B3, centresSampling10_B4, c='k', marker='*')
ax3.scatter(centresSampling100_B3, centresSampling100_B4, c='k', marker='^')

ax3.set_title("KMeans Sampling Tests (NIR-SWIR)")
ax3.set_xlabel("Stretched NIR")
ax3.set_ylabel("Stretched SWIR")

ax3.axis(axOutRange)


ax4 = fig.add_subplot(2,2,4)

ax4.scatter(centresSampling1_B4, centresSampling1_B2, c='k', marker='o')
ax4.scatter(centresSampling10_B4, centresSampling10_B2, c='k', marker='*')
ax4.scatter(centresSampling100_B4, centresSampling100_B2, c='k', marker='^')

ax4.set_title("KMeans Sampling Tests (SWIR-Red)")
ax4.set_xlabel("Stretched SWIR")
ax4.set_ylabel("Stretched Red")

ax4.axis(axOutRange)



pointSymbols = [sample1Scatter,sample10Scatter,sample100Scatter]
labels = ["Sample 1", "Sample 10","Sample 100"]

plt.figlegend(pointSymbols, labels, 'upper right')

plt.savefig("Figure2_KMeansSampling.pdf", format='PDF')

#plt.show()

