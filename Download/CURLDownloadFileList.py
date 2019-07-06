#!/usr/bin/env python

"""
CURLDownloadFileList.py

A script to download files from an input list using pycurl.

Author: Pete Bunting (pfb@aber.ac.uk)
Date: 20/05/2014

"""

import os
import argparse
import sys
import pycurl
import time
import random

def readFileList(fileList):
    fTxt = open(fileList, 'r')
    files = []
    for line in fTxt:
        line = line.strip()
        if (not len(line) == 0) and (not line[0] == '#'):
            files.append(line)
    return files

def downloadProgress(download_t, download_d, upload_t, upload_d):
    try:
        frac = float(download_d)/float(download_t)
    except:
        frac = 0
    sys.stdout.write("\r%s %3i%%" % ("Download:", frac*100)  )


def downloadFiles(fileListFile, failsListFile, outputPath, pauseTimeInit, fileCheck, timeOut, username=None, password=None):
    print(fileListFile)
    fileList = readFileList(fileListFile)
    #print(fileList)
    
    # Create the fails list with blank file.
    failsFile = open(failsListFile, 'w')
    failsFile.close()
    
    halfPause = int(pauseTimeInit/2)
    lowPauseTime = pauseTimeInit - halfPause
    upPauseTime = pauseTimeInit + halfPause
    
    for file in fileList:
        fileName = file.split('/')[-1]
        print(fileName)
        downloadFile = True
        if fileCheck:
            if os.path.exists(os.path.join(outputPath, fileName)):
                downloadFile = False
            else:
                downloadFile = True
        
        if downloadFile:
            fp = open(os.path.join(outputPath, fileName), "wb")
            
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, file)
            curl.setopt(pycurl.FOLLOWLOCATION, True)
            curl.setopt(pycurl.NOPROGRESS, 0)
            curl.setopt(pycurl.PROGRESSFUNCTION, downloadProgress)
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)   
            curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            curl.setopt(pycurl.MAXREDIRS, 5)
            curl.setopt(pycurl.CONNECTTIMEOUT, 50)
            curl.setopt(pycurl.TIMEOUT, timeOut)
            curl.setopt(pycurl.FTP_RESPONSE_TIMEOUT, 600)
            curl.setopt(pycurl.NOSIGNAL, 1)
            if (not username is None) and (not password is None):
                curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_ANY)
                curl.setopt(pycurl.USERPWD, username+':'+password)
            curl.setopt(pycurl.WRITEDATA, fp)
            try:
                print("Start time: " + time.strftime("%c"))
                curl.perform()
                print("\nTotal-time: " + str(curl.getinfo(curl.TOTAL_TIME)))
                print("Download speed: %.2f bytes/second" % (curl.getinfo(curl.SPEED_DOWNLOAD)))
                print("Document size: %d bytes" % (curl.getinfo(curl.SIZE_DOWNLOAD)))
            except:
                failsFile = open(failsListFile, 'a')
                failsFile.write(file + "\n")
                failsFile.close()
                import traceback
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()
            curl.close()
            fp.close()
            sys.stdout.flush()
            # Pause in loop - give the server time before another connection is made...
            pauseTime = random.randint(lowPauseTime, upPauseTime)
            print("Pausing for " + str(pauseTime) + " seconds.\n")
            time.sleep(pauseTime)

if __name__ == '__main__':
    """
    The command line user interface
    """
    parser = argparse.ArgumentParser(prog='CURLDownloadFileList.py',
                                    description='''Download a list of files using CURL.''')
    # Request the version number.
    parser.add_argument('-v', '--version', action='version', version='0.0.1 ')
    
    parser.add_argument('-i', '--filelist', type=str, required=True,
                        help='''List of files to download, one file per line with full URL.''')
                        
    parser.add_argument('-f', '--failslist', type=str, required=True,
                        help='''Output text file with the files which failed (timed out) listed one file per line with full URL.''')

    parser.add_argument('-o', '--outputpath', type=str, required=True,
                        help='''Output path to where files will be downloaded.''')
                        
    parser.add_argument('-p', '--pause', type=int, required=False, default=30,
                        help='''A pause between downloads, in seconds - attempt to avoid 
                                rejection from server when doing big downloads... Note the
                                actual pause time is randomly generated as pause time +- half 
                                pause time specified''')
                                
    parser.add_argument('-t', '--timeout', type=int, required=False, default=28800,
                        help='''The download timeout in seconds, this is the maximum amount 
                                of time it will spend on one download. Default is 28800 (8 hours)''')
  
    parser.add_argument("--nofilecheck", action='store_true', default=False, 
                        help='''Specifies that a check to see if the file being downloaded 
                                is already within the output directory is made. If the 
                                file is found it is not redownloaded.''')
                                
    parser.add_argument('--username', type=str,
                        help='''If authentication is required provide a user name.''')
    parser.add_argument('--password', type=str,
                        help='''If authentication is required provide a password.''')
    
    # Call the parser to parse the arguments.
    args = parser.parse_args()

    if not args.username is None:
        if args.password is None:
            print("Password must be provided if username is provided.")
            sys.exit()
    
    if not args.password is None:
        if args.username is None:
            print("Username must be provided if password is provided.")
            sys.exit()

    downloadFiles(args.filelist, args.failslist, args.outputpath, args.pause, (not args.nofilecheck), args.timeout, args.username, args.password)


