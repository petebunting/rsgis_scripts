#! /usr/bin/env python

import os
import sys

class fileNameUtils (object):

    def fileReplacePartOfName(self, fileList, filePath, replaceStr, withStr):
        replaceStr = replaceStr.strip()
        withStr = withStr.strip()
        os.chdir(filePath)
        cwd = os.getcwd()
        print 'Working directory: ', cwd
        for i in range(len(fileList)):
            filename =  str(fileList[i])
            findOut = 1
            newFilename = filename.replace(replaceStr, withStr, filename.count(replaceStr))
            os.rename(filename, newFilename)
            print filename, 'has been replaced by ', newFilename

    def fileReplacePartOfNamePattern(self, fileList, filePath, pattern, replaceStr, withStr):
        pattern = pattern.strip()
        replaceStr = replaceStr.strip()
        withStr = withStr.strip()
        os.chdir(filePath)
        cwd = os.getcwd()
        print 'Working directory: ', cwd
        for i in range(len(fileList)):
            filename =  str(fileList[i])
            findOut = filename.find(pattern, 0, len(filename))
            if not findOut == -1:
                newFilename = filename.replace(replaceStr, withStr, filename.count(replaceStr))
                os.rename(filename, newFilename)
                print filename, 'has been replaced by ', newFilename
            else:
                print filename, ' does not require renaming.'

    def fileFirstLetterLowerPattern(self, fileList, filePath, pattern):
        pattern = pattern.strip()
        os.chdir(filePath)
        cwd = os.getcwd()
        print 'Working directory: ', cwd
        for i in range(len(fileList)):
            filename =  str(fileList[i])
            findOut = filename.find(pattern, 0, len(filename))
            if (not filename[0].islower()) and filename[0].isalpha() and (not findOut == -1):
                output  = filename.replace(filename[0], filename[0].lower(), 1)
                os.rename(filename, output)
                print filename, 'has been replaced by ', output
            else:
                print filename, ' does not require renaming.'

    def fileFirstLetterUpperPattern(self, fileList, filePath, pattern):
        pattern = pattern.strip()
        os.chdir(filePath)
        cwd = os.getcwd()
        print 'Working directory: ', cwd
        for i in range(len(fileList)):
            filename =  str(fileList[i])
            findOut = filename.find(pattern, 0, len(filename))
            if (filename[0].islower()) and filename[0].isalpha() and (not findOut == -1):
                output  = filename.replace(filename[0], filename[0].upper(), 1)
                os.rename(filename, output)
                print filename, 'has been replaced by ', output
            else:
                print filename, ' does not require renaming.'

    def fileFirstLetterLower(self, fileList, filePath):
        os.chdir(filePath)
        cwd = os.getcwd()
        print 'Working directory: ', cwd
        for i in range(len(fileList)):
            filename =  str(fileList[i])
            if (not filename[0].islower()) and filename[0].isalpha():
                output  = filename.replace(filename[0], filename[0].lower(), 1)
                os.rename(filename, output)
                print filename, 'has been replaced by ', output
            else:
                print filename, ' does not require renaming.'
                
    def fileFirstLetterUpper(self, fileList, filePath):
        os.chdir(filePath)
        cwd = os.getcwd()
        print 'Working directory: ', cwd
        for i in range(len(fileList)):
            filename =  str(fileList[i])
            if (filename[0].islower()) and filename[0].isalpha():
                output  = filename.replace(filename[0], filename[0].upper(), 1)
                os.rename(filename, output)
                print filename, 'has been replaced by ', output
            else:
                print filename, ' does not require renaming.'
    
    def run(self):
        
        numArgs = len(sys.argv)
        
        filePath = ''
        function = -1
        
        if numArgs >= 3:
            filePath = sys.argv[1]
            function = int(sys.argv[2])
            
            if not os.path.exists(filePath):
                print 'Filepath does not exist'
                self.help()
            else:
                print filePath, ' is OK.'        
                if not os.path.isdir(filePath):
                    print 'Filepath is not a directory!'
                    self.help()
                else:
                    print filePath, ' is a directory.'        
                    fileList = os.listdir(filePath)
                    if function == 0:
                        self.fileFirstLetterLower(fileList, filePath)
                    elif function == 1:
                        self.fileFirstLetterUpper(fileList, filePath)
                    elif function == 2:
                        if numArgs == 4:
                            pattern = sys.argv[3]
                            self.fileFirstLetterLowerPattern(fileList, filePath, pattern)
                        else:
                            self.help()
                    elif function == 3:
                        if numArgs == 4:
                            pattern = sys.argv[3]
                            self.fileFirstLetterUpperPattern(fileList, filePath, pattern)
                        else:
                            self.help()
                    elif function == 4:
                        if numArgs == 5:
                            replaceStr = sys.argv[3]
                            withStr = sys.argv[4]
                            self.fileReplacePartOfName(fileList, filePath, replaceStr, withStr)
                        else:
                            self.help()
                    elif function == 5:
                        if numArgs == 6:
                            pattern = sys.argv[3]
                            replaceStr = sys.argv[4]
                            withStr = sys.argv[5]
                            self.fileReplacePartOfNamePattern(fileList, filePath, pattern, replaceStr, withStr)
                        else:
                            self.help()
                    else:
                        self.help()
        else:
            self.help()            
    
    def help(self):
        print 'fileNameUtils HELP!! ;)'
        print 'python fileNameUtils <String dirPATH> <int function>'
        print 'Functions avaliable: '
        print '\t0 - Make first Letter of filename lowercase'
        print '\t1 - Make first Letter of filename uppercase'
        print '\t2 - Make first Letter of filename lowercase with pattern'
        print '\t3 - Make first Letter of filename uppercase with pattern'
        print '\t4 - Replace string with new string within filename'
        print '\t5 - Replace string with new string within filename with pattern'
    
if __name__ == '__main__':
    
    obj = fileNameUtils()
    obj.run()
    
