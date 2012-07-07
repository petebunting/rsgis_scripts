#! /usr/bin/env python

############################################################################
# Copyright (c) 2012 Dr. Peter Bunting, Aberystwyth University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# Purpose:  A script for find files and uploading to server.
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 20/04/2012
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
#############################################################################

import os.path
import sys
import optparse

class UploadFiles (object):

    def checkFileExtension(self, filename, extension):
        foundExtension = False;
        filenamesplit = os.path.splitext(filename)
        fileExtension = filenamesplit[1].strip()
        if(fileExtension == extension):
            foundExtension = True
        return foundExtension

    def findFilesIterative(self, filelist, directory, extension):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                dirFileList = os.listdir(directory)
                for filename in dirFileList:
                    if(os.path.isdir(os.path.join(directory,filename))):
                        self.findFilesIterative(filelist, os.path.join(directory,filename), extension)
                    elif(os.path.isfile(os.path.join(directory,filename))):
                        if(self.checkFileExtension(filename, extension)):
                            filelist.append(os.path.join(directory,filename))
                    else:
                        print filename + ' is NOT a file or directory!'
            else:
                print directory + ' is not a directory!'
        else:
            print directory + ' does not exist!'

    def findFilesIterativeInDir(self, filelist, directory, extension, withinDir):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                dirFileList = os.listdir(directory)
                for filename in dirFileList:
                    if(os.path.isdir(os.path.join(directory,filename))):
                        self.findFilesIterativeInDir(filelist, os.path.join(directory,filename), extension, withinDir)
                    elif(os.path.isfile(os.path.join(directory,filename))):
                        if(os.path.basename(directory) == withinDir and self.checkFileExtension(filename, extension)):
                            filelist.append(os.path.join(directory,filename))
                    else:
                        print filename + ' is NOT a file or directory!'
            else:
                print directory + ' is not a directory!'
        else:
            print directory + ' does not exist!'

    def uploadFiles(self, fileList, serverUrl):
        command = str("scp ")
        for file in fileList:
             command += str("\"") + file + str("\" ")
        command += serverUrl
        print command
        print "There are ", len(fileList), " files to upload."
        os.system(command)


    def run(self, cmdargs):
        fileList = list()
        if cmdargs.directory is None:
            self.findFilesIterative(fileList, cmdargs.inputPath, cmdargs.extension)
        else:
            self.findFilesIterativeInDir(fileList, cmdargs.inputPath, cmdargs.extension, cmdargs.directory)

        self.uploadFiles(fileList, cmdargs.desturl)

# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputPath", default=None, help="Input file path")
    p.add_option("-u","--url", dest="desturl", default=None, help="URL to upload files.")
    p.add_option("-e","--ext", dest="extension", default=None, help="File extension to upload")
    p.add_option("-d","--directory", dest="directory", default=None, help="Directory within which files should be sort.")

    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputPath is None:
        p.print_help()
        print "Input file path must be set."
        sys.exit()

    if self.desturl is None:
        p.print_help()
        print "Output URL must be set."
        sys.exit()

if __name__ == '__main__':
    cmdargs = CmdArgs()
    obj = UploadFiles()
    obj.run(cmdargs)
