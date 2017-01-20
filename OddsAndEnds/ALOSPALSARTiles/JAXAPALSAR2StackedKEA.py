#! /usr/bin/env python

import os
import os.path
import argparse
import glob
import shutil
import subprocess

import rsgislib
from rsgislib import imagefilter
from rsgislib import imagecalc
from rsgislib import imageutils
from rsgislib import rastergis

HH_P1_FILE_PATTERN = '*_sl_HH'
HV_P1_FILE_PATTERN = '*_sl_HV'

HH_P2_FILE_PATTERN = '*_sl_HH_F02DAR'
HV_P2_FILE_PATTERN = '*_sl_HV_F02DAR'

HH_P2_FP_FILE_PATTERN = '*_sl_HH_FP6QAR'
HV_P2_FP_FILE_PATTERN = '*_sl_HV_FP6QAR'

MASK_FILE_PATTERN = '*_mask'
DATE_FILE_PATTERN = '*_date'
LINCI_FILE_PATTERN = '*_linci'

def processSingleFile(inputFile, outputDIR, tmpath, calcExtraBands, palsar2=False):
    inputFile = os.path.abspath(inputFile)
    outputDIR = os.path.abspath(outputDIR)
    tmpath = os.path.abspath(tmpath)
    print("Processing: " + inputFile)
    baseName = os.path.basename(inputFile).split(".")[0]
    print("\t" + baseName)
    rsgisUtils = rsgislib.RSGISPyUtils()
    uidStr = "_"+rsgisUtils.uidGenerator()
    createdTmp = False
    if not os.path.exists(tmpath):
        os.makedirs(tmpath)
        createdTmp = True
    
    extract2DIR = os.path.join(tmpath, baseName+uidStr)
    if not os.path.exists(extract2DIR):
        os.makedirs(extract2DIR)
    os.chdir(extract2DIR)
    
    cmd = 'tar -xzf ' + inputFile
    print(cmd)
    subprocess.call(cmd, shell=True)
    
    try:
        if palsar2:
            hhFiles = glob.glob(os.path.join(extract2DIR, HH_P2_FILE_PATTERN))
            hvFiles = glob.glob(os.path.join(extract2DIR, HV_P2_FILE_PATTERN))
            
            if len(hhFiles) == 0:
                hhFiles = glob.glob(os.path.join(extract2DIR, HH_P2_FP_FILE_PATTERN))
            if len(hvFiles) == 0:
                hvFiles = glob.glob(os.path.join(extract2DIR, HV_P2_FP_FILE_PATTERN))
            
            in_hh_file = hhFiles[0]
            in_hv_file = hvFiles[0]
        else:
            in_hh_file = glob.glob(os.path.join(extract2DIR, HH_P1_FILE_PATTERN))[0]
            in_hv_file = glob.glob(os.path.join(extract2DIR, HV_P1_FILE_PATTERN))[0]
    except IndexError:
        raise Exception('Could not find data - check filenames')
    
    bands_list = [in_hh_file, in_hv_file]
    band_names = ['HH','HV']
    
    # Create extra image bands
    for calcBand in calcExtraBands:    
        if calcBand == 'COVARHH':
            extraBandFile = os.path.join(extract2DIR, baseName + '_covhh.kea')
            imagefilter.applyCoeffOfVarFilter(in_hh_file, extraBandFile, 5, 'KEA', rsgislib.TYPE_32FLOAT)
            bandName = 'CoVHH'
            bands_list.append(extraBandFile)
            band_names.append(bandName)
        if calcBand == 'COVARHV':
            extraBandFile = os.path.join(extract2DIR, baseName + '_covhv.kea')
            imagefilter.applyCoeffOfVarFilter(in_hv_file, extraBandFile, 5, 'KEA', rsgislib.TYPE_32FLOAT)
            bandName = 'CoVHV'
            bands_list.append(extraBandFile)
            band_names.append(bandName)
        if calcBand == 'HHHV':
            extraBandFile = os.path.join(extract2DIR, baseName + '_hhhv.kea')
            bandDefns = [imagecalc.BandDefn('hh', in_hh_file, 1),
                         imagecalc.BandDefn('hv', in_hv_file, 1)]
            imagecalc.bandMath(extraBandFile, 'hv==0?0:hh/hv', 'KEA', rsgislib.TYPE_32FLOAT, bandDefns) 
            bandName = 'HH/HV'
            bands_list.append(extraBandFile)
            band_names.append(bandName)
    
    # Create stack
    stackFile = os.path.join(outputDIR, baseName + '_stack.kea')
    imageutils.stackImageBands(bands_list, band_names, stackFile, None, 0, 'KEA', rsgislib.TYPE_32FLOAT) 
    imageutils.popImageStats(stackFile, usenodataval=True, nodataval=0, calcpyramids=True)
    
    try:
        in_mask_file = glob.glob(os.path.join(extract2DIR, MASK_FILE_PATTERN))[0]
        out_mask_file = os.path.join(outputDIR, baseName + '_mask.kea')
        cmd = 'gdal_translate -of KEA ' + in_mask_file + ' ' + out_mask_file
        subprocess.call(cmd, shell=True)
        rastergis.populateStats(out_mask_file, True, True)
    except IndexError:
        print("WARNING: Could not find the mask file... Ignoring.")
    
    try:
        in_date_file = glob.glob(os.path.join(extract2DIR, DATE_FILE_PATTERN))[0]
        out_date_file = os.path.join(outputDIR, baseName + '_date.kea')
        cmd = 'gdal_translate -of KEA ' + in_date_file + ' ' + out_date_file
        subprocess.call(cmd, shell=True)
        rastergis.populateStats(out_date_file, True, True)
    except IndexError:
        print("WARNING: Could not find the date file... Ignoring.")
        
    try:
        in_linci_file = glob.glob(os.path.join(extract2DIR, LINCI_FILE_PATTERN))[0]
        out_linci_file = os.path.join(outputDIR, baseName + '_linci.kea')
        cmd = 'gdal_translate -of KEA ' + in_linci_file + ' ' + out_linci_file
        subprocess.call(cmd, shell=True)
        rastergis.populateStats(out_linci_file, True, True)
    except IndexError:
        print("WARNING: Could not find the linci file... Ignoring.")
    
    shutil.rmtree(extract2DIR)
    if createdTmp:
        shutil.rmtree(tmpath)
    
