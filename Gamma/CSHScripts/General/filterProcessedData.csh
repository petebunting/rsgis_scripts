#! /bin/csh
#

# Create a list of the directories, where the data is located.
set list_dir = `ls -d al*`
#
# For each under_directory, execute the geocoding.
foreach dir_name ($list_dir)
  #
  cd $dir_name
    set width = `grep width g$dir_name.dem.par | cut -d : -f 1 --complement`
    # *** Lee Filter (Lee, 1980) ***
   # usage: lee <input_data> <output_data> <width> <nlooks> <bx> [by] 
   lee $dir_name.topo.hh.utm  $dir_name.lee.topo.hh.utm $width 5 5 5
   lee $dir_name.topo.hv.utm  $dir_name.lee.topo.hv.utm  $width 5 5 5
   # Copy header
   cp $dir_name.topo.hh.hdr $dir_name.lee.topo.hh.hdr
   cp $dir_name.topo.hv.hdr $dir_name.lee.topo.hv.hdr
  cd ..
#
end
