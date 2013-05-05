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

import os, sys, optparse, subprocess, re, glob, pp

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
        print(unzipCommand)
        os.system(unzipCommand)
        removeCommand = 'rm ' + fileName + '.tar.gz'
        os.system(removeCommand)

    def createHeader(self, inFileDIR):
        os.chdir(inFileDIR)
        inHHFile = glob.glob('*HH')[0]
        inHVFile = glob.glob('*HV')[0]
        inHeaderFile = glob.glob('*.hdr')[0]
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

        inHHHeader.write(headerText)
        inHVHeader.write(headerText)
        
        inHeader.close()
        inHHHeader.close()
        inHVHeader.close()
        
        return inHHFile, inHVFile

    def createStack(self, inFile, inSceneDIR, xmlFileList):
    
        inXMLFile = inSceneDIR + '/' + inFile + '_stack.xml'
        inXML = open(inXMLFile, 'w')
        inFilePath = inSceneDIR + '/' + inFile   
 
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

    <!-- Convert to dB -->
    <rsgis:command algor="imagecalc" option="bandmaths" output="IMAGE_HHdB_tif.tif" format="GTiff" expression="20 * log(b1) - 83.0" >
        <rsgis:variable name="b1" image="IMAGE_HH" band="1" />
    </rsgis:command>
    
    <rsgis:command algor="imagecalc" option="bandmaths" output="IMAGE_HVdB_tif.tif" format="GTiff" expression="20 * log(b1) - 83.0" >
        <rsgis:variable name="b1" image="IMAGE_HV" band="1" />
    </rsgis:command>

    <!-- Stretch Data -->
    <rsgis:command algor="commandline" option="execute" command="gdal_translate -of ENVI -ot Byte -scale 3000 10000 0 255 IMAGE_HH IMAGE_HH_stretch_temp.env" />
    <rsgis:command algor="commandline" option="execute" command="gdal_translate -of ENVI -ot Byte -scale 1000 3000 0 255 IMAGE_HV IMAGE_HV_stretch_temp.env" />
    <rsgis:command algor="commandline" option="execute" command="gdal_translate -of ENVI -ot Byte -scale 1 4 0 255 IMAGE_HHDivHV.env IMAGE_HHDivHV_stretch_temp.env" />

    <!-- Create Composite-->
<rsgis:command algor="stackbands" option="imgs" output="IMAGE_stretch_tif.tif" format="GTiff" datatype="Byte" >
    <rsgis:image file="IMAGE_HH_stretch_temp.env" />
    <rsgis:image file="IMAGE_HV_stretch_temp.env" />
    <rsgis:image file="IMAGE_HHDivHV_stretch_temp.env" />
</rsgis:command>

    <!-- Delete temp images -->
    <rsgis:command algor="commandline" option="execute" command="rm IMAGE_HHDivHV.*" /> 
    <rsgis:command algor="commandline" option="execute" command="rm IMAGE*temp*" /> 
    
    <!-- Create VRT -->
    <rsgis:command algor="commandline" option="execute" command="gdalwarp -overwrite -of VRT -t_srs EPSG:4326 IMAGE_stretch_tif.tif IMAGE_vrt.vrt" />

    <!-- Create KML -->
    <rsgis:command algor="commandline" option="execute" command="gdal2tiles.py -k IMAGE_vrt.vrt IMAGE_kml/" />

</rsgis:commands>'''
        xmlText = re.sub('IMAGE',inFilePath, xmlText)
        inXML.write(xmlText)
        inXML.close()
        
        os.chdir(inSceneDIR)
        runXML = 'rsgisexe -x ' + inXMLFile
        xmlFileList.append(inXMLFile)
        #os.system(runXML)
   
    def runSingleCommand(self, command):
        import subprocess
        out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        print(stdout)
        print(stderr)

    def run(self, inDIR):
        filelist = []
        xmlFileList = [] # Create list for XML files
        os.chdir(inDIR)
        fileList = glob.glob('KC*') #os.listdir(inDIR)
        
        for fileName in fileList:
            print(fileName)
            inFile = fileName
            baseFile = fileName #re.sub('\.tar\.gz','',fileName)
            #self.unTar(inDIR, baseFile)
            inHHFile, inHVFile = self.createHeader(inDIR + '/' + baseFile + '/')
            inSceneDIR =  inDIR + '/' + baseFile + '/' 
            inBaseFile = re.sub('_HH','',inHHFile)
            self.createStack(inBaseFile, inSceneDIR, xmlFileList)
    
        # Excecute XML
        jobs = []
        job_server = pp.Server(ncpus=4) # Set up jobserver
        for xmlFile in xmlFileList: # Add xmlfiles to jobserver
            #os.system('rsgisexe -x ' + xmlFile)
            jobs.append(job_server.submit(self.runSingleCommand,('rsgisexe -x ' + xmlFile,),modules=("subprocess",)))

        for job in jobs: # Run jobs
            job()


if __name__ == '__main__':
    obj = BatchRunCommand()
    inDIR = sys.argv[1]
    obj.run(inDIR)
