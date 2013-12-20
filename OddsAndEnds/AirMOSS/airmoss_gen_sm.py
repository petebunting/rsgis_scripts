#!/usr/bin/env python
# A script to generate soil moisture at 
# various depths from AirMOSS data.
#
# Assumes data has already been converted to a 
# format GDAL can read and coefficients
# are the last 3 bands in the image.
#
# Requires the RIOS library.
#
# Dan Clewley (clewley@usc.edu)
# 11/11/2013
#
import sys, argparse
from rios import applier
from rios import cuiprogress
import numpy as np

def genSM(info, inputs, outputs, otherargs):
    """
    Generates soil moisture at depth from AirMOSS
    retreval.
    """

    outSMStack = []

    for depth in otherargs.depths:

        coeffA = inputs.inimage[-1]
        coeffB = inputs.inimage[-2]
        coeffC = inputs.inimage[-3]

        sm = coeffA + coeffB*depth + coeffC*(depth**2)

        outSMStack.append(sm)

    outputs.outimage = np.array(outSMStack,dtype=np.float32)

# Get input parameters
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inimage", type=str, help="Input image",required=True)
parser.add_argument("-o", "--outimage", type=str, help="Output image", required=True)
args = parser.parse_args()    

infiles = applier.FilenameAssociations()
infiles.inimage = args.inimage

outfiles = applier.FilenameAssociations()
outfiles.outimage = args.outimage

controls = applier.ApplierControls()
controls.progress = cuiprogress.CUIProgressBar()
controls.setCalcStats(True)

# Set up depths
otherargs = applier.OtherInputs()
otherargs.depths = np.arange(0,1.05,0.05)

outBandNames = []

for depth in otherargs.depths:
    name = str(int(depth*100.)) + ' cm'
    outBandNames.append(name)

controls.setLayerNames(outBandNames)

applier.apply(genSM, infiles, outfiles, otherargs, controls=controls)


