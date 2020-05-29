# The $2 number is the column of interest. 
awk '{print $2}' file

# If you are wanting to get the commands to delete a set of files you could do something like:
ls -l > file_list
awk '{print "rm " $9}' file_list > rm_file_list
sh rm_file_list

