# Created by Pete Bunting (petebunting@mac.com)
#
# Calculate image stats and pyramids for a directory of input files.
#

# Inputs:
# $1 is the input directory
# $2 is the file extension of the input images.
# $3 is the no data value

FILES=$1/*.$2
for f in $FILES
do
  echo "Processing $f file..."
  rsgiscalcimgstats.py -i ${f} -n $3
done