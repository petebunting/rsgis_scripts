#! /bin/csh
#
# Create a list of the under-directories, where the data is located.
set list_dir = `ls -d  al*`
#
# For each under_directory.
foreach dir_name ($list_dir)
  #
  cd $dir_name
  #
   cd l1data
   #
   cp *lev1.hdr /data/UTM55/NEW_ORDER_INJUNE/Renamed/ 
   #
   # Move to the root directory
   cd ..
   cd ..
#
end
