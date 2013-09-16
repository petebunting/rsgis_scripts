 #! /usr/bin/env python

#######################################
# Convert the HDF4 LEDAPS files to GDAL
# images.
#
# Email: petebunting@mac.com
# Date: 07/04/2013
# Version: 1.0
#######################################

# Import the numpy library
import numpy
# Import the GDAL library
from osgeo import gdal
# Import the GDAL/OGR spatial reference library
from osgeo import osr
from osgeo import ogr
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
    

def createGDALImageRefl(hdfImg, outImgPath, headerParams, wktStr, format):
    driver = gdal.GetDriverByName( format )
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
        print 'Driver %s supports Create() method.' % format
    else:
        print 'Driver %s not NOT support Create() method - choose another format.' % format
    
    dst_ds = driver.Create( outImgPath, int(headerParams['SizeX']), int(headerParams['SizeX']), 6, gdal.GDT_Int16 )
    dst_ds.SetGeoTransform( [ float(headerParams['TLX']), float(headerParams['PixelSize']), float(headerParams['OrientationAngle']), float(headerParams['TLY']), float(headerParams['OrientationAngle']), -float(headerParams['PixelSize']) ] )

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
        
    print "Processing Band 2"
    band = hdfImg.select('band2')
    dst_ds.GetRasterBand(2).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    dst_ds.GetRasterBand(2).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(2).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(2).SetMetadataItem("add_offset", str(bandAttr['add_offset'][0]))
    dst_ds.GetRasterBand(2).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(2).SetMetadataItem("scale_factor_err", str(bandAttr['scale_factor_err'][0]))
    dst_ds.GetRasterBand(2).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    dst_ds.GetRasterBand(2).SetMetadataItem("calibrated_nt", str(bandAttr['calibrated_nt'][0]))
    dst_ds.GetRasterBand(2).SetMetadataItem("SaturateValue", str(bandAttr['_SaturateValue'][0]))
    
    print "Processing Band 3"
    band = hdfImg.select('band3')
    dst_ds.GetRasterBand(3).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    dst_ds.GetRasterBand(3).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(3).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(3).SetMetadataItem("add_offset", str(bandAttr['add_offset'][0]))
    dst_ds.GetRasterBand(3).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(3).SetMetadataItem("scale_factor_err", str(bandAttr['scale_factor_err'][0]))
    dst_ds.GetRasterBand(3).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    dst_ds.GetRasterBand(3).SetMetadataItem("calibrated_nt", str(bandAttr['calibrated_nt'][0]))
    dst_ds.GetRasterBand(3).SetMetadataItem("SaturateValue", str(bandAttr['_SaturateValue'][0]))
    
    print "Processing Band 4"
    band = hdfImg.select('band4')
    dst_ds.GetRasterBand(4).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    dst_ds.GetRasterBand(4).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(4).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(4).SetMetadataItem("add_offset", str(bandAttr['add_offset'][0]))
    dst_ds.GetRasterBand(4).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(4).SetMetadataItem("scale_factor_err", str(bandAttr['scale_factor_err'][0]))
    dst_ds.GetRasterBand(4).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    dst_ds.GetRasterBand(4).SetMetadataItem("calibrated_nt", str(bandAttr['calibrated_nt'][0]))
    dst_ds.GetRasterBand(4).SetMetadataItem("SaturateValue", str(bandAttr['_SaturateValue'][0]))
    
    print "Processing Band 5"
    band = hdfImg.select('band5')
    dst_ds.GetRasterBand(5).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    dst_ds.GetRasterBand(5).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(5).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(5).SetMetadataItem("add_offset", str(bandAttr['add_offset'][0]))
    dst_ds.GetRasterBand(5).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(5).SetMetadataItem("scale_factor_err", str(bandAttr['scale_factor_err'][0]))
    dst_ds.GetRasterBand(5).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    dst_ds.GetRasterBand(5).SetMetadataItem("calibrated_nt", str(bandAttr['calibrated_nt'][0]))
    dst_ds.GetRasterBand(5).SetMetadataItem("SaturateValue", str(bandAttr['_SaturateValue'][0]))
    
    print "Processing Band 7"
    band = hdfImg.select('band7')
    dst_ds.GetRasterBand(6).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    dst_ds.GetRasterBand(6).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(6).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(6).SetMetadataItem("add_offset", str(bandAttr['add_offset'][0]))
    dst_ds.GetRasterBand(6).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(6).SetMetadataItem("scale_factor_err", str(bandAttr['scale_factor_err'][0]))
    dst_ds.GetRasterBand(6).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    dst_ds.GetRasterBand(6).SetMetadataItem("calibrated_nt", str(bandAttr['calibrated_nt'][0]))
    dst_ds.GetRasterBand(6).SetMetadataItem("SaturateValue", str(bandAttr['_SaturateValue'][0]))
    
    dst_ds.SetMetadataItem("AcquisitionDate", str(headerParams['AcquisitionDate']))
    dst_ds.SetMetadataItem("SolarAzimuth", str(headerParams['SolarAzimuth']))
    dst_ds.SetMetadataItem("SolarZenith", str(headerParams['SolarZenith']))
    dst_ds.SetMetadataItem("WRS_Row", str(headerParams['WRS_Row']))
    
    dst_ds = None
    
    
