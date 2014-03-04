#! /bin/csh
#
# Script to convert JAXA 1.1 data to GAMMA SLC
#
# Created by Joao M. B. Carreiras (IG&ES/AU and IICT).
# Copyright 2012 Joao M. B. Carreiras. All rights reserved.
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
# Modified by Dan Clewley 05/01/11 as template for BatchGamma.py
#

# Create the SLC and ISP parameter file in MSP format.
par_EORC_PALSAR LEDFILENAME temp_hh.slc.par HHFILENAME temp_hh.slc
par_EORC_PALSAR LEDFILENAME temp_hv.slc.par HVFILENAME temp_hv.slc
#
# Calibrate the SLCs. Since the SLCs are already corrected for antenna pattern, 
# we only need to correct for the absolute calibration factor. 
# For level 1.1 data processed by JAXA after January 9, 2009, 
# the absolute calibration factor is -115.0 dB.
# See https://auig.eoc.jaxa.jp/auigs/en/doc/an/20090109en_3.html
radcal_SLC temp_hh.slc temp_hh.slc.par SCENENAME_hh.slc SCENENAME_hh.slc.par 1 - 0 0 1 0 -115.0
radcal_SLC temp_hv.slc temp_hv.slc.par SCENENAME_hv.slc SCENENAME_hv.slc.par 1 - 0 0 1 0 -115.0

# Generate a file with the SLC extents.
SLC_corners SCENENAME_hh.slc.par > SCENENAME_hh.slc.corners
SLC_corners SCENENAME_hv.slc.par > SCENENAME_hv.slc.corners

# Remove temp files.
rm temp*slc*

