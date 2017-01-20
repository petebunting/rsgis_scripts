#! /usr/bin/env python

import argparse
import glob
import os.path
import rsgislib
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=False, type=str, help="Input directory containing tar.gz file(s)")
parser.add_argument("-l", "--filelist", required=False, type=str, help="Input file containing a list of input files (used in place of -i).")
parser.add_argument("-o", "--output", required=True, type=str, help="Output file")
parser.add_argument("-d", "--outdir", required=True, type=str, help="Output directory for KEA files")
parser.add_argument("-t", "--tmpath", required=True, type=str, help="Tempory path which will be generated and removed during processing.")
parser.add_argument("-c", "--calcbands", choices=['HHHV', 'COVARHH', 'COVARHV'], nargs='+', required=True, help='''Specify extra band to be calculated to make a composite.''')
parser.add_argument("-p", "--palsar2", action="store_true", default=False, help="Specify that a PALSAR2 scene is being processed.")

args = parser.parse_args()

inDIRPath = args.input
fileListPath = args.filelist
outDIRPath = os.path.abspath(args.outdir)
tmpDIRPath = os.path.abspath(args.tmpath)

calcBands = ""
for calc in args.calcbands:
    calcBands = calcBands + calc + " "

fileList = []

if not inDIRPath is None:
    fileList = glob.glob(os.path.join(inDIRPath, '*.tar.gz'))
elif not fileListPath is None:
    rsgisUtils = rsgislib.RSGISPyUtils()
    fileList = rsgisUtils.readTextFile2List(fileListPath)
else:
    print("You must specify either the -i or -l option.")
    sys.exit()

outFile = open(args.output, 'w')
for file in fileList:
    cmd = "python /scratch/pete.bunting/GlobalMangroveWatch/Scripts/JAXAPALSAR2StackedKEA.py -i " + file + " -o " + outDIRPath + " -t " + tmpDIRPath + " -c " + calcBands
    if args.palsar2:
        cmd = cmd + " --palsar2"
    outFile.write(cmd + '\n')

outFile.flush()
outFile.close()

