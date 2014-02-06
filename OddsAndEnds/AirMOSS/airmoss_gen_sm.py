#!/usr/bin/env python
#
# airmoss_gen_sm.py
#
# A script to generate soil moisture at 
# various depths from AirMOSS data.
#
# Assumes data has already been converted to a 
# format GDAL can read and coefficients
# are the last 3 bands in the image.
#
# Requires the RIOS library (https://bitbucket.org/chchrsc/rios/)
#
# Dan Clewley (clewley@usc.edu)
# 11/11/2013
#
# Copyright 2014 Daniel Clewley. All rights reserved.
# 
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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


