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
useRLM = True
try:
    import statsmodels.api as sm
except ImportError:
    useRLM = False
    
debugMode = False # Should log files be produced.
    
# Set T (number of days in a year)
T = 365
# Calculate 2 pi / T
twoPiDivT = 2 * np.pi / T
def annualCos(doy, year, i):
    """ Calculates a1 ... aN terms
        Returns an array with values where year == i
        0 where year != i """
    return np.cos(1./i * twoPiDivT * doy)
    
def annualSin(doy, year, i):
    """ Calculates b1 ... bN terms
        Returns an array with values where year == i
        0 where year != i """
    return np.sin(1./i * twoPiDivT * doy)
    
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
# Day used for plotting
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
# Subset data here
fitStartYear = 1
condition = np.logical_or(yearN == fitStartYear, yearN == fitStartYear+1)

yearNTrain = np.extract(condition, yearN)
doyTrain = np.extract(condition, doy)
dayTrain = np.extract(condition, day)
ndviTrain = np.extract(condition, ndvi)

# FITTING STARTS HERE
modelTerms = []
a0Term = yearNTrain / yearNTrain # 1
#print 'a0Term = ', a0Term
modelTerms.append(a0Term)
# Calculate interanual terms, use a subset here
#for i in range(int(max(yearNTrain))):
for i in range(1):
    #print 'yearN = ', yearN
    aiTerm = annualCos(doyTrain, yearNTrain, i+1)
    biTerm = annualSin(doyTrain, yearNTrain, i+1)
    #print 'aiTerm = ', aiTerm
    modelTerms.append(aiTerm)
    modelTerms.append(biTerm)
# Bimodal variation terms
anTerm = bimodalCos(doyTrain)
bnTerm = bimodalSin(doyTrain)
modelTerms.append(anTerm)
modelTerms.append(bnTerm)

# Solve A x = b to give x
b = ndviTrain
A = np.array(modelTerms).T

if useRLM == True:
    print "Robust fitting"
    rlmmodel = sm.RLM(b, A, M=sm.robust.norms.HuberT())
    rlmResults = rlmmodel.fit()
    x = rlmResults.params
else:
    x = np.linalg.lstsq(A, b)[0]
    
# FITTING ENDS HERE
# Coefficients - 
print "Coefficients: "
print x

predictNDVI = np.dot(A, x)
if debugMode:
    np.savetxt('predictNDVI.csv',predictNDVI, delimiter=',')

# Subset testing data
condition = (yearN == fitStartYear+2)

yearNTest = np.extract(condition, yearN)
doyTest = np.extract(condition, doy)
dayTest = np.extract(condition, day)
ndviTest = np.extract(condition, ndvi)

# Loop through + 1 year of data
predictNDVI2 = []
sumSq = 0

nTestDays = doyTest.shape[0]

for i in range(nTestDays):    
    pNDVI = x[0] + (x[1] * (np.cos(twoPiDivT * doyTest[i]))) + ( x[2] * (np.sin(twoPiDivT * doyTest[i]) )) + (x[-2] * np.cos(2 * twoPiDivT * doyTest[i])) + (x[-1] * np.sin(2 * twoPiDivT * doyTest[i]))

    predictNDVI2.append(pNDVI)

    sumSq = (ndviTest[i] - predictNDVI2)**2

rmse = np.sqrt(np.average(sumSq))

print 'RMSE = ' + str(rmse)

if debugMode:
    np.savetxt('predictNDVI2.csv',predictNDVI2, delimiter=',')

if debugMode:
    np.savetxt('ndviTest.csv',ndviTest, delimiter=',')

# Plot the data
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111)
ax.set_xlabel('Total day')
ax.set_ylabel('NDVI')
plt.plot(np.append(dayTrain,dayTest), np.append(ndviTrain,ndviTest), 'o', label='Original data', markersize=5)
plt.plot(dayTrain, predictNDVI, 'r', label='Fitted line')
plt.plot(dayTest, predictNDVI2, 'r--', label='Predicted NDVI')
plt.legend(loc=8, ncol=3)
plt.savefig(outPlotFile, format='PDF')