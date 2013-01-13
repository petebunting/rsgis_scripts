#!/usr/bin/env python

import sys

# Parameter File
numOfYears = 20
initalAdultPairPop=15
winterSurvivalRate=0.59
averageEggsPerPair=3.64
averageFledgelingsPerPair=2.2
preditorControl=True

# Internal Variables.
numOfAdultsPairs = initalAdultPairPop
numOfFledgelings = 14
numOfFledgelingsYearOld = 8 
numOfEggs = 0

# Timing loop
for year in range(numOfYears):
    numOfAdultsPairs += (numOfFledgelingsYearOld/2)
    numOfFledgelingsYearOld = numOfFledgelings
    
    # Winter Survival
    numOfAdultsPairs=numOfAdultsPairs*0.59
    numOfFledgelingsYearOld=numOfFledgelingsYearOld*0.59
    
    # Numbers of Eggs to hatch
    numOfEggs = numOfAdultsPairs * averageEggsPerPair
    
    # Number of Eggs to Fledgeling
    numOfFledgelings = numOfAdultsPairs * averageFledgelingsPerPair
    
    if preditorControl:
        numOfFledgelings=numOfFledgelings*0.75
    else:
        numOfFledgelings=numOfFledgelings*0.18

    print "Year: ", year
    print "Number of Adult Pairs: ", numOfAdultsPairs
    print "Number of Fledgelings: ", numOfFledgelings
    print "Number of Fledgelings a Year old: ", numOfFledgelingsYearOld, "\n"
        
    
    
    
    
    
    


