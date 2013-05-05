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
#
# Updated 20/04/2013
# - Create header files for date, linci and mask files.
# - Stack optional

#######################################

import os, sys, re, glob

class BatchRunCommand (object):
    def findExtension(self, filename, ext):
        count = filename.count('.')
        elements = filename.split('.',count)
        if elements[count] == ext:
            return True
        else:
            return False

    def unTar(self, inDIR, fileName):
        if os.path.isdir(os.path.join(inDIR,fileName)):
            print((' Skipping ' + os.path.join(inDIR,fileName) + '.tar.gz'))
            return 0
        else:
            mkdirCommand = 'mkdir ' + inDIR + '/' + fileName
            os.system(mkdirCommand)
            mvCommand = 'cp ' + inDIR + '/' + fileName + '.tar.gz ' + inDIR + '/' + fileName + '/'
            os.system(mvCommand)
            os.chdir(inDIR + '/' + fileName)
            unzipCommand = 'tar -xf ' + fileName + '.tar.gz'
            os.system(unzipCommand)
            removeCommand = 'rm ' + fileName + '.tar.gz'
            os.system(removeCommand)

    def createHeader(self, inFileDIR):
        os.chdir(inFileDIR)
        inHHFile = glob.glob('*HH')[0]
        inHVFile = glob.glob('*HV')[0]
        inDateFile = glob.glob('*_date')[0]
        inIncFile = glob.glob('*_linci')[0]
        inMaskFile = glob.glob('*_mask')[0]
        inHeaderFile = glob.glob('KC*.hdr')[0]

        inHHHeaderFile = inHHFile + '.hdr'
        inHVHeaderFile = inHVFile + '.hdr'
        inDateHeaderFile = inDateFile + '.hdr'
        inIncHeaderFile = inIncFile + '.hdr'
        inMaskHeaderFile = inMaskFile + '.hdr'

        inHeader = open(inHeaderFile, 'r')
        inHHHeader = open(inHHHeaderFile, 'w')
        inHVHeader = open(inHVHeaderFile, 'w')
        inDateHeader = open(inDateHeaderFile,'w')
        inIncHeader = open(inIncHeaderFile,'w')
        inMaskHeader = open(inMaskHeaderFile,'w')
        
        inULong = ''
        inULat = ''
        
        i = 1
        for line in inHeader:
            if i == 13:
                inULat = line.strip()
            elif i == 14:
                inULon = line.strip()
            i+=1

        inULat = str(int(inULat) * 3600)
        inULon = str(int(inULon) * 3600)
        
        headerText = '''ENVI
description = {
 %s}
samples = 4500
lines   = 4500
bands   = 1
header offset = 0
file type = ENVI Standard
data type = 12
interleave = bsq
sensor type = Unknown
byte order = 0
map info = {Geographic Lat/Lon, 1.0000, 1.0000, %s, %s, 8.0000000000e-01, 8.0000000000e-01, WGS-84, units=Seconds}
wavelength units = Unknown
''' %(inHeaderFile, inULon, inULat)

        headerTextByte = '''ENVI
description = {
 %s}
samples = 4500
lines   = 4500
bands   = 1
header offset = 0
file type = ENVI Standard
data type = 1
interleave = bsq
sensor type = Unknown
byte order = 0
map info = {Geographic Lat/Lon, 1.0000, 1.0000, %s, %s, 8.0000000000e-01, 8.0000000000e-01, WGS-84, units=Seconds}
wavelength units = Unknown
''' %(inHeaderFile, inULon, inULat)

        inHHHeader.write(headerText)
        inHVHeader.write(headerText)
        inDateHeader.write(headerText)
        inIncHeader.write(headerTextByte)
        inMaskHeader.write(headerTextByte)
        
        inHeader.close()
        inHHHeader.close()
        inHVHeader.close()
        inDateHeader.close()
        inIncHeader.close()
        inMaskHeader.close()
        
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
    <rsgis:command algor="imagecalc" option="bandmaths" output="IMAGE_HHDivHV.env" expression="hh / hv" >
        <rsgis:variable name="hh" image="IMAGE_HH" band="1" />
        <rsgis:variable name="hv" image="IMAGE_HV" band="1" />
    </rsgis:command>

    <!-- Stretch Data -->
    <rsgis:command algor="imageutils" option="stretch" image="IMAGE_HH" output="IMAGE_HH_stretch_temp.env" format="ENVI" datatype="Byte" ignorezeros="yes" stretch="LinearStdDev" stddev="2" onePassSD="yes"/>
    <rsgis:command algor="imageutils" option="stretch" image="IMAGE_HV" output="IMAGE_HV_stretch_temp.env" format="ENVI" datatype="Byte" ignorezeros="yes" stretch="LinearStdDev" stddev="2" onePassSD="yes"/>
    <rsgis:command algor="imageutils" option="stretch" image="IMAGE_HHDivHV.env" output="IMAGE_HHDivHV_stretch_temp.env" format="ENVI" datatype="Byte" ignorezeros="yes" stretch="LinearStdDev" stddev="2" onePassSD="yes"/>

    <!-- Create Composite-->
    <rsgis:command algor="stackbands" option="imgs" output="IMAGE_stretch_tif.tif" format="GTiff" datatype="Byte" >
        <rsgis:image file="IMAGE_HH_stretch_temp.env" />
        <rsgis:image file="IMAGE_HV_stretch_temp.env" />
        <rsgis:image file="IMAGE_HHDivHV_stretch_temp.env" />
    </rsgis:command>

    <!-- Delete temp images -->
    <rsgis:command algor="commandline" option="execute" command="rm IMAGE_HHDivHV.*" /> 
    <rsgis:command algor="commandline" option="execute" command="rm IMAGE*temp*" /> 
    
    <!-- Create KML -->
    <rsgis:command algor="commandline" option="execute" command="gdal_translate -of KMLSUPEROVERLAY IMAGE_stretch_tif.tif IMAGE.kmz" />

    <!-- Delete temp images -->
    <rsgis:command algor="commandline" option="execute" command="rm IMAGE_stretch_tif*" /> 
</rsgis:commands>'''
        xmlText = re.sub('IMAGE',inFile, xmlText)
        inXML.write(xmlText)
        inXML.close()
        
        runXML = 'rsgisexe -x ' + inXMLFile
        os.system(runXML)
    

    def run(self, inDIR,createStack=False):
        filelist = []
        os.chdir(inDIR)
        fileList = glob.glob('KC*')
        
        for fileName in fileList:
            skipFile = False
            print(fileName)
            if fileName.find('.tar.gz') > -1:
                baseFile = re.sub('\.tar\.gz','',fileName)
                tarResult = self.unTar(inDIR, baseFile)
                if tarResult == 0:
                    skipFile = True
            else:
                baseFile = fileName
            if skipFile == False:
                try:
                    inHHFile, inHVFile = self.createHeader(inDIR + '/' + baseFile + '/')
                    inBaseFile =  inDIR + '/' + baseFile + '/' + re.sub('_HH','',inHHFile)
                    if createStack:
                        self.createStack(inBaseFile)
                except IndexError:
                    print(" ERROR: Not all files found!")

if __name__ == '__main__':
    obj = BatchRunCommand()
    createStack=False
    if len(sys.argv) >= 2:
        inDIR = os.path.abspath(sys.argv[1])
        if len(sys.argv) == 3:
            if sys.argv[2].strip() == '-stack':
                createStack = True
    else:
        print('''Not enough parameters provided.
Usage:
    python UnTarHeaderALOS.py inDIR [-stack]
''')
        exit()
    obj.run(inDIR, createStack)
