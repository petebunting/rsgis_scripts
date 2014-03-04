#! /usr/bin/env python

#########################################################################################
#########################################################################################
## BatchGamma.py
##
## A python script to process
## ALOS data using GAMMA
## Takes template files containing
## GAMMA commands and creates new file
## to process individual scene
## Author: Dan Clewley 
## Email: daniel.clewley@gmail.com
## Date 15/02/2010
##
## Permission is hereby granted, free of charge, to any person 
## obtaining a copy of this software and associated documentation 
## files (the "Software"), to deal in the Software without restriction, 
## including without limitation the rights to use, copy, modify, 
## merge, publish, distribute, sublicense, and/or sell copies of the 
## Software, and to permit persons to whom the Software is furnished 
## to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be 
## included in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
## OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
## IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
## ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
## CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
## WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##
## Input parameters
## 1) inDIR: directory containing raw, gzipped, data
## 2) inSceneList: text file containing scenes to be processed, type '-' to process all scenes in inDIR
## 3) processDIR: directory to process files
## 4) outDIRL: directory to copy files back to, type '-' to skip copying back
## 5) Parameter file
## 
## In the template file the following names must be used:
## - Leader file - LEDFILENAME
## - HH Image File - HHFILENAME
## - HV Image File - HVFILENAME                  
## - Scenename (used for all output files) - SCENENAME
## All other names will remain the same
##
## Before running the script the path must be set for GAMMA
##
## UPDATE - 18/04/2010 (Dan Clewley)
## - Added utility to cut and resample SRTM subset from 30 m SRTM
## - Added option to take zone as input parameter and set paths and CSH templates based on this
##
## UPDATE - 22/02/2011 (Dan Clewley)
## - Added option to generate alpha-entropy products in PolSARPro
##
## UPDATE - 26/01/2012 (Dan Clewley)
## - Added option to subset pan on scene basis (as with SRTM)
## - Option to supply paths as parameter file
##
## UPDATE - 26/10/2012 (Dan Clewley)
## - Parameters now supplied via a text file
## - Same script used for FBS / FBD / PLR 
##
## UPDATE - 12/02/2014 (Dan Clewley)
## - Function in RIOS now used for topo correction (doesn't require LAT package).
## - Option to provide single scene name.
## - Argparse now used to read in options.
## - Ability to use more projections.
## - General tidy up.
##
#########################################################################################
#########################################################################################

import os, sys, string, re, glob
import argparse
import time 

# Set up common functions
def stripExtension(inFileName):
    # Try some common extension
    outName = re.sub('\.tar\.gz','',inFileName)
    outName = re.sub('\.zip','',outName)

    return outName

def sortFinalData(fileList, dataDIR, sceneDIR, topoCorrect=False):

    """ Sort data into final files (keepData), archived files
        and files to remove (rmData)
    """

    if topoCorrect:
        keepData = ['_topo.','.png','_readme.txt']
    else:
        keepData = ['.utm','.mask','.dem','.hgt','.hdr','.png','_readme.txt']

    rmData = ['slc','1.1__A','1.0__A','_srtm_sub','mli','coeffs','BRS','.utm_to_rdc','offs','sim.sar']

    for fileName in fileList:
        filePath = os.path.join(dataDIR, fileName)
        if os.path.isfile(filePath):
            for keepStr in keepData:
                if fileName.find(keepStr) > -1:
                    cmdmvdata = 'mv ' +  filePath + ' ' + sceneDIR
                    os.system(cmdmvdata)
            for rmStr in rmData:
                if fileName.find(rmStr) > -1:
                    cmdrmdata = 'rm ' +  filePath
                    os.system(cmdrmdata)
            if os.path.isdir(filePath):
                cmdrmdata = 'rm -fr' +  filePath
                os.system(cmdrmdata)


