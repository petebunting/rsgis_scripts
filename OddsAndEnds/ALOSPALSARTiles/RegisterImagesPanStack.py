#! /usr/bin/env python

#######################################
# RegisterImagesPan.py
# For registering PALSAR tiles to panchromatic mosaic
# Dan Clewley
# 09/05/2012
#######################################

import os, sys, optparse, subprocess, re, glob, pp

class BatchRunCommand (object):

    def generateRegXML(self, inDIR, fileName, xmlFileList):
    
        inBaseFileName = re.sub('\.env','',fileName)
        inStackFileName = re.sub('y2010','stack',inBaseFileName)
        inStackFileName = re.sub('y2007','stack',inStackFileName)
        inStackFileName = re.sub('y2008','stack',inStackFileName)
        inStackFileName = re.sub('y2009','stack',inStackFileName)
        inFile = os.path.join(inDIR, inBaseFileName)
        inStackFile = os.path.join('/fasttemp/Registration/TilesStack',inStackFileName) 
        inXMLFile = inFile + '_register.xml'
        xmlFileList.append(inXMLFile)
        inXML = open(inXMLFile, 'w')
   
        xmlText = ''

        inGCPFile = inStackFile + '_gcp.txt'

        # Check if GCP file already exists
        if (os.path.isfile(inGCPFile)):
            xmlText = '''<?xml version="1.0" encoding="UTF-8" ?>
<!--
    Description:
       XML File for execution within RSGISLib
       Created by Daniel Clewley on Wed May 9 09:20:21 2012.
       Copyright (c) 2012 Aberystwyth University. All rights reserved.
-->

<rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">

    <!-- Warp image -->
    <rsgis:command algor="registration" option="polywarp" gcps="STACK_gcp.txt" image="IMAGE.env" output="IMAGE_warp.env" projection="/data/home/ddc06/Documents/Development/RSGISScripts/WKT/slatsalbers_update.wkt" resolution="25" polyOrder="3"/>

</rsgis:commands>'''

        else:
            xmlText = '''<?xml version="1.0" encoding="UTF-8" ?>
<!--
    Description:
       XML File for execution within RSGISLib
       Created by Daniel Clewley on Wed May 9 09:20:21 2012.
       Copyright (c) 2012 Aberystwyth University. All rights reserved.
-->

<rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">

    <!-- Generate GCPs -->
    <rsgis:command algor="registration" option="singlelayer" reference="/fasttemp/Registration/LandsatPan/landsat_pan_mosaic_bbb.env" floating="STACK.env" output="STACK_gcp.txt" outputType="rsgis_img2map" metric="correlation" pixelgap="250" window="100" search="5" threshold="0.4" stddevRef="2" stddevFloat="2" subpixelresolution="4" distanceThreshold="500" maxiterations="5" movementThreshold="0.5" pSmoothness="2" />

    <!-- Warp image -->
    <rsgis:command algor="registration" option="polywarp" gcps="STACK_gcp.txt" image="IMAGE.env" output="IMAGE_warp.env" projection="/data/home/ddc06/Documents/Development/RSGISScripts/WKT/slatsalbers_update.wkt" resolution="25" polyOrder="3"/>

</rsgis:commands>'''

        xmlText = re.sub('IMAGE',inFile, xmlText) # Using reletive paths
        xmlText = re.sub('STACK',inStackFile, xmlText) # Using reletive paths
        inXML.write(xmlText)
        inXML.close()

    def runSingleCommand(self, command):
        import subprocess
        out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        print stdout
        print stderr

    def run(self, inDIR):
    
        filelist = []
        xmlFileList = [] # Setup list to hold xml files
        os.chdir(inDIR)
        fileList = glob.glob('*env') #os.listdir(inDIR)
        
        for fileName in fileList:
            self.generateRegXML(inDIR, fileName, xmlFileList) # Generate XML Files
        
        # Excecute XML
        jobs = []
        job_server = pp.Server(ncpus=8) # Set up jobserver
        for xmlFile in xmlFileList: # Add xmlfiles to jobserver
            #os.system('rsgisexe -x ' + xmlFile)
            jobs.append(job_server.submit(self.runSingleCommand,('rsgisexe -x ' + xmlFile,),modules=("subprocess",)))
        
        for job in jobs: # Run jobs
            job() 

if __name__ == '__main__':
    obj = BatchRunCommand()
    inDIR = sys.argv[1]
    obj.run(inDIR)
