#! /usr/bin/env python

#######################################
# A class automatically generate ENVI
# header files from the GAMMA outputted
# par parameter files.
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 06/03/2008
# Version: 1.0
#######################################

import os.path
import sys
import tarfile
from ALOSParams import ALOSParams

class ALOSUnpackRenameTar (object):
    
    def checkforSemiColons(self, line):
        foundSemiColon = False
        for i in range(len(line)):
            if line[i] == ';':
                foundSemiColon = True
        return foundSemiColon

    def parseDataFile(self, dataFile, list):
        for eachLine in dataFile:
            #print eachLine
            semiColon = self.checkforSemiColons(eachLine)
            if semiColon == False:
                tmpData = ALOSParams()
                tmpData.createData(eachLine)
                list.append(tmpData)    
    
    def printParams(self, dataList):
        for data in dataList:
            print data.toString()
            
    def findALOSParams(self, dataList, sceneID):
        for data in dataList:
            if data.sameScnID(sceneID):
                return data
        raise Exception('Could not find sceneID..')
        
    
    def checkFileExtension(self, filename, extension):
        foundExtension = False;
        filenamesplit = os.path.splitext(filename)
        fileExtension = filenamesplit[1].strip()
        if(fileExtension == extension):
            foundExtension = True
        return foundExtension
    
    def findFiles(self, filelist, directory, extension):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                fileList = os.listdir(directory)
                for filename in fileList:
                    #print filename
                    if(os.path.isdir(os.path.join(directory,filename))):
                        #print filename + ' is a directory.'
                        self.findFiles(filelist, os.path.join(directory,filename), extension)
                    elif(os.path.isfile(os.path.join(directory,filename))):
                        #print filename + ' is a file.'
                        if(self.checkFileExtension(filename, extension)):
                            #print 'FOUND FILE - ADD TO LIST!'
                            filelist.append(os.path.join(directory,filename))
                    else:
                        print filename + ' is NOT a file or directory!'
            else:
                print directory + ' is not a directory!'
        else:
            print directory + ' does not exist!'
    
    def getALOSSceneID(self, filepath):
        tar = tarfile.open(filepath)
        names = list();
        for tarinfo in tar:
           if tarinfo.isfile():
               names.append(tarinfo.name)
        tar.close()
        sceneID=''
        for name in names:
            filePathSplit = os.path.split(name)
            filename = filePathSplit[1]
            #print 'filename: ', filename, '  ', filename[0:7]
            if filename[0:7] == 'IMG-HH-':
                sceneID = filename[7:22]
        return sceneID
    
    
    def getALOSStdFilename(self, alosParams):
        # Provide base
        filename = 'alpsba_' + alosParams.getScnID()[6:15] + '_'
        # Add Incidence Angle
        if alosParams.getOffNadir() == 41.5:
            filename = filename + 'a'
        elif alosParams.getOffNadir() == 34.3:
            filename = filename + 'b'
        elif alosParams.getOffNadir() == 21.5:
            filename = filename + 'c'
        elif alosParams.getOffNadir() == 13.5:
            filename = filename + 'd'
        else:
            filename = filename + alosParams.getOffNadirStr() + '_'
        # Add lat/long
        filename = filename + alosParams.getStrLat()
        filename = filename + alosParams.getStrLong()
        # Add date
        filename = filename + '_' + alosParams.getDateStr()
        # Add mode
        if alosParams.getOpeMD() == 'FBS':
            filename = filename + '_bs_'
        elif alosParams.getOpeMD() == 'FBD':
            filename = filename + '_bd_'
        elif alosParams.getOpeMD() == 'PLR':
            filename = filename + '_pl_'
        else:
            raise Exception('Mode \'' + alosParams.getOpeMD() + '\' not known')
        # Add Level    
        if alosParams.getLevel() == 1:
            filename = filename + 'lev1'
        elif alosParams.getLevel() == 1.5:
            filename = filename + 'lev1_5'
        else:
            raise Exception ('Level \'' + alosParams.getLevel() + '\' unknown')
        return filename
    
    def getFolderNameFromTar(self, file):
        tar = tarfile.open(file)
        name = ''
        for tarinfo in tar:
           if tarinfo.isdir():
               name = tarinfo.name
               break
        tar.close()
        
        dirName = ''
        for i in range(len(name)):
            if name[i] == '/':
                break
            else:
                dirName = dirName + name[i]
        return dirName
    
    def untarFile(self, file, ext, outDIR):
        os.chdir(outDIR)
        tarcommand = 'tar -xvf '
        gzcommand = 'tar -xvzf '
        command = ''
        if ext == '.tar':
            command = tarcommand
        elif ext == '.gz':
            command = gzcommand
        command = tarcommand + file
        print command
        os.system(command)
            
    def tarDIR(self, dir, tarDIR, outDIR, filename):
        os.chdir(tarDIR)
        command = 'tar -czf ' + os.path.join(outDIR,filename) + '.tar.gz ' + dir
        print command
        os.system(command)
    
    def untarRename(self, fileList, alosParams, ext, outDIR, outDIRTar):
        for file in fileList:
            try:
                print 'Processing: ', file
                sceneID = self.getALOSSceneID(file)
                print 'SceneID: ', sceneID
                ALOSParam = self.findALOSParams(alosParams, sceneID)
                print ALOSParam.toString()
                newFilename = self.getALOSStdFilename(ALOSParam)
                print 'New filename: ', newFilename
                
                folderName = self.getFolderNameFromTar(file)
                print 'Current Folder Name:', folderName
                
                self.untarFile(file, ext, outDIR)
                os.chdir(outDIR)
                os.rename(folderName, newFilename)
                
                toTar = os.path.join(outDIR, newFilename)
                if not os.path.isdir(toTar):
                   raise Exception('Failed to create tar')
               
                self.tarDIR(newFilename, outDIR, outDIRTar, newFilename)
                print 'Finished File'
            except Exception, e:
                print 'ERROR OCCURED, skipping ' + str(file)
                print 'ERROR ' + str(e)
                
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 6:
            dir = sys.argv[1].strip()
            paramsFilepath = sys.argv[2].strip()
            ext = sys.argv[3].strip()
            outDIR = sys.argv[4].strip()
            outTarDIR = sys.argv[5].strip()
            print 'Parameters file: ', paramsFilepath
            
            # Get params from which filename can be created.
            alosParams = list()
            try:
                paramsFile = open(paramsFilepath, 'r') 
            except IOError, e:
                print '\nCould not open file:\n', e
                return
            self.parseDataFile(paramsFile, alosParams)
            #self.printParams(alosParams)
            
            # Find all files.
            filelist = list()
            self.findFiles(filelist, dir, ext)
            
            # Process each tar file.
            self.untarRename(filelist, alosParams, ext, outDIR, outTarDIR)
            
        else:
            self.help()
    
    def help(self):
        print 'python ALOSUnpackRenameTar <input DIR> <Parameters_file> <ext> <output DIR (unpack)> <output DIR (TAR.GZ)>'
        

if __name__ == '__main__':
    obj = ALOSUnpackRenameTar()
    obj.run()