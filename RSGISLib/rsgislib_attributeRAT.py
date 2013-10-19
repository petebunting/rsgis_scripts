#!/usr/bin/env python

#############################################
# rsgislib_attributeRAT.py
#
# A script to calculate attribute a RAT with 
# statistics from each band in an input image.
#
# Requires RSGISLib HG version > 639
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

def populateImageStats(inputImage, clumpsFile, outascii, threshold, calcMin, calcMax, calcSum, calcMean, calcStDev, calcMedian, calcCount, calcArea, calcLength, calcWidth, calcLengthWidth):
    
    """ Attribute RAT with stats from all bands in an input
        image.
    """

    # Open image
    dataset = gdal.Open(inputImage, gdal.GA_ReadOnly)
    
    # Set up list to hold statistics to calculate
    stats2Calc = list()
    
    # Loop through number of bands in image
    nBands = dataset.RasterCount

    # Set up array to hold all column names (used when exporting to ASCII)
    outFieldsList = []
    
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
            outFieldsList.append(minName)
        if calcMax:
            maxName = bandName + 'Max'
            outFieldsList.append(maxName)
        if calcSum:
            sumName = bandName + 'Sum'
            outFieldsList.append(sumName)
        if calcMean:
            meanName = bandName + 'Avg'
            outFieldsList.append(meanName)
        if calcStDev:
            stDevName = bandName + 'Std'
            outFieldsList.append(stDevName)
        if calcMedian:
            medianName = bandName + 'Med'
            outFieldsList.append(medianName)
        if calcCount:
            countName = bandName + 'Pix'
            outFieldsList.append(countName)

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

    # Calculate shapes, if required
    if calcArea or calcLength or calcWidth or calcLengthWidth:
        print("\nCalculating shape indices")
        shapes = list()
        if calcArea:
            shapes.append(rastergis.ShapeIndex(colName="Area", idx=rsgislib.SHAPE_SHAPEAREA))
            outFieldsList.append("Area")
        if calcLength:
            shapes.append(rastergis.ShapeIndex(colName="Length", idx=rsgislib.SHAPE_LENGTH))
            outFieldsList.append("Length")
        if calcWidth:
            shapes.append(rastergis.ShapeIndex(colName="Width", idx=rsgislib.SHAPE_WIDTH))
            outFieldsList.append("Width")
        if calcLengthWidth:
            shapes.append(rastergis.ShapeIndex(colName="LengthWidthRatio", idx=rsgislib.SHAPE_LENGTHWIDTH))
            outFieldsList.append("LengthWidthRatio")

        t.start(True)
        rastergis.calcShapeIndices(clumpsFile, shapes)
        t.end()
    
    # Export to ASCII if required
    if outascii is not None:
        print("\nExporting as ASCII")
        t.start(True)
        rastergis.export2Ascii(clumpsFile, outascii, outFieldsList)
        t.end()

# Set up options
parser = argparse.ArgumentParser()
parser.add_argument("--inimage", type=str, help="Input image.", required=True)
parser.add_argument("--inclumps", type=str, \
    help="Input clumps file", required=True)
parser.add_argument("--outascii", type=str, help="Output ASCII file (CSV) - optional", default=None)
parser.add_argument("--min", dest='calcMin', default=False, action='store_true')
parser.add_argument("--max", dest='calcMax', default=False, action='store_true')
parser.add_argument("--mean", dest='calcMean', default=False, action='store_true')
parser.add_argument("--stddev", dest='calcStDev', default=False, \
    action='store_true')
parser.add_argument("--median", dest='calcMedian', default=False, action='store_true')
parser.add_argument("--sum", dest='calcSum', default=False, action='store_true')
parser.add_argument("--count", dest='calcCount', default=False, action='store_true')
parser.add_argument("--area", dest='calcArea', default=False, action='store_true')
parser.add_argument("--length", dest='calcLength', default=False, action='store_true')
parser.add_argument("--width", dest='calcWidth', default=False, action='store_true')
parser.add_argument("--lengthwidth", dest='calcLengthWidth', default=False, action='store_true')
parser.add_argument("--threshold", dest='threshold', type=float, default=0.0)

args = parser.parse_args() 

populateImageStats(args.inimage, args.inclumps, args.outascii, args.threshold, args.calcMin, args.calcMax, args.calcSum, args.calcMean, args.calcStDev, args.calcMedian, args.calcCount, args.calcArea, args.calcLength, args.calcWidth, args.calcLengthWidth)


