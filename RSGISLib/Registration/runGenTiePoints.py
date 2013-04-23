#! /usr/bin/env python

#######################################
# runGenTiePoints.py 
# A script for generating tie points
# using RSGISLib
# Parallel python used to run in parallel
#
# Dan Clewley (daniel.clewley@gmail.com)
# 09/03/2013
#
# Modified from:
# RegisterImagesPan.py
# Dan Clewley - 09/05/2012
#######################################

import os, sys, argparse, subprocess, re, glob

# Check if pp is on the system for running in parallel.
usePP = True

try:
    import pp
except ImportError:
    usePP = False

class BatchRunCommand (object):

    def __init__(self, inDIR, outDIR, inRefImage, ext):
        self.inDIR = inDIR
        self.outDIR = outDIR
        self.inRefImage = inRefImage
        self.ext = ext
        self.scriptsPath = os.sys.path[0]

    def generateRegXML(self, fileName, xmlFileList):
    
        inBaseFileName = re.sub('\.' + self.ext,'',fileName)
        inFile = os.path.join(self.inDIR, fileName)
        outGCPFile = os.path.join(self.outDIR, inBaseFileName) + '_gcp.txt'
        outGCPDiffFile = os.path.join(self.outDIR, inBaseFileName) + '_gcp_diffs.txt'
        inXMLFile = os.path.join(self.outDIR, inBaseFileName) + '_genTiePoints.xml'
        xmlFileList.append(inXMLFile)
        inXML = open(inXMLFile, 'w')
   
        xmlText = '''<?xml version="1.0" encoding="UTF-8" ?>
<!--
    Description:
       XML File for execution within RSGISLib
       Created by Daniel Clewley on Sat March 9 20:39:21 2013.
       Copyright (c) 2012 Aberystwyth University. All rights reserved.
-->

<rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">

    <!-- Generate GCPs -->
    <rsgis:command algor="registration" option="singlelayer" reference="%s" floating="%s" output="%s" outputType="rsgis_img2map" metric="correlation" pixelgap="250" window="250" search="5" threshold="0.4" stddevRef="2" stddevFloat="2" subpixelresolution="4" distanceThreshold="500" maxiterations="5" movementThreshold="0.5" pSmoothness="2" />

    <rsgis:command algor="commandline" option="execute" command="python %s/addFloatCoords2TiePoints.py %s %s %s" >

</rsgis:commands>'''%(self.inRefImage, inFile, outGCPFile, self.scriptsPath, inFile, outGCPFile, outGCPDiffFile)

        inXML.write(xmlText)
        inXML.close()

    def runSingleCommand(self, command):
        """ A function to run a single command using
            subprocess.
        """
        import subprocess
        out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        print(stdout)
        print(stderr)

    def run(self, xmlOnly=False):
    
        filelist = []
        xmlFileList = [] # Setup list to hold xml files
        os.chdir(self.inDIR)
        fileList = glob.glob('*.' + self.ext) #os.listdir(inDIR)
        
        for fileName in fileList:
            self.generateRegXML(fileName, xmlFileList) # Generate XML Files
        
        # Excecute XML
        if xmlOnly == False:
            if usePP:
                jobs = []
                job_server = pp.Server() # Set up jobserver
                for xmlFile in xmlFileList: # Add xmlfiles to jobserver
                       jobs.append(job_server.submit(self.runSingleCommand,('rsgisexe -x ' + xmlFile,),modules=("subprocess",)))
                       
                for job in jobs: # Run jobserver
                    job() 
    
            else:
                for xmlFile in xmlFileList:
                    os.system('rsgisexe -x ' + xmlFile)
        else:
            print('Generated tie points for: ' + str(len(xmlFileList)) + ' files')
            print('\nIf GNU parallel is installed you can run using:')
            print(' find ' + self.outDIR + ' -name *_genTiePoints.xml | parallel rsgisexe -x')
        

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--indir", type=str, help="Input directory, containing tiles")
    parser.add_argument("-o", "--outdir", type=str, help="Output directory for XML scripts and tie points")
    parser.add_argument("-r", "--refimage", type=str, help="Reference image")
    parser.add_argument("-e", "--ext", type=str, default='kea', help="File extension to search for (default=kea)")
    parser.add_argument("--xmlonly", dest='genXMLOnly', action='store_true')
    args = parser.parse_args()    
    
    if args.indir == None:
        print('No input directory provided')
        parser.print_help()
        exit()
    if args.outdir == None:
        print('No output directory provided')
        parser.print_help()
        exit()
    if args.refimage == None:
        print('No reference image provided')
        parser.print_help()
        exit()
    

    obj = BatchRunCommand(args.indir, args.outdir, args.refimage, args.ext)
    obj.run(args.genXMLOnly)