# Read in parameters
parser = argparse.ArgumentParser(prog='BatchGamma', usage=''' BatchGamma.py
Utility script to process SAR data using GAMMA. 
Performs the following steps:
 1) Copies data to processing directory.
 2) Sets up CSH scripts to run GAMMA commands.
 3) Processes to SLC / Converts to GAMMA format SLC.
 4) Geocodes data to target projection and resolution.
   a) Subsets DEM to scene and prepares for GAMMA. Will also do panchromatic image, if requested.
 5) Generates ENVI headers
    Topographically corrects data (optional).
 6) Creates quicklooks
 7) Sorts data and copies back to output directory (if one is provided)

Daniel Clewley (daniel.clewley@gmail.com)

''')
parser.add_argument("-i", "--indir", type=str, required=True, help="Input directory, containing files to be processed")
parser.add_argument("-t", "--processingdir", type=str, required=True, help="Directory to process files in")
parser.add_argument("-p", "--parameters", type=str, required=True, help="Parameter file name")
parser.add_argument("-o", "--outdir", type=str, default=None, help="Directory to copy processed scenes back to (optional)")
parser.add_argument("-f", "--filename", type=str, action='append', required=False, default=None, help="Name of file(s) to process")
parser.add_argument("-l", "--filelist", type=str, default=None, required=False, help="Text file containing list of files to process")
parser.add_argument("--nocopy", default=False, action='store_true', required=False, help="DEBUG: Don't copy data")
parser.add_argument("--noslc", default=False, action='store_true', required=False, help="DEBUG: Don't run script to generate SLC")
parser.add_argument("--nosubset", default=False, action='store_true', required=False, help="DEBUG: Don't run script subset DEM")
parser.add_argument("--nogeo", default=False, action='store_true', required=False, help="DEBUG: Don't run script to geocode")

args = parser.parse_args()    

inDIR = args.indir
processDIR = args.processingdir
parameterFileName = args.parameters

outDIR = args.outdir

outDegrees = False
srtm = ''
pan = ''
subsetDEM = False
topoCorrect = False
genAlphaEntropy = False
subsetPan = False
targetRes = 30
thetaref = 39.0
metaContactName = ""
metaContactEmail = ""
rawSLCTemplateSet = False
slcGeoTemplateSet = False
srtmSet = False
panSet = False
outext = 'kea' # Extension for topo corrected files
outProjFile = None # WKT file defining output projection
outProjName = 'UTM' # Out projection Name (uses same format as GAMMA Par file)
topoFilterSize=None

# Get scripts path
batchPath = os.sys.path[0]
scriptsPath = re.sub('Python/BatchGamma','', batchPath)

# Add required Python directories to path.
sys.path.append(scriptsPath + 'Python/GenerateHeader/')
sys.path.append(scriptsPath + 'Python/QuickLook/')
sys.path.append(scriptsPath + 'Python/SubsetDEM/')
sys.path.append(scriptsPath + 'Python/SubsetPAN/')
sys.path.append(scriptsPath + 'Python/GeneratePAR/')
sys.path.append(scriptsPath + 'Python/BatchGamma/')
sys.path.append(scriptsPath + 'Python/TopoCorrect/')

from GenerateENVIHeader import GenerateENVIHeader
from GenerateENVIHeaderLatLong import GenerateENVIHeaderLatLong
from CreateSARQuickLook import CreateQuickLook
from SubsetDEM import SubsetDEM
from SubsetPAN import SubsetPAN
from GenerateDEMParFile import GenerateDEMParFile
from BatchGammaUtilities import BatchGammaMeta
import topoCorrection

# Set up paths for default templates
postProcessDEMTemplate = scriptsPath + 'CSHTemplates/General/post_process_dem_template.csh'
postProcessPANTemplate = scriptsPath + 'CSHTemplates/General/post_process_pan_template.csh'
generateHalphaTemplateFBD = scriptsPath + 'CSHTemplates/PolSARPro/generate_Halpha_FBD.csh'
geoHalphaTemplateFBD = scriptsPath + 'CSHTemplates/PolSARPro/geocode_Halpha.csh'
generateHalphaTemplatePLR = scriptsPath + 'CSHTemplates/PolSARPro/generate_Halpha.csh'
geoHalphaTemplatePLR = scriptsPath + 'CSHTemplates/PolSARPro/geocode_HAalpha.csh'
llProjFile = scriptsPath + 'Projection/LL_WGS84.wkt'

