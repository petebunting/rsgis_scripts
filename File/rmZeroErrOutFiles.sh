# Created by Pete Bunting (petebunting@mac.com)
#
# A simple script to delete the error and output files
# of if the error file has a file of zero (i.e., there
# were no errors). 
#
# These files a generally produced from a HPC systems.
#

# Inputs:
# $1 is the base path

FILES=$1*.err
for f in $FILES
do
  echo "Processing $f file..."
  FILESIZE=$(stat -c%s "$f")
  echo $FILESIZE
  if [ "$FILESIZE" = 0 ] ; then
    # code
    fileBase=`basename ${f} .err`
    rm "${fileBase}.out"
    rm $f
  fi
done