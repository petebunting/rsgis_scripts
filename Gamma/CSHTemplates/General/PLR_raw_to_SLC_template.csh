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
PALSAR_proc LEDFILENAME SCENENAME_vv.sar.par pSCENENAME_vv.slc.par VVFILENAME SCENENAME_vv.raw 1 1
PALSAR_proc LEDFILENAME SCENENAME_vh.sar.par pSCENENAME_vh.slc.par VVFILENAME SCENENAME_vh.raw 1 1
#
# 2nd, generation of the calibration file and update of the SAR sensor parameter file using the external calibration file.
PALSAR_antpat SCENENAME_hh.sar.par pSCENENAME_hh.slc.par $MSP_HOMEsensors/palsar_ant_20061024.dat SCENENAME_hh.PALSAR_antpat_MSP.dat - 0 0
PALSAR_antpat SCENENAME_hv.sar.par pSCENENAME_hv.slc.par $MSP_HOMEsensors/palsar_ant_20061024.dat SCENENAME_hv.PALSAR_antpat_MSP.dat - 0 1
PALSAR_antpat SCENENAME_vv.sar.par pSCENENAME_vv.slc.par $MSP_HOMEsensors/palsar_ant_20061024.dat SCENENAME_vv.PALSAR_antpat_MSP.dat - 1 1
PALSAR_antpat SCENENAME_vh.sar.par pSCENENAME_vh.slc.par $MSP_HOMEsensors/palsar_ant_20061024.dat SCENENAME_vh.PALSAR_antpat_MSP.dat - 1 0
#
# 3rd, determine the Doppler ambiguity.
dop_mlcc SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.raw SCENENAME_hh.mlcc
dop_mlcc SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.raw SCENENAME_hv.mlcc
dop_mlcc SCENENAME_vv.sar.par pSCENENAME_vv.slc.par SCENENAME_vv.raw SCENENAME_vv.mlcc
dop_mlcc SCENENAME_vh.sar.par pSCENENAME_vh.slc.par SCENENAME_vh.raw SCENENAME_vh.mlcc
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
set_value pSCENENAME_vv.slc.par pSCENENAME_vv.slc.par "doppler_polynomial" "$a1" 0
set_value pSCENENAME_vh.slc.par pSCENENAME_vh.slc.par "doppler_polynomial" "$a1" 0
#
# 5th, range compression.
pre_rc SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.raw SCENENAME_hh.rc - - - - - - - - 1 -
pre_rc SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.raw SCENENAME_hv.rc - - - - - - - - 1 -
pre_rc SCENENAME_vv.sar.par pSCENENAME_vv.slc.par SCENENAME_vv.raw SCENENAME_vv.rc - - - - - - - - 1 -
pre_rc SCENENAME_vh.sar.par pSCENENAME_vh.slc.par SCENENAME_vh.raw SCENENAME_vh.rc - - - - - - - - 1 -
#
# 6th, estimate autofocus (twice) for one polarisation (e.g., HH) and copy the effective velocity to the other MSP 
# parameter file, so that all polarisation channels will be identical.
autof SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.rc SCENENAME_hh.af 5.0 1 4096
autof SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.rc SCENENAME_hh.af 5.0 1 4096
set a2 = `grep sensor_velocity_vector pSCENENAME_hh.slc.par |cut -d : -f 1 --complement`
set_value pSCENENAME_hv.slc.par pSCENENAME_hv.slc.par "sensor_velocity_vector" "$a2" 0
set_value pSCENENAME_vv.slc.par pSCENENAME_vv.slc.par "sensor_velocity_vector" "$a2" 0
set_value pSCENENAME_vh.slc.par pSCENENAME_vh.slc.par "sensor_velocity_vector" "$a2" 0

#
# 7th, azimuth compression.
az_proc SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.rc SCENENAME_hh.slc 16384 0 -45.4 0 2.12
az_proc SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.rc SCENENAME_hv.slc 16384 0 -53.6 0 2.12
az_proc SCENENAME_vv.sar.par pSCENENAME_vv.slc.par SCENENAME_vv.rc SCENENAME_vv.slc 16384 0 -43.9 0 2.12
az_proc SCENENAME_vh.sar.par pSCENENAME_vh.slc.par SCENENAME_vh.rc SCENENAME_vh.slc 16384 0 -54.5 0 2.12

#
# 8th, generating the ISP parameter files.
par_MSP SCENENAME_hh.sar.par pSCENENAME_hh.slc.par SCENENAME_hh.slc.par
par_MSP SCENENAME_hv.sar.par pSCENENAME_hv.slc.par SCENENAME_hv.slc.par
par_MSP SCENENAME_vv.sar.par pSCENENAME_vv.slc.par SCENENAME_vv.slc.par
par_MSP SCENENAME_vh.sar.par pSCENENAME_vh.slc.par SCENENAME_vh.slc.par

# 9th, generation of the offset file. As it runs interactively, it needs to read all the default values from a text 
# file (i.e., create_offset_in). 
create_offset SCENENAME_hh.slc.par SCENENAME_vv.slc.par SCENENAME.hh_vv.slc.off < /usr/local/GAMMA_20081204/EssentialFiles/create_offset_in
#
# 10th, update of the offsets. Introduce the offset in the offset polynomial file (in the offset file).
# It is just necessary to set the offset value to +0.5 or -0.5 azimuth lines.
set t1 = `grep start_time SCENENAME_hh.slc.par |cut -c 25-36`
set t2 = `grep start_time SCENENAME_vv.slc.par |cut -c 25-36`
echo "start time HH: "$t1"   start time VV: "$t2""
set daz = `echo "$t1" "$t2" | awk '{if ($1 == $2) print 0.0; if ($1 < $2) print -0.5; if ($1 > $2) print 0.5;}'`
echo "azimuth offset:" "$daz"
set_value SCENENAME.hh_vv.slc.off SCENENAME.hh_vv.slc.off "azimuth_offset_polynomial" ""$daz" 0.0 0.0 0.0" 0.0
set_value SCENENAME.hh_vv.slc.off SCENENAME.hh_vv.slc.off "range_offset_polynomial" "0.0 0.0 0.0 0.0" 0.0
#
# 11th, co-registration. Resample the VV SLC using the offset polynomial.
SLC_interp SCENENAME_vv.slc SCENENAME_hh.slc.par SCENENAME_vv.slc.par SCENENAME.hh_vv.slc.off SCENENAME_vv.rslc SCENENAME_vv.rslc.par
SLC_interp SCENENAME_vh.slc SCENENAME_hh.slc.par SCENENAME_vh.slc.par SCENENAME.hh_vv.slc.off SCENENAME_vh.rslc SCENENAME_vh.rslc.par

# Overwrite origional SLC
mv SCENENAME_vv.rslc SCENENAME_vv.slc
mv SCENENAME_vh.rslc SCENENAME_vh.slc
mv SCENENAME_vv.rslc.par SCENENAME_vv.slc.par
mv SCENENAME_vh.rslc.par SCENENAME_vh.slc.par
#
# 12 th, generating a file with the SLC extents.
SLC_corners SCENENAME_hh.slc.par > SCENENAME_hh.slc.corners
SLC_corners SCENENAME_hv.slc.par > SCENENAME_hv.slc.corners
SLC_corners SCENENAME_vv.slc.par > SCENENAME_vv.slc.corners
SLC_corners SCENENAME_vh.slc.par > SCENENAME_vh.slc.corners
#
#
# Remove raw data
rm *.rc
rm *.raw
