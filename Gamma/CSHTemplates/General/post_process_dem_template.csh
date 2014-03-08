#! /bin/csh
#
# Script to post-process DEM
#
# Created by Dan Clewley (IGES/AU).
# Copyright 2012 Dan Clewley. All rights reserved.
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
# Swap Bytes
swap_bytes  SCENENAME_srtm_sub SCENENAME_srtm_sub_swap 4

# Replace <= 0 with 1
set width  = `grep width  SCENENAME_srtm_sub_par | cut -d : -f 1 --complement`

replace_values SCENENAME_srtm_sub_swap 0 1 temp_dem $width 2 2

# Interpolate
# Have set to default values in gamma (SRTM has already been processed)
interp_ad temp_dem SCENENAME_srtm_sub $width - - - - 2 1

# Remove temp files
rm SCENENAME_srtm_sub_swap
rm temp_dem
