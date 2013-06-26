#!/usr/bin/env python

# script2gdalmeta.py
# A script to dump a script (assumed to be shell) into 
# the metadata of a gdal dataset.
#
# Dan Clewley (daniel.clewley@gmail.com) - 26/06/2013
#

import osgeo.gdal as gdal
import argparse
import sys, os
from time import strftime

def getMetadataKeyFilename(fileName):
    metadataKey = 'PROCESSING_HISTORY'
    extension = os.path.splitext(fileName)[-1]

    if extension == '.xml': # RSGISLib XML
        metadataKey = 'PROCESSING_RSGISLIB_XML_SCRIPT' 
    elif extension == '.py': # Python
        metadataKey = 'PROCESSING_PYTHON_SCRIPT'
    return metadataKey

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
                print(key + ": " + value)
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

    commandDescription = '''
Add the content of a script to the metadata of a GDAL dataset.
RSGISLib XML scripts are added / appended to the key:
    PROCESSING_RSGISLIB_XML_SCRIPT
Python Scripts are added / appended to the key:
    PROCESSING_PYTHON_SCRIPT
All other scripts are added / appended to the key:
    PROCESSING_HISTORY

Calling without a script file will print out the 'PROCESSING_HISTORY' key'''

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Specify the input image file.")
    parser.add_argument("-f", "--file", type=str, help="File containing script to write to metadata.")

    args = parser.parse_args()

    writeNewData = False
    
    if args.input == None:
        print("Error: No input image file provided.")
        parser.print_help()
        print(commandDescription)
        sys.exit()

    if args.file == None:
        writeNewData = False
    else:
        writeNewData = True

    if writeNewData:

        # Get metadata key based on script extension
        scriptMetadataKey = getMetadataKeyFilename(args.file)

         # Write time and filename to metadata
        timeStr = strftime('%Y/%m/%d %H:%M:%S')
        scriptText = '# ' + timeStr + ' - ' + os.path.split(args.file)[-1] + ":\n"

        # Read script into a string
        scriptFile = open(args.file,'rU')

        for line in scriptFile:
            scriptText = scriptText + line + '\n'

        # Set metadata
        setMetadata(args.input, scriptMetadataKey, scriptText)

    else:
        getMetadata(args.input, 'PROCESSING_HISTORY')

