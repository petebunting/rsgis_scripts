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
#######################################

import os, sys, re

class CreateSARKMLHHOnly (object):

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
        
    def getScaleLine(self, filename):
        # Calculate scaling factors based on filename
        
        maxVal = 1
        if filename.find('hh') > 0 or filename.find('vv') > 0:
            maxVal = 0.25
        elif filename.find('hv') > 0 or filename.find('vv') > 0:
            maxVal = 0.05
        elif filename.find('alpha') > 0:
            maxVal = 50
        # Add more for more filetypes eg., rad.
        
        command_scale = ' -scale 0 %s 0 255 ' % str(maxVal)
        
        return command_scale
        

    def convertfiles(self, inFilePath, fileList, outFilePath, ext):
        inFilePath = inFilePath.strip()
        outFilePath = outFilePath.strip()
        command_gdal = 'gdal_translate'
        command_of = ' -of KMLSUPEROVERLAY '
        command_ot = ' -ot byte ' # Set the output format of the imagary
        command_size = ' -outsize 1000 1000' #' -outsize ' + outSize +'% ' + outSize + '% ' # Set the output size in percent
        command_scale = ' -scale 0 0.25 0 255 ' # Scale the pixel values of the image from inMin inMax outMin outMax, can be used to strech the data, leave as ' ' to retain gdal_defaults
        command = ''
        for file in fileList:
            extmatch = self.findExtension(file, ext)
            if extmatch:
                if file.find('.topo.hh') > 0:
                    print(file)
                    inFilename = file
                    baseFile = self.removeExtension(file, ext)
                    baseFile = re.sub('\.\Z','', baseFile) # Remove dot at end of string
                    baseFile = re.sub('\.','_', baseFile) # Remove dots within string
                    command_scale = self.getScaleLine(baseFile)
                    
                    # Create output directory for KML (creates a lot of files)
                    outDIR = outFilePath + '/' + baseFile + '_kml'
                    mkOutDIRCMD = 'mkdir ' + outDIR
                    os.system(mkOutDIRCMD)
                    
                    if ext == '.hdr':
                        inFilename = baseFile
                    command = command_gdal + command_of + command_ot + command_scale + ' ' + inFilePath + '/' + inFilename + ' ' + outDIR + '/' + baseFile + '_kml.kml'
                    print(command)
                    os.system(command)
            
    def run(self, inFilePath, outFilePath, inputExtension):
            if os.path.exists(inFilePath) and os.path.isdir(inFilePath) and os.path.exists(outFilePath) and os.path.isdir(outFilePath):
                print('File paths are OK')
                fileList = os.listdir(inFilePath)
                self.convertfiles(inFilePath, fileList, outFilePath, inputExtension)
            else:
                print('Check file paths.. Exiting...')
                self.help()

    def help(self):
        print('python CreateSARKMLHHOnly.py <inputDIR> <outputDIR> <input_Extension>')

if __name__ == '__main__':    
    obj = CreateSARKMLHHOnly()
    numArgs = len(sys.argv)
    inFilePath = ''
    outFilePath = ''
    
    if numArgs == 4:
        inFilePath = sys.argv[1]
        outFilePath = sys.argv[2]
        inputExtension = sys.argv[3]
        obj.run(inFilePath, outFilePath, inputExtension)
    else:
        obj.help()
