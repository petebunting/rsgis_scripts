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

class TarTest (object):
    
    def run(self):
        tar = tarfile.open("/Users/pete/Temp/test_tar/test_tar.tar.gz")
        for tarinfo in tar:
            print tarinfo.name, "is", tarinfo.size, "bytes in size and is",
            if tarinfo.isreg():
                print "a regular file."
            elif tarinfo.isdir():
                print "a directory."
            else:
                print "something else."
        tar.close()
    
    def help(self):
        print 'python TarTest <tar file>'
        

if __name__ == '__main__':
    obj = TarTest()
    obj.run()