 #! /usr/bin/env python

#######################################
# A python script to download a list of 
# file via curl...
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 29/11/2008
# Version: 1.0
# Version: 1.1
#######################################

import os.path
import sys, re

class CurlDownload (object):    
    
    def parseTextFile(self, inputTextFile, filenames):
        for eachLine in inputTextFile:
            filenames.append(re.sub('\n','',os.path.basename(eachLine)))
            
    def downloadFiles(self, filenames, outputDIR, curlCommand):
        command = ''
        fulloutputpath = ''
        for i in range(len(filenames)):
            fulloutputpath = os.path.join(outputDIR, filenames[i])
            if os.path.exists(fulloutputpath):
                print('Already downloaded ' + filenames[i])
            else:
                command = curl + filenames[i] + ' > ' + fulloutputpath
                #print command
                os.system(command)
            
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 3:
            inputTextFilePath = sys.argv[1]
            outputDIR = sys.argv[2]
            curlCommand = sys.argv[3]
            if os.path.exists(inputTextFilePath):
                urls = list()
                filenames = list();
                try:
                    inputTextFile = open(inputTextFilePath, 'r')
                    self.parseTextFile(inputTextFile, filenames)
                    inputTextFile.close()
                except IOError as e:
                    print('\nCould not open file:\n', e)
                    return
                
                if os.path.exists(outputDIR):
                    self.downloadFiles(filenames, outputDIR, curlCommand)
                else:
                    print(outputDIR, ' does not exist')
                    return
                
            else:
                print('File \'' + inputTextFilePath + '\' does not exist.')
        else:
            self.help()
    
    def help(self):
        print('''
Usage:
 python downloadPALSAR.py infilelist.txt outDIR curlCommand
e.g.,
 python downloadPALSAR.py /data/filelist.txt /data/Downloads "curl -u USER:PASS ftp.myftpserver.com/pathtofiles"
''')
    
if __name__ == '__main__':
    obj = CurlDownload()
    obj.run()
