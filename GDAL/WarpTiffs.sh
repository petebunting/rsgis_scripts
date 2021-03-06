# Created by Pete Bunting (petebunting@mac.com)
#
# A simple script to run GDAL Warp on a set of input images (tifs).
# This script is to be used when a transformation is specified in 
# the image header and the file needs to be warped to apply the 
# transformation.
#

# Inputs:
# $1 is the input directory 
# $2 is the output directory
# $3 is the output file format (GDAL driver)
# $4 is the file extension for the output format.

FILES=$1/*.tif
for f in $FILES
do
  echo "Processing $f file..."
  filename=`basename ${f} .tif`
  echo "Output: ${2}/${filename}_warp.tif"
  gdalwarp -overwrite -r cubic -multi -wt Float32 -of GTIFF -co "TILED=YES COMPRESS=DEFLATE ZLEVEL=1" ${f} ${2}/${filename}_warp.tif
  gdalcalcstats ${2}/${filename}_warp.tif -ignore 0
done