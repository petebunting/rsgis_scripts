#! /bin/csh
#
# Script to geocode ALOS SLC data
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
# Modified by Dan Clewley 19/04/10 to use SRTM subset 
#
# The files that must be present are:
# - the DEM file, in big endian format, short integer, in the projection we want the SAR to be geocoded to;
# - the DEM parameter file;
# - a default offset text file called "diff_par_in".
#
#
# The first step is to create a Multi-Look Image(MLI) from the SLC
# data. The number of looks in range and azimuth was set above.
multi_look SCENENAME.hh.slc SCENENAME.hh.slc.par SCENENAME.hh.mli SCENENAME.hh.mli.par 1 4
#
# The second step is to generate a initial lookup table (LUT), that will tell us for each pixel of the DEM image
# which is the corresponding pixel in the SAR image. The file "gSCENENAME.dem.par" contains all the parameters
# for the geocoded SAR data.
gc_map SCENENAME.hh.mli.par -  SCENENAME_srtm_sub_par SCENENAME_srtm_sub gSCENENAME.dem.par gSCENENAME.dem gSCENENAME.rough.geo_to_rdc 1 1	 SCENENAME.sim.sar - - SCENENAME.inc - SCENENAME.pix
#
# The third step is to transform the Landsat image from own geocoding to geocoding map projection. As the Landsat image
# is already in the same projection of the geocoding map projection, this command will only extract the part of the
# Landsat image necessary for geocoding the SAR data. Afterwards, we need to convert it to floating point.
map_trans /data/UTM54/PAN_UTM54/pan_25m_utm54_north_par /data/UTM54/PAN_UTM54/pan_25m_utm54_north.env gSCENENAME.dem.par gSCENENAME.landsat.uchar 2 2 0 3
uchar2float gSCENENAME.landsat.uchar gSCENENAME.landsat.float   
#
# The fourth step is to refine the initial LUT, as the one produced in a previous step has locational errors
# and needs to be refined. Several procedures are needed to refine the LUT.
#
# a)we need to transform the region Landsat image from map to SAR geometry. To get the number of columns
# (width) of the Landsat image in map geometry we can use, e.g., the command "grep width gSCENENAME.dem.par". To
# get the number of samples of the Landsat image in SAR geometry we can use, e.g., the command
# "grep range_samples SCENENAME.hh.mli.par".
# For the resampling we can choose several methods, in this case we use nearest neighbour, and several
# image formats, in this case we choose float.
set w1 = `grep width gSCENENAME.dem.par |cut -d : -f 1 --complement`
set rs1 = `grep range_samples SCENENAME.hh.mli.par |cut -d : -f 1 --complement`
geocode gSCENENAME.rough.geo_to_rdc gSCENENAME.landsat.float "$w1" SCENENAME.landsat.sar "$rs1"

#
# If we want we can compare the Landsat and the actual SAR images, in radar geometry, in order to have
# a feel for the overlap between the two images.
#dis2pwr SCENENAME.landsat.sar SCENENAME.hh.mli "$rs1" "$rs1"
#
# b)To compute the offsets between the Landsat image and the actual SAR we apply a procedure similar
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
create_diff_par SCENENAME.hh.mli.par - SCENENAME.diff_par 1 < /data/UTM54/Scripts/Essential_Files/diff_par_in
#
# First guess of offsets (not required, but helpful in some cases). If the two images have small contrast,
# "init_offsetm" might lead to a wrong estimate of the constant offsets. It is therefore recommended to use
# this command with care.
init_offsetm SCENENAME.hh.mli SCENENAME.landsat.sar SCENENAME.diff_par > SCENENAME.geocode_error.txt
#
# Second, to find the local offsets we take windows all over the images and in each we compute the offset in range
# and azimuth by correlating the intensities. For the offset computation we apply a several-step procedure.
# The sequence offset_pwrm offset_fitm shall be run as many times as possible, playing with number of windows and
# window size.
offset_pwrm SCENENAME.hh.mli SCENENAME.landsat.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 128 128 gSCENENAME_offsets_hh 1 8 32
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 1 >> SCENENAME.geocode_error.txt
offset_pwrm SCENENAME.hh.mli SCENENAME.landsat.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 128 128 gSCENENAME_offsets_hh 1 16 64
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 3 >> SCENENAME.geocode_error.txt
offset_pwrm SCENENAME.hh.mli SCENENAME.landsat.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 128 128 gSCENENAME_offsets_hh 1 24 96
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 3 >> SCENENAME.geocode_error.txt
offset_pwrm SCENENAME.hh.mli SCENENAME.landsat.sar SCENENAME.diff_par gSCENENAME_offs_hh gSCENENAME_snr_hh 96 96 gSCENENAME_offsets_hh 1 24 96
offset_fitm gSCENENAME_offs_hh gSCENENAME_snr_hh SCENENAME.diff_par gSCENENAME_coffs_hh gSCENENAME_coffsets_hh - 3 >> SCENENAME.geocode_error.txt
#
# To refine the lookup table based on the offset polynomial. The new refined lookup table (*.utm_to_rdc)
# contains now at each pixel (i.e. map position) the correct position of a pixel in the SAR image. The value
# "$w1" refers to the number of columns of the SAR image in map geometry.
gc_map_fine gSCENENAME.rough.geo_to_rdc "$w1" SCENENAME.diff_par gSCENENAME.utm_to_rdc 0
#
# Before proceeding with the geocoding of the MLI image, we can check the co-registration between Landsat image in SAR geometry
# and the actual MLI image.
#geocode gSCENENAME.utm_to_rdc $landsat.gSCENENAME.float "$w1" $landsat.gSCENENAME.ref "$rs1"
#
# and display the two, for comparison;
#dis2pwr $landsat.gSCENENAME.ref SCENENAME.hh.mli "$rs1" "$rs1"
#
# Finally, to geocode the MLI images.
geocode_back SCENENAME.hh.mli "$rs1" gSCENENAME.utm_to_rdc SCENENAME.hh.utm "$w1"
#
# Generate the SUN raster file (*.ras) for the MLI geocoded image.
#raspwr SCENENAME.hh.utm "$w1" - - 10 10
#
