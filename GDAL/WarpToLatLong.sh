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
# $3 input image file extension

FILES=$1/*.$3
for f in $FILES
do
  echo "Processing $f file..."
  filename=`basename ${f} ${3}`
  echo "Output: ${2}/${filename}_latlong.kea"
  gdalwarp -overwrite -r cubic -multi -wt Float32 -srcnodata 0 -dstnodata 0 -t_srs latlong_WGS84.wkt -of KEA ${f} ${2}/${filename}_latlong.kea
  gdalcalcstats ${2}/${filename}_latlong.kea -ignore 0
done