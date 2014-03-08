#!/usr/bin/env python
#
# A script topographically correct SAR data using RIOS applier.
#
# Dan Clewley (clewley@usc.edu) - 05/02/2013
#
# The correction uses:
#
# sigma0_norm = sigma0 * (A_flat / A_slope) * (cos(theta_ref) / cos(theta_loc))^n
#
# Where n is a parameter related to optical thicknes. Defaults to 1.
#
# Castel et al. 2001. Sensitivity of space-borne SAR data to forest parameters over sloping terrain. 
# Theory and experiment. International journal of remote sensing. 22(12) pp. 2351-2376
#
# Designed to take outputs of GAMMA:
# - Sigma0
# - Normalised pixel area (A_flat / A_slope) '.pix'
# - Local incidence angle '.inc'
#
# Can be run as a stand alone script or from within BatchGamma.py to process
# multiple files (different polarizations).
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
#
#

import sys
import argparse
from rios import applier
from rios import cuiprogress
import numpy as np
import os, glob

havescipy = True

try:
    from scipy import ndimage
except ImportError:
    havescipy = False

def getOutDriver(outFileName):
    
    """ Set output driver type and creation options
        based on file extension.

        Returns driver name and list of creation options
        as dictionary.
    """

    outControls = {}

    gdalFormat = 'ENVI'
    gdalCOOptions = []
    calcStats = False

    extension = os.path.splitext(outFileName)[-1] 
    if extension == '.kea':
        gdalFormat = 'KEA'
        calcStats = True
    elif extension == '.tif':
        gdalFormat = 'GTiff'
        gdalCOOptions = ['COMPRESS=DEFLATE']
        calcStats = True
    elif extension == '.img':
        gdalFormat = 'HFA'
        gdalCOOptions = ['COMPRESSED=YES']
        calcStats = True
    elif extension == '.pix':
        gdalFormat = 'PCIDSK'
        gdalCOOptions = ['COMPRESSION=RLE']
        calcStats = True

    outControls['gdalFormat'] = gdalFormat
    outControls['gdalCOOptions'] = gdalCOOptions
    outControls['calcStats'] = gdalCOOptions

    return outControls
    

def castelCorrection(info, inputs, outputs, otherargs):
    """
    Apply topographic correction of Castel et al (2001)
    """
    theta_ref_deg = otherargs.thetaref
    nFactor = otherargs.nFactor
    filterSize = otherargs.filterSize
    theta_ref = np.deg2rad(theta_ref_deg)
    insigma=inputs.insigma.astype(np.float32)
    inpix=inputs.inpix.astype(np.float32)
    inlinc=inputs.inlinc.astype(np.float32)
    
    if havescipy and filterSize is not None:
        inpix = ndimage.uniform_filter(inpix,size=filterSize)
        inlinc = ndimage.uniform_filter(inlinc,size=filterSize)

    outputs.outimage = insigma * inpix * (np.cos(theta_ref) / np.cos(inlinc))

def runCorrection(insigma, inlinc, inpix, outsigma, thetaref=39.0, nFactor=1.0, filterSize=None):

    controls = applier.ApplierControls()
    
    # Set up input images
    infiles = applier.FilenameAssociations()
    infiles.insigma = insigma
    infiles.inlinc = inlinc
    infiles.inpix = inpix
    
    # Set up output image
    outfiles = applier.FilenameAssociations()
    outfiles.outimage = outsigma

    # Set format for output image
    outControls = getOutDriver(outsigma)

    # Set options
    controls.setOutputDriverName(outControls['gdalFormat'])
    controls.setCreationOptions(outControls['gdalCOOptions'])
    controls.setCalcStats(outControls['calcStats'])

    # Set up parameters
    otherargs = applier.OtherInputs()
    otherargs.thetaref = thetaref
    otherargs.nFactor = nFactor
    otherargs.filterSize = filterSize
    
    # Run correction
    controls.progress = cuiprogress.CUIProgressBar()
    applier.apply(castelCorrection, infiles, outfiles, otherargs, controls=controls)

def runCorrectionDIR(inDIR, sigmaExt='utm', lincExt='inc', pixExt='pix', outExt='kea', thetaref=39.0, nFactor=1, filterSize=None):
    """ Run correction for directory.
        Finds files based on supplied extension.
    """
    try:
        inlinc = glob.glob(inDIR + '/*' + lincExt)[0]
        inpix = glob.glob(inDIR + '/*' + pixExt)[0]
    except Exception as err:
        print("Couldn't find local incidence angle or pixel area images, is the extension correct?")
        print(err)
    
    inSigmaList = glob.glob(inDIR + '/*' + sigmaExt)
    
    for insigma in inSigmaList:
        insigmaBase = os.path.splitext(insigma)[0]
        outsigma = insigmaBase + '_topo.' + outExt
        runCorrection(insigma, inlinc, inpix, outsigma, thetaref, nFactor, filterSize)

if __name__ == '__main__':

    # Read in parameters
       
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--insigma", type=str, required=True, help="Input sigma0 file")
    parser.add_argument("-p", "--inpix", type=str, required=True, help="Input pixel area")
    parser.add_argument("-l", "--inlinc", type=str, required=True, help="Input local incidence angle")
    parser.add_argument("-o", "--outsigma", type=str, required=True, help="Output topographically corrected sigma0")
    parser.add_argument("--thetaref", type=float, required=False, default=39.0, help="Reference incidence angle (default 39)")
    parser.add_argument("--n", type=float, required=False, default=1.0, help="n parameter (default 1)")
    parser.add_argument("--filterSize", type=int, required=False, default=None, help="Size of filter to apply to linc and pix data")
    args = parser.parse_args()    

    # Run
    runCorrection(args.insigma, args.inlinc, args.inpix, args.outsigma, args.thetaref, args.n, args.filterSize)
  

