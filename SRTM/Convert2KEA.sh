# Created by Pete Bunting (petebunting@mac.com)
#
# A simple script to use gdal_translate to convert files 
# to the KEA format.
#

# Inputs:
# $1 is the input directory 
# $2 is the output directory
# $3 is the input files extension

FILES=$1/*.$3
for f in $FILES
do
  echo "Processing $f file..."
  filename=`basename ${f} .${3}`
  echo "Output: ${2}/${filename}.kea"
  gdal_translate -of KEA ${f} ${2}/${filename}.kea
  gdalcalcstats ${2}/${filename}.kea -ignore -32768
done