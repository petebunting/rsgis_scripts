#! /bin/csh
#
# Create a list of the under-directories, where the data is located.
cd $1
set list_dir = `ls -d  alpsba*`

# For each under_directory, execute the geocoding.
foreach dir_name ($list_dir)
  #
  echo $dir_name
  cd $dir_name
  #
  # Remove gamma0 and topo files (easy to recreate)
  rm *topo*utm
  rm *topo*hdr
  rm *gamma*utm
  rm *gamma*hdr
  # Move to the root directory
  cd ..
#
end