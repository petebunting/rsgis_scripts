 #! /usr/bin/env python

#######################################
# A python script to download a list of 
# file via curl...
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 29/11/2008
# Version: 1.0
#######################################

import os.path
import sys

class CurlDownload (object):    
    
    def parseTextFile(self, inputTextFile, urls, filenames):
        for eachLine in inputTextFile:
            print eachLine
            urls.append(eachLine.strip())
            filenames.append(os.path.basename(eachLine))
            
    def downloadFiles(self, urls, filenames, outputDIR, usrpass):
        curl = 'curl -x wwwcache.aber.ac.uk:8080 -u ' + usrpass + ' -# '
        command = ''
        fulloutputpath = ''
        for i in range(len(urls)):
            fulloutputpath = os.path.join(outputDIR, filenames[i])
            command = curl + urls[i] + ' > ' + fulloutputpath
            print command
            os.system(command)
            
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 4:
            inputTextFilePath = sys.argv[1]
            outputDIR = sys.argv[2]
            usrpass = sys.argv[3]
            if os.path.exists(inputTextFilePath):
                urls = list()
                filenames = list();
                try:
                    inputTextFile = open(inputTextFilePath, 'r')
                    self.parseTextFile(inputTextFile, urls, filenames)
                    inputTextFile.close()
                except IOError, e:
                    print '\nCould not open file:\n', e
                    return
                
                if os.path.exists(outputDIR):
                    self.downloadFiles(urls, filenames, outputDIR, usrpass)
                else:
                    print outputDIR, ' does not exist'
                    return
                
            else:
                print 'File \'' + inputTextFilePath + '\' does not exist.'
        else:
            self.help()
    
    def help(self):
        print 'python CurlDownload <inputFile> <outputDIR> <user:pass>'
    
    
        
    
if __name__ == '__main__':
    obj = CurlDownload()
    obj.run()