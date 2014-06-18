#!/usr/bin/env python
#
# two_band_scatter_plot.py
#
# Produces 2D histogram showing a pixel-to-pixel comparison
# of two rasters.
# 
# Dan Clewley (daniel.clewley@gmail.com) - 29/04/2014

# 2D histogram example from:
# http://oceanpython.org/2013/02/25/2d-histogram/

import sys, argparse
from rios import applier
from rios import cuiprogress
import numpy as numpy
from scipy import stats
import matplotlib.pylab as plt
from matplotlib import colorbar

def getData(info, inputs, outputs, otherargs):
    """
    Gets data and saves to two numpy vectors
    """
    # Get band
    imageA = inputs.imageA[otherargs.bandA]
    imageB = inputs.imageB[otherargs.bandB]

    imageB = imageB * otherargs.scale

    # Flattern
    imageAFlat = imageA.reshape((1,imageA.shape[0]*imageA.shape[1]))[0]
    imageBFlat = imageB.reshape((1,imageB.shape[0]*imageB.shape[1]))[0]

    # Create single array
    dataAB = numpy.vstack((imageAFlat,imageBFlat))

    # Set zero to nan
    dataAB = numpy.where(dataAB==0,numpy.nan,dataAB)

    # Remove non-finite values
    dataAB = dataAB[:,numpy.isfinite(dataAB).all(axis=0)]

    # Add to existing array
    otherargs.outdataA = numpy.concatenate((otherargs.outdataA, dataAB[0]))
    otherargs.outdataB = numpy.concatenate((otherargs.outdataB, dataAB[1]))

def calcStats(inDataA, inDataB):
    """ Calculate statistics for two vectors """
    
    outStats = {}
    outStats['dataBias'] = numpy.mean(inDataA - inDataB)
    outStats['dataRMSE'] = numpy.sqrt(numpy.mean((inDataA - inDataB)**2))

    # Linear fit
    slope, intercept, r_value, p_value, std_err = stats.linregress(inDataA, inDataB)
    outStats['dataSlope'] = slope
    outStats['dataIntercept'] = intercept
    outStats['dataR2'] = r_value**2

    print('Bias: ',round(outStats['dataBias'],2))
    print('RMSE: ', round(outStats['dataRMSE'],2))
    print('Slope: ', round(outStats['dataSlope'],2))
    print('Intercept: ', round(outStats['dataIntercept'],2))
    print('R2: ', round(outStats['dataR2'],2))

    return outStats

def plotData(inDataA, inDataB, outPlot, labelA=None, labelB=None, plotMin=None, plotMax=None, independentXY=False):

    if labelA is None:
        labelA = "Image A"
    if labelB is None:
        labelB = "Image B"

    # Calc stats
    print('#####################')
    dataStats = calcStats(inDataA, inDataB)
    print('#####################')

    # Set axis limits
    if plotMin is None:
        plotMin = numpy.min([numpy.min(inDataA),numpy.min(inDataB)])
    if plotMax is None:
        plotMax = numpy.max([numpy.max(inDataA),numpy.max(inDataB)])
        
    # Set axis limits
    if independentXY:
        plotMinX = numpy.min(inDataA)
        plotMinY = numpy.min(inDataB)
        plotMaxX = numpy.max(inDataA)
        plotMaxY = numpy.max(inDataB)
    else:
        plotMinX = plotMin
        plotMaxX = plotMax
        plotMinY = plotMinX
        plotMaxY = plotMaxX

    # Calculate the 2D histogram
    nbins = 200
    histRange = [[plotMinX, plotMaxX], [plotMinY,plotMaxY]] 
    H, xedges, yedges = numpy.histogram2d(inDataA,inDataB,bins=nbins,range=histRange)
     
    # H needs to be rotated and flipped
    H = numpy.rot90(H)
    H = numpy.flipud(H)
     
    # Mask zeros
    Hmasked = numpy.ma.masked_where(H==0,H) # Mask pixels with a value of zero
    # Log
    Hmasked = numpy.log10(Hmasked)     

    # Plot 2D histogram using pcolor
    fig2 = plt.figure()
    plt.pcolormesh(xedges,yedges,Hmasked)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Log(Pixels)')

    one2oneLine = numpy.arange(plotMin, plotMax*1.2,(plotMax - plotMin)/10)
    plt.plot(one2oneLine, one2oneLine,'--',color='black')

    # Set limit
    plt.xlim((plotMinX, plotMaxX))
    plt.ylim((plotMinY, plotMaxY))

    # Label axes
    plt.xlabel(labelA)
    plt.ylabel(labelB)
    #plt.grid(True)

    # Save figure
    if args.plot.find('.pdf') > 0:
        plt.savefig(args.plot, format='PDF')
    elif args.plot.find('.png') > 0:
        plt.savefig(args.plot, format='PNG',dpi=300)
    else:
        print('Outplot file must end in PNG or PDF') 
    

def createPlots(imageA, imageB, outPlot, bandA=1, bandB=1, labelA=None, labelB=None, plotMin=None, plotMax=None, scale=1, independentXY=False):

    controls = applier.ApplierControls()
    
    # Set up input images
    infiles = applier.FilenameAssociations()
    infiles.imageA = imageA
    infiles.imageB = imageB

    outfiles = applier.FilenameAssociations()
    
    # Set up parameters
    otherargs = applier.OtherInputs()
    otherargs.bandA = bandA - 1
    otherargs.bandB = bandB - 1
    otherargs.outdataA = numpy.array([],dtype=numpy.float32)
    otherargs.outdataB = numpy.array([],dtype=numpy.float32)
    otherargs.scale = scale
    
    # Get data
    print('Extracting data')
    controls.progress = cuiprogress.CUIProgressBar()
    applier.apply(getData, infiles, outfiles, otherargs, controls=controls)

    # Produce plot
    print('Saving plot')
    plotData(otherargs.outdataA, otherargs.outdataB, outPlot, labelA, labelB, plotMin, plotMax, independentXY)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--imageA", type=str, help="Image A",required=True)
    parser.add_argument("--imageB", type=str, help="Image B",required=True)
    parser.add_argument("--bandA", type=int, default=1, help="Band in image A",required=False)
    parser.add_argument("--bandB", type=int, default=1, help="Band in image B",required=False)
    parser.add_argument("--labelA", type=str,default=None, help="Label for image A", required=False)
    parser.add_argument("--labelB", type=str,default=None, help="Label for image B", required=False)
    parser.add_argument("--plot", type=str, help="Out plot (png / pdf)", required=True)
    parser.add_argument("--plotMin", type=float, default=None, help="Minimum for plot",required=False)
    parser.add_argument("--plotMax", type=float, default=None, help="Maximum for plot",required=False)
    parser.add_argument("--scale", type=float, default=1, help="Scaling between imageA and imageB (default=1)",required=False)
    parser.add_argument("--independent_axes", action='store_true',default=False, help="Use independent min/max for image A and B (default=False)",required=False)
    args = parser.parse_args()    
    
    createPlots(args.imageA, args.imageB, args.plot, args.bandA, args.bandB, args.labelA, args.labelB, args.plotMin, args.plotMax, args.scale, args.independent_axes)

