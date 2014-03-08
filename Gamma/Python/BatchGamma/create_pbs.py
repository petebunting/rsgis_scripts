#! /usr/bin/env python
# create_pbs.py
# Utility script to create PBS scripts to run
# BatchGamma.py on HPC
#
# Dan Clewley (daniel.clewley@gmail.com)
#

import argparse, os, subprocess, re

def stripExtension(inFileName):
    outName = re.sub('\.tar\.gz','',inFileName)
    outName = re.sub('\.zip','',outName)
    
    return outName

# Read in parameters
parser = argparse.ArgumentParser(prog='pbs_batch_gamma.py', usage='''Utility script to create and submit PBS scripts for running BatchGamma on a HPC.
Searches input directory or takes a list of scenes and submits each scene as a seperate job. 

Contents of parameter file are as follows:

LCTemplate:FBD_JAXA_1_1_to_SLC_template.csh
slcGeoTemplate:FBD_SLC_to_GEO_template.csh
outProj:Projection.wkt
targetRes:30
thetaref:39
subsetDEM:True
topoCorrect:True
metaContactName:ContactName
metaContactEmail:Contact Email

Where the full path to all files must be provided.

Daniel Clewley (daniel.clewley@gmail.com)

''')
parser.add_argument("-i", "--indir", type=str, required=True, help="Input directory, containing files to be processed")
parser.add_argument("-t", "--processingdir", type=str, required=True, help="Directory to process files in")
parser.add_argument("-p", "--parameters", type=str, required=True, help="Parameter file name")
parser.add_argument("-l", "--filelist", type=str, default=None, required=False, help="Text file containing list of files to process")
parser.add_argument("-s","--scriptsdir", type=str, required=True, help="Directory to store PBS scripts and output log files")
parser.add_argument("-o", "--outdir", type=str, default=None, required=False, help="Directory to copy processed scenes back to (optional)")
parser.add_argument("--submit", default=False, action='store_true', help="Submit jobs using qsub as they are created")

args = parser.parse_args()    


# Check if outdir is required
if args.outdir is None:
    outdirOption = ''
else:
    outdirOption = '--outdir ' + args.outdir

processScenes = []

# If a list of files is provided use these
if args.filelist is not None:
    inSceneList = open(args.filelist, 'r')
    for line in inSceneList:
        inSceneName = stripExtension(line.strip())
        processScenes.append(inSceneName)
    inSceneList.close()

# Else process all scenes in input directory
else:
    fileList = os.listdir(args.indir)
    for fileName in fileList:
        # Check file is a decent size (exclude text files in same directory)
        if os.path.getsize(os.path.join(args.indir,fileName)) > 10e6:
            inSceneName = stripExtension(fileName)
            processScenes.append(inSceneName)

jobID = 1
for scene in processScenes:

    jobName = 'gamma_' + str(jobID) 

    outPBS = '''#!/bin/bash
#
# PBS Script to run GAMMA for Scene
# {0}
#
#PBS -q production
#PBS -N {6}
#PBS -l select=1:ncpus=1:mem=1920mb
#PBS -l walltime=00:59:00
#PBS -l place=free
#PBS -V

# Change into directory
cd {1}

# Run script
BatchGamma.py \
--indir {2} \
--filename {0} \
--processingdir {3} {4} \
--parameters {5} \
  > {0}_batchgamma.log 2>&1
  '''.format(scene, args.scriptsdir, args.indir, args.processingdir, outdirOption, args.parameters, jobName)
  
    outFileName = os.path.join(args.scriptsdir, scene + '_run.sh')
    outFile = open(outFileName,'w')
    outFile.write(outPBS)
    outFile.close()
    
    if args.submit:
        subprocess.call(['qsub',outFileName])
    jobID+=1
