# Created by Pete Bunting (petebunting@mac.com)
#
# A simple script to run GDAL Warp on a set of input images (tifs).
# This script is to be used when a transformation is specified in 
# the image header and the file needs to be warped to apply the 
# transformation.
#

# Inputs:
# $1 is the input directory
# $2 is the file extension of the input images.

FILES=$1/*.$2
for f in $FILES
do
  echo "Processing $f file..."
  gdalcalcstats ${f} -ignore 0
done