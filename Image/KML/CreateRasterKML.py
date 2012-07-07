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

import os, sys, re

class CreateRasterKMLQk (object):

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
        

    def convertfiles(self, inFilePath, fileList, outFilePath, ext, linkFile, prjName, minVal, maxVal):
        outputKMLFiles = list()
        inFilePath = inFilePath.strip()
        outFilePath = outFilePath.strip()
        command_gdal = 'gdal_translate'
        command_of = ' -of KMLSUPEROVERLAY '
        command_ot = ' -ot byte ' # Set the output format of the imagary
        command_size = ' -outsize 1000 1000' #' -outsize ' + outSize +'% ' + outSize + '% ' # Set the output size in percent
        command_scale = ' -scale ' + str(minVal) + ' ' + str(maxVal) + ' 0 255 ' # Scale the pixel values of the image from inMin inMax outMin outMax, can be used to strech the data, leave as ' ' to retain gdal_defaults
        command = ''
        for file in fileList:
            extmatch = self.findExtension(file, ext)
            if extmatch:
                print file
                inFilename = file
                baseFile = self.removeExtension(file, ext)
                baseFile = re.sub('\.\Z','', baseFile) # Remove dot at end of string
                baseFile = re.sub('\.','_', baseFile) # Remove dots within string
                
                # Create output directory for KML (creates a lot of files)
                outDIR = outFilePath + '/' + baseFile + '_kml'
                mkOutDIRCMD = 'mkdir ' + outDIR
                os.system(mkOutDIRCMD)
                
                if ext == '.hdr':
                    inFilename = baseFile
                command = command_gdal + command_of + command_ot + command_scale + ' ' + inFilePath + '/' + inFilename + ' ' + outDIR + '/' + baseFile + '_kml.kml'
                print command
                os.system(command)
                outputKMLFiles.append(baseFile)
        outputKMLLinkFile = open(linkFile, 'w')
        outputKMLLinkFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        outputKMLLinkFile.write("<kml xmlns=\"http://earth.google.com/kml/2.1\">\n")
        outputKMLLinkFile.write("\t<Document>\n")
        outputKMLLinkFile.write("\t\t<name>" + prjName + "</name>\n")
        outputKMLLinkFile.write("\t\t<open>1</open>\n")
        outputKMLLinkFile.write("\t\t<visibility>1</visibility>\n")
        for kmlFile in outputKMLFiles:
            outDIR = './' + kmlFile + '_kml'
            outputKMLLinkFile.write("\t\t<NetworkLink>\n")
            outputKMLLinkFile.write("\t\t\t<open>1</open>\n")
            outputKMLLinkFile.write("\t\t\t<name>" + kmlFile + "</name>\n")
            outputKMLLinkFile.write("\t\t\t<Link>\n")
            outputKMLLinkFile.write("\t\t\t\t<href>" + outDIR + "/" + kmlFile + "_kml.kml" + "</href>\n")
            #outputKMLLinkFile.write("\t\t\t\t<viewRefreshMode>onRegion</viewRefreshMode>\n")
            outputKMLLinkFile.write("\t\t\t</Link>\n")
            outputKMLLinkFile.write("\t\t</NetworkLink>\n")
        outputKMLLinkFile.write("\t</Document>\n")  
        outputKMLLinkFile.write("</kml>\n")

            
    def run(self, inFilePath, outFilePath, inputExtension, linkFileprjName, ):
        if os.path.exists(inFilePath) and os.path.isdir(inFilePath) and os.path.exists(outFilePath) and os.path.isdir(outFilePath):
            print 'File paths are OK'
            fileList = os.listdir(inFilePath)
            self.convertfiles(inFilePath, fileList, outFilePath, inputExtension, linkFile, prjName, 0 , 255)
        else:
            print 'Check file paths.. Exiting...'
            self.help()
            
    def run(self, inFilePath, outFilePath, inputExtension, linkFile, prjName, minVal, maxVal):
        if os.path.exists(inFilePath) and os.path.isdir(inFilePath) and os.path.exists(outFilePath) and os.path.isdir(outFilePath):
            print 'File paths are OK'
            fileList = os.listdir(inFilePath)
            self.convertfiles(inFilePath, fileList, outFilePath, inputExtension, linkFile, prjName, minVal, maxVal)
        else:
            print 'Check file paths.. Exiting...'
            self.help()

    def help(self):
        print 'python CreateSARKML.py <inputDIR> <outputDIR> <input_Extension> <Link File> <Name> [Optional: Min Max]'

if __name__ == '__main__':    
    obj = CreateRasterKMLQk()
    numArgs = len(sys.argv)
    inFilePath = ''
    outFilePath = ''
    
    if numArgs == 6:
        inFilePath = sys.argv[1]
        outFilePath = sys.argv[2]
        inputExtension = sys.argv[3]
        linkFile = sys.argv[4]
        prjName = sys.argv[5]
        obj.run(inFilePath, outFilePath, inputExtension, linkFile, prjName)
    if numArgs == 8:
        inFilePath = sys.argv[1]
        outFilePath = sys.argv[2]
        inputExtension = sys.argv[3]
        linkFile = sys.argv[4]
        prjName = sys.argv[5]
        inputMin = float(sys.argv[6])
        inputMax = float(sys.argv[7])
        obj.run(inFilePath, outFilePath, inputExtension, linkFile, prjName, inputMin, inputMax)
    else:
        obj.help()
