#!/usr/bin/env python
##################################################################
# A script to export a CSV file from a MySQL database
#
# Part of GoogleMapsTrainingPointsTool
# Dan Clewley (clewley@usc.edu)
# 19/03/2013
# Copyright 2013 Daniel Clewley.
##################################################################

import os, sys, csv
import mysql.connector as msc

sys.path.append(os.sys.path[0])

# Directory on webserver to hold tempory files when requested by users
# This file needs to be cleared at regular intervals.
wwwTempDIR = '/var/www/downloads'
outPointsFile = 'outPoints.csv'

# Get password for MYSQL
mysqlip = 'localhost'
mysqluser = 'USER'
mysqlpass = 'PASS'
mysqldb = 'DATABASE'

outFileName = os.path.join(wwwTempDIR, outPointsFile)
outFile = open(outFileName,'w')

# Connect to database
sensordb = msc.connect(user=mysqluser, password=mysqlpass, host=mysqlip, database=mysqldb)

# Set up cursor
cursor = sensordb.cursor(buffered=True)

sqlCommand = "SELECT * FROM `Points` WHERE class != '';"
cursor.execute(sqlCommand)
sensordb.close()

outHeader = 'ID,Lat,Long,Class\n'
outFile.write(outHeader)

for row in cursor.fetchall():
    outLine = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + row[3].strip() + '\n'
    outFile.write(outLine)

outFile.close()

print outPointsFile
