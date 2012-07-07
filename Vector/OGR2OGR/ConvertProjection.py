#! /usr/bin/env python

#######################################
# ConvertProjection.py
# 
# A script to convert the projection
# of a shapefile using ogr2ogr
# For more ogr2ogr options see
# www.gdal.org/ogr2ogr.html
#
# Modified from ConvertImageryTIFF by
# Pete Bunting
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 26/05/2011
# Version: 1.0
#######################################

import os, sys, re

class ConvertProjection (object):
        
    def checkFileExtension(self, filename, ext):
        count = filename.count('.')
        elements = filename.split('.',count)
        if elements[count] == ext:
            return True
        else:
            return False
    
    def convertProj(self, inDIR, outDIR, fileName, outProjDef, outProjName):
       inSHP = os.path.join(inDIR,fileName)
       outSHPName = re.sub('\.shp', '_' + outProjName, fileName) + '.shp'
       outSHP = os.path.join(outDIR, outSHPName)
       ogr2ogrCMD = 'ogr2ogr -overwrite -f "ESRI Shapefile" -t_srs %s %s %s' %(outProjDef, outSHP, inSHP)
       os.system(ogr2ogrCMD)

    def run(self, inDIR, outDIR, outProjDef, outProjName):
        fileList = os.listdir(inDIR)
        for fileName in fileList:
            if self.checkFileExtension(fileName, 'shp'):
                print fileName
                self.convertProj(inDIR, outDIR, fileName, outProjDef, outProjName) 

    def help(self):
        print '''--CreateCSVfromSHP--
Reproject all shapefile in\na directory.
Can define output extention to be added to file name (e.g., \'utm\' will add \'_utm.shp\' to
the end of the input file name.
Use \'-\' to set output shapefiles to input DIR
Usage:
python ConvertProjection.py <inputDIR> <outputDIR=-> <projectionDefinition> <projection fileName addition (optional)>'''

if __name__ == '__main__':    
    obj = ConvertProjection()
    numArgs = len(sys.argv)
    if numArgs == 4:
       inDIR = sys.argv[1]
       outDIR = sys.argv[2].strip()
       if outDIR == '-':
           outDIR = inDIR
       outProjDef = sys.argv[3]
       outProjName = 'reproj'
       obj.run(inDIR, outDIR, outProjDef, outProjName)
    elif numArgs == 5:
       inDIR = sys.argv[1]
       outDIR = sys.argv[2].strip()
       if outDIR == '-':
           outDIR = inDIR
       outProjDef = sys.argv[3]
       outProjName = sys.argv[4].strip()
       obj.run(inDIR, outDIR, outProjDef, outProjName)
    else:
        obj.help()
