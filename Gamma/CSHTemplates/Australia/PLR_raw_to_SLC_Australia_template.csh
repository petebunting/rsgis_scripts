#! /bin/csh
#
# Script to process RAW ALOS data to Level 1_1
# Created by Joao Carreiras
#
# Modified by Dan Clewley 01/02/10 to run single scene only
# Modified by Dan Clewley 16/02/10 as template for BatchGamma.py

#
# From this point forward is just the processing from 1.0 (raw) to 1.1 (SLC).
#
# 1st, generation of the SAR sensor parameter file, and MSP parameter file.
PALSAR_proc LEDFILENAME SCENENAME.hh.sar.par pSCENENAME.hh.slc.par HHFILENAME SCENENAME.hh.raw 0 0
PALSAR_proc LEDFILENAME SCENENAME.hv.sar.par pSCENENAME.hv.slc.par HVFILENAME SCENENAME.hv.raw 0 1
PALSAR_proc LEDFILENAME SCENENAME.vv.sar.par pSCENENAME.vv.slc.par VVFILENAME SCENENAME.vv.raw 1 1
PALSAR_proc LEDFILENAME SCENENAME.vh.sar.par pSCENENAME.vh.slc.par VVFILENAME SCENENAME.vh.raw 1 1
#
# 2nd, generation of the calibration file and update of the SAR sensor parameter file using the external calibration file.
PALSAR_antpat SCENENAME.hh.sar.par pSCENENAME.hh.slc.par /usr/local/GAMMA_20081204/MSP_v11.5/sensors/palsar_ant_20061024.dat SCENENAME.hh.PALSAR_antpat_MSP.dat - 0 0
PALSAR_antpat SCENENAME.hv.sar.par pSCENENAME.hv.slc.par /usr/local/GAMMA_20081204/MSP_v11.5/sensors/palsar_ant_20061024.dat SCENENAME.hv.PALSAR_antpat_MSP.dat - 0 1
PALSAR_antpat SCENENAME.vv.sar.par pSCENENAME.vv.slc.par /usr/local/GAMMA_20081204/MSP_v11.5/sensors/palsar_ant_20061024.dat SCENENAME.vv.PALSAR_antpat_MSP.dat - 1 1
PALSAR_antpat SCENENAME.vh.sar.par pSCENENAME.vh.slc.par /usr/local/GAMMA_20081204/MSP_v11.5/sensors/palsar_ant_20061024.dat SCENENAME.vh.PALSAR_antpat_MSP.dat - 1 0
#
# 3rd, determine the Doppler ambiguity.
dop_mlcc SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.raw SCENENAME.hh.mlcc
dop_mlcc SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.raw SCENENAME.hv.mlcc
dop_mlcc SCENENAME.vv.sar.par pSCENENAME.vv.slc.par SCENENAME.vv.raw SCENENAME.vv.mlcc
dop_mlcc SCENENAME.vh.sar.par pSCENENAME.vh.slc.par SCENENAME.vh.raw SCENENAME.vh.mlcc
#
# 4th, estimation of Doppler centroid. The different polarisations present different start times.
# For this reason, estimation of the Doppler centroid is done for one polarisation (e.g., HH), 
# and the Doppler centroid and effective velocity are copied to the parameter file of the other polarisation.
# In this way, all the images will have the same geometry and phase reference, i.e., they will all overlap.
# For this, use the program "doppler" first on the master polarisation (e.g., HH) and then the program "set_value"
# to update the MSP processing parameter files of the other polarisation.
doppler SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.raw SCENENAME.hh.dop
set a1 = `grep doppler_polynomial pSCENENAME.hh.slc.par |cut -d : -f 1 --complement`
set_value pSCENENAME.hv.slc.par pSCENENAME.hv.slc.par "doppler_polynomial" "$a1" 0
set_value pSCENENAME.vv.slc.par pSCENENAME.vv.slc.par "doppler_polynomial" "$a1" 0
set_value pSCENENAME.vh.slc.par pSCENENAME.vh.slc.par "doppler_polynomial" "$a1" 0
#
# 5th, range compression.
pre_rc SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.raw SCENENAME.hh.rc - - - - - - - - 1 -
pre_rc SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.raw SCENENAME.hv.rc - - - - - - - - 1 -
pre_rc SCENENAME.vv.sar.par pSCENENAME.vv.slc.par SCENENAME.vv.raw SCENENAME.vv.rc - - - - - - - - 1 -
pre_rc SCENENAME.vh.sar.par pSCENENAME.vh.slc.par SCENENAME.vh.raw SCENENAME.vh.rc - - - - - - - - 1 -
#
# 6th, estimate autofocus (twice) for one polarisation (e.g., HH) and copy the effective velocity to the other MSP 
# parameter file, so that all polarisation channels will be identical.
autof SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.rc SCENENAME.hh.af 5.0 1 4096
autof SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.rc SCENENAME.hh.af 5.0 1 4096
set a2 = `grep sensor_velocity_vector pSCENENAME.hh.slc.par |cut -d : -f 1 --complement`
set_value pSCENENAME.hv.slc.par pSCENENAME.hv.slc.par "sensor_velocity_vector" "$a2" 0
set_value pSCENENAME.vv.slc.par pSCENENAME.vv.slc.par "sensor_velocity_vector" "$a2" 0
set_value pSCENENAME.vh.slc.par pSCENENAME.vh.slc.par "sensor_velocity_vector" "$a2" 0

