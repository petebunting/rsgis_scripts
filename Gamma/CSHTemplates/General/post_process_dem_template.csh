#! /bin/csh
#
# Script to process RAW ALOS data to Level 1_1
# Created by Dan Clewley 18/04/2010
#

# Swap Bytes
swap_bytes  SCENENAME_srtm_sub SCENENAME_srtm_sub_swap 2

# Replace <= 0 with 1
set width  = `grep width  SCENENAME_srtm_sub_par | cut -d : -f 1 --complement`

replace_values SCENENAME_srtm_sub_swap 0 1 temp_dem $width 2 4

# Interpolate
# Have set to default values in gamma (SRTM has already been processed)
interp_ad temp_dem SCENENAME_srtm_sub $width - - - - 4 1

# Remove temp files
rm SCENENAME_srtm_sub_swap
rm temp_dem

# Display DEM
#disdem_par Siberia.eqa.dem_new Siberia.dem_par