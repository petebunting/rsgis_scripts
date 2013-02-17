#! /usr/bin/env python

#######################################
# A script to find and replace strings
# within all text files in a directory
#
# Author: Dan Clewley
# Email: daniel.clewley@googlemail.com
# Date: 03/07/2012
# Version: 1.0
#######################################

import os.path, sys, re

# Add extension of files to search for
extListString = 'cpp,h,r,py,txt,sh,html,php,xml,f,tex' 

class findReplaceObj(object):
    ''' Object to find and replace strings within
input string'''
    def __init__(self, findString, replaceString):
        self.findString = findString
        self.replaceString = replaceString
    
    def frReplace(self, inString):
        #outString = re.sub(self.findString, self.replaceString, inString)
        outString = inString.replace(self.findString, self.replaceString)
        return outString
        
class extFind(object):
    ''' Check for extension of file against a list of extensions'''
    def __init__(self, extListString):
        self.fileExtList = []
        count = extListString.count(',')
        elements = extListString.split(',',count)
        for element in elements:
            if element != '':
                self.fileExtList.append(element.strip())
        
    def findExt(self, fileName):
        count = fileName.count('.')
        elements = fileName.split('.',count)
        for fileExt in self.fileExtList:
            if elements[count] == fileExt:
                return True
        return False    
    
class FindReplaceTextDIR (object):
    
    def findFiles(self, filelist, directory, inExt):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                fileList = os.listdir(directory)
                for filename in fileList:
                    if(os.path.isdir(os.path.join(directory,filename))):
                        self.findFiles(filelist, os.path.join(directory,filename), inExt)
                    else:
                        if inExt.findExt(filename):
                            filelist.append(os.path.join(directory,filename))
            else:
                print directory + ' is not a directory!'
        else:
            print directory + ' does not exist!'
    
    def readFindReplaceText(self, findReplaceList, inFRTextFile):
        inFile = open(inFRTextFile, 'rU')
        for line in inFile:
            count = line.count('#')
            if count == 1:
                elements = line.split('#', count)
                findReplaceList.append(findReplaceObj(elements[0], re.sub('\n','',elements[1])))
        inFile.close()
    
    def findReplaceTextFile(self, inFileName, findReplaceList):
        # Read file to memory
        inFile = open(inFileName, 'rU')
        inFileString = ''
        for line in inFile:
            inFileString = inFileString + line
        inFile.close()
        
        outFileString = inFileString
        
        # Run find and replace
        for fritem in findReplaceList:
            outFileString = fritem.frReplace(outFileString)
        
        if outFileString != inFileString:
            print "Replacing text in: ", inFileName        
            # Write out file (if something has changed)
            outFile = open(inFileName, 'w')
            outFile.write(outFileString)
            outFile.close()
    
    def run(self):
        numArgs = len(sys.argv)
        if numArgs == 3:
            inDIR = sys.argv[1].strip()
            inFRTextFile = sys.argv[2].strip()
            findReplaceList = []
            filelist = []
            # Read in text file extensions
            inExt = extFind(extListString)
            
            # Read in find / replace strings
            self.readFindReplaceText(findReplaceList, inFRTextFile)
            # Find files
            self.findFiles(filelist, inDIR, inExt)
            for inFile in filelist:
                self.findReplaceTextFile(inFile, findReplaceList)
                       
        else:
            self.help()
    
    def help(self):
        print '''Find and replace strings within all text files with the extensions:'''
        print ' ' + extListString
        print '''in input directory.
Usage:
 python FindReplaceTextDIR <inDIR> <inFindReplaceList>
Strings to find and replace provided as text file (inFindReplaceList) in the
format:
findString#replaceString
'''

if __name__ == '__main__':
    obj = FindReplaceTextDIR()
    obj.run()