def createGDALImageThermal(hdfImg, outImgPath, headerParams, wktStr, format):
    driver = gdal.GetDriverByName( format )
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
        print 'Driver %s supports Create() method.' % format
    else:
        print 'Driver %s not NOT support Create() method - choose another format.' % format
    
    dst_ds = driver.Create( outImgPath, int(headerParams['SizeX']), int(headerParams['SizeX']), 1, gdal.GDT_Int16 )
    dst_ds.SetGeoTransform( [ float(headerParams['TLX']), float(headerParams['PixelSize']), float(headerParams['OrientationAngle']), float(headerParams['TLY']), float(headerParams['OrientationAngle']), -float(headerParams['PixelSize']) ] )

    dst_ds.SetProjection( wktStr )
    
    print "Processing Band 6"
    band = hdfImg.select('band6')
    dst_ds.GetRasterBand(1).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    #print bandAttr
    dst_ds.GetRasterBand(1).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(1).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("units", str(bandAttr['units'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    
    dst_ds.SetMetadataItem("AcquisitionDate", str(headerParams['AcquisitionDate']))
    dst_ds.SetMetadataItem("SolarAzimuth", str(headerParams['SolarAzimuth']))
    dst_ds.SetMetadataItem("SolarZenith", str(headerParams['SolarZenith']))
    dst_ds.SetMetadataItem("WRS_Row", str(headerParams['WRS_Row']))
    
    dst_ds = None
    
    
def createGDALImageAtmosphere(hdfImg, outImgPath, headerParams, wktStr, format):
    driver = gdal.GetDriverByName( format )
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
        print 'Driver %s supports Create() method.' % format
    else:
        print 'Driver %s not NOT support Create() method - choose another format.' % format
    
    dst_ds = driver.Create( outImgPath, int(headerParams['SizeX']), int(headerParams['SizeX']), 1, gdal.GDT_Int16 )
    dst_ds.SetGeoTransform( [ float(headerParams['TLX']), float(headerParams['PixelSize']), float(headerParams['OrientationAngle']), float(headerParams['TLY']), float(headerParams['OrientationAngle']), -float(headerParams['PixelSize']) ] )

    dst_ds.SetProjection( wktStr )
    
    print "Processing Atmosphere Opacity"
    band = hdfImg.select('atmos_opacity')
    dst_ds.GetRasterBand(1).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    #print bandAttr
    dst_ds.GetRasterBand(1).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(1).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("units", str(bandAttr['units'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("scale_factor", str(bandAttr['scale_factor'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    
    dst_ds.SetMetadataItem("AcquisitionDate", str(headerParams['AcquisitionDate']))
    dst_ds.SetMetadataItem("SolarAzimuth", str(headerParams['SolarAzimuth']))
    dst_ds.SetMetadataItem("SolarZenith", str(headerParams['SolarZenith']))
    dst_ds.SetMetadataItem("WRS_Row", str(headerParams['WRS_Row']))
    
    dst_ds = None
    
def createGDALImageQA(hdfImg, outImgPath, headerParams, wktStr, format):
    driver = gdal.GetDriverByName( format )
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
        print 'Driver %s supports Create() method.' % format
    else:
        print 'Driver %s not NOT support Create() method - choose another format.' % format
    
    dst_ds = driver.Create( outImgPath, int(headerParams['SizeX']), int(headerParams['SizeX']), 1, gdal.GDT_Int16 )
    dst_ds.SetGeoTransform( [ float(headerParams['TLX']), float(headerParams['PixelSize']), float(headerParams['OrientationAngle']), float(headerParams['TLY']), float(headerParams['OrientationAngle']), -float(headerParams['PixelSize']) ] )

    dst_ds.SetProjection( wktStr )
    
    print "Processing QA Image"
    band = hdfImg.select('lndsr_QA')
    dst_ds.GetRasterBand(1).WriteArray( band[:] )
    bandAttr = band.attributes(full=1)
    print bandAttr
    dst_ds.GetRasterBand(1).SetNoDataValue(float(bandAttr['_FillValue'][0]))
    dst_ds.GetRasterBand(1).SetDescription(str(bandAttr['long_name'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("units", str(bandAttr['units'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem("valid_range", str(bandAttr['valid_range'][0]))
    dst_ds.GetRasterBand(1).SetMetadataItem('LAYER_TYPE', 'thematic')
    
    #classnames = np.empty(15, dtype=np.dtype('a255'))
    #classnames[0] = ""
    #classnames[1] = ""
    #classnames[2] = ""
    #classnames[3] = ""
    #classnames[4] = ""
    #classnames[5] = ""
    #classnames[6] = "Unused"
    #classnames[7] = "Unused"
    #classnames[8] = "Unused"
    #classnames[9] = "Unused"
    #classnames[10] = "Unused"
    #classnames[11] = "Unused"
    #classnames[12] = "Unused"
    #classnames[13] = "Unused"
    #classnames[14] = "Unused"
    #classnames[15] = "Unused"
    
    
    
    dst_ds.SetMetadataItem("AcquisitionDate", str(headerParams['AcquisitionDate']))
    dst_ds.SetMetadataItem("SolarAzimuth", str(headerParams['SolarAzimuth']))
    dst_ds.SetMetadataItem("SolarZenith", str(headerParams['SolarZenith']))
    dst_ds.SetMetadataItem("WRS_Row", str(headerParams['WRS_Row']))
    
    dst_ds = None
    
def run(inputFile, outputReflFile, outputThermalFile, outputFileAtmos, outputFileQA, wktFile, imageFormat):   
    hdfImg = pyhdf.SD.SD(inputFile)
    print "Available Datasets"
    print hdfImg.datasets()
    print "Get Header Attributes"
    attr = hdfImg.attributes(full=1)
    #print attr
    
    print "Reading WKT file:"
    wktStr = readTextFile(wktFile)
    print wktStr
    
    headerParams = dict()
        
    headerParams['AcquisitionDate'] = attr['AcquisitionDate'][0]
    headerParams['WRS_Row'] = attr['WRS_Row'][0]
    headerParams['SolarAzimuth'] = attr['SolarAzimuth'][0]
    headerParams['SolarZenith'] = attr['SolarZenith'][0]
    headerParams['OrientationAngle'] = attr['OrientationAngle'][0]
    headerParams['PixelSize'] = attr['PixelSize'][0]
    
    headerParams['WestBoundingCoordinate'] = attr['WestBoundingCoordinate'][0]
    headerParams['EastBoundingCoordinate'] = attr['EastBoundingCoordinate'][0]
    headerParams['NorthBoundingCoordinate'] = attr['NorthBoundingCoordinate'][0]
    headerParams['SouthBoundingCoordinate'] = attr['SouthBoundingCoordinate'][0]
    
    #print headerParams
    
    tlCoords = findElement(attr['StructMetadata.0'][0], 'UpperLeftPointMtrs')
    
    tlCoords = tlCoords.lstrip('(')
    tlCoords = tlCoords.rstrip(')')
    
    print "TLCoords = ", tlCoords
    coords = stringTokenizer(tlCoords, ',')
    
    headerParams['TLX'] = coords[0]
    headerParams['TLY'] = coords[1]
    
    headerParams['SizeX'] = findElement(attr['StructMetadata.0'][0], 'XDim')
    headerParams['SizeY'] = findElement(attr['StructMetadata.0'][0], 'YDim')

    #wgs84Proj = osr.SpatialReference()
    #wgs84Proj.ImportFromEPSG(4326)
    
    #inWKTProj = osr.SpatialReference()
    #inWKTProj.ImportFromWkt(wktStr)
    
    #wktPt = 'POINT(%s %s)' % (headerParams['WestBoundingCoordinate'], headerParams['NorthBoundingCoordinate'])
    #print(wktPt)
    #point = ogr.CreateGeometryFromWkt(wktPt)
    #point.AssignSpatialReference(wgs84Proj)
    #point.TransformTo(inWKTProj)
    #print(point)
    
    #headerParams['TLX'] = point.GetX()
    #headerParams['TLY'] = point.GetY()
    
    #print "BandNumbers = ", attr['BandNumbers'][0]
    print "AcquisitionDate = ", headerParams['AcquisitionDate']
    print "WRS_Row = ", headerParams['WRS_Row'] 
    print "SolarAzimuth = ", headerParams['SolarAzimuth']
    print "SolarZenith = ", headerParams['SolarZenith']
    print "OrientationAngle = ", headerParams['OrientationAngle']
    print "PixelSize = ", headerParams['PixelSize']
    print "TLX = ", headerParams['TLX'] 
    print "TLY = ", headerParams['TLY']
    print "SizeX = ", headerParams['SizeX'] 
    print "SizeY = ", headerParams['SizeY']
    
    print "WestBoundingCoordinate = ", headerParams['WestBoundingCoordinate'] 
    print "EastBoundingCoordinate = ", headerParams['EastBoundingCoordinate']
    print "NorthBoundingCoordinate = ", headerParams['NorthBoundingCoordinate'] 
    print "SouthBoundingCoordinate = ", headerParams['SouthBoundingCoordinate']
    
    
    if not outputReflFile == None:
        print "\nCreate GDAL Dataset from Reflectance Bands"
        createGDALImageRefl(hdfImg, outputReflFile, headerParams, wktStr, imageFormat)
    
    if not outputThermalFile == None:
        print "\nCreate GDAL Dataset from Thermal Band"
        createGDALImageThermal(hdfImg, outputThermalFile, headerParams, wktStr, imageFormat)
    
    if not outputFileAtmos == None:
        print "\nCreate GDAL Dataset from Atmosphere Band"
        createGDALImageAtmosphere(hdfImg, outputFileAtmos, headerParams, wktStr, imageFormat)

    if not outputFileQA == None:
        print "\nCreate GDAL Dataset from QA Band"
        print "The QA channel is currently not exported -- need to work out reading individual bits..."
        #createGDALImageQA(hdfImg, outputFileQA, headerParams, wktStr, imageFormat)
    
    print "\n*** COMPLETE ***\n"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Define the argument for specifying the input file.
    parser.add_argument("-i", "--input", type=str,  help="Specify the input image file.")
    # Define the argument for specifying the output file.
    parser.add_argument("-r", "--outputrefl", type=str, help="Specify the output reflectance image file.")
    # Define the argument for specifying the output file.
    parser.add_argument("-t", "--outputthermal", type=str, help="Specify the output reflectance image file.")
    # Define the argument for specifying the output file.
    parser.add_argument("-a", "--outputatoms", type=str, help="Specify the output atmosphere image file.")
    # Define the argument for specifying the output file.
    parser.add_argument("-q", "--outputqa", type=str, help="Specify the output QA image file.")
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
    if (args.outputrefl == None) and (args.outputthermal == None) and (args.outputatoms == None) and (args.outputqa == None):
        # Print an error message if not and exit.
        print "Error: No output image file were provided - Need at least one."
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
    
    
    run(args.input, args.outputrefl, args.outputthermal, args.outputatoms, args.outputqa, args.wkt, args.format)



