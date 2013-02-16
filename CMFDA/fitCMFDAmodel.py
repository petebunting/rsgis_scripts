#######################################################
# A python script to fit the model Continuous Monitoring 
# of Forest Disturbance Algorithm (CMFDA) model proposed in:
# Zhu, Z., Woodcock, C.E. & Olofsson, P., 2012. 
# Continuous monitoring of forest disturbance using all 
# available Landsat imagery. 
# Remote Sensing of Enviroment, 122, pp.75-91
#
# Dan Clewley (daniel.clewley@gmail.com) - 14/02/2013
#
#######################################################

import os, sys
import numpy as np
import matplotlib.pyplot as plt

# Set T (number of days in a year)
T = 365
# Calculate 2 pi / T
twoPiDivT = 2 * np.pi / T

def annualCos(doy, year, i):
    """ Calculates a1 ... aN terms
        Returns an array with values where year == i
        0 where year != i """
    return np.where(year == i, np.cos(1./i * twoPiDivT * doy), 0)
    
def annualSin(doy, year, i):
    """ Calculates b1 ... bN terms
        Returns an array with values where year == i
        0 where year != i """
    return np.where(year == i, np.sin(1./i * twoPiDivT * doy), 0)

def bimodalCos(doy):
    # aN+1 term
    return np.cos(2 * twoPiDivT * doy)

def bimodalSin(doy):
    # bN+1 term
    return np.sin(2 * twoPiDivT * doy)

# Read in data
if len(sys.argv) != 3:
    print ''' Not enough parameters provided.
Usage:
    python fitCMFDAmodel.py inTextFile.csv outPlotFile.pdf
'''
    exit()
    
inTextFile = sys.argv[1]
outPlotFile = sys.argv[2]

inData = np.genfromtxt(inTextFile, delimiter=",",skip_header=1)

# Set data start year
startYear = 2000 

# Scale NDVI
ndvi = inData[:,2] / 10000.

# Set first year to 1
yearN = inData[:,1] - (startYear - 1)

day = inData[:,0] + ((yearN - 1) * 365)
doy = inData[:,0] 

""" 
    Set up model in the matrix form:
    A x = b
    
    Where:
    - b is a vector of the NDVI
    - A is matrix of the sin and cos terms of the model    
    - x is the vector of coefficients, to be found. 
"""

modelTerms = []

a0Term = inData[:,1] / inData[:,1] # 1
modelTerms.append(a0Term)

# Calculate interanual terms
for i in range(int(max(yearN))):
    aiTerm = annualCos(doy, yearN, i+1)
    biTerm = annualSin(doy, yearN, i+1)
    
    modelTerms.append(aiTerm)
    modelTerms.append(biTerm)

# Bimodal variation terms
anTerm = bimodalCos(doy)
bnTerm = bimodalSin(doy)

modelTerms.append(anTerm)
modelTerms.append(bnTerm)

# Solve A x = b to give x
b = ndvi
A = np.array(modelTerms).T
x = np.linalg.lstsq(A, b)[0]

print "Coefficients: "
print x

predictNDVI = np.dot(A, x)

# Plot the data
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111)
ax.set_xlabel('Total day')
ax.set_ylabel('NDVI')
plt.plot(day, ndvi, 'o', label='Original data', markersize=5)
plt.plot(day, predictNDVI, 'r', label='Fitted line')
plt.legend()
plt.savefig(outPlotFile, format='PDF')



