#! /bin/csh
#
# Script to geocode ALOS SLC data
# Created by Joao Carreiras
#
# Modified by Dan Clewley 01/02/10 to run single scene only
# Modified by Dan Clewley 16/02/10 as template for BatchGamma.py

#
# The files that must be present are:
# - the DEM file, in big endian format, short integer, in the projection we want the SAR to be geocoded to;
# - the DEM parameter file;
# - a default offset text file called "diff_par_in".
#
#
# The first step is to create a Multi-Look Image(MLI) from the SLC
# data. The number of looks in range and azimuth was set above.
multi_look SCENENAME.hh.slc SCENENAME.hh.slc.par SCENENAME.hh.mli SCENENAME.hh.mli.par 1 5
multi_look SCENENAME.hv.slc SCENENAME.hv.slc.par SCENENAME.hv.mli SCENENAME.hv.mli.par 1 5
#
# The second step is to generate a initial lookup table (LUT), that will tell us for each pixel of the DEM image
# which is the corresponding pixel in the SAR image. The file "gSCENENAME.dem.par" contains all the parameters
# for the geocoded SAR data.
gc_map SCENENAME.hh.mli.par -  SCENENAME_srtm_sub_par SCENENAME_srtm_sub gSCENENAME.dem.par gSCENENAME.dem gSCENENAME.rough.utm_to_rdc 1 1 SCENENAME.sim.sar - - SCENENAME.inc - SCENENAME.pix
#
# The third step is to refine the initial LUT, as the one produced in a previous step has locational errors
# and needs to be refined. Several procedures are needed to refine the LUT.
#
# a)we need to transform the region simulated SAR image from map to SAR geometry. To get the number of columns"
# (width) of the simulated SAR image in map geometry we can use, e.g., the command "grep width gSCENENAME.dem.par". To
# get the number of samples of the simulated SAR image in SAR geometry we can use, e.g., the command
# "grep range_samples SCENENAME.hh.mli.par".
# For the resampling we can choose several methods, in this case we use nearest neighbour, and several
# image formats, in this case we choose float.
set w1 = `grep width gSCENENAME.dem.par |cut -d : -f 1 --complement`
set rs1 = `grep range_samples SCENENAME.hh.mli.par |cut -d : -f 1 --complement`
geocode gSCENENAME.rough.utm_to_rdc SCENENAME.sim.sar "$w1" SCENENAME.sim.sar.sar "$rs1"
#
# b)To compute the offsets between the simulated SAR image and the actual SAR we apply a procedure similar
# to the co-registration of two SLC images for interferometry. First of all we need to generate a file
# (text file) in which the offsets will be stored (diff_par_in).To start with we accept all default
# values. As this command runs interactively, create a text file with the required values and then pass it to 
# the command. In this case we will create first a file called "diff_par_in" with the required values, which is 
# this case are the defaults:
# scene title: ?????
# range, azimuth offsets of image-2 relative to image-1 (samples):  0  0
# enter number of offset measurements in range, azimuth:  16  16
# search window sizes (32, 64, 128...) (range, azimuth):  256  256
# minimum matching SNR (nominal=6.5):      7.000
create_diff_par SCENENAME.hh.mli.par - SCENENAME.diff_par 1 < /usr/local/GAMMA_20081204/EssentialFiles/diff_par_in
#
# First guess of offsets (not required, but helpful in some cases). If the two images have small contrast,
# "init_offsetm" might lead to a wrong estimate of the constant offsets. It is therefore recommended to use
# this command with care.
init_offsetm SCENENAME.hh.mli SCENENAME.sim.sar.sar SCENENAME.diff_par > SCENENAME.geocode_error.txt
#
# Second, to find the local offsets we take windows all over the images and in each we compute the offset in range
# and azimuth by correlating the intensities. For the offset computation we apply a several-step procedure.
# The sequence offset_pwrm offset_fitm shall be run as many times as possible, playing with number of windows and
# window size.
offset_pwrm SCENENAME.hh.mli SCENENAME.sim.sar.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 128 128 gSCENENAME_offsets_hh 1 8 32
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 1 >> SCENENAME.geocode_error.txt
offset_pwrm SCENENAME.hh.mli SCENENAME.sim.sar.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 128 128 gSCENENAME_offsets_hh 1 16 64
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 3 >> SCENENAME.geocode_error.txt
offset_pwrm SCENENAME.hh.mli SCENENAME.sim.sar.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 128 128 gSCENENAME_offsets_hh 1 24 96
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 3 >> SCENENAME.geocode_error.txt
offset_pwrm SCENENAME.hh.mli SCENENAME.sim.sar.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 96 96 gSCENENAME_offsets_hh 1 24 96
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 3 >> SCENENAME.geocode_error.txt
#
# To refine the lookup table based on the offset polynomial. The new refined lookup table (*.utm_to_rdc)
# contains now at each pixel (i.e. map position) the correct position of a pixel in the SAR image. The value
# "$w1" refers to the number of columns of the SAR image in map geometry.
gc_map_fine gSCENENAME.rough.utm_to_rdc "$w1" SCENENAME.diff_par gSCENENAME.utm_to_rdc 0
#
# Finally, to geocode the MLI images.
geocode_back SCENENAME.hh.mli "$rs1" gSCENENAME.utm_to_rdc SCENENAME.hh.utm "$w1"
geocode_back SCENENAME.hv.mli "$rs1" gSCENENAME.utm_to_rdc SCENENAME.hv.utm "$w1"
#
# Generate the SUN raster file (*.ras) for the MLI geocoded image.
#raspwr SCENENAME.hh.utm "$w1" - - 10 10
#raspwr SCENENAME.hv.utm "$w1" - - 10 10
#
# Remove files that are no longer needed
#rm *.env
#rm *.slc
#rm *.slc.par
#rm *.mli
#rm *.mli.par
#rm *.rough.utm_to_rdc
#rm *.sar
#rm *.dem
#
