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
#
# 2nd, generation of the calibration file and update of the SAR sensor parameter file using the external calibration file.
PALSAR_antpat SCENENAME.hh.sar.par pSCENENAME.hh.slc.par /usr/local/GAMMA_20080630/MSP_v11.5/sensors/palsar_ant_20061024.dat SCENENAME.hh.PALSAR_antpat_MSP.dat - 0 0
PALSAR_antpat SCENENAME.hv.sar.par pSCENENAME.hv.slc.par /usr/local/GAMMA_20080630/MSP_v11.5/sensors/palsar_ant_20061024.dat SCENENAME.hv.PALSAR_antpat_MSP.dat - 0 1
#
# 3rd, determine the Doppler ambiguity.
dop_mlcc SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.raw SCENENAME.hh.mlcc
dop_mlcc SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.raw SCENENAME.hv.mlcc
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
#
# 5th, range compression.
pre_rc SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.raw SCENENAME.hh.rc - - - - - - - - 1 -
pre_rc SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.raw SCENENAME.hv.rc - - - - - - - - 1 -
#
# 6th, estimate autofocus (twice) for one polarisation (e.g., HH) and copy the effective velocity to the other MSP 
# parameter file, so that all polarisation channels will be identical.
autof SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.rc SCENENAME.hh.af 5.0 1 4096
autof SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.rc SCENENAME.hh.af 5.0 1 4096
set a2 = `grep sensor_velocity_vector pSCENENAME.hh.slc.par |cut -d : -f 1 --complement`
set_value pSCENENAME.hv.slc.par pSCENENAME.hv.slc.par "sensor_velocity_vector" "$a2" 0
#
# 7th, azimuth compression.
az_proc SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.rc SCENENAME.hh.slc 16384 0 -51.8 0 2.12
az_proc SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.rc SCENENAME.hv.slc 16384 0 -58.3 0 2.12
#
# 8th, generating the ISP parameter files.
par_MSP SCENENAME.hh.sar.par pSCENENAME.hh.slc.par SCENENAME.hh.slc.par
par_MSP SCENENAME.hv.sar.par pSCENENAME.hv.slc.par SCENENAME.hv.slc.par
#
# 9th, generating a file with the SLC extents.
SLC_corners SCENENAME.hh.slc.par > SCENENAME.hh.slc.corners
SLC_corners SCENENAME.hv.slc.par > SCENENAME.hv.slc.corners
#
# 10th, generating SUN raster image of SLC intensity images.
# First, we need to get the number of samples in the SLC image
set rs = `grep range_pixels pSCENENAME.hh.slc.par |cut -d : -f 1 --complement`
# and now we generate the SUN raster images (*.ras), averaged 10x in range and 10x in azimuth.
rasSLC SCENENAME.hh.slc "$rs" - - 10 10
rasSLC SCENENAME.hv.slc "$rs" - - 10 10
#
# Remove raw data
rm *ALPSRP*
rm *.rc
rm *.raw