 #! /usr/bin/env python

#######################################
# Convert the HDF4 MODIS files to GDAL
# images.
#
# Email: petebunting@mac.com
# Date: 09/04/2013
# Version: 1.0
#######################################

# Import the numpy library
import numpy
# Import the GDAL library
from osgeo import gdal
# Import the GDAL/OGR spatial reference library
from osgeo import osr
# Import the HDF4 reader.
import pyhdf.SD
# Import the system library
import sys
# Import the python Argument parser
import argparse

def stringTokenizer(line, delimiter):
    tokens = list()
    token = str()
    for i in range(len(line)):
        if line[i] == delimiter:
            tokens.append(token)
            token = str()
        else:
            token = token + line[i]
    tokens.append(token)
    return tokens

def findElement(struct, vName):
    strStruct = str(struct)
    items = strStruct.split('\n')
    outVal = ""
    for item in items:
        item = item.strip()
        tokens = stringTokenizer(item, '=')
        if tokens[0] == vName:
            outVal = tokens[1]        
    return outVal

def readTextFile(file):
    dataFile = open(file, 'r')
    txtStr = ""
    for line in dataFile:
        txtStr += line.strip()
    dataFile.close()
    return txtStr
    

def createGDALImage(hdfImg, outImgPath, headerParams, wktStr, format):
    driver = gdal.GetDriverByName( format )
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
        print 'Driver %s supports Create() method.' % format
    else:
        print 'Driver %s not NOT support Create() method - choose another format.' % format
    
    dst_ds = driver.Create( outImgPath, int(headerParams['SizeX']), int(headerParams['SizeX']), 6, gdal.GDT_Int16 )

    dst_ds.SetProjection( wktStr )
    
    print "Processing Band 1"
    band = hdfImg.select('band1')
    dst_ds.GetRasterBand(1).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    dst_ds.GetRasterBand(1).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(1).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("add_offset", str(bandAttr['add_offset'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("scale_factor_err", str(bandAttr['scale_factor_err'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("calibrated_nt", str(bandAttr['calibrated_nt'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("SaturateValue", str(bandAttr['_SaturateValue'][0]))
        
    
    
    dst_ds = None
    

def createGCPs(lat, long, xSize, ySize):
    print "Trying to create GCPs..."
    
    for x in range(xSize):
        for y in range(ySize):
            print str(x) + "," + str(y)
    
    
    
def run(inputFile, outputFile, hdfDataset, wktFile, imageFormat):   
    hdfImg = pyhdf.SD.SD(inputFile)
    print "Available Datasets"
    print hdfImg.datasets()
    print "Get Header Attributes"
    attr = hdfImg.attributes(full=1)
    #print attr
    
    
    lat = hdfImg.select('Latitude')
    long = hdfImg.select('Longitude')
    
    #print lat[:]
    #print long[:]
    
    dims = numpy.shape(lat[:])
    
    xSize = dims[0]
    ySize = dims[1]
    
    print "Image DIMS: [", xSize, ",", ySize, "]"
    
    print "Generate GCPs."
    gcps = createGCPs(lat, long, xSize, ySize)
    
    print "Reading WKT file:"
    wktStr = readTextFile(wktFile)
    print wktStr
    
    
    # Check with the datsets exists within the HDF file.
    
    #if not outputReflFile == None:
    #    print "\nCreate GDAL Dataset from Reflectance Bands"
    #    createGDALImageRefl(hdfImg, outputReflFile, headerParams, wktStr, imageFormat)
    
    print "\n*** COMPLETE ***\n"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Define the argument for specifying the input file.
    parser.add_argument("-i", "--input", type=str,  help="Specify the input image file.")
    # Define the argument for specifying the output file.
    parser.add_argument("-o", "--output", type=str, help="Specify the output image file.")
    # Define the argument for specifying the HDF dataset.
    parser.add_argument("-d", "--dataset", type=str, help="Specify the dataset within the HDF file.")
    # Define the argument for specifying the WKT projection file.
    parser.add_argument("-w", "--wkt", type=str, help="Specify the WKT projection file.")
    # Define the argument for specifying the image file format.
    parser.add_argument("-f", "--format", type=str, help="Specify the image file format.")
    # Call the parser to parse the arguments.
    args = parser.parse_args()
    
    # Check that the input parameter has been specified.
    if args.input == None:
        # Print an error message if not and exit.
        print "Error: No input image file provided."
        sys.exit()
        
    # Check that the output parameter has been specified.
    if args.output == None:
        # Print an error message if not and exit.
        print "Error: No output image file provided."
        sys.exit()
        
    # Check that the output parameter has been specified.
    if args.dataset == None:
        # Print an error message if not and exit.
        print "Error: No input HDF dataset specified."
        sys.exit()
        
    # Check that the wkt parameter has been specified.
    if args.wkt == None:
        # Print an error message if not and exit.
        print "Error: No input wkt file provided."
        sys.exit()
        
    # Check that the output image format has been specified.
    if args.format == None:
        # Print an error message if not and exit.
        print "Error: No output image format provided."
        sys.exit()
    
    
    run(args.input, args.output, args.dataset, args.wkt, args.format)



