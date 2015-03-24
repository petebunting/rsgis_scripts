#!/usr/bin/env python
##################################################################
# A script to gernerate SQL for loading points from a CSV file
# into a database.
#
# Part of GoogleMapsTrainingPointsTool
# Dan Clewley (clewley@usc.edu)
# 19/03/2013
# Copyright 2013 Daniel Clewley.
##################################################################

import csv, os, sys, re

# Open CSV file
if len(sys.argv) < 2:
    print('''Not enough parameters provided.
Usage:
 python load_nodeinfo.py incsv.csv out.sql
''')
    sys.exit(1)
inFileName = sys.argv[1]
outFileName = sys.argv[2]

inFile = csv.reader(open(inFileName, 'rU'))
outFile = open(outFileName,'w')


# Skip header line
next(inFile)

# Open database connection

nodeInfoInsertStr = '''INSERT INTO `Points`(ID,latitude,longitude,class)'''

for line in inFile:
    valuesStr = '''VALUES ('%s',%s,%s,'')'''%(line[0],line[9],line[10])

    sqlCommand = nodeInfoInsertStr + valuesStr + ';'
    outFile.write(sqlCommand)
   
outFile.close()

print('''Load to database using:
mysql -u USER --password=PASSWORD -D DATABASE < %s'''%outFileName)
