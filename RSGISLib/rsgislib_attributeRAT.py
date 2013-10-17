#!/usr/bin/env python

#############################################
# rsgislib_attributeRAT.py
#
# A script to calculate attribute a RAT with 
# statistics from each band in an input image.
#
# Dan Clewley (daniel.clewley@gmail.com) 17/10/2013
# 
#############################################
import sys, argparse

try:
    import rsgislib
    from rsgislib import rastergis
except ImportError:
    print("ERROR: Couldn't import RSGISLib python modules")
    sys.exit()

try:
    import osgeo.gdal as gdal
except ImportError:
    print("ERROR: Couldn't import GDAL python bindings")
    sys.exit()

def populateImageStats(inputImage, clumpsFile, threshold, calcMin, calcMax, calcSum, calcMean, calcStDev, calcMedian, calcCount):
    
    """ Attribute RAT with stats from all bands in an input
        image.
    """

    # Open image
    dataset = gdal.Open(inputImage, gdal.GA_ReadOnly)
    
    # Set up list to hold statistics to calculate
    stats2Calc = list()
    
    # Loop through number of bands in image
    nBands = dataset.RasterCount
    for i in range(nBands):
        bandName = dataset.GetRasterBand(i+1).GetDescription()
        # If band name is not set set to bandN
        if bandName == '':
            bandName = 'Band' + str(i+1)

        # Initialise stats to calculate at None
        minName = None
        maxName = None
        sumName = None
        meanName = None
        stDevName = None
        medianName = None
        countName = None

        if calcMin:
            minName = bandName + 'Min'
        if calcMax:
            maxName = bandName + 'Max'
        if calcSum:
            sumName = bandName + 'Sum'
        if calcMean:
            meanName = bandName + 'Avg'
        if calcStDev:
            stDevName = bandName + 'Std'
        if calcMedian:
            medianName = bandName + 'Med'
        if calcCount:
            countName = bandName + 'Pix'

        stats2Calc.append(rastergis.BandAttStats(band=i+1, 
                    countField=countName, minField=minName, 
                    maxField=maxName, sumField=sumName, 
                    medianField=medianName, stdDevField=stDevName, 
                    meanField=meanName))
    
    # Calc stats
    print('''Calculating statistics for %i Bands'''%(nBands))
    t = rsgislib.RSGISTime()
    t.start(True)
    rastergis.populateRATWithStats(inputImage, clumpsFile, stats2Calc)
    t.end()


# Set up options
parser = argparse.ArgumentParser()
parser.add_argument("--inimage", type=str, help="Input image.", required=True)
parser.add_argument("--inclumps", type=str, \
    help="Input clumps file", required=True)
parser.add_argument("--min", dest='calcMin', default=False, action='store_true')
parser.add_argument("--max", dest='calcMax', default=False, action='store_true')
parser.add_argument("--mean", dest='calcMean', default=False, action='store_true')
parser.add_argument("--stddev", dest='calcStDev', default=False, \
    action='store_true')
parser.add_argument("--median", dest='calcMedian', default=False, action='store_true')
parser.add_argument("--sum", dest='calcSum', default=False, action='store_true')
parser.add_argument("--count", dest='calcCount', default=False, action='store_true')
parser.add_argument("--threshold", dest='threshold', type=float, default=0.0)

args = parser.parse_args() 

populateImageStats(args.inimage, args.inclumps, args.threshold, args.calcMin, args.calcMax, args.calcSum, args.calcMean, args.calcStDev, args.calcMedian, args.calcCount)


