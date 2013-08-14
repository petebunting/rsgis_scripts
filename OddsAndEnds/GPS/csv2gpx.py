#!/usr/bin/env python

#############################################
# csv2gpx
# A script to convert a csv file containing 
# point locations to a GPX file.
#
# Dan Clewley (clewley@usc.edu) 14/08/2013
# 
#############################################

import sys, csv
from time import strftime

##########################################
# SET UP COLUMNS FOR DATA (STARTS AT 0)
# EDIT HERE TO CHANGE COLS
latCol = 0
lonCol = 1
nameCol = 2
##########################################

if len(sys.argv) < 3:
    print('''ERROR: Not enough parameters provided.
Usage:
    python csv2gpx inCSV.csv outGPX.gpx
''')
    sys.exit()
inFileName = sys.argv[1]
outFileName = sys.argv[2]

inFileHandler = open(inFileName,'rU')
inFile = csv.reader(inFileHandler)

# Skip header row
next(inFile)

# Write out header for GPX file
outGPXString = '''<?xml version="1.0"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1" xmlns:gpxtrx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:trp="http://www.garmin.com/xmlschemas/TripExtensions/v1" xmlns:adv="http://www.garmin.com/xmlschemas/AdventuresExtensions/v1" xmlns:prs="http://www.garmin.com/xmlschemas/PressureExtension/v1" creator="Garmin Desktop App" version="1.1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/ActivityExtension/v1 http://www8.garmin.com/xmlschemas/ActivityExtensionv1.xsd http://www.garmin.com/xmlschemas/AdventuresExtensions/v1 http://www8.garmin.com/xmlschemas/AdventuresExtensionv1.xsd http://www.garmin.com/xmlschemas/PressureExtension/v1 http://www.garmin.com/xmlschemas/PressureExtensionv1.xsd http://www.garmin.com/xmlschemas/TripExtensions/v1 http://www.garmin.com/xmlschemas/TripExtensionsv1.xsd">

  <metadata>
    <link href="http://www.garmin.com">
      <text>Garmin International</text>
    </link>
    <time>%s</time>
    <bounds maxlat="MAXLAT" maxlon="MAXLON" minlat="MINLAT" minlon="MINLON"/>
  </metadata>
  
'''%(strftime('%Y-%m-%dT%H:%M:%SZ'))

# Create arrays to hold lat / long (to calculate bounding box)
latAll = []
lonAll = []

# Create new record for each line
for line in inFile:
    record = {}
    record['LAT'] = float(line[latCol])
    record['LON'] = float(line[lonCol])
    record['NAME'] = line[nameCol]
    record['TIME'] = strftime('%Y-%m-%dT%H:%M:%SZ')
    
    latAll.append(record['LAT'])
    lonAll.append(record['LON'])
    
    outGPXString = outGPXString + '''   <wpt lat="%(LAT)f" lon="%(LON)f">
    <time>%(TIME)s</time>
    <name>%(NAME)s</name>
    <sym>Flag, Blue</sym>
    <type>user</type>
    <extensions>
      <gpxx:WaypointExtension>
        <gpxx:DisplayMode>SymbolAndName</gpxx:DisplayMode>
      </gpxx:WaypointExtension>
    </extensions>
    </wpt>
    
    '''% record
    
inFileHandler.close()

outGPXString = outGPXString + '</gpx>'

# Replace min/max for bounding box
outGPXString = outGPXString.replace('MAXLAT',str(max(latAll)))
outGPXString = outGPXString.replace('MINLAT',str(min(latAll)))
outGPXString = outGPXString.replace('MAXLON',str(max(lonAll)))
outGPXString = outGPXString.replace('MINLON',str(min(lonAll)))

# Write out
outFile = open(outFileName,'w')
outFile.write(outGPXString)
outFile.close()

print('Saved to: ' + outFileName)