generateHalphaTemplate = generateHalphaTemplateFBD
geoHalphaTemplate = geoHalphaTemplateFBD

#######################################################################################################
# Read parameters from parameter file
parameterFile = open(parameterFileName,'rU')
for line in parameterFile:
    if line.count(':') >= 1:
        elements = line.split(':',line.count(':'))
        if elements[0].strip().lower() == 'rawslctemplate':
            rawSLCTemplate = elements[1].strip()
            rawSLCTemplateSet = True
        elif elements[0].strip().lower() == 'slcgeotemplate':
            slcGeoTemplate = elements[1].strip()
            slcGeoTemplateSet = True
        elif elements[0].strip().lower() == 'dem':
            srtm = elements[1].strip()
            srtmSet = True
        elif elements[0].strip().lower() == 'pan':
            pan = elements[1].strip()
            panSet = True
        elif elements[0].strip().lower() == 'outext':
            outext = elements[1].strip()
        elif elements[0].strip().lower() == 'thetaref':
            thetaref = float(elements[1].strip())
        elif elements[0].strip().lower() == 'targetres':
            targetRes = float(elements[1].strip())
        elif elements[0].strip().lower() == 'outprojwkt':
            outProjFile = elements[1].strip() 
        elif elements[0].strip().lower() == 'outprojname':
            outProjName = elements[1].strip() 
        elif elements[0].strip().lower() == 'subsetdem':
            if (elements[1].strip().lower() == 'true') or (elements[1].strip().lower() == 'yes'):
                subsetDEM = True
            else:
                subsetDEM = False
        elif elements[0].strip().lower() == 'subsetpan':
            if (elements[1].strip().lower() == 'true') or (elements[1].strip().lower() == 'yes'):
                subsetPan = True
            else:
                subsetPan = False
        elif elements[0].strip().lower() == 'genalphaentropy':
            if (elements[1].strip().lower() == 'true') or (elements[1].strip().lower() == 'yes'):
                genAlphaEntropy = True
            else:
                genAlphaEntropy = False
        elif elements[0].strip().lower() == 'topocorrect':
            if (elements[1].strip().lower() == 'true') or (elements[1].strip().lower() == 'yes'):
                topoCorrect = True
            else:
                topoCorrect = False
        elif elements[0].strip().lower() == 'topofiltersize':
            topoFilterSize = int(elements[1].strip())
        elif elements[0].strip().lower() == 'metacontactname':
            metaContactName = elements[1].strip()
        elif elements[0].strip().lower() == 'metacontactemail':
            metaContactEmail = elements[1].strip()

if rawSLCTemplateSet == False:
    print("ERROR: No SLC template set. Set using 'rawSLCTemplate' in parameter file")
    exit() 
if slcGeoTemplateSet == False:
    print("ERROR: No georefferencing template set. Set using 'slcGeoTemplate' in parameter file")
    exit()
if srtmSet == False:
    print("ERROR: No DEM provided. set using 'dem' in parameter file")
    exit()
if outProjFile is None:
    print("ERROR: No projection file provided. set using 'outProjWKT' in parameter file")
if panSet == False:
    subsetPan=False

#######################################################################################################
    
processScenes = list()

# Scenes to process

# If one or more scenes are provided add these to list
if args.filename is not None:
    for element in args.filename:
        inSceneName = stripExtension(element)
        processScenes.append(inSceneName)

# Or if a list of files is provided add to list
elif args.filelist is not None:
    inSceneList = open(args.filelist, 'r')
    for line in inSceneList:
        inSceneName = stripExtension(line.strip())
        processScenes.append(inSceneName)
    inSceneList.close()

# Else process all scenes in input directory
else:
    fileList = os.listdir(inDIR)
    for fileName in fileList:
        # Check file is a decent size (exclude text files in same directory)
        if os.path.getsize(os.path.join(inDIR,fileName)) > 10e6:
            inSceneName = stripExtension(fileName)
            processScenes.append(inSceneName)

for scene in processScenes:
    print('###########################################################')
    print(' Processing ' + scene)
    print(' Started processing at: ' +  time.strftime("%H:%M:%S, %a %b %m %Y.") )
    
    scriptsList = [] # List of scripts used for processing (for writing to metadata)

    sceneDIR = processDIR + '/' + scene + '/'
    dataDIR = processDIR + '/' + scene + '/l1data'
    
    print('----------------------------------')
    print('1) Getting data...')    
    if not args.nocopy:
        print(' a) Copying file...')
        cpSceneCMD = 'cp ' + inDIR + '/' + scene + '* ' + processDIR
        os.system(cpSceneCMD)
   
    os.chdir(processDIR)
    
    # Check if file is compressed - 
    if os.path.isfile(scene + '.tar.gz'):
        print(' b) Un-tarring file...')
        unTarCMD = 'tar -xf ' + scene + '.tar.gz'
        os.system(unTarCMD)
        
        # Remove tar file
        os.remove(scene + '.tar.gz')

    elif os.path.isfile(scene + '.zip'):
        print(' b) Un-zipping file...')
        unZipCMD = 'unzip ' + scene + '.zip'
        os.system(unZipCMD)
        
        # Remove zip file
        os.remove(scene + '.zip')    
        
    # Check if directory contains subfolder l1data
    subDIR = False
    try:
        fileList = os.listdir(sceneDIR)
        subDIR = False
        for fileName in fileList:
            if fileName == 'l1data':
                subDIR = True
    except OSError:
        # If not found search for, assume only unprocessed scene in folder
        lsCMD = 'ls ' + processDIR + '/*lev1'
        out = os.popen(lsCMD)
        newScene = re.sub('\n','',str(out.readline()))
        sceneDIR = processDIR + '/' + newScene + '/'
        
        print('Could not find ' + scene + ' processing, assuming name has changed to: ' + newScene)
        
    if subDIR == False:
        # If no directory called l1data, create one and move all data into it
        mkdirCMD = 'mkdir ' + processDIR + '/' + scene + '/l1data'
        os.system(mkdirCMD)
        mvCMD1 = 'mv ' + sceneDIR + '*ALP* ' + dataDIR 
        mvCMD2 = 'mv ' + sceneDIR + 'Restore* ' + dataDIR 
        mvCMD3 = 'mv ' + sceneDIR + '*txt ' + dataDIR
        os.system(mvCMD1)
        os.system(mvCMD2)
        os.system(mvCMD3) 
        # Remove JAXA log dir if it exists
        if os.path.isdir(os.path.join(sceneDIR,'log')):
            os.system('rm -fr ' + os.path.join(sceneDIR,'log'))
                
    print(' Data DIR = ' + dataDIR)
    os.chdir(dataDIR)
    
    # Create temp output files
    temp1 = 'temp1.csh'
    temp2 = 'temp2.csh'
    temp3 = 'temp3.csh'
    temp4 = 'temp4.csh'
    temp5 = 'temp5.csh'
    rawSLCScript = 'raw_to_SLC.csh'
    slcGeoScript = 'SLC_to_GEO.csh'
    postProcessDEMScript = 'PostProcessDEM.csh'
    postProcessPANScript = 'PostProcessPAN.csh'
    alphaEntropyScript = 'genAlphaEntropy.csh'
    geocodeAlphaEntropyScript = 'geoAlphaEntropy.csh'
    topoCorrectScript = 'topoCorrect.csh'
    
    print('----------------------------------')
    print('2) Creating GAMMA scripts...')
    # Check processing level of data
    LEDFileList = glob.glob('LED*')
    if len(LEDFileList) > 0:
        LEDFile = LEDFileList[0]
        replaceLEDCMD = 'sed \'s/LEDFILENAME/' + LEDFile + '/g\' ' + rawSLCTemplate + ' > ' + temp1
        os.system(replaceLEDCMD)
    else:
        raise Exception('Leader file not found!')

    # Replace IMG-HH file Name
    HHFileList = glob.glob('IMG-HH*')
    if len(HHFileList) > 0:
        HHFile = HHFileList[0]
        replaceHHCMD = 'sed \'s/HHFILENAME/' + HHFile + '/g\' ' + temp1 + ' > ' + temp2
    else:
        replaceHHCMD = 'cp ' + temp1 + ' ' + temp2
    os.system(replaceHHCMD)    

    # Replace IMG-HV file Name
    HVFileList = glob.glob('IMG-HV*')
    if len(HVFileList) > 0:
        HVFile = HVFileList[0]
        replaceHVCMD = 'sed \'s/HVFILENAME/' + HVFile + '/g\' ' + temp2 + ' > ' + temp3
    else:
        replaceHVCMD = 'cp ' + temp2 + ' ' + temp3
    os.system(replaceHVCMD)
    
    # Replace IMG-VV file Name
    VVFileList = glob.glob('IMG-VV*')
    if len(VVFileList) > 0:
        VVFile = VVFileList[0]
        replaceVVCMD = 'sed \'s/VVFILENAME/' + VVFile + '/g\' ' + temp3 + ' > ' + temp4
        # Set alpha / entropy templates for polarimetric data instead of FBD
        generateHalphaTemplate = generateHalphaTemplatePLR
        geoHalphaTemplate = geoHalphaTemplatePLR
        
    else:
        replaceVVCMD = 'cp ' + temp3 + ' ' + temp4
    os.system(replaceVVCMD)
    
    # Replace IMG-VH file Name
    VHFileList = glob.glob('IMG-VH*')
    if len(VHFileList) > 0:
        VHFile = VHFileList[0]
        replaceVHCMD = 'sed \'s/VVFILENAME/' + VHFile + '/g\' ' + temp4 + ' > ' + temp5
    else:
        replaceVHCMD = 'cp ' + temp4 + ' ' + temp5
    os.system(replaceVHCMD)
    
    # Replace dots in scenename with underscores
    scene = re.sub('\.','_',scene)

    # Replace Scenename
    replaceSceneNameSLCCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + temp5 + ' > ' + rawSLCScript
    replaceSceneNameGEOCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + slcGeoTemplate + ' > ' + slcGeoScript
    os.system(replaceSceneNameSLCCMD)
    os.system(replaceSceneNameGEOCMD)
    if subsetDEM:
        replaceSceneNamePostProcessDEMCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + postProcessDEMTemplate + ' > ' + postProcessDEMScript
        os.system(replaceSceneNamePostProcessDEMCMD)
       
    if subsetPan:
        replaceSceneNamePostProcessDEMCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + postProcessPANTemplate + ' > ' + postProcessPANScript
        os.system(replaceSceneNamePostProcessDEMCMD)
        
    if genAlphaEntropy:
        replaceHaCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + generateHalphaTemplate + ' > ' + alphaEntropyScript
        replaceHaGeoCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + geoHalphaTemplate + ' > ' + geocodeAlphaEntropyScript
        os.system(replaceHaCMD)
        os.system(replaceHaGeoCMD)
    
    if topoCorrect:
        topoCorrectFile = open(topoCorrectScript,'w')
        topoCorrectCMD = 'topoCorrection.py --insigma {0}_hh.utm --inpix {0}.pix --inlinc {0}.inc --outsigma {0}_hh_topo.{1} --thetaref {2} --n 1 --filterSize {3}\n'.format(scene, outext, thetaref, topoFilterSize)
        topoCorrectFile.write(topoCorrectCMD)
        topoCorrectFile.close()

    # Remove Temp Files
    rmTempCMD = 'rm temp*csh'
    os.system(rmTempCMD)
    
    # Run SLC
    print('----------------------------------')
    if not args.noslc:
        print('3) Running script to generate SLC...')
        runSLCCMD = 'csh ' + rawSLCScript + ' > slc.log'
        os.system(runSLCCMD)
        scriptsList.append(os.path.join(dataDIR, rawSLCTemplate))
        
    # Alpha-Entropy
    if genAlphaEntropy:
        print(' Generating alpha-Entropy image...')
        runAlphaEntropyCMD = 'csh ' + alphaEntropyScript + ' > alphaEntropy.log'
        os.system(runAlphaEntropyCMD)
        scriptsList.append(os.path.join(dataDIR, alphaEntropyScript))
        scriptsList.append(os.path.join(dataDIR, 'alphaEntropy.log'))
        
    # Run GEO
    print('----------------------------------')
    print('4) Running script to geocode SLC...')
    
    # Subset DEM if required.
    if subsetDEM and not args.nosubset:
        print(' a) creating DEM subset...')
        subDEM = SubsetDEM()
        srtmSub = dataDIR + '/' + scene + '_srtm_sub'
        srtmSubHeader = srtmSub + '.hdr'
        srtmSubPar = srtmSub + '_par'
        gammaCornerFile = dataDIR + '/' + scene + '_hh.slc.corners'
        subDEM.run(srtm, srtmSub, gammaCornerFile, outProjFile, targetRes)
        genPar = GenerateDEMParFile()
        genPar.run(srtmSubHeader, srtmSubPar, srtmSub, outProjName)
        print(' b) post-processing DEM...')
        runPostProcessDEMCMD = 'csh ' + postProcessDEMScript + ' > dem.log'
        os.system(runPostProcessDEMCMD)
    
    if subsetPan and not args.nosubset:
        print(' b) creating subset of panchromatic image ...')
        subPAN = SubsetPAN()
        panSub = dataDIR + '/' + scene + '_pan_sub'
        panSubHeader = panSub + '.hdr'
        panSubPar = panSub + '_par'
        gammaCornerFile = dataDIR + '/' + scene + '_hh.slc.corners'
        subPAN.run(pan, panSub, gammaCornerFile, llProjFile, outProjFile, targetRes)
        genPar = GenerateDEMParFile()
        genPar.run(panSubHeader, panSubPar)
        print(' b) post-processing PAN...')
        runPostProcessPANCMD = 'csh ' + postProcessPANScript + ' > dem.log'
        os.system(runPostProcessPANCMD)
    
    if not args.nogeo:
        print(' c) starting geocoding...')
        runGEOCMD = 'csh ' + slcGeoScript + ' > geo.log'
        os.system(runGEOCMD)
        scriptsList.append(os.path.join(dataDIR, runGEOCMD))
        
    if genAlphaEntropy: 
        print(' Geocoding alpha-Entropy image...') # Geocode alpha entropy image
        runAlphaEntropyCMD = 'csh ' + geocodeAlphaEntropyScript + ' > geoAlphaEntropy.log'
        os.system(runAlphaEntropyCMD)
    
    # Generate ENVI Header
    print('----------------------------------')
    print('5) Generating ENVI Header')
    if outDegrees:
        header = GenerateENVIHeaderLatLong()
        header.run('spatial', dataDIR, 'utm')
        header.run('spatial', dataDIR, 'inc')
        header.run('spatial', dataDIR, 'pix')
        header.run('spatial', dataDIR, 'dem')
        header.run('spatial', dataDIR, 'hgt')
    else:
        header = GenerateENVIHeader()
        header.run('spatial', dataDIR, 'utm', outProjFile)
        header.run('spatial', dataDIR, 'inc', outProjFile)
        header.run('spatial', dataDIR, 'pix', outProjFile)
        header.run('spatial', dataDIR, 'dem', outProjFile)
        header.run('spatial', dataDIR, 'hgt', outProjFile)

    if topoCorrect:
        print(' b) topographically correcting data...')

        topoCorrection.runCorrectionDIR(dataDIR, sigmaExt='utm', outExt=outext, thetaref=thetaref, nFactor=1, filterSize=topoFilterSize)
        scriptsList.append(os.path.join(dataDIR, topoCorrectScript))
     
    print('----------------------------------')
    print('6) Generating QuickLooks')
    quickLook = CreateQuickLook()
    if topoCorrect:
        quickLook.run(dataDIR, dataDIR, 'utm')
    else:
        quickLook.run(dataDIR, dataDIR, outext)
            
    # If no output directory is set don't remove files or copy back to server
    if outDIR is not None:
        # Sort data and copy back to server
        print('----------------------------------')
        print('7) Sorting data and copying back to server')
        
        fileList = os.listdir(dataDIR)
        
        # Sort out data
        sortFinalData(fileList, dataDIR, sceneDIR, topoCorrect)

        # Add scripts to metadata of final image. Only supported with KEA or ERDAS imagine files.
        if topoCorrect and (outext == 'kea' or outext == 'img'):
            keaList = glob.glob('*topo.')
            for keaFile in keaList:
                for scriptFile in scriptsList:
                    os.system('script2gdalmeta.py -i {0} -f {1}'.format(keaFile,scriptFile))

        # Rename and compress other data.
        os.chdir(sceneDIR)
        processingDIRName = time.strftime("processing_%Y%m%d") 
        cmdrename = 'mv {0} {1}'.format(dataDIR, processingDIRName)
        os.system(cmdrename)
        cmdcompress = 'tar -czf {0}.tar.gz {0}'.format(processingDIRName)
        os.system(cmdcompress)
        cmdrmprocess = 'rm -fr {0}'.format(processingDIRName)
        os.system(cmdrmprocess)
        
        # Rename data from level 1 to level 1_5
        fileList = os.listdir(sceneDIR)
        for fileName in fileList:
            newFileName = re.sub('lev1_1','lev1_5',fileName)
            newFileName = re.sub('lev1','lev1_5',newFileName)
            newFileName = re.sub('1_1','1_5',newFileName)
            newFileName = re.sub('1_0','1_5',newFileName)
            if newFileName != fileName:
                renamecmd = 'mv ' + os.path.join(sceneDIR, fileName) + ' ' + os.path.join(sceneDIR, newFileName)
                os.system(renamecmd)
       
        # Rename Directory
        newSceneDIR = re.sub('lev1_1','lev1_5',sceneDIR)
        newSceneDIR = re.sub('lev1','lev1_5',newSceneDIR)
        newSceneDIR = re.sub('1_1','1_5',newSceneDIR)
        newSceneDIR = re.sub('1_0','1_5',newSceneDIR)
        newSceneDIR = re.sub('1.1','1_5',newSceneDIR)
        newSceneDIR = re.sub('1.0','1_5',newSceneDIR)

        cmdrenamedir = 'mv ' + sceneDIR + ' ' + newSceneDIR
        os.system(cmdrenamedir)
        
        # Create metadata file
        meta = BatchGammaMeta(newSceneDIR, metaContactName, metaContactEmail)
        meta.writeMetaText()
        
        # Copy back
        cpcmd = 'cp -r ' + newSceneDIR + ' ' + outDIR + '/'
        os.system(cpcmd)
        
        # Delete data from processing DIR
        rmcmd = 'rm -fr ' + newSceneDIR
        os.system(rmcmd)    

    print(' Finished  processing at: ' +  time.strftime("%H:%M:%S, %a %b %m %Y."))
    print('###########################################################')
 
