#! /bin/csh
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
  # Assign the file that has the offset defaults, for co-registration.
  set create_offset_in = /data/UTM55/Programs/Essential_Files/create_offset_in
  #
  # Assign the file with the HH raw data to a variable.
  set image_name_hh  = `ls IMG-HH*`
  # Assign the file with the HV raw data to a variable.
  set image_name_hv  = `ls IMG-HV*`
  # Assign the file with the VV raw data to a variable.
  set image_name_vv  = `ls IMG-VV*`
  # Assign the leader file to a variable.
  set leader_name    = `ls LED*`
  #
  # From this point forward is just the processing from 1.0 (raw) to 1.1 (SLC).
  #
  # 1st, generation of the SAR sensor parameter file, and MSP parameter file.
  PALSAR_proc $leader_name $dir_name.hh.sar.par p$dir_name.hh.slc.par $image_name_hh $dir_name.hh.raw 0 0
  PALSAR_proc $leader_name $dir_name.hv.sar.par p$dir_name.hv.slc.par $image_name_hv $dir_name.hv.raw 0 1
  PALSAR_proc $leader_name $dir_name.vv.sar.par p$dir_name.vv.slc.par $image_name_vv $dir_name.vv.raw 1 1
  #
  # 2nd, generation of the calibration file and update of the SAR sensor parameter file using the external calibration file.
  PALSAR_antpat $dir_name.hh.sar.par p$dir_name.hh.slc.par $ant_pat $dir_name.hh.PALSAR_antpat_MSP.dat - 0 0
  PALSAR_antpat $dir_name.hv.sar.par p$dir_name.hv.slc.par $ant_pat $dir_name.hv.PALSAR_antpat_MSP.dat - 0 1
  PALSAR_antpat $dir_name.vv.sar.par p$dir_name.vv.slc.par $ant_pat $dir_name.vv.PALSAR_antpat_MSP.dat - 1 1
  #
  # 3rd, determine the Doppler ambiguity.
  dop_mlcc $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.raw $dir_name.hh.mlcc
  dop_mlcc $dir_name.hv.sar.par p$dir_name.hv.slc.par $dir_name.hv.raw $dir_name.hv.mlcc
  dop_mlcc $dir_name.vv.sar.par p$dir_name.vv.slc.par $dir_name.vv.raw $dir_name.vv.mlcc
  #
  # 4th, estimation of Doppler centroid. The different polarisations present different start times.
  # For this reason, estimation of the Doppler centroid is done for one polarisation (e.g., HH), 
  # and the Doppler centroid and effective velocity are copied to the parameter files of the other polarisations.
  # In this way, all the images will have the same geometry and phase reference, i.e., they will all overlap.
  # For this, use the program "doppler" first on the master polarisation (e.g., HH) and then the program "set_value"
  # to update the MSP processing parameter files of the other polarisations.
  doppler $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.raw $dir_name.hh.dop
  set a1 = `grep doppler_polynomial p$dir_name.hh.slc.par |cut -d : -f 1 --complement`
  set_value p$dir_name.hv.slc.par p$dir_name.hv.slc.par "doppler_polynomial" "$a1" 0
  set_value p$dir_name.vv.slc.par p$dir_name.vv.slc.par "doppler_polynomial" "$a1" 0
  #
  # 5th, range compression
  pre_rc $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.raw $dir_name.hh.rc - - - - - - - - 1 -
  pre_rc $dir_name.hv.sar.par p$dir_name.hv.slc.par $dir_name.hv.raw $dir_name.hv.rc - - - - - - - - 1 -
  pre_rc $dir_name.vv.sar.par p$dir_name.vv.slc.par $dir_name.vv.raw $dir_name.vv.rc - - - - - - - - 1 -
  #
  # 6th, estimate autofocus (twice) for one polarisation (e.g., HH) and copy the effective velocity to the other MSP
  # parameter files, so that all polarisation channels will be identical. 
  autof $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.rc $dir_name.hh.af 5.0 1 4096
  autof $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.rc $dir_name.hh.af 5.0 1 4096
  set a2 = `grep sensor_velocity_vector p$dir_name.hh.slc.par |cut -d : -f 1 --complement`
  set_value p$dir_name.hv.slc.par p$dir_name.hv.slc.par "sensor_velocity_vector" "$a2" 0
  set_value p$dir_name.vv.slc.par p$dir_name.vv.slc.par "sensor_velocity_vector" "$a2" 0
  #
  # 7th, azimuth compression.
  az_proc $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.rc $dir_name.hh.slc 16384 0 -45.4 0 2.12
  az_proc $dir_name.hv.sar.par p$dir_name.hv.slc.par $dir_name.hv.rc $dir_name.hv.slc 16384 0 -53.6 0 2.12
  az_proc $dir_name.vv.sar.par p$dir_name.vv.slc.par $dir_name.vv.rc $dir_name.vv.slc 16384 0 -43.9 0 2.12
  #
  # For PALSAR fully polarimetric data additional resampling is necessary because there is a half line shift 
  # in azimuth between the HH and the VV channel. For the resampling, the ISP programs should be used. Notice that 
  # the HH and the HV channels are co-registered, as well as the VV and VH channels.
  #
  # 8th, generating the ISP parameter files.
  par_MSP $dir_name.hh.sar.par p$dir_name.hh.slc.par $dir_name.hh.slc.par
  par_MSP $dir_name.hv.sar.par p$dir_name.hv.slc.par $dir_name.hv.slc.par
  par_MSP $dir_name.vv.sar.par p$dir_name.vv.slc.par $dir_name.vv.slc.par
  #
  # 9th, generation of the offset file. As it runs interactively, it needs to read all the default values from a text 
  # file (i.e., create_offset_in). 
  create_offset $dir_name.hh.slc.par $dir_name.vv.slc.par $dir_name.hh_vv.slc.off < $create_offset_in
  #
  # 10th, update of the offsets. Introduce the offset in the offset polynomial file (in the offset file).
  # It is just necessary to set the offset value to +0.5 or -0.5 azimuth lines.
  set t1 = `grep start_time $dir_name.hh.slc.par |cut -c 25-36`
  set t2 = `grep start_time $dir_name.vv.slc.par |cut -c 25-36`
  echo "start time HH: "$t1"   start time VV: "$t2""
  set daz = `echo "$t1" "$t2" | awk '{if ($1 == $2) print 0.0; if ($1 < $2) print -0.5; if ($1 > $2) print 0.5;}'`
  echo "azimuth offset:" "$daz"
  set_value $dir_name.hh_vv.slc.off $dir_name.hh_vv.slc.off "azimuth_offset_polynomial" ""$daz" 0.0 0.0 0.0" 0.0
  set_value $dir_name.hh_vv.slc.off $dir_name.hh_vv.slc.off "range_offset_polynomial" "0.0 0.0 0.0 0.0" 0.0
  #
  # 11th, co-registration. Resample the VV SLC using the offset polynomial.
  SLC_interp $dir_name.vv.slc $dir_name.hh.slc.par $dir_name.vv.slc.par $dir_name.hh_vv.slc.off $dir_name.vv.rslc $dir_name.vv.rslc.par
  #
  # 12th, generating the files with the SLC extents.
  SLC_corners $dir_name.hh.slc.par > $dir_name.hh.slc.corners
  SLC_corners $dir_name.hv.slc.par > $dir_name.hv.slc.corners
  SLC_corners $dir_name.vv.rslc.par > $dir_name.vv.rslc.corners
  #
  # 13th, Generating the SUN raster images of SLC intensity images.
  # First, we need to get the number of samples in the SLC image
  set rs = `grep range_pixels p$dir_name.hh.slc.par |cut -d : -f 1 --complement`
  # and now we generate the SUN raster images (*.ras), averaged 10 x in range and 10x in azimuth.
  rasSLC $dir_name.hh.slc "$rs" - - 10 10
  rasSLC $dir_name.hv.slc "$rs" - - 10 10
  rasSLC $dir_name.vv.rslc "$rs" - - 10 10
  #
  # Remove files that are no longer needed.
  rm *.raw
  rm *.rc
  # Change to the root-level directory.
  cd ..
  # If inside each directory is another directory, e.g., l1data, then the
  # following command must be enabled
  cd ..
#
end
