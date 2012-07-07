#!/bin/bash

# create the directory to store the raster files in ($rundir)
# $LCRFS_LOCALDISC is the location of the local disc
# we make it unique using the $JOB_ID and $USER variables
rundir="${LCRFS_LOCALDISC}/${JOB_ID}_${USER}"
mkdir $rundir

# recall some files from son
lcrfs_recall /backup/clustermuster/buntingp/las/$1 $rundir

# run the script in the same directory as job submission
outname=$rundir/${2}
echo $outname

spdtranslate -i LAS -o UPD -x FIRST_RETURN $rundir/$1 $outname

# save output file back to son
#lcrfs_mkdir /backup/clustermuster/buntingp/spd
lcrfs_save $outname /backup/clustermuster/buntingp/spd

# clean up $rundir when finished (very important!)
rm -rf $rundir
