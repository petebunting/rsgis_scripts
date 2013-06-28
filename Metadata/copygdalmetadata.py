#!/usr/bin/env python

# copygdalmeta.py
# A script to copy metadata from one file and add / append.
# to another file.
#
# Dan Clewley (daniel.clewley@gmail.com) - 27/06/2013
#

import osgeo.gdal as gdal
import argparse
import sys

def copyMetadata(inputFile, outputFile, metadataKey):
    """ Copy metadata from existing dataset to new dataset.
    """
    inDataset = gdal.Open(inputFile, gdal.GA_ReadOnly)
    outDataset = gdal.Open(outputFile, gdal.GA_Update)
    if not inDataset is None:
        inMetadata = inDataset.GetMetadata()
        outMetadata = outDataset.GetMetadata()
        
        # Check for key in input metadata
        metadataExists = False
        try:
            newMetadata = "# From '%s':\n"%(inputFile) + inMetadata[metadataKey] + "\n# End from '%s'"%(inputFile)
            metadataExists = True
        except KeyError:
            print("No metadata for key '%s' in input file"%(metadataKey))

        if metadataExists:
            try:
                existingMetadata = outMetadata[metadataKey]
                outMetadata[metadataKey] = existingMetadata + '\n' + newMetadata
            except KeyError:
                outMetadata[metadataKey] = newMetadata
            outDataset.SetMetadata(outMetadata)
                
    else:
        # Print an error message if the file 
        # could not be opened.
        print("Could not open the input image file: " + inDataset)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Specify the input image file (to copy metadata from).")
    parser.add_argument("-o", "--output", type=str, help="Specify the output image file (to copy metadata to).")
    parser.add_argument("-k", "--key", type=str, help="Specify the metadata field key.")

    args = parser.parse_args()
    
    writeNewData = False
    
    if args.input == None:
        print("Error: No input image file provided.")
        parser.print_help()
        sys.exit()

    if args.output == None:
        print("Error: No output image file provided.")
        parser.print_help()
        sys.exit()

    if args.key == None:
        print("Error: No metadata field key was provided.")
        parser.print_help()
        sys.exit()

    copyMetadata(args.input, args.output, args.key)



