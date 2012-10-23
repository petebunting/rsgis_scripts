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
# The first thing is to assign a list of the directories with the data to be processed to a variable.
set list_dir = `ls -d  alpsba*`
#
# Then, in each sub-directory, process the data from 1.0 (raw) to 1.1 (SLC).
foreach dir_name ($list_dir)
  #
  # Change to each directory to be processed.
  cd $dir_name
  # If inside each directory is another directory, e.g., l1data, then the
  # following command must be enabled
  cd l1data
  #
  # Assign the antenna pattern file to a variable.
  set ant_pat = /data/UTM55/Programs/Essential_Files/palsar_ant_20061024.dat
  #
  # Assign the file with the raw data to a variable.
  set image_name = `ls IMG*`
  # Assign the leader file to a variable.
  set leader_name = `ls LED*`
  #
  # From this point forward is just the processing from 1.0 (raw) to 1.1 (SLC).
  #
  # 1st, generation of the SAR sensor parameter file, and MSP parameter file.
  PALSAR_proc $leader_name $dir_name.hh.sar.par p$dir_name.hh.slc.par $image_name $dir_name.hh.raw 0 0
  #
  # 2nd, generation of the calibration file and update of the SAR sensor parameter file using the external calibration file.
  PALSAR_antpat $dir_name.hh.sar.par p$dir_name.hh.slc.par $ant_pat $dir_name.hh.PALSAR_antpat_MSP.dat - 0 0
  #
  # 3rd, determine the Doppler ambiguity.
  dop_mlcc $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.raw $dir_name.hh.mlcc
  #
  # 4th, estimation of Doppler centroid.
  doppler $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.raw $dir_name.hh.dop
  #
  # 5th, range compression.
  pre_rc $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.raw $dir_name.hh.rc - - - - - - - - 1 -
  #
  # 6th, autofocus twice.
  autof $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.rc $dir_name.hh.af 5.0 1 4096
  autof $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.rc $dir_name.hh.af 5.0 1 4096
  #
  # 7th, azimuth compression.
  az_proc $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.rc $dir_name.hh.slc 16384 0 -51.9 0 2.12
  #
  # 8th, generating the ISP parameter file.
  par_MSP $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.slc.par
  #
  # 9th, generating a file with the SLC extents.
  SLC_corners $dir_name.hh.slc.par > $dir_name.hh.slc.corners
  #
  # 10th, generating a SUN raster image of SLC intensity image.
  # First, we need to get the number of samples in the SLC image
  set rs = `grep range_pixels p$dir_name.hh.slc.par |cut -d : -f 1 --complement`
  # and now we generate a SUN raster image (*.ras), averaged 10 x in range and 10x in azimuth.
  rasSLC $dir_name.hh.slc "$rs" - - 10 10
  #
  # Remove files that are no longer needed.
  rm *.raw
  rm *.rc
  #
  # Change to the root-level directory.
  cd ..
  # If inside each directory is another directory, e.g., l1data, then the
  # following command must be enabled
  cd ..
#
end
