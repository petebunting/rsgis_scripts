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

FILES=$1/*.kea
for f in $FILES
do
  echo "Processing $f file..."
  filename=`basename ${f} .kea`
  echo "Output: ${2}/${filename}_latlong.kea"
  gdalwarp -overwrite -r cubic -multi -wt Float32 -srcnodata 0 -dstnodata 0 -t_srs EPSG:4326 -of KEA ${f} ${2}/${filename}_latlong.kea
  gdalcalcstats ${2}/${filename}_latlong.kea -ignore 0
done