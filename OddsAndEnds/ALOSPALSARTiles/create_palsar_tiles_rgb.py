#!/usr/bin/env python
"""
create_palsar_tiles_rgb.py

A script to untar and create RGB colour
composite for ALOS PALSAR tiles in the same
format as those downloaded from:

http://www.eorc.jaxa.jp/ALOS/en/palsar_fnf/fnf_index.htm

Dan Clewley (daniel.clewley@gmail.com) 
06/05/2015

"""

from __future__ import print_function
import os
import sys
import subprocess
import argparse
import glob
import shutil
import tempfile
import rsgislib
from rsgislib import imagecalc
from rsgislib import imageutils
from rsgislib import imagefilter

# Set pattern to match for HH and HV files
# If not using JAXA 25 m tiles might need to adjust this
HH_FILE_PATTERN = '*_sl_HH'
HV_FILE_PATTERN = '*_sl_HV'

# Standard deviation to use when stretching image
STRETCH_STDEV = 2

def untar_file(in_tar_path, remove_tar=False):
    """
    Untars a file into a new directory
    with the same name as the tar archive.

    Can optionally remove the tar file.
    """
    # Get current directory
    start_dir = os.getcwd()

    # Split into directory and tar file name
    in_dir, in_tar = os.path.split(in_tar_path)

    # Get path for output files
    file_dir = os.path.join(in_dir, in_tar.rstrip('.tar.gz'))

    # Create directory to unzip file into
    try:
        os.makedirs(file_dir)
    except OSError:
        print('Directory alredy exists')
    
    # Move into new directory
    shutil.move(in_tar_path, file_dir)

    # Untar (need to be in directory)
    os.chdir(file_dir)
    subprocess.call(['tar','-xvf',in_tar])

    if remove_tar:
        print('Removing {}'.format(in_tar))
        os.remove(in_tar)
        
    # Change back to directory started in
    os.chdir(start_dir)

    return file_dir

