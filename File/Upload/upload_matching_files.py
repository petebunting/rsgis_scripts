#!/usr/bin/env python

"""
upload_matching_files.py

Recursivly search for files, given in a text file and upload to FTP server.

Dan Clewley - 11/04/2015

"""
from __future__ import print_function 
import subprocess
import argparse
import sys
import os

# Fill in details of FTP Server here
FTP_ADDRESS = ''
FTP_USER = ''
FTP_PASSWORD = ''

def get_matching_file_paths(in_filelist, search_dir):
    """
    Recursivly searches a directory to find
    files matching those in a text file

    Returns a list of files with paths
    """
    
    match_list = []
    with open(in_filelist,'rU') as f:
        check_file_list = f.read().split('\n')

    # Get absolute path 
    search_dir = os.path.abspath(search_dir)

    # Walk through directory
    for dir_name, sub_dir_name, file_list in os.walk(search_dir):
        for file_name in file_list:
            match_files = [check_file for check_file in check_file_list if check_file.strip() == file_name]
            if len(match_files) > 0:
                match_list.append(os.path.join(dir_name, file_name))

    return match_list

def upload_files(file_list, target_dir, upload=True):
    """
    Upload files in 'file_list' to FTP server

    Removes files from list on sucessful upload
    """
    for filenum,file_path in enumerate(file_list):
        print('Uploading {}/{}'.format(filenum+1, len(file_list)))
        curl_command = ['curl',
                        '--user', '{}:{}'.format(FTP_USER,FTP_PASSWORD),
                        '-T',file_path,
                        'ftp://{}/{}/'.format(FTP_ADDRESS,target_dir)]
        if upload:
            curl_out = subprocess.call(curl_command)
            if curl_out == 0:
                file_list.remove(file_path)
        else:
            print(' '.join(curl_command))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find and upload files')
    parser.add_argument('-i', '--filelist',
                        help ='List of files (new file on each line)',
                        required=True)
    parser.add_argument('-d', '--dir',
                        help ='Directory to search for files',
                        required=True)
    parser.add_argument('-t', '--targetdir',
                        help ='Target directory to upload files to',
                        required=False,
                        default='')
    parser.add_argument('--print',
                        help ='Print cURL command only (do not upload)',
                        action='store_true',
                        default=False)
    args=parser.parse_args()
    
    file_list = get_matching_file_paths(args.filelist, args.dir)

    upload_files(file_list, args.targetdir, upload=(not args.print))

    if len(file_list) > 0:
        print('The following files were found but not uploaded:',file=sys.stderr)
        print('\n'.join(file_list),file=sys.stderr)
 

