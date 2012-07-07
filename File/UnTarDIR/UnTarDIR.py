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

class UnTarDIR (object):
    
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
    
    def untargzFiles(self, filelist, outDIR):
        os.chdir(outDIR)
    	tarcommand = 'tar -xvzf '
    	command = ''
        try:
            for filename in filelist:
                print filename
                command = tarcommand + filename
                os.system(command)
        except IOError, e:
            print 'IOError Occurred: ' + str(e)
            
            
    def untarfiles(self, filelist, outDIR):
    	os.chdir(outDIR)
    	tarcommand = 'tar -xvf '
    	command = ''
        try:
            for filename in filelist:
                print filename
                command = tarcommand + filename
                os.system(command)
        except IOError, e:
            print 'IOError Occurred: ' + str(e)
            
    
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 4:
            dir = sys.argv[1].strip()
            extension = sys.argv[2].strip()
            outDIR = sys.argv[3].strip()
            filelist = list()
            self.findFiles(filelist, dir, extension)
            if(str(extension) == 'gz'):
                self.untargzFiles(filelist, outDIR)
            else:
                self.untarfiles(filelist, outDIR)
        else:
            self.help()
    
    def help(self):
        print 'python UnTarDIR <DIR> <EXT (.gz|.tar)> <output DIR>'
        

if __name__ == '__main__':
    obj = UnTarDIR()
    obj.run()