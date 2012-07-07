#! /usr/bin/env python

#######################################
# A script to remove SVN files (.svn)
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 06/03/2008
# Version: 1.0
#######################################

import os.path
import sys

class RMSVN (object):
    
    def findFiles(self, filelist, directory):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                fileList = os.listdir(directory)
                for filename in fileList:
                    #print filename
                    if(os.path.isdir(os.path.join(directory,filename))):
                        #print filename + ' is a directory.'
                        self.findFiles(filelist, os.path.join(directory,filename))
                        if filename == '.svn':
                            filelist.append(os.path.join(directory,filename))
            else:
                print directory + ' is not a directory!'
        else:
            print directory + ' does not exist!'
     
    def rmSVN(self, filelist):
        rmcommand = 'rm -Rf '
        command = ''
        try:
            for filename in filelist:
                command = rmcommand + ' ' + filename
                print command
                os.system(command)
        except IOError, e:
            print 'IOError Occurred: ' + str(e)
            
    
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 2:
            dir = sys.argv[1].strip()
            filelist = list()
            self.findFiles(filelist, dir)
            self.rmSVN(filelist)
           
        else:
            self.help()
    
    def help(self):
        print 'python RMSVN <DIR>'
        

if __name__ == '__main__':
    obj = RMSVN()
    obj.run()