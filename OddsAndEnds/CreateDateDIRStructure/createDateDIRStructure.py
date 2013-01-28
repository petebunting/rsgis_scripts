# Function to create directory structure of years, months and days.

import os, sys
import numpy as np

def padZeros(inInt, digits=2):
    ''' Function to add zerors before number '''
    inStr = str(inInt)
    outStr = inStr.zfill(digits)
    return outStr

if len(sys.argv) < 2:
    print 'Path is required'
    exit()

basepath = sys.argv[1]

years = np.arange(2012,2016)
months = np.arange(1,13)
days = np.arange(1,32)

for currentyear in years:
    yeardir = os.path.join(basepath,str(currentyear))
    os.mkdir(yeardir)
    for currentmonth in months:
        monthdir = os.path.join(yeardir, padZeros(currentmonth))
        os.mkdir(monthdir)
        for currentday in days:
            daydir = os.path.join(monthdir, padZeros(currentday))
            os.mkdir(daydir)
