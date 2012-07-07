#! /usr/bin/env python

#######################################
# CreateCSVfromSHP.py
# 
# A script to create a csv file from a
# shapefile using ogr2ogr
# For more ogr2ogr options see
# www.gdal.org/ogr2ogr.html
#
# Modified from ConvertImageryTIFF by
# Pete Bunting
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 26/04/2010
# Version: 1.0
#######################################

import os, sys

class CreateCSVfromSHP (object):
        
    def checkFileExtension(self, filename, ext):
        count = filename.count('.')
        elements = filename.split('.',count)
        if elements[count] == ext:
            return True
        else:
            return False
    
    def createCSV(self, inDIR, fileName):
       inSHP = inDIR + '/' + fileName
       tempOutDIR = inDIR + '/temp'
       
       ogr2ogrCMD = 'ogr2ogr -f \"CSV\" %s %s ' %(tempOutDIR, inSHP)
       os.system(ogr2ogrCMD)
       
       # Move CSV file from temp dir
       mvCSVCMD = 'mv %s/* %s' %(tempOutDIR, inDIR)
       os.system(mvCSVCMD)
       
       # Remove temp dir
       rmTempDIRCMD = 'rm -fr ' + tempOutDIR
       os.system(rmTempDIRCMD)
       
    def run(self, inDIR):
        fileList = os.listdir(inDIR)
        for fileName in fileList:
            if self.checkFileExtension(fileName, 'shp'):
                print fileName
                self.createCSV(inDIR, fileName) 

    def help(self):
        print '--CreateCSVfromSHP--'
        print 'Create CSV files for all shapefile in\na directory.'
        print 'Usage:'
        print ' python CreateCSVfromSHP.py <inputDIR>'

if __name__ == '__main__':    
    obj = CreateCSVfromSHP()
    numArgs = len(sys.argv)
    if numArgs == 2:
       inDIR = sys.argv[1]
       obj.run(inDIR)
    else:
        obj.help()
