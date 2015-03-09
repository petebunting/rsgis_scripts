# Created by Pete Bunting (petebunting@mac.com)
#
# A simple script to use gdal_translate to convert KEA files 
# to the ASCII format.
#

# Inputs:
# $1 is the input directory 
# $2 is the output directory

FILES=$1/*.kea
for f in $FILES
do
  echo "Processing $f file..."
  filename=`basename ${f} .kea`
  echo "Output: ${2}/${filename}.asc"
  gdal_translate -of AAIGrid ${f} ${2}/${filename}.asc
done