#!/usr/bin/env python

# managegdalmeta.py
# A script to write metadata to a GDAL dataset or read existing metadata
#
# Dan Clewley (daniel.clewley@gmail.com) - 26/06/2013
#

import osgeo.gdal as gdal
import argparse
import sys

def setMetadata(inputFile, metadataKey, metadataText):
    """ Sets metadata item to GDAL dataset using provided
        metadataKey. Appends text to existing field (if it exists)
        or adds a new field.
    """
    dataset = gdal.Open(inputFile, gdal.GA_Update)
    if not dataset is None:
        metadata = dataset.GetMetadata()
        
        datasetMetadata = ''

        try:
            datasetMetadata = metadata[metadataKey] + '\n' + metadataText
            print("Appending to existing '%s'"%(metadataKey))
        except KeyError:
            print("Creating new metadata item '%s'"%(metadataKey))
            datasetMetadata = metadataText

        metadata[metadataKey] = datasetMetadata
        dataset.SetMetadata(metadata)
    else:
        # Print an error message if the file 
        # could not be opened.
        print("Could not open the input image file: " + inputFile)

def getMetadata(inputFile, metadataKey):
    """ Reads metadata item from GDAL dataset using provided
        metadataKey. 
    """
    dataset = gdal.Open(inputFile, gdal.GA_Update)
    if not dataset is None:
        metadata = dataset.GetMetadata()
        
        # Print all metadata
        if (metadataKey == "") or (metadataKey == "ALL"):
            for key, value in metadata.items():
                print(key + ":\n" + value)
        # Or for specific key
        else:
            try:
                print(metadata[metadataKey])
            except KeyError:
                print("ERROR: The key '%s' was not found."%(metadataKey))
            
    else:
        # Print an error message if the file 
        # could not be opened.
        print("Could not open the input image file: " + inputFile)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Specify the input image file.")
    parser.add_argument("-k", "--key", type=str, help="Specify the metadata field key. Set to 'ALL' to display all fields.")
    parser.add_argument("-t", "--text", type=str, help="Specify the text to write to the metadata field (optional)")

    args = parser.parse_args()
    
    writeNewData = False
    
    if args.input == None:
        print("Error: No input image file provided.")
        parser.print_help()
        sys.exit()

    if args.key == None:
        print("Error: No metadata field key was provided.")
        parser.print_help()
        sys.exit()
        
    if args.text != None:
        writeNewData = True
        if args.key == "ALL":
            print('ERROR: Must specify a key for writing.')

    if writeNewData:
        setMetadata(args.input, args.key, args.text)
    else:
        getMetadata(args.input, args.key)



