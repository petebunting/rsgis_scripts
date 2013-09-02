#!/usr/bin/env python

#############################################
# ZonalStats.py
#
# A script to calculate zonal statistics
# using RSGISLib python bindings
# Requires RSGISLib > Mercurial version 588
#
# Dan Clewley (daniel.clewley@gmail.com) 18/08/2013
# 
#############################################

import os, sys, argparse
try:
    import rsgislib
    from rsgislib import zonalstats
except ImportError:
    print("ERROR: Couldn't import RSGISLib python modules")
    sys.exit()

# Set up options
parser = argparse.ArgumentParser()
parser.add_argument("--inimage", type=str, help="Input image.")
parser.add_argument("--invector", type=str, \
    help="Input Shapefile containing regions of interest.")
parser.add_argument("--outstats", type=str, \
    help="Output Shapefile / CSV file with statistics.")
parser.add_argument("--force", dest='force', default=False, action='store_true', \
    help="Force removal of output shapefile if it exists.")
parser.add_argument("--noprojwarnings", dest='noprojwarnings', default=False, \
    action='store_true', \
    help="Don't print warning if projection is different for 'inimage' \
    and 'invector'")
parser.add_argument("--min", dest='calcMin', default=False, action='store_true')
parser.add_argument("--max", dest='calcMax', default=False, action='store_true')
parser.add_argument("--mean", dest='calcMean', default=False, action='store_true')
parser.add_argument("--stddev", dest='calcStDev', default=False, \
    action='store_true')
parser.add_argument("--mode", dest='calcMode', default=False, action='store_true')
parser.add_argument("--sum", dest='calcSum', default=False, action='store_true')
args = parser.parse_args() 

# Check we have required input and output files
if args.inimage == None:
    print('No input image provided')
    parser.print_help()
    sys.exit()

if args.invector == None:
    print('No input vector provided')
    parser.print_help()
    sys.exit()

if args.outstats == None:
    print('No output shapefile provided')
    parser.print_help()
    sys.exit()

# Set up ZonalAttributes object with statistics to calculate
zonalattributes = zonalstats.ZonalAttributes(minThreshold=None, \
maxThreshold=None, calcCount=False, calcMin=args.calcMin, \
calcMax=args.calcMax, calcMean=args.calcMean, calcStdDev=args.calcStDev, \
calcMode=args.calcMode, calcSum=args.calcSum)

# Use input raster band names (if available) for output
# column names
useBandNames = True
# Include pixels where the center is in the polygon
zonalStatsMethod = zonalstats.METHOD_POLYCONTAINSPIXELCENTER

# Check if a CSV or Shapefile is required for output statistics.
if os.path.splitext(args.outstats)[-1] == '.csv':
    zonalstats.pixelStats2TXT(args.inimage, args.invector, args.outstats, \
    zonalattributes, useBandNames, args.noprojwarnings, zonalStatsMethod)
elif os.path.splitext(args.outstats)[-1] == '.shp':
    zonalstats.pixelStats2SHP(args.inimage, args.invector, args.outstats, \
    zonalattributes, args.force, useBandNames, args.noprojwarnings, \
    zonalStatsMethod) 
else:
    print("--outstats file must end in '.csv' (CSV) or '.shp' \
    (ESRI Shapefile)")