def create_palsar_rgb_composite(in_tile_dir, stretchtxt, calcCoVHH, calcCoVHV):
    """
    Create scaled 8-bit RGB composite
    of HH, HV and HH/HV PALSAR data in GeoTiff format

    Stores intermediate files in temp directory and removes
    after.

    """
    try:
        in_hh_file = glob.glob(os.path.join(in_tile_dir, HH_FILE_PATTERN))[0]
        in_hv_file = glob.glob(os.path.join(in_tile_dir, HV_FILE_PATTERN))[0]
    except IndexError:
        raise Exception('Could not find data - check filenames')

    tile_basename = os.path.basename(in_tile_dir)
    out_composite = os.path.join(in_tile_dir, tile_basename + '_composite.tif')

    # Make temp directory for intermediate files
    temp_dir = tempfile.mkdtemp(prefix='palsar_stack_')
    #print("Temp DIR: " + temp_dir)

    # Create HH/HV image 
    temp_3rdBand_file = ''
    bandName = ''
    if calcCoVHH:
        temp_3rdBand_file = os.path.join(temp_dir, tile_basename + '_covhh.tif')
        imagefilter.applyCoeffOfVarFilter(in_hh_file, temp_3rdBand_file, 5, 'GTiff', rsgislib.TYPE_32FLOAT)
        bandName = 'CoVHH'
    elif calcCoVHV:
        temp_3rdBand_file = os.path.join(temp_dir, tile_basename + '_covhv.tif')
        imagefilter.applyCoeffOfVarFilter(in_hv_file, temp_3rdBand_file, 5, 'GTiff', rsgislib.TYPE_32FLOAT)
        bandName = 'CoVHV'
    else:
        temp_3rdBand_file = os.path.join(temp_dir, tile_basename + '_hhhv.tif')
        bandDefns = [imagecalc.BandDefn('hh', in_hh_file, 1),
                     imagecalc.BandDefn('hv', in_hv_file, 1)]
        imagecalc.bandMath(temp_3rdBand_file, 'hh/hv', 'GTiff', rsgislib.TYPE_32FLOAT, bandDefns) 
        bandName = 'HH/HV'

    # Create stack
    temp_stack = os.path.join(temp_dir, tile_basename + '_stack.tif')
    bands_list = [in_hh_file, in_hv_file, temp_3rdBand_file]
    band_names = ['HH','HV', bandName]
    imageutils.stackImageBands(bands_list, band_names, temp_stack, None, 0, 'GTiff', rsgislib.TYPE_32FLOAT) 

    # Apply stretch
    if stretchtxt == None:
        imageutils.stretchImage(temp_stack, out_composite, False, '', True, False, 'GTiff', 
            rsgislib.TYPE_8INT, imageutils.STRETCH_LINEARSTDDEV, STRETCH_STDEV)
    else:
        imageutils.stretchImageWithStats(temp_stack, out_composite, stretchtxt, 'GTiff', 
            rsgislib.TYPE_8INT, imageutils.STRETCH_LINEARMINMAX, 0)

    # Remove temp directory
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    script_description = '''Create 8-bit (Byte) RGB GeoTiff from ALOS
PALSAR tiles in the same format as those downloaded from:

http://www.eorc.jaxa.jp/ALOS/en/palsar_fnf/fnf_index.htm

Bands are:
    Red - HH
    Green - HV
    Blue - HV/HH
    
or

Bands are:
    Red - HH
    Green - HV
    Blue - Coefficient of variance(HH | HV)


DN scaled from 0 - 255 using a {} standard deviation stretch or via a defined text file.

Files are assumed to match the pattern:

HH - "{}"
HV - "{}"

Typical usage
--------------

Untar and create composites:

    create_palsar_tiles_rgb.py --unzip zipped_files_dir

Create composites from untarred files:

    create_palsar_tiles_rgb.py N38W120_10_MOS N39W120_10_MOS

'''.format(STRETCH_STDEV, HH_FILE_PATTERN, HV_FILE_PATTERN)

    parser = argparse.ArgumentParser(description=script_description,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('indir', nargs='+',type=str, 
                        help="Input directory of .tar.gz files or list of unzipped directories")
    parser.add_argument('--unzip',
                        action='store_true',
                        help='''Input files are in tar.gz archives, uncompress first''',
                        default=False,
                        required=False)
    parser.add_argument('--removezip',
                        action='store_true',
                        help='''Remove tar.gz archive once uncompressed
                         (only use if backed up elsewhere!)''',
                        default=False)
    
    parser.add_argument('--stretchtxt', type=str, help='''Use a text file to specify the stretch parameters''')
    parser.add_argument('--CoVHH',
                        action='store_true',
                        help='''Use coefficient of variance for the HH band''',
                        default=False)
    parser.add_argument('--CoVHV',
                        action='store_true',
                        help='''Use coefficient of variance for the HV band''',
                        default=False)
    
    args=parser.parse_args() 

    # Get list of tar.gz files (if unzipping)
    if args.unzip:
        if not os.path.isdir(args.indir[0]):
            print('ERROR: {} is not a directory'.format(args.indir[0]), file=sys.stderr)
            sys.exit(1)
        else:
            tile_list = glob.glob(os.path.join(args.indir[0],'*.tar.gz'))
            if len(tile_list) == 0:
                print('ERROR: No ".tar.gz" files found in {}'.format(args.indir[0], file=sys.stderr))
                sys.exit(1)
    # If not unzipping, assume a list of files has been passed in.
    else:
        tile_list = args.indir
    
    # Convert all paths to absolute paths (will be changing directories)
    tile_list = [os.path.abspath(tile) for tile in tile_list]

    for tile in tile_list:
        # Unzip if needed
        if args.unzip or tile.find('.tar.gz') > -1:
            tile_dir = untar_file(tile, args.removezip)
        else:
            tile_dir = tile
            if not os.path.isdir(tile_dir):
                print('{} is not a directory'.format(tile_dir), file=sys.stderr)
        # Create composite
        create_palsar_rgb_composite(tile_dir, args.stretchtxt, args.CoVHH, args.CoVHV)

            
