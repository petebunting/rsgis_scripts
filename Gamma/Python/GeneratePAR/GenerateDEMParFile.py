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

class GenerateDEMParFile (object):
        
    def getFileName(self, filePath):
        count = filePath.count('/')
        elements = filePath.split('/', count)
        name = re.sub('_par','',elements[count])
        return name
        
    def getParametersfromHDR(self, inHeaderFile, parameters):
        if(os.path.isfile(inHeaderFile)):
            #print 'Found parameters file'
            try:
                parFile = open(inHeaderFile, 'r') 
                for eachLine in parFile:
                    #print eachLine
                    count = eachLine.count('=')
                    #print 'count = ' + str(count)
                    if(count == 1):
                        elements = eachLine.split('=', count)
                        elements[0] = elements[0].strip()
                        elements[1] = elements[1].strip()
                        if elements[0] == 'samples':
                            parameters.append(elements[1])
                        elif elements[0] == 'lines':
                            parameters.append(elements[1])
                        elif elements[0] == 'map info':
                            elements[1] = re.sub('\{','',elements[1])
                            elements[1] = re.sub('\}','',elements[1])
                            elements[1] = re.sub('\s+','',elements[1])
    
                            count = elements[1].count(',')
                            mapElements = elements[1].split(',', count)
                            i = 0
                            while i < count:
                                parameters.append(mapElements[i])
                                i = i + 1
                            
                parFile.close()
            except IOError as e:
                print(('\nCould not open file: ', e))
                raise IOError(e)
        else:
            raise BaseException
 
    def generateOutputParameters(self, parameters, outputParameters):
        # Append width
        outputParameters.append(parameters[0])
        # Append nlines
        outputParameters.append(parameters[1])
        
        # Get coordinates of corner
        resolution = float(parameters[7])
        post_north = '-' + str(resolution)
        post_east = ' ' + str(resolution)
        corner_north = float(parameters[6]) - resolution
        corner_east = float(parameters[5]) + resolution
        
        outputParameters.append(str(corner_north))
        outputParameters.append(str(corner_east))
        outputParameters.append(str(post_north))
        outputParameters.append(str(post_east))
        
        # Get zone information
        zone = int(parameters[9])
        hemisphere = parameters[10]
        center_longitude = (zone * 6) - 183
        
        if hemisphere == 'North':
            fNorting = 0000000.000
        else:
            fNorting = 10000000.000
        
        outputParameters.append(str(zone))
        outputParameters.append(str(fNorting))
        outputParameters.append(str(center_longitude))
        
    def generateParFile(self, outputParameters, outParFile):
        outPar = open(outParFile,'w')
        fileName = self.getFileName(outParFile)
        out = '''Gamma DIFF&GEO DEM/MAP parameter file
title: %s
DEM_projection:     UTM
data_format:        INTEGER*2
DEM_hgt_offset:          0.00000
DEM_scale:               1.00000
width:               %s
nlines:              %s
corner_north:  %s   m
corner_east:   %s   m
post_north:    %s   m
post_east:     %s   m

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
projection_zone:                 %s
false_easting:           500000.000   m
false_northing:        %s   m
projection_k0:            0.9996000
center_longitude:       %s   decimal degrees
center_latitude:          0.0000000   decimal degrees\n''' % (fileName, outputParameters[0],outputParameters[1],outputParameters[2],outputParameters[3],outputParameters[4],outputParameters[5],outputParameters[6],outputParameters[7],outputParameters[8])
        
        outPar.write(out)
        outPar.close()              

    def run(self, inHeaderFile, outParFile):
        # Get parameters from header file
        parameters = list() 
        outputParameters = list()
        
        self.getFileName(outParFile)
        
        self.getParametersfromHDR(inHeaderFile, parameters)
        
        # Generate parameters for output file
        self.generateOutputParameters(parameters,outputParameters)
        
        # Write to par file 
        self.generateParFile(outputParameters, outParFile)
    
    def help(self):
        print('Script to generate GAMMA Par file from ENVI header file')
        print('python GenerateParFile.py <inHeaderFile> <outParFile>')

if __name__ == '__main__':
    obj = GenerateDEMParFile()
    numArgs = len(sys.argv)
    if numArgs == 3:
        inHeaderFile = sys.argv[1].strip()
        outParFile = sys.argv[2].strip()
        obj.run(inHeaderFile, outParFile)
    else:
        obj.help()
