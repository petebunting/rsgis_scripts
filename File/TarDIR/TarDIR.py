#! /usr/bin/env python

#######################################
# A Pyhton scroipt to tar / tar.gz
# all files in a directory
# Modified from UnTarDIR.py
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 06/03/2008
# Version: 1.0
#######################################

import os.path
import sys

class TarDIR (object):
    
    def targzFiles(self, filelist, inDIR):
        os.chdir(inDIR)
    	tarcommand = 'tar -czf '
    	command = ''
        try:
            for filename in filelist:
                print filename
                command = tarcommand + filename + '.tar.gz  ' + filename + '/'
                os.system(command)
        except IOError, e:
            print 'IOError Occurred: ' + str(e)
            
            
    def tarfiles(self, filelist, inDIR):
        os.chdir(inDIR)
    	tarcommand = 'tar -cf '
    	command = ''
        try:
            for filename in filelist:
                print filename
                command = tarcommand + filename + '.tar.gz  ' + filename + '/'
                os.system(command)
        except IOError, e:
            print 'IOError Occurred: ' + str(e)
            
    
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 3:
            inDIR = sys.argv[1].strip()
            extension = sys.argv[2].strip()
            filelist = list()
            filelist = os.listdir(inDIR)
            if(str(extension) == 'gz'):
                self.targzFiles(filelist, inDIR)
            else:
                self.tarfiles(filelist, inDIR)
        else:
            self.help()
    
    def help(self):
        print 'python TarDIR <InDIR> <EXT (.gz|.tar)>'
        

if __name__ == '__main__':
    obj = TarDIR()
    obj.run()