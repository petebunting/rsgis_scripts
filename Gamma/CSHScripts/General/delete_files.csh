#! /bin/csh
#
# Create a list of the under-directories, where the data is located.
set list_dir = `ls -d  al*`
#
# For each under_directory, execute the geocoding.
foreach dir_name ($list_dir)
  #
  cd $dir_name
  cd l1data
  #
  # Remove files that are no longer needed
  #rm l7*
  #rm sh*
  rm al*
  #rm diff*
  #rm landsat*
  rm pal*
  #rm range*
  #rm srtm*
  rm utm*
  rm *.dem.par
  #
  # Move to the root directory
  cd ..
  cd ..
#
end
