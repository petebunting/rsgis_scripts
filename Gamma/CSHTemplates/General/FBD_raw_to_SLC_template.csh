#! /bin/csh
#
# Script to process RAW ALOS data to Level 1_1
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
# Modified by Dan Clewley 01/02/10 to run single scene only
# Modified by Dan Clewley 16/02/10 as template for BatchGamma.py

#
# From this point forward is just the processing from 1.0 (raw) to 1.1 (SLC).
#
# 1st, generation of the SAR sensor parameter file, and MSP parameter file.
PALSAR_proc LEDFILENAME SCENENAME_hh.sar.par pSCENENAME_hh.slc.par HHFILENAME SCENENAME_hh.raw 0 0
PALSAR_proc LEDFILENAME SCENENAME_hv.sar.par pSCENENAME_hv.slc.par HVFILENAME SCENENAME_hv.raw 0 1
#
# 2nd, generation of the calibration file and update of the SAR sensor parameter file using the external calibration file.
PALSAR_antpat SCENENAME_hh.sar.par pSCENENAME_hh.slc.par $MSP_HOME/sensors/palsar_ant_20061024.dat SCENENAME_hh.PALSAR_antpat_MSP.dat - 0 0
PALSAR_antpat SCENENAME_hv.sar.par pSCENENAME_hv.slc.par $MSP_HOME/sensors/palsar_ant_20061024.dat SCENENAME_hv.PALSAR_antpat_MSP.dat - 0 1
#
# 3rd, determine the Doppler ambiguity.
dop_mlcc SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.raw SCENENAME_hh.mlcc
dop_mlcc SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.raw SCENENAME_hv.mlcc
#
# 4th, estimation of Doppler centroid. The different polarisations present different start times.
# For this reason, estimation of the Doppler centroid is done for one polarisation (e.g., HH), 
# and the Doppler centroid and effective velocity are copied to the parameter file of the other polarisation.
# In this way, all the images will have the same geometry and phase reference, i.e., they will all overlap.
# For this, use the program "doppler" first on the master polarisation (e.g., HH) and then the program "set_value"
# to update the MSP processing parameter files of the other polarisation.
doppler SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.raw SCENENAME_hh.dop
set a1 = `grep doppler_polynomial pSCENENAME_hh.slc.par |cut -d : -f 1 --complement`
set_value pSCENENAME_hv.slc.par pSCENENAME_hv.slc.par "doppler_polynomial" "$a1" 0
#
# 5th, range compression.
pre_rc SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.raw SCENENAME_hh.rc - - - - - - - - 1 -
pre_rc SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.raw SCENENAME_hv.rc - - - - - - - - 1 -
#
# 6th, estimate autofocus (twice) for one polarisation (e.g., HH) and copy the effective velocity to the other MSP 
# parameter file, so that all polarisation channels will be identical.
autof SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.rc SCENENAME_hh.af 5.0 1 4096
autof SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.rc SCENENAME_hh.af 5.0 1 4096
set a2 = `grep sensor_velocity_vector pSCENENAME_hh.slc.par |cut -d : -f 1 --complement`
set_value pSCENENAME_hv.slc.par pSCENENAME_hv.slc.par "sensor_velocity_vector" "$a2" 0
#
# 7th, azimuth compression.
az_proc SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.rc SCENENAME_hh.slc 16384 0 -51.8 0 2.12
az_proc SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.rc SCENENAME_hv.slc 16384 0 -58.3 0 2.12
#
# 8th, generating the ISP parameter files.
par_MSP SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.slc.par
par_MSP SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.slc.par
#
# 9th, generating a file with the SLC extents.
SLC_corners SCENENAME_hh.slc.par > SCENENAME_hh.slc.corners
SLC_corners SCENENAME_hv.slc.par > SCENENAME_hv.slc.corners
#
# 10th, generating SUN raster image of SLC intensity images.
# First, we need to get the number of samples in the SLC image
set rs = `grep range_pixels pSCENENAME_hh.slc.par |cut -d : -f 1 --complement`
# and now we generate the SUN raster images (*.ras), averaged 10x in range and 10x in azimuth.
#rasSLC SCENENAME_hh.slc "$rs" - - 10 10
#rasSLC SCENENAME_hv.slc "$rs" - - 10 10
#
# Remove raw data
rm *.rc
rm *.raw
