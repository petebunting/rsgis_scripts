# A script to copy every Nth line from a CSV file 
# to a new CSV file
#
# Dan Clewley (clewley@usc.edu)
# 28/10/2013
#

import csv
import argparse

# Set up options
parser = argparse.ArgumentParser()
parser.add_argument("-i","--incsv", type=str, help="Input CSV.", required=True)
parser.add_argument("-o","--outcsv", type=str, help="Output CSV.", required=True)
parser.add_argument("-n", dest="n",type=int, help="Copy every n lines.", required=True)

args = parser.parse_args() 

inFileHandler = open(args.incsv,'rU')
outFileHandler = open(args.outcsv,'w')

inFile = csv.reader(inFileHandler)
outFile = csv.writer(outFileHandler)


# Write out header row
outFile.writerow(next(inFile))

# Itterate through file
i = 1
for line in inFile:
    if i < args.n:
        i+=1
    else:
        outFile.writerow(line)
        i = 1

# Close files
inFileHandler.close()
outFileHandler.close()
