#! /usr/bin/env python

"""
add_gmw_palsar_header.py

Adds ENVI header file to Global Mangrove Watch
format PALSAR FBD files.

Dan Clewley
"""
from __future__ import print_function
import os
import sys
import re
import glob
import argparse

def create_envi_headers(inFileDIR):
    """
    Create ENVI header
    for all files
    """

    # Change to input directory
    os.chdir(inFileDIR)

    try:
        inHHFile = glob.glob('*HH')[0]
        inHVFile = glob.glob('*HV')[0]
        inDateFile = glob.glob('*_date')[0]
        inIncFile = glob.glob('*_linci')[0]
        inMaskFile = glob.glob('*_mask')[0]
        inHeaderFile = glob.glob('KC*.hdr')[0]
    except IndexError:
        print('Not all expected files were found in input directory')
        print('Found:')
        all_files = os.listdir(inFileDIR)
        print('\n'.join(all_files))
        raise

    inHHHeaderFile = inHHFile + '.hdr'
    inHVHeaderFile = inHVFile + '.hdr'
    inDateHeaderFile = inDateFile + '.hdr'
    inIncHeaderFile = inIncFile + '.hdr'
    inMaskHeaderFile = inMaskFile + '.hdr'

    inHeader = open(inHeaderFile, 'r')
    inHHHeader = open(inHHHeaderFile, 'w')
    inHVHeader = open(inHVHeaderFile, 'w')
    inDateHeader = open(inDateHeaderFile,'w')
    inIncHeader = open(inIncHeaderFile,'w')
    inMaskHeader = open(inMaskHeaderFile,'w')
    
    inULong = ''
    inULat = ''
    
    i = 1
    for line in inHeader:
        if i == 13:
            inULat = line.strip()
        elif i == 14:
            inULon = line.strip()
        i+=1

    inULat = str(int(inULat) * 3600)
    inULon = str(int(inULon) * 3600)
    
    headerText = '''ENVI
description = {{
 {} }}
samples = 4500
lines   = 4500
bands   = 1
header offset = 0
file type = ENVI Standard
data type = 12
interleave = bsq
sensor type = Unknown
byte order = 0
map info = {{ Geographic Lat/Lon, 1.0000, 1.0000, {}, {}, 8.0000000000e-01, 8.0000000000e-01, WGS-84, units=Seconds }}
wavelength units = Unknown
'''.format(inHeaderFile, inULon, inULat)

    headerTextByte = '''ENVI
description = {{
 {} }}
samples = 4500
lines   = 4500
bands   = 1
header offset = 0
file type = ENVI Standard
data type = 1
interleave = bsq
sensor type = Unknown
byte order = 0
map info = {{ Geographic Lat/Lon, 1.0000, 1.0000, {}, {}, 8.0000000000e-01, 8.0000000000e-01, WGS-84, units=Seconds}}
wavelength units = Unknown
''' .format(inHeaderFile, inULon, inULat)

    inHHHeader.write(headerText)
    inHVHeader.write(headerText)
    inDateHeader.write(headerText)
    inIncHeader.write(headerTextByte)
    inMaskHeader.write(headerTextByte)
    
    inHeader.close()
    inHHHeader.close()
    inHVHeader.close()
    inDateHeader.close()
    inIncHeader.close()
    inMaskHeader.close()
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create ENVI header files for GMW PALSAR Tiles')
    parser.add_argument("tiledirs", nargs='+',type=str, help="Input directory(s)")
    args=parser.parse_args() 

    # Get absolute path
    tile_dir_paths = [os.path.abspath(tile) for tile in args.tiledirs]

    for tile_dir in tile_dir_paths:
        if os.path.isdir(tile_dir):
            try:
                create_envi_headers(tile_dir)
                print('Added headers for {}'.format(os.path.split(tile_dir)[-1]))
            except Exception:
                print('ERROR: No headers created for {}'.format(tile_dir), file=sys.stderr)
