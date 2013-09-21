# Created by Pete Bunting (petebunting@mac.com)
#
# A simple script to use gdal_translate to convert files 
# to the KEA format.
#

# Inputs:
# $1 is the input directory 
# $2 is the output directory

FILES=$1/*.kea
for f in $FILES
do
  echo "Processing $f file..."
  filename=`basename ${f} .kea`
  echo "Output: ${2}/${filename}.tif"
  gdal_translate -of GTIFF ${f} ${2}/${filename}.tif
  gdaladdo ${2}/${filename}.tif 2 4 8 16 32
done