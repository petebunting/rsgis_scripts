# Created by Pete Bunting (petebunting@mac.com)
#
# A simple script to run GDAL Warp on a set of input images to
# re-project them to the OSGB ESPG 
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
  echo "Output: ${2}/${filename}_osgb.kea"
  gdalwarp -overwrite -r cubic -multi -wt Float32 -srcnodata 0 -dstnodata 0 -t_srs EPSG:27700 -of KEA ${f} ${2}/${filename}_osgb.kea
  gdalcalcstats ${2}/${filename}_osgb.kea -ignore 0
done