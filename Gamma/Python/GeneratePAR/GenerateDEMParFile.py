#! /usr/bin/env python

#######################################
# A class automatically generate GAMMA
# par file from ENVI header 
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 16/04/2010
# Version: 1.0
#######################################

import os.path
import sys, re
import argparse
from abc import ABCMeta, abstractmethod

haveGDAL = False
try:
    from osgeo import gdal, osr
    haveGDAL = True
except ImportError:
    print('Warning: Could not import GDAL. Only UTM projection is supported')

def getFileName(filePath):
    count = filePath.count('/')
    elements = filePath.split('/', count)
    name = re.sub('_par','',elements[count])
    return name

class ParFileObject (object):

    def __init__(self):
        self.imageparameters = {}

    @abstractmethod
    def getParameters(self, inHeaderFile, inImageFile): pass
    
    @abstractmethod
    def generateParFile(self, outParFile): pass
        
    def envi2gammaDataType(self,inEnvi):
        """ Convert from integer ENVI data type
            to GAMMA data type stored in par file
        """
        dataTypes = {}
        dataTypes[2] =  'INTEGER*2'
        dataTypes[12] =  'INTEGER*2'
        dataTypes[4] =  'REAL*4'       
        
        return dataTypes[int(inEnvi)]

class ParFileUTM (ParFileObject):

    """ Generate parameter file for UTM projection """

    def __init__(self):
        ParFileObject.__init__(self)
        self.headerparameters = []

    def getParameters(self, inHeaderFile, inImageFile = None):
        if inHeaderFile is None:
            raise Exception('No inHeaderFile provided')

        self.getParametersfromHDR(inHeaderFile)
        self.generateOutputParameters()

    def getParametersfromHDR(self, inHeaderFile):
        """ Extract parameters from ENVI header file """
        if(os.path.isfile(inHeaderFile)):
            datatype = 'INTEGER*2'
            try:
                parFile = open(inHeaderFile, 'rU') 
                for eachLine in parFile:
                    #print eachLine
                    count = eachLine.count('=')
                    #print 'count = ' + str(count)
                    if(count == 1):
                        elements = eachLine.split('=', count)
                        elements[0] = elements[0].strip()
                        elements[1] = elements[1].strip()
                        if elements[0] == 'samples':
                            self.headerparameters.append(elements[1])
                        elif elements[0] == 'lines':
                            self.headerparameters.append(elements[1])
                        elif elements[0] == 'data type':   
                            datatypeENVI = int(elements[1])
                        elif elements[0] == 'map info':
                            elements[1] = re.sub('\{','',elements[1])
                            elements[1] = re.sub('\}','',elements[1])
                            elements[1] = re.sub('\s+','',elements[1])
    
                            count = elements[1].count(',')
                            mapElements = elements[1].split(',', count)
                            i = 0
                            while i < count:
                                self.headerparameters.append(mapElements[i])
                                i = i + 1
                            
                parFile.close()
                
                # Convert ENVI to Gamma data type
                datatype = self.envi2gammaDataType(datatypeENVI)
                
                self.headerparameters.append(datatype)
                
            except IOError as e:
                print('\nCould not open file: ', e)
                raise IOError(e)
        else:
            raise BaseException
 
    def generateOutputParameters(self):
        # Append width
        self.imageparameters['width'] = self.headerparameters[0]
        # Append nlines
        self.imageparameters['nlines'] = self.headerparameters[1]
        
        # Get coordinates of corner
        resolution = float(self.headerparameters[7])
        self.imageparameters['resolution'] = resolution
        self.imageparameters['post_north'] = '-' + str(resolution)
        self.imageparameters['post_east'] = ' ' + str(resolution)

        # Subtract half pixel as corner coordinates in GAMMA start in the centre.
        self.imageparameters['corner_north'] = float(self.headerparameters[6]) - (resolution / 2.0)
        self.imageparameters['corner_east'] = float(self.headerparameters[5]) + (resolution / 2.0)
        
        # Get zone information
        zone = int(self.headerparameters[9])
        self.imageparameters['zone'] = zone
        hemisphere = self.headerparameters[10]
        self.imageparameters['hemisphere'] = hemisphere
        self.imageparameters['center_longitude'] = (zone * 6) - 183.0
        
        if hemisphere == 'North':
            self.imageparameters['fNorting'] = 0000000.000
        else:
            self.imageparameters['fNorting'] = 10000000.000
        
        # Data type
        self.imageparameters['datatype'] = self.headerparameters[-1]
        
    def generateParFile(self, outParFile):
        outPar = open(outParFile,'w')
        fileName = getFileName(outParFile)
        self.imageparameters['title'] = fileName

        out = '''Gamma DIFF&GEO DEM/MAP parameter file
title: {title}
DEM_projection:     UTM
data_format:        {datatype}
DEM_hgt_offset:          0.00000
DEM_scale:               1.00000
width:               {width}
nlines:              {nlines}
corner_north:  {corner_north}   m
corner_east:   {corner_east}   m
post_north:    {post_north}   m
post_east:     {post_east}   m

ellipsoid_name: WGS 84
ellipsoid_ra:        6378137.000   m
ellipsoid_reciprocal_flattening:  298.2572236

datum_name: WGS 1984
datum_shift_dx:              0.000   m
datum_shift_dy:              0.000   m
datum_shift_dz:              0.000   m
datum_scale_m:         0.00000e+00
datum_rotation_alpha:  0.00000e+00   arc-sec
datum_rotation_beta:   0.00000e+00   arc-sec
datum_rotation_gamma:  0.00000e+00   arc-sec
datum_country_list Global Definition, WGS84, World

projection_name: UTM
projection_zone:                 {zone}
false_easting:           500000.000   m
false_northing:         {fNorting}   m
projection_k0:            0.9996000
center_longitude:         {center_longitude}   decimal degrees
center_latitude:          0.0000000   decimal degrees\n'''.format(**self.imageparameters)
        
        outPar.write(out)
        outPar.close()              

