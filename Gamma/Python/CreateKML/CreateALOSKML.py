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

class CreateALOSKML (object):

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
		<rsgis:variable name="hh" image="IMAGE.topo.hh.utm" band="1" />
		<rsgis:variable name="hv" image="IMAGE.topo.hv.utm" band="1" />
	</rsgis:command>


	<!-- Create Composite-->
<rsgis:command algor="stackbands" option="imgs" output="IMAGE.env">
	<rsgis:image file="IMAGE.topo.hh.utm" />
	<rsgis:image file="IMAGE.topo.hv.utm" />
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
    <rsgis:command algor="commandline" option="execute" command="gdalwarp -overwrite -of VRT -t_srs EPSG:4326 IMAGE_tif.tif IMAGE_vrt.vrt" />

    <!-- Create KML -->
    <rsgis:command algor="commandline" option="execute" command="gdal2tiles.py -k IMAGE_vrt.vrt IMAGE_kml/" />

</rsgis:commands>'''
        xmlText = re.sub('IMAGE',inFile, xmlText)
        inXML.write(xmlText)
        inXML.close()
        
        runXML = 'rsgisexe -x ' + inXMLFile
        os.system(runXML)
    

    def run(self, inDIR, outKMLDIR):
        dirList = []
        dirList = os.listdir(inDIR)
        
        for directory in dirList:
            if os.path.isdir(directory):
                fileList = []
                fileList = os.listdir(directory)
            
                for fileName in fileList:
                    inFile = fileName
                    if fileName.find('.topo.hh.utm') > 0:
                        baseFile = re.sub('\.topo\.hh\.utm','',fileName)
                        inBaseFile =  inDIR + '/' + directory + '/' + baseFile
                        self.createStack(inBaseFile)
                        cpKMLCMD = 'cp -r ' + inDIR + '/' + directory + '/' + baseFile + '_kml ' + outKMLDIR
                        os.system(cpKMLCMD)

if __name__ == '__main__':
    obj = CreateALOSKML()
    inDIR = sys.argv[1]
    outKMLDIR = sys.argv[2]
    obj.run(inDIR, outKMLDIR)
