#! /usr/bin/env python

#######################################
# MergeSHPfiles.py
# A python script to merge shapefiles
# Author: <YOUR NAME>
# Email: <YOUR EMAIL>
# Date: DD/MM/YYYY
# Version: 1.0
#######################################

import os

# Import the sys package from within the 
# standard library
import sys

class MergeSHPfiles (object):

    def getOGRTypeFromExt(self, fileName):
        # A function to get the ORG format string
        # based on a file extension
        extension = os.path.splitext(fileName)[-1] 

        if extension == '.shp':
            return "ESRI Shapefile"
        elif extension == '.kml':
            return "KML"
        elif extension == '.sqlite':
            return "SQLite"
        else:
            raise Exception('Type not recognised')

    # A function to remove a .shp extension from a file name
    def removeSHPExtension(self, name):
        # The output file name
        outName = name
        # Find how many '.shp' strings are in the current file
        # name
        count = name.find('.shp', 0, len(name))
        # If there are no instances of .shp then -1 will be returned
        if not count == -1:
            # Replace all instances of .shp with empty string.
            outName = name.replace('.shp', '', name.count('.shp'))
        # Return output file name without .shp
        return outName
    
    # A function to remove the file path a file 
    # (in this case a windows file path)
    def removeFilePath(self, name):
        # Remove white space (i.e., spaces, tabs)
        name = name.strip()
        # Count the number of slashs 
        # A double slash is required because \ is a 
        # string escape charater.
        count = name.count('/')
        # Split string into a list where slashs occurs
        nameSegments = name.split('/', count)
        # Return the last item in the list
        return nameSegments[count]
    
    # A function to test the file extension of a file
    def checkFileExtension(self, filename, extension):
        # Boolean variable to be returned by the function
        foundExtension = False;
        # Split the filename into two parts (name + ext)
        filenamesplit = os.path.splitext(filename)
        # Get the file extension into a varaiable
        fileExtension = filenamesplit[1].strip()
        # Decide whether extensions are equal
        if(fileExtension == extension):
            foundExtension = True
        # Return result
        return foundExtension
        
    
    # A function which iterates through the directory and checks file extensions
    def findFilesExt(self, directory, extension, fileList):
        # check whether the current directory exits
        if os.path.exists(directory):
            # check whether the given directory is a directory
            if os.path.isdir(directory):
                # list all the files within the directory
                dirFileList = os.listdir(directory)
                # Loop through the individual files within the directory
                for filename in dirFileList:
                    # Check whether file is directory or file
                    if(os.path.isdir(os.path.join(directory,filename))):
                        self.findFilesExt(os.path.join(directory,filename), extension, fileList)
                    elif(self.checkFileExtension(filename, extension)):
                        fileList.append(os.path.join(directory,filename))
            else:
                print(directory + ' is not a directory!')
        else:
            print(directory + ' does not exist!')

    # A function to control the merging of shapefiles
    def mergeSHPfiles(self, filePath, newSHPfile):
        # Get the list of files within the directory
        # provided with the extension .shp
       fileList = list()
       self.findFilesExt(filePath, '.shp', fileList)
       # Variable used to identify the first file
       first = True
       # Format string for outFile
       formatStr = ' -f "' + self.getOGRTypeFromExt(newSHPfile) + '" '

       # A string for the command to be built
       command = ''
       # Iterate through the files.
       for file in fileList:
           print("Adding:" + file) 
           if first and formatStr.find('SQLite') < -1:
               # If the first file make a copy to create the output file
               # Don't need to create copy for SQLite
               command = 'ogr2ogr ' + formatStr + newSHPfile + ' "' + file + '"'
               first = False
           else:
               # Otherwise append the current shapefile to the output file
               command = 'ogr2ogr -update -append ' + formatStr + newSHPfile + ' "'  + \
               file + '" -nln ' + \
               self.removeSHPExtension(self.removeFilePath(newSHPfile))
           # Execute the current command
           os.system(command)

    # A function which controls the rest of the script
    def run(self):
        # Get the number of arguments
        numArgs = len(sys.argv)
        # Check there are only 2 input argument (i.e., the input file
        # and output base).
        # Note that argument 0 (i.e., sys.argv[0]) is the name
        # of the script uncurrently running.
        if numArgs == 3:
            # Retrieve the input directory
            filePath = sys.argv[1]
            # Retrieve the output file
            newSHPfile = sys.argv[2]
            
            # Check input file path exists and is a directory
            if not os.path.exists(filePath):
                print('Filepath does not exist')
            elif not os.path.isdir(filePath):
                print('Filepath is not a directory!')
            else:
                # Merge the shapefiles within the filePath
                self.mergeSHPfiles(filePath, newSHPfile)
        else:
            print("ERROR. Command should have the form:")
            print("python MergeSHPfiles_cmd.py <Input File Path> <Output File>")

# The start of the code
if __name__ == '__main__':
    # Make an instance of the class
    obj = MergeSHPfiles()
    # Call the function run()
    obj.run()
