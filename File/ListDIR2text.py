#! /usr/bin/env python

#######################################
# A script to list files with a specific
# extention within directory
#
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 24/04/2013
# Version: 1.0
#######################################

import os.path
import sys
import argparse

class ListFile2Text (object):
    
    def checkFileExtension(self, filename, extension):
        foundExtension = False;
        filenamesplit = os.path.splitext(filename)
        fileExtension = filenamesplit[1].strip()
        if(fileExtension == extension):
            foundExtension = True
        return foundExtension
    
    def findFiles(self, filelist, directory, extension):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                fileList = os.listdir(directory)
                for filename in fileList:
                    if(os.path.isdir(os.path.join(directory,filename))):
                        self.findFiles(filelist, os.path.join(directory,filename), extension)
                    elif(os.path.isfile(os.path.join(directory,filename))):
                        if(self.checkFileExtension(filename, extension)):
                            filelist.append(os.path.join(directory,filename))
                    else:
                        print(filename + ' is NOT a file or directory!')
            else:
                print(directory + ' is not a directory!')
        else:
            print(directory + ' does not exist!')
    
    def run(self, dir, ext, output):
        filelist = list()
        self.findFiles(filelist, dir, ext)
        
        outFile = open(output, 'w')
        for file in filelist:
            outFile.write(file)
            outFile.write('\n')
        outFile.close()
        

if __name__ == '__main__':
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", type=str, help="The directory within which the files are to be listed.")
    parser.add_argument("-e", "--ext", type=str, help="File extention of the files of interest.")
    parser.add_argument("-o", "--output", type=str, help="Output text file.")
    # Call the parser to parse the arguments.
    args = parser.parse_args()
    
    if args.dir == None:
        # Print an error message if not and exit.
        print("Error: No dir option provided.")
        sys.exit()
    if args.ext == None:
        # Print an error message if not and exit.
        print("Error: No ext option provided.")
        sys.exit()
    if args.output == None:
        # Print an error message if not and exit.
        print("Error: No output option provided.")
        sys.exit()



    obj = ListFile2Text()
    obj.run(args.dir, args.ext, args.output)