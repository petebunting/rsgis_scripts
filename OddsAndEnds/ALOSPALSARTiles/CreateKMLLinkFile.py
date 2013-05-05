#! /usr/bin/env python

#######################################
# CreateQuickLook.py
# 
# A script to create quickview files PNG
# files of Remote sensing imagary using
# Gdal
# For more options on gdal_translate see
# http://www.gdal.org/gdal_translate.html
#
# Modified from ConvertImageryTIFF by
# Pete Bunting
#
# Author: Dan Clewley
# Email: ddc06@aber.ac.uk
# Date: 12/06/2009
# Version: 1.1
# Modified 22/02/2011 - Dan Clewley
# Version to create quicklooks from GAMMA output
# Checks filename to get scaleing factors
#
# Modifed by Pete Bunting to make a general 
# script for creating raster KML files.
#
#######################################

import os, sys, re, glob

class CreateKMLLinkFile (object):

    def removeExtension(self, name, ext):
        outName = name
        count = name.find(ext.lower(), 0, len(name.lower()))
        if not count == -1:
            outName = name.replace(ext.lower(), '', name.count(ext.lower()))
        return outName
            
    def findExtension(self, filename, ext):
        count = filename.count('.')
        elements = filename.split('.',count)
        if elements[count] == ext:
            return True
        else:
            return False
        
    def removeFilePathUNIX(self, name):
        name = name.strip()
        count = name.count('/')
        nameSegments = name.split('/', count)
        return nameSegments[count]
        
    def removeFilePathWINS(self, name):
        name = name.strip()
        count = name.count('\\')
        nameSegments = name.split('\\', count)
        return nameSegments[count]
        

    def convertfiles(self, inFilePath, fileList, outFile, searchStr, outputPath, prjName):
        inFilePath = inFilePath.strip()
        os.chdir(inFilePath)
	fileList = glob.glob(searchStr)
	outputKMLLinkFile = open(outFile, 'w')
        outputKMLLinkFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        outputKMLLinkFile.write("<kml xmlns=\"http://earth.google.com/kml/2.1\">\n")
        outputKMLLinkFile.write("\t<Document>\n")
        outputKMLLinkFile.write("\t\t<name>" + prjName + "</name>\n")
        outputKMLLinkFile.write("\t\t<open>1</open>\n")
        outputKMLLinkFile.write("\t\t<visibility>1</visibility>\n")
        for file in fileList:
    	    print(file)
	    kmlPath = os.path.join(file, "doc.kml")
	    baseFile = re.sub('_kml','',file)
	    outputKMLLinkFile.write("\t\t<NetworkLink>\n")
	    outputKMLLinkFile.write("\t\t\t<open>1</open>\n")
	    outputKMLLinkFile.write("\t\t\t<name>" + baseFile + "</name>\n")
	    outputKMLLinkFile.write("\t\t\t<Link>\n")
	    outputKMLLinkFile.write("\t\t\t\t<href>" + outputPath + "/" + kmlPath + "</href>\n")
#outputK    MLLinkFile.write("\t\t\t\t<viewRefreshMode>onRegion</viewRefreshMode>\n")
	    outputKMLLinkFile.write("\t\t\t</Link>\n")
	    outputKMLLinkFile.write("\t\t</NetworkLink>\n")
            
	outputKMLLinkFile.write("\t</Document>\n")  
        outputKMLLinkFile.write("</kml>\n")

            
    def run(self, inFilePath, outFile, searchStr, outputPath, prjName):
        if os.path.exists(inFilePath) and os.path.isdir(inFilePath):
            print('File paths are OK')
            fileList = os.listdir(inFilePath)
            self.convertfiles(inFilePath, fileList, outFile, searchStr, outputPath, prjName)
        else:
            print('Check file paths.. Exiting...')
            self.help()

    def help(self):
        print('python CreateKMLLinkFile.py <inputDIR> <outputFile> <searchStr> <output_Path> <Name>')

if __name__ == '__main__':    
    obj = CreateKMLLinkFile()
    numArgs = len(sys.argv)
    inFilePath = ''
    outFilePath = ''
    
    if numArgs == 6:
        inFilePath = sys.argv[1]
        outFile = sys.argv[2]
        searchStr = sys.argv[3]
        outputPath = sys.argv[4]
        prjName = sys.argv[5]
        obj.run(inFilePath, outFile, searchStr, outputPath, prjName)
    else:
        obj.help()
