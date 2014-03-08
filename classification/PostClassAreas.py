#!/usr/bin/env python
#
# PostClassAreas.py
# 
# Daniel Clewley (daniel.clewley@gmail.com)
# 19/20/2014
#

import numpy as np
from pandas.io.parsers import read_csv
import pandas
import argparse

scriptDescription = '''Adjusts areas based pixel counts using the confusion matrix to
provide an unbiased estimate of area within each class.

Uses the techique described in:

Tenenbein, A. A double sampling scheme for estimating from misclassified multinomial data
with applications to sampling inspection. Technometrics, 14, 187–202.

Confusion matrix is assumed to have observed values as rows and predicted values as columns (default from randomForest in R). Pass in the transpose flag if observed values are columns. Format is a CSV file with no header or row labels.

Areas is a CSV file, with no header, containing the following information:

Class,area

Area can be pixel count or any units.

'''

parser = argparse.ArgumentParser(description=scriptDescription)
parser.add_argument("-c", "--confusionmatrix", type=str, required=True, help="Confusion matrix")
parser.add_argument("-a", "--areas", type=str, required=True, help="Areas for each class")
parser.add_argument("-o", "--out", type=str, required=False, default=None, help="Output file for adjusted areas")
parser.add_argument("-t", "--transpose", action='store_true', required=False, default=False, help="Transpose matrix, required if prediced class is rows (default is columns).")

args = parser.parse_args()   

# Read data into numpy arrays
confusionMatrixFile = args.confusionmatrix
areasFile = args.areas

confusionMatrix = np.genfromtxt(confusionMatrixFile, delimiter=',')
areasDF = read_csv(areasFile, sep=',',header=None, names=['Class','Area'])

# Transpose matrix if needed
if args.transpose:
    confusionMatrix = confusionMatrix.transpose()

# Create seperate array for areas
areas = areasDF['Area']
areas = areas.astype(float)

if areas.shape[0] != confusionMatrix.shape[1]:
    raise Exception("Must have the same number of classes \
    in areas and confusion matrix")

origAreas = np.zeros_like(areas)
adjustedAreas = np.zeros_like(areas)
totalArea = areas.sum()

for i in range(areas.shape[0]):

    pi_i = 0
    for j in range(areas.shape[0]):
        p_j = areas[j]

        n_j = confusionMatrix[:,j].sum()
        n_ij = confusionMatrix[i,j]

        pi_i += (p_j * (n_ij / n_j))
    
    adjustedAreas[i] = pi_i

    origAreas[i] = areas[i]

print('Check areas are equal:')
print('Origional: ', origAreas.sum())
print('Adjusted: ', adjustedAreas.sum())
    
printAreas = pandas.DataFrame({'Class Name' : areasDF['Class'], 'Original': origAreas,'Adjusted' : adjustedAreas})
 
print(printAreas)

if args.out is not None:
    print('\nSaving to: ',args.out)
    printAreas.to_csv(args.out, sep=',',index=False)