class ParFileAEAC (ParFileObject):

    """ Generate parameter file for Albers Equal Area Conic projection """

    def __init__(self):
        ParFileObject.__init__(self)

    def getParameters(self, inHeaderFile, inImageFile):
        if inImageFile is None:
            raise Exception('No inImageFile provided')
   
        """ Get projection information using GDAL.
        """
        dataset = gdal.Open(inImageFile, gdal.GA_ReadOnly )
        projection = dataset.GetProjection()

        self.imageparameters['datatype'] = 'REAL*4' # Hardcode for now

        geotransform = dataset.GetGeoTransform()
        xSize = dataset.RasterXSize
        ySize = dataset.RasterYSize

        self.imageparameters['width'] = xSize
        self.imageparameters['nlines'] = ySize

        # Get bounding box
        minX = geotransform[0]
        maxY = geotransform[3]
        pixSizeX = geotransform[1]
        pixSizeY = geotransform[5]
        maxX = minX + (xSize * pixSizeX)
        minY = maxY + (ySize * pixSizeY)
 
        self.imageparameters['resolution'] = (pixSizeX + pixSizeY) / 2.0
        self.imageparameters['post_north'] = pixSizeY
        self.imageparameters['post_east'] = pixSizeX

        # Subtract half pixel as corner coordinates in GAMMA start in the centre.
        self.imageparameters['corner_north'] = maxY
        self.imageparameters['corner_east'] = minX
 
        imgSRS = osr.SpatialReference()
        imgSRS.ImportFromWkt(projection)

        self.imageparameters['latitude_of_center'] = imgSRS.GetProjParm('latitude_of_center')
        self.imageparameters['longitude_of_center'] = imgSRS.GetProjParm('longitude_of_center')

        self.imageparameters['standard_parallel_1'] = imgSRS.GetProjParm('standard_parallel_1')
        self.imageparameters['standard_parallel_2'] = imgSRS.GetProjParm('standard_parallel_2')

        # Close dataset
        dataset = None

    def generateParFile(self, outParFile):
        outPar = open(outParFile,'w')
        fileName = getFileName(outParFile)
        self.imageparameters['title'] = fileName

        out = '''Gamma DIFF&GEO DEM/MAP parameter file
title: {title}
DEM_projection:     AEAC
data_format:        {datatype}
DEM_hgt_offset:          0.00000
DEM_scale:               1.00000
width:                {width}
nlines:               {nlines}
corner_north:  {corner_north}   m
corner_east:    {corner_east}   m
post_north:    {post_north}   m
post_east:      {post_east}   m
first_std_parallel:      {standard_parallel_1}   decimal degrees
second_std_parallel:     {standard_parallel_2}   decimal degrees

ellipsoid_name: WGS 84
ellipsoid_ra:        6378137.000   m
ellipsoid_reciprocal_flattening:  298.2572236

datum_name: WGS 1984
datum_shift_dx:              0.000   m
datum_shift_dy:              0.000   m
datum_shift_dz:              0.000   m
datum_scale_m:         0.00000e+00
datum_rotation_alpha:  0.00000e+00   arc-sec
datum_rotation_beta:   0.00000e+00   arc-sec
datum_rotation_gamma:  0.00000e+00   arc-sec
datum_country_list Global Definition, WGS84, World

projection_name: 
projection_zone:                  0
false_easting:                0.000   m
false_northing:               0.000   m
projection_k0:            1.0000000
center_longitude:      {longitude_of_center}   decimal degrees
center_latitude:       {latitude_of_center}   decimal degrees\n'''.format(**self.imageparameters)
        
        outPar.write(out)
        outPar.close()              

class GenerateDEMParFile (object):

    def __init__(self):
        self.imageparameters = {}
        
    def getProjFromGDAL(self, inImageFile, parameters):
        """ Get projection information using GDAL.
        """
        dataset = gdal.Open(inImageFile, gdal.GA_ReadOnly )
        projection = dataset.GetProjection()

        imgSRS = osr.SpatialReference()
        imgSRS.ImportFromWkt(projection)

    def run(self, inHeaderFile, outParFile, inImageFile = None, projectionName = 'UTM'):

        if projectionName == 'UTM':
            parfile = ParFileUTM()
        elif projectionName == 'AEAC':
            parfile = ParFileAEAC()
        else:
            raise Exception('Projection name not recognised')
        
        # Get Parameters
        parfile.getParameters(inHeaderFile, inImageFile)
        
        # Write to par file 
        parfile.generateParFile(outParFile)
    
if __name__ == '__main__':
    obj = GenerateDEMParFile()

    # Read in parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("--inimage", type=str, required=False, default=None, help="Input image file")
    parser.add_argument("--inheader", type=str, required=False, default=None, help="Input header file")
    parser.add_argument("--outpar", type=str, required=True, help="Output parameter file")
    parser.add_argument("--proj", type=str, default='UTM', required=False, help="Name of projection")
    
    args = parser.parse_args()    

    obj.run(args.inheader, args.outpar, args.inimage, args.proj)
