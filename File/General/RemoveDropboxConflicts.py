#! /usr/bin/env python

#######################################
# A script to remove Dropbox 'conflicted copy' files
#
# Adapted from script to remove SVN files
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 06/03/2008
# Version: 1.0
#######################################

import os.path
import sys

class RemoveSwap (object):
    
    ''' Find and remove files ending with ~'''
    
    def findFiles(self, filelist, directory):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                fileList = os.listdir(directory)
                for filename in fileList:
                    if(os.path.isdir(os.path.join(directory,filename))):
                        self.findFiles(filelist, os.path.join(directory,filename))
                    else:
                        if filename.find('conflicted copy') > 0:
                            filelist.append(os.path.join(directory,filename))
            else:
                print directory + ' is not a directory!'
        else:
            print directory + ' does not exist!'
     
    def rmSwap(self, filelist):
        rmcommand = 'rm '
        command = ''
        try:
            for filename in filelist:
                print 'deleting ' + filename
                os.remove(filename)
        except IOError, e:
            print 'IOError Occurred: ' + str(e)
            
    
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 2:
            dir = sys.argv[1].strip()
            filelist = list()
            self.findFiles(filelist, dir)
            self.rmSwap(filelist)
           
        else:
            self.help()
    
    def help(self):
        print '''
A script to remove files with 'conflicted copy' in the name (created by dropbox).
Usage:
    python RemoveDropboxConflicts <DIR>'''
        

if __name__ == '__main__':
    obj = RemoveSwap()
    obj.run()