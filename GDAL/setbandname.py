#!/usr/bin/env python

# setbandname.py
# A script to set the band name for gdal data
# Pete Bunting (pfb@aber.ac.uk)
# Taken from 'Python Scripting for Spatial Data Processing'
# Available from:
# https://bitbucket.org/petebunting/python-tutorial-for-spatial-data-processing/downloads
#
# Released under the Creative Commons Attribution-ShareAlike 3.0 Unported License
#

# Import the GDAL python library
import osgeo.gdal as gdal
# Import the python Argument parser
import argparse
# Import the System library
import sys
# Import the CSV library
import csv

# A function to set the no data value
# for each image band.
def setBandName(inputFile, band, name):
    # Open the image file, in update mode
    # so that the image can be edited. 
    dataset = gdal.Open(inputFile, gdal.GA_Update)
    # Check that the image  has been opened.
    if not dataset is None:
        # Get the image band
        imgBand = dataset.GetRasterBand(band)
        # Check the image band was available.
        if not imgBand is None:
            # Set the image band name.
            imgBand.SetDescription(name)
        else:
            # Print out an error message.
            print("Could not open the image band: ", band)
    else:
        # Print an error message if the file 
        # could not be opened.
        print("Could not open the input image file: ", inputFile)

# This is the first part of the script to 
# be executed.
if __name__ == '__main__':
    # Create the command line options 
    # parser.
    parser = argparse.ArgumentParser()
    # Define the argument for specifying the input file.
    parser.add_argument("-i", "--input", type=str, 
                        help="Specify the input image file.")
    # Define the argument for specifying image band.
    parser.add_argument("-b", "--band", type=int, 
                        help="Specify image band.")
    # Define the argument for specifying band name.
    parser.add_argument("-n", "--name", type=str, 
                        help="Specify the band name.")
    parser.add_argument("-f", "--namesfile",type=str,
                        help="Text file containing band numbers and names, seperated by a comma")
    # Call the parser to parse the arguments.
    args = parser.parse_args()

    useBandNamesFile=True
    
    # Check that the input parameter has been specified.
    if args.input == None:
        # Print an error message if not and exit.
        print("Error: No input image file provided.")
        print(parser.print_help())
        sys.exit()
        
    # Check for a text file containing band names
    if args.namesfile == None:
        useBandNamesFile=False

    if useBandNamesFile == False:
        # Check that the band parameter has been specified.
        if args.band == None:
            # Print an error message if not and exit.
            print("Error: the band was not specified, and a file containing band names was not provided.")
            print(parser.print_help())
            sys.exit()
            
        # Check that the name parameter has been specified.
        if args.name == None:
            # Print an error message if not and exit.
            print("Error: the band name was not specified and a file containing band names was not provided.")
            print(parser.print_help())
            sys.exit()

    if useBandNamesFile and (args.name != None or args.band != None):
        print("WARNING: Using band names from text file only")
        
    # Otherwise, run the function to set the band
    # name.
    if useBandNamesFile:
        bandNamesFile=csv.reader(open(args.namesfile,'rU'))
        for line in bandNamesFile:
            bandNum=line[0]
            bandName=line[1]
            if line[0].isdigit():
                print('Setting band: ' + bandNum + ' to: ' + bandName)
                setBandName(args.input, int(bandNum), bandName)
            else:
                print('"'+line[0]+'" is not a valid band number')

    else:
        setBandName(args.input, args.band, args.name)