#
# 7th, azimuth compression.
az_proc SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.rc SCENENAME.hh.slc 16384 0 -45.4 0 2.12
az_proc SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.rc SCENENAME.hv.slc 16384 0 -53.6 0 2.12
az_proc SCENENAME.vv.sar.par pSCENENAME.vv.slc.par SCENENAME.vv.rc SCENENAME.vv.slc 16384 0 -43.9 0 2.12
az_proc SCENENAME.vh.sar.par pSCENENAME.vh.slc.par SCENENAME.vh.rc SCENENAME.vh.slc 16384 0 -54.5 0 2.12

#
# 8th, generating the ISP parameter files.
par_MSP SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.slc.par
par_MSP SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.slc.par
par_MSP SCENENAME.vv.sar.par pSCENENAME.vv.slc.par SCENENAME.vv.slc.par
par_MSP SCENENAME.vh.sar.par pSCENENAME.vh.slc.par SCENENAME.vh.slc.par

# 9th, generation of the offset file. As it runs interactively, it needs to read all the default values from a text 
# file (i.e., create_offset_in). 
create_offset SCENENAME.hh.slc.par SCENENAME.vv.slc.par SCENENAME.hh_vv.slc.off < /usr/local/GAMMA_20081204/EssentialFiles/create_offset_in
#
# 10th, update of the offsets. Introduce the offset in the offset polynomial file (in the offset file).
# It is just necessary to set the offset value to +0.5 or -0.5 azimuth lines.
set t1 = `grep start_time SCENENAME.hh.slc.par |cut -c 25-36`
set t2 = `grep start_time SCENENAME.vv.slc.par |cut -c 25-36`
echo "start time HH: "$t1"   start time VV: "$t2""
set daz = `echo "$t1" "$t2" | awk '{if ($1 == $2) print 0.0; if ($1 < $2) print -0.5; if ($1 > $2) print 0.5;}'`
echo "azimuth offset:" "$daz"
set_value SCENENAME.hh_vv.slc.off SCENENAME.hh_vv.slc.off "azimuth_offset_polynomial" ""$daz" 0.0 0.0 0.0" 0.0
set_value SCENENAME.hh_vv.slc.off SCENENAME.hh_vv.slc.off "range_offset_polynomial" "0.0 0.0 0.0 0.0" 0.0
#
# 11th, co-registration. Resample the VV SLC using the offset polynomial.
SLC_interp SCENENAME.vv.slc SCENENAME.hh.slc.par SCENENAME.vv.slc.par SCENENAME.hh_vv.slc.off SCENENAME.vv.rslc SCENENAME.vv.rslc.par
SLC_interp SCENENAME.vh.slc SCENENAME.hh.slc.par SCENENAME.vh.slc.par SCENENAME.hh_vv.slc.off SCENENAME.vh.rslc SCENENAME.vh.rslc.par

# Overwrite origional SLC
mv SCENENAME.vv.rslc SCENENAME.vv.slc
mv SCENENAME.vh.rslc SCENENAME.vh.slc
mv SCENENAME.vv.rslc.par SCENENAME.vv.slc.par
mv SCENENAME.vh.rslc.par SCENENAME.vh.slc.par
#
# 12 th, generating a file with the SLC extents.
SLC_corners SCENENAME.hh.slc.par > SCENENAME.hh.slc.corners
SLC_corners SCENENAME.hv.slc.par > SCENENAME.hv.slc.corners
SLC_corners SCENENAME.vv.slc.par > SCENENAME.vv.slc.corners
SLC_corners SCENENAME.vh.slc.par > SCENENAME.vh.slc.corners
#
#
# Remove raw data
rm *ALPSRP*
rm *.rc
rm *.raw