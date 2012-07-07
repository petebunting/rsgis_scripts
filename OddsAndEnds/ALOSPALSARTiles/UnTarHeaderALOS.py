#! /usr/bin/env python

#######################################
# UnTarHeaderALOS.py
# For Processing JAXA ALOS Tiles
# - UnTars Tiles
# - Generates ENVI Heaeder
# - Stacks with HH / HV ratio image
# - Generates KML
# Dan Clewley
# 20/02/2012
#######################################

import os, sys, optparse, subprocess, re, glob

class BatchRunCommand (object):
    def findExtension(self, filename, ext):
        count = filename.count('.')
        elements = filename.split('.',count)
        if elements[count] == ext:
            return True
        else:
            return False

    def unTar(self, inDIR, fileName):
        mkdirCommand = 'mkdir ' + inDIR + '/' + fileName
        os.system(mkdirCommand)
        mvCommand = 'cp ' + inDIR + '/' + fileName + '.tar.gz ' + inDIR + '/' + fileName + '/'
        os.system(mvCommand)
        os.chdir(inDIR + '/' + fileName)
        unzipCommand = 'tar -xvf ' + fileName + '.tar.gz'
        #print unzipCommand
        os.system(unzipCommand)
        removeCommand = 'rm ' + fileName + '.tar.gz'
        os.system(removeCommand)

    def createHeader(self, inFileDIR):
        os.chdir(inFileDIR)
        inHHFile = glob.glob('*HH')[0]
        inHVFile = glob.glob('*HV')[0]
        inHeaderFile = glob.glob('*_hdr')[0]
        inHHHeaderFile = inHHFile + '.hdr'
        inHVHeaderFile = inHVFile + '.hdr'
        
        inHeader = open(inHeaderFile, 'r')
        inHHHeader = open(inHHHeaderFile, 'w')
        inHVHeader = open(inHVHeaderFile, 'w')
        
        inULong = ''
        inULat = ''
        
        i = 1
        for line in inHeader:
            if i == 13:
                inULat = line.strip()
            elif i == 14:
                inULon = line.strip()
            i+=1
        
        headerText = '''ENVI
description = {
 %s}
samples = 4500
lines   = 4500
bands   = 1
header offset = 0
file type = ENVI Standard
data type = 2
interleave = bsq
sensor type = Unknown
byte order = 0
map info = {Geographic Lat/Lon, 1.0000, 1.0000, %s, %s, 2.2220000000e-04, 2.2220000000e-04, WGS-84, units=Degrees}
wavelength units = Unknown
''' %(inHeaderFile, inULon, inULat)

        inHHHeader.write(headerText)
        inHVHeader.write(headerText)
        
        inHeader.close()
        inHHHeader.close()
        inHVHeader.close()
        
        return inHHFile, inHVFile

    def createStack(self, inFile):
    
        inXMLFile = inFile + '_stack.xml'
        inXML = open(inXMLFile, 'w')
    
        xmlText = '''<?xml version="1.0" encoding="UTF-8" ?>
<!--
	Description:
		XML File for execution within RSGISLib
	Created by Daniel Clewley on Fri Jan 20 09:20:21 2012.
	Copyright (c) 2012 Aberystwyth University. All rights reserved.
-->

<rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">

	<!-- HH / HV -->
	<rsgis:command algor="imagecalc" option="bandmaths" output="IMAGE_hhDivHV.env" expression="hh / hv" >
		<rsgis:variable name="hh" image="IMAGE_HH" band="1" />
		<rsgis:variable name="hv" image="IMAGE_HV" band="1" />
	</rsgis:command>


	<!-- Create Composite-->
<rsgis:command algor="stackbands" option="imgs" output="IMAGE.env">
	<rsgis:image file="IMAGE_HH" />
	<rsgis:image file="IMAGE_HV" />
	<rsgis:image file="IMAGE_hhDivHV.env" />
</rsgis:command>

    <!-- Delete ratio image -->
    <rsgis:command algor="commandline" option="execute" command="rm IMAGE_hhDivHV.env" /> 
    
    <!-- Apply standard deviation stretch -->
	<rsgis:command algor="imageutils" option="stretch" image="IMAGE.env" output="IMAGE_sdstretch.env" stretch="LinearStdDev" stddev="1"/>
	
    <!-- Create GTiff -->
    <rsgis:command algor="commandline" option="execute" command="gdal_translate -of GTiff -ot Byte -scale 0 255 0 255 IMAGE_sdstretch.env IMAGE_tif.tif" />
    
    <!-- Delete stretched image -->
    <rsgis:command algor="commandline" option="execute" command="rm IMAGE_sdstretch.env" />
    
    <!-- Create VRT -->
    <rsgis:command algor="commandline" option="execute" command="gdalwarp -of VRT -t_srs EPSG:4326 IMAGE_tif.tif IMAGE_vrt.vrt" />

    <!-- Create KML -->
    <rsgis:command algor="commandline" option="execute" command="gdal2tiles.py -k IMAGE_vrt.vrt IMAGE_kml/" />

</rsgis:commands>'''
        xmlText = re.sub('IMAGE',inFile, xmlText)
        inXML.write(xmlText)
        inXML.close()
        
        runXML = 'rsgisexe -x ' + inXMLFile
        os.system(runXML)
    

    def run(self, inDIR):
        filelist = []
        fileList = os.listdir(inDIR)
        
        for fileName in fileList:
            inFile = fileName
            if self.findExtension(fileName, 'gz'):
                baseFile = re.sub('\.tar\.gz','',fileName)
                self.unTar(inDIR, baseFile)
                inHHFile, inHVFile = self.createHeader(inDIR + '/' + baseFile + '/')
                inBaseFile =  inDIR + '/' + baseFile + '/' + re.sub('_HH','',inHHFile)
                #self.createStack(inBaseFile) # Skip creating stack

if __name__ == '__main__':
    obj = BatchRunCommand()
    inDIR = sys.argv[1]
    obj.run(inDIR)
