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
set list_dir = `ls -d alpsba*`
#
# For each under_directory, execute the geocoding.
foreach dir_name ($list_dir)
  #
  # The files that must be present are:
  # # - the DEM file, in big endian format, short integer, in the projection we want the SAR to be geocoded to;
  # # - the DEM parameter file;
  # # - the Landsat file, in little endian format, byte, in the projection we want the SAR to be geocoded to;
  # # - the Landsat parameter file (but must state that the data is REAL*4);
  # # - a default offset text file called "diff_par_in".
  # #
  # Moving to each one of the directories to be processed
  cd $dir_name
  # If inside each directory is another directory, e.g., l1data, then the following command must be enabled
  cd l1data
  #
  # Set the name of the DEM file.
  set dem = /data/UTM55/SRTM_UTM55/shraem_qld_20000211_ab0u5_25m_bilinear_ieee_nonull_injune
  #
  # Set the name of the DEM parameter file.
  set dem_par = /data/UTM55/SRTM_UTM55/shraem_qld_20000211_ab0u5_25m_bilinear_ieee_nonull_injune.par
  #
  # Set the name of the Landsat file.
  set landsat = /data/UTM55/PAN_UTM55/pan_25m_utm55_south.env
  #
  # Set the name of the Landsat parameter file.
  set landsat_par = /data/UTM55/PAN_UTM55/pan_25m_utm55_south_par
  #
  # Set the name of the default offset parameter file
  set diff_par_in = /data/UTM55/Programs/Essential_Files/diff_par_in
  #
  # Set the names of the SLC files and corresponding ISP parameter files.
  # set image_name_hh     = `ls al*.hh.slc`
  # set image_name_hh_par = `ls al*.hh.slc.par`
  #
  # Set the name of the region where the geocoding will take place.
  set region            = utm55."$dir_name"
  #
  # Set the number of looks in range and azimuth.
  set mltlook_rg        = 2
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
  multi_look $image_name_hh $image_name_hh_par $dir_name.mli $dir_name.mli.par $mltlook_rg $mltlook_az
  #
  # The second step is to generate a initial lookup table (LUT), that will tell us for each pixel of the DEM image
  # which is the corresponding pixel in the SAR image. The file "$region.dem.par" contains all the parameters
  # for the geocoded SAR data.
  gc_map $dir_name.mli.par - $dem_par $dem $region.dem.par $region.dem $region.rough.geo_to_rdc $ovrsamp_y $ovrsamp_x - - - $dir_name.inc - $dir_name.pix
  #
  # The third step is to transform the Landsat image from own geocoding to geocoding map projection. As the Landsat image
  # is already in the same projection of the geocoding map projection, this command will only extract the part of the
  # Landsat image necessary for geocoding the SAR data. Afterwards, we need to convert it to floating point.
  map_trans $landsat_par $landsat $region.dem.par $landsat.$region.uchar 1 1 0 3
  uchar2float $landsat.$region.uchar $landsat.$region.float
  #
  # The fourth step is to refine the initial LUT, as the one produced in a previous step has locational errors
  # and needs to be refined. Several procedures are needed to refine the LUT.
  #
  # a)we need to transform the region Landsat image from map to SAR geometry. To get the number of columns
  # (width) of the Landsat image in map geometry we can use, e.g., the command "grep width $region.dem.par". To
  # get the number of samples of the Landsat image in SAR geometry we can use, e.g., the command
  # "grep range_samples $dir_name.mli.par".
  # For the resampling we can choose several methods, in this case we use nearest neighbour, and several
  # image formats, in this case we choose float.
  set w1 = `grep width $region.dem.par |cut -d : -f 1 --complement`
  set rs1 = `grep range_samples $dir_name.mli.par |cut -d : -f 1 --complement`
  geocode $region.rough.geo_to_rdc $landsat.$region.float "$w1" $landsat.$region.sar "$rs1"
  #
  # If we want we can compare the Landsat and the actual SAR images, in radar geometry, in order to have
  # a feel for the overlap between the two images.
  #dis2pwr $landsat.$region.sar $dir_name.mli "$rs1" "$rs1"
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
  create_diff_par $dir_name.mli.par - $dir_name.diff_par 1 < diff_par_in
  #
  # First guess of offsets (not required, but helpful in some cases). If the two images have small contrast,
  # "init_offsetm" might lead to a wrong estimate of the constant offsets. It is therefore recommended to use
  # this command with care.
  init_offsetm $dir_name.mli $landsat.$region.sar $dir_name.diff_par > $dir_name.geocode_error.txt
  #
  # Second, to find the local offsets we take windows all over the images and in each we compute the offset in range
  # and azimuth by correlating the intensities. For the offset computation we apply a several-step procedure.
  # The sequence offset_pwrm offset_fitm shall be run as many times as possible, playing with number of windows and
  # window size.
  offset_pwrm $dir_name.mli $landsat.$region.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 128 128 $region"_offsets_hh" 1 8 32
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 1 >> $dir_name.geocode_error.txt
  offset_pwrm $dir_name.mli $landsat.$region.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 128 128 $region"_offsets_hh" 1 16 64
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 3 >> $dir_name.geocode_error.txt
  offset_pwrm $dir_name.mli $landsat.$region.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 128 128 $region"_offsets_hh" 1 24 96
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 3 >> $dir_name.geocode_error.txt
  offset_pwrm $dir_name.mli $landsat.$region.sar $dir_name.diff_par $region"_offs_hh" $region"_snr_hh" 96 96 $region"_offsets_hh" 1 24 96
  offset_fitm $region"_offs_hh" $region"_snr_hh" $dir_name.diff_par $region"_coffs_hh" $region"_coffsets_hh" - 3 >> $dir_name.geocode_error.txt
  #
  # To refine the lookup table based on the offset polynomial. The new refined lookup table (*.utm_to_rdc)
  # contains now at each pixel (i.e. map position) the correct position of a pixel in the SAR image. The value
  # "$w1" refers to the number of columns of the SAR image in map geometry.
  gc_map_fine $region.rough.geo_to_rdc "$w1" $dir_name.diff_par $region.utm_to_rdc 0
  #
  # Before proceeding with the geocoding of the MLI image, we can check the co-registration between Landsat image in SAR geometry
  # and the actual MLI image.
  #geocode $region.utm_to_rdc $landsat.$region.float "$w1" $landsat.$region.ref "$rs1"
  #
  # and display the two, for comparison;
  #dis2pwr $landsat.$region.ref $dir_name.mli "$rs1" "$rs1"
  #
  # Finally, to geocode the MLI images.
  geocode_back $dir_name.mli "$rs1" $region.utm_to_rdc $dir_name.hh.utm "$w1"
  #
  # To check the quality of the result we can display the geocoded SAR image together with the Landsat image.
  #dis2pwr $landsat.$region.float $dir_name.hh.utm "$w1" "$w1"
  #
  # Generate the SUN raster file (*.ras) for the MLI geocoded image.
  raspwr $dir_name.hh.utm "$w1" - - 10 10
  #
  # Remove files that are no longer needed
  rm *.env
  rm *.rough.geo_to_rdc
  rm *.sar
  rm *.float
  rm *.dem
  rm *.uchar
  #
  # Move to the root directory
  cd ..
  # If inside each directory is another directory, e.g., l1data, then the
  # following command must be enabled
  cd ..
#
end
