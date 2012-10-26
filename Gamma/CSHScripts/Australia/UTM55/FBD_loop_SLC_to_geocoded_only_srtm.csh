#! /bin/csh
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
# Create a list of the under-directories, where the SLC data is located.
set list_dir = `ls -d al*`
#
# For each under_directory, execute the geocoding.
foreach dir_name ($list_dir)
  #
  # The files that must be present are:
  # - the DEM file, in big endian format, short integer, in the projection we want the SAR to be geocoded to;
  # - the DEM parameter file;
  # - a default offset text file called "diff_par_in".
  # Moving to each one of the directories to be processed
  cd $dir_name
  # If inside each directory is another directory, e.g., l1data, then the
  # following command must be enabled
  cd l1data
  #
  # Copy all the required files from the root directory to each "l1data" directory
  cp /media/QUEENSLAND1/alos/Australia/utm_56/srtm/shraem_aus_20000211_g0_z56_utmS_50m_ieee_rpj.env .
  cp /media/QUEENSLAND1/alos/Australia/utm_56/srtm/srtm_utm56_par_new .
  cp /media/QUEENSLAND1/Essential_Files/diff_par_in .
  #
  # Set the name of the DEM file.
  set dem = shraem_aus_20000211_g0_z56_utmS_50m_ieee_rpj.env
  #
  # Set the name of the DEM parameter file.
  set dem_par = srtm_utm56_par_new
  #
  # Set the names of the SLC files and corresponding ISP parameter files.
  set image_name_hh     = `ls al*.hh.slc`
  set image_name_hh_par = `ls al*.hh.slc.par`
  set image_name_hv     = `ls al*.hv.slc`
  set image_name_hv_par = `ls al*.hv.slc.par`
  #
  # Set the name of the region where the geocoding will take place.
  set region            = utm56."$dir_name"
  #
  # Set the number of looks in range and azimuth.
  set mltlook_rg        = 1
  set mltlook_az        = 5
  #
  # Set the oversampling for the DEM image. E.g., if the DEM image has 50 m spatial 
  # resolution, and we want to geocode an MLI image to 12.5 m, then the oversampling factor 
  # would be 4 in X and Y.
  set ovrsamp_x         = 4
  set ovrsamp_y         = 4
  #
  # The first step is to create a Multi-Look Image(MLI) from the SLC
  # data. The number of looks in range and azimuth was set above.
  multi_look $image_name_hh $image_name_hh_par $dir_name.hh.mli $dir_name.hh.mli.par $mltlook_rg $mltlook_az
  multi_look $image_name_hv $image_name_hv_par $dir_name.hv.mli $dir_name.hv.mli.par $mltlook_rg $mltlook_az
  #
  # The second step is to generate a initial lookup table (LUT), that will tell us for each pixel of the DEM image
  # which is the corresponding pixel in the SAR image. The file "$region.dem.par" contains all the parameters
  # for the geocoded SAR data.
  gc_map $dir_name.hh.mli.par - $dem_par $dem $region.dem.par $region.dem $region.rough.geo_to_rdc $ovrsamp_y $ovrsamp_x $dir_name.sim.sar - - $dir_name.inc
  #
  # The third step is to refine the initial LUT, as the one produced in a previous step has locational errors
  # and needs to be refined. Several procedures are needed to refine the LUT.
  #
  # a)we need to transform the region simulated SAR image from map to SAR geometry. To get the number of columns
  # (width) of the simulated SAR image in map geometry we can use, e.g., the command "grep width $region.dem.par". To
  # get the number of samples of the simulated SAR image in SAR geometry we can use, e.g., the command
  # "grep range_samples $dir_name.hh.mli.par".
  # For the resampling we can choose several methods, in this case we use nearest neighbour, and several
  # image formats, in this case we choose float.
  set w1 = `grep width $region.dem.par |cut -d : -f 1 --complement`
  set rs1 = `grep range_samples $dir_name.hh.mli.par |cut -d : -f 1 --complement`
  geocode $region.rough.geo_to_rdc $dir_name.sim.sar "$w1" $dir_name.sim.sar.sar "$rs1"
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
  create_diff_par $dir_name.hh.mli.par - $dir_name.diff_par 1 < diff_par_in
  #
  # First guess of offsets (not required, but helpful in some cases). If the two images have small contrast,
  # "init_offsetm" might lead to a wrong estimate of the constant offsets. It is therefore recommended to use
  # this command with care.
  init_offsetm $dir_name.hh.mli $dir_name.sim.sar.sar $dir_name.diff_par > $dir_name.geocode_error.txt
  #
  # Second, to find the local offsets we take windows all over the images and in each we compute the offset in range
  # and azimuth by correlating the intensities. For the offset computation we apply a several-step procedure.
  # The sequence offset_pwrm offset_fitm shall be run as many times as possible, playing with number of windows and
  # window size.
  offset_pwrm $dir_name.hh.mli $dir_name.sim.sar.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 128 128 $region"_offsets_hh" 1 8 32
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 1 >> $dir_name.geocode_error.txt
  offset_pwrm $dir_name.hh.mli $dir_name.sim.sar.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 128 128 $region"_offsets_hh" 1 16 64
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 3 >> $dir_name.geocode_error.txt
  offset_pwrm $dir_name.hh.mli $dir_name.sim.sar.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 128 128 $region"_offsets_hh" 1 24 96
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 3 >> $dir_name.geocode_error.txt
  offset_pwrm $dir_name.hh.mli $dir_name.sim.sar.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 96 96 $region"_offsets_hh" 1 24 96
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 3 >> $dir_name.geocode_error.txt
  #
  # To refine the lookup table based on the offset polynomial. The new refined lookup table (*.geo_to_rdc)
  # contains now at each pixel (i.e. map position) the correct position of a pixel in the SAR image. The value
  # "$w1" refers to the number of columns of the SAR image in map geometry.
  gc_map_fine $region.rough.geo_to_rdc "$w1" $dir_name.diff_par $region.geo_to_rdc 0
  #
  # Finally, to geocode the MLI images.
  geocode_back $dir_name.hh.mli "$rs1" $region.geo_to_rdc $dir_name.hh.utm "$w1"
  geocode_back $dir_name.hv.mli "$rs1" $region.geo_to_rdc $dir_name.hv.utm "$w1"
  #
  # Generate the SUN raster file (*.ras) for the MLI geocoded image.
  raspwr $dir_name.hh.utm "$w1" - - 10 10
  raspwr $dir_name.hv.utm "$w1" - - 10 10
  #
  # Remove files that are no longer needed
  rm *.env
  rm *.rough.geo_to_rdc
  rm *.sar
  rm l7tmpa*
  rm *.dem
  #
  # Move to the root directory
  cd ..
  # If inside each directory is another directory, e.g., l1data, then the
  # following command must be enabled
  cd ..
#
end