def findProcessInDIR(inputDIR, outputDIR, tmpath, calcExtraBand, palsar2=False):
    inputDIR = os.path.abspath(inputDIR)
    outputDIR = os.path.abspath(outputDIR)
    tmpath = os.path.abspath(tmpath)
    createdTmp = False
    if not os.path.exists(tmpath):
        os.makedirs(tmpath)
        createdTmp = True
        
    inFileList = glob.glob(os.path.join(inputDIR, "*.tar.gz"))
    for file in inFileList:
        processSingleFile(file, outputDIR, tmpath, calcExtraBand, palsar2)
    
    if createdTmp:
        shutil.rmtree(tmpath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, type=str, help="Input directory or file containing tar.gz file(s)")
    parser.add_argument("-o", "--output", required=True, type=str, help="Output directory for KEA files")
    parser.add_argument("-t", "--tmpath", required=True, type=str, help="Tempory path which will be generated and removed during processing.")
    parser.add_argument("-c", "--calcband", choices=['HHHV', 'COVARHH', 'COVARHV'], nargs='+', required=True, help='''Specify extra band to be calculated to make a composite.''')
    parser.add_argument("-p", "--palsar2", action="store_true", default=False, help="Specify that a PALSAR2 scene is being processed.")
                        
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        print("Input is a directory")
        findProcessInDIR(args.input, args.output, args.tmpath, args.calcband, args.palsar2)
    else:
        print("Input is a single file")
        processSingleFile(args.input, args.output, args.tmpath, args.calcband, args.palsar2)


