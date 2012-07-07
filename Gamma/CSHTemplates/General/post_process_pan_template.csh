#! /bin/csh
#
# Script to process RAW ALOS data to Level 1_1
# Created by Dan Clewley 18/04/2010
#

# Swap Bytes
swap_bytes  SCENENAME_pan_sub SCENENAME_pan_sub_swap 2

mv SCENENAME_pan_sub_swap SCENENAME_pan_sub

# Display DEM
#disdem_par Siberia.eqa.dem_new Siberia.dem_par
