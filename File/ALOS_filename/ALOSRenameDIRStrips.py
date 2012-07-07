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
import shutil
import sys
import tarfile
from ALOSParamsFile import ALOSParamsFile

class ALOSStripUnpackRenameTar (object):
    
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
    
    def getALOSStdFilename(self, alosParams):
        # Provide base
        filename = 'alpsba_' + alosParams.getScnID() + '_'
        # Add Incidence Angle
        if alosParams.getOffNadir() == '415':
            filename = filename + 'a'
        elif alosParams.getOffNadir() == '343':
            filename = filename + 'b'
        elif alosParams.getOffNadir() == '215':
            filename = filename + 'c'
        elif alosParams.getOffNadir() == '135':
            filename = filename + 'd'
        else:
            filename = filename + alosParams.getOffNadirStr() + '_'
        # Add lat/long
        filename = filename + alosParams.getRSP()
        filename = filename + alosParams.getUpLat()
        filename = filename + alosParams.getLowLat()
        # Add date
        filename = filename + '_' + alosParams.getScnCDate()
        # Add mode
        if alosParams.getDataType() == 'FBS':
            filename = filename + '_bs_'
        elif alosParams.getDataType() == 'FBD':
            filename = filename + '_bd_'
        elif alosParams.getDataType() == 'PLR':
            filename = filename + '_pl_'
        else:
            raise Exception('Mode \'' + alosParams.getDataType() + '\' not known')
        # Add Level    
        filename = filename + 'lev1'
        return filename
    
    def getFolderNameFromTar(self, file):
        tar = tarfile.open(file)
        names = list();
        for tarinfo in tar:
           if tarinfo.isdir():
               names.append(tarinfo.name)
        tar.close()
        
        dirNames = list()
        for name in names:
            dirName = ''
            count = 1;
            for i in range(len(name)):
                if count > 1:
                    if name[i] == '/' and name[i-1] == '.' :
                        dirName = dirName
                    elif name[i] == '/' :
                        break
                    else:
                        dirName = dirName + name[i]
                elif name[i] == '/' :
                    break
                elif name[i] == '.' :
                    dirName = dirName
                else:
                    dirName = dirName + name[i]
                count = count + 1
            dirNames.append(dirName)
        return dirNames
    
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
    
    def untarRename(self, fileList, ext, outDIR, outDIRTar):
        for file in fileList:
            try:
                print 'FILE: ' + file
                
                folderNames = self.getFolderNameFromTar(file)
                print folderNames
                
                tmpNameData = ALOSParamsFile()
                tmpNameData.createData(os.path.basename(file), folderNames[1])
                
                newfilename = self.getALOSStdFilename(tmpNameData)
                print newfilename
                
                folderName = ''
                if ext == '.gz':
                    folderName = os.path.splitext(os.path.splitext(os.path.basename(file))[0])[0]
                elif ext == '.tar':
                    folderName = os.path.splitext(os.path.basename(file))[0]
                else:
                     raise Exception('Did not reconise extension!')
                print folderName
                
                os.chdir(outDIR)
                os.mkdir(newfilename)
                newOutDIR = os.path.join(outDIR, newfilename)
                print newOutDIR
                
                if not os.path.isdir(newOutDIR):
                    raise Exception('Failed to create new directory')
                
                self.untarFile(file, ext, newOutDIR)
                os.chdir(outDIR)
                                
                self.tarDIR(newfilename, outDIR, outDIRTar, newfilename)
            except Exception, e:
                print 'ERROR OCCURED, skipping ' + str(file)
                print 'ERROR ' + str(e)
                
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 5:
            dir = sys.argv[1].strip()
            outDIR = sys.argv[2].strip()
            outTarDIR = sys.argv[3].strip()
            ext = sys.argv[4].strip()
            
            # Find all files.
            filelist = list()
            self.findFiles(filelist, dir, ext)
            
            # Process each tar file.
            self.untarRename(filelist, ext, outDIR, outTarDIR)
            
        else:
            self.help()
    
    def help(self):
        print 'python ALOSRenameDIRStrips.py <input DIR> <TMP DIR> <output DIR (TAR.GZ)> <extension>'
        

if __name__ == '__main__':
    obj = ALOSStripUnpackRenameTar()
    obj.run()