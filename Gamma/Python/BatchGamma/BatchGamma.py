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
#########################################################################################
#########################################################################################

import os, sys, string, re, glob
from time import gmtime, strftime

print '''Script to process FBD ALOS scenes
python BatchGammaFBD.py <inDIR> <inSceneList> <processDIR> <outDIR> <parameter file>
 Input parameters:
 1) inDIR: directory containing raw, gzipped, data
 2) inSceneList: text file containing scenes to be processed, type '-' to process all scenes in inDIR
 3) processDIR: directory to process files
 4) outDIR: directory to copy files back to, type '-' to skip copying back
 5) Parameter file'''

#########################################################################################

# Set ALOS file Prefix
alosFilePrefix = 'alps'

# Check for the correct number of parameters
numArgs = len(sys.argv)
if numArgs != 6:
    print "Not enough parameters supplied!"
    exit()

parameterFileName = sys.argv[5]

zone = 'utm'
srtm = ''
pan = ''
subsetDEM = True
topoCorrect = True
genAlphaEntropy = False #True
subsetPAN = True
res = 30

batchPath = os.sys.path[0]
scriptsPath = re.sub('Python/BatchGamma','', batchPath)

sys.path.append(scriptsPath + 'Python/GenerateHeader/')
sys.path.append(scriptsPath + 'Python/QuickLook/')
sys.path.append(scriptsPath + 'Python/SubsetDEM/')
sys.path.append(scriptsPath + 'Python/SubsetPAN/')
sys.path.append(scriptsPath + 'Python/GeneratePAR/')
sys.path.append(scriptsPath + 'Python/BatchGamma/')
topoCorrectionTemplate = scriptsPath + 'CSHTemplates/General/FBD_topo_correction_template.csh'
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
# Get parameters from parameter file

rawSLCTemplateSet = False
slcGeoTemplateSet = False
srtmSet = False
panSet = False

parameterFile = open(parameterFileName,'rU')
for line in parameterFile:
    if line.count(':') >= 1:
        elements = line.split(':',line.count(':'))
        if elements[0].strip() == 'rawSLCTemplate':
            rawSLCTemplate = elements[1].strip()
            rawSLCTemplateSet = True
        elif elements[0].strip() == 'slcGeoTemplate':
            slcGeoTemplate = elements[1].strip()
            slcGeoTemplateSet = True
        elif elements[0].strip() == 'dem':
            srtm = elements[1].strip()
            srtmSet = True
        elif elements[0].strip() == 'pan':
            pan = elements[1].strip()
            panSet = True
        elif elements[0].strip() == 'outProj':
            utmProjFile = elements[1].strip() 
        elif elements[0].strip() == 'demRes':
            demRes = elements[1].strip() 
        elif elements[0].strip() == 'subsetDEM':
            if elements[1].strip() == 'True':
                subsetDEM = True
            else:
                subsetDEM = False
        elif elements[0].strip() == 'subsetPan':
            if elements[1].strip() == 'True':
                subsetPan = True
            else:
                subsetPan = False
        elif elements[0].strip() == 'genAlphaEntropy':
            if elements[1].strip() == 'True':
                genAlphaEntropy = True
            else:
                genAlphaEntropy = False
        elif elements[0].strip() == 'topoCorrect':
            if elements[1].strip() == 'True':
                topoCorrect = True
            else:
                topoCorrect = False

if rawSLCTemplateSet == False:
    print "ERROR: No SLC template set. Set using 'rawSLCTemplate' in parameter file"
    exit() 
if slcGeoTemplateSet == False:
    print "ERROR: No georefferencing template set. Set using 'slcGeoTemplate' in parameter file"
    exit()
if srtmSet == False:
    print "ERROR: No DEM provided. Set using 'dem' in parameter file"
    exit()
if panSet == False:
    print "WARNING: No panchromatic mosic provided. If required for georefferencing Set using 'pan' in parameter file"
    exit()

#######################################################################################################
    
from GenerateENVIHeader import GenerateENVIHeader
from GenerateENVIHeaderLatLong import GenerateENVIHeaderLatLong
from CreateSARQuickLook import CreateQuickLook
from SubsetDEM import SubsetDEM
from SubsetPAN import SubsetPAN
from GenerateDEMParFile import GenerateDEMParFile
from BatchGammaMeta import BatchGammaMeta

inDIR = sys.argv[1].strip()
inSceneListFile = sys.argv[2].strip()
processDIR = sys.argv[3].strip()
outDIR = sys.argv[4].strip()

processScenes = list()

# Scenes to process
if inSceneListFile == '-': # If no process list provided process all scenes in DIR
    fileList = os.listdir(inDIR)
    for fileName in fileList:
       if fileName[0:4] == alosFilePrefix:
           processScenes.append(re.sub('.tar.gz','',fileName))

else: 
    inSceneList = open(inSceneListFile, 'r')
    for line in inSceneList:
        processScenes.append(line.strip())

for scene in processScenes:
    print '###########################################################'
    print ' Processing ' + scene 
    print ' Started processing at: ' +  str(strftime("%H:%M:%S", gmtime()))
    print '###########################################################'
    cpSceneCMD = 'cp ' + inDIR + '/' + scene + '* ' + processDIR
    unTarCMD = 'tar -xf ' + scene + '.tar.gz'
    sceneDIR = processDIR + '/' + scene + '/'
    dataDIR = processDIR + '/' + scene + '/l1data'
    
    print '----------------------------------'
    print '1) Getting data...'    
    print ' a) Copying file...'
    os.system(cpSceneCMD)
    os.chdir(processDIR)
    print ' b) Un-tarring file...'
    os.system(unTarCMD)
    # Remove tar file
    os.remove(scene + '.tar.gz')
     
    # Check if directory contains subfolder l1data
    subDIR = False
    try:
        fileList = os.listdir(sceneDIR)
        subDIR = False
        for fileName in fileList:
            if fileName == 'l1data':
                subDIR = True
    except OSError:
        # If not found search for assume only unprocessed scene in folder
        lsCMD = 'ls ' + processDIR + '/*lev1'
        out = os.popen(lsCMD)
        newScene = re.sub('\n','',str(out.readline()))
        sceneDIR = processDIR + '/' + newScene + '/'
        
        print 'Could not find ' + scene + ' processing, assuming name has changed to: ' + newScene
        
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
                
    print ' Data DIR = ' + dataDIR
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
    topoCorrectScript = 'TopoCorrect.csh'
    alphaEntropyScript = 'genAlphaEntropy.csh'
    geocodeAlphaEntropyScript = 'geoAlphaEntropy.csh'
    
    print '----------------------------------'
    print '2) Creating GAMMA scripts...'
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
    

    
    # Replace Scenename
    replaceSceneNameSLCCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + temp5 + ' > ' + rawSLCScript
    replaceSceneNameGEOCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + slcGeoTemplate + ' > ' + slcGeoScript
    os.system(replaceSceneNameSLCCMD)
    os.system(replaceSceneNameGEOCMD)
    if subsetDEM:
        replaceSceneNamePostProcessDEMCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + postProcessDEMTemplate + ' > ' + postProcessDEMScript
        os.system(replaceSceneNamePostProcessDEMCMD)
       
    if subsetPAN:
        replaceSceneNamePostProcessDEMCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + postProcessPANTemplate + ' > ' + postProcessPANScript
        os.system(replaceSceneNamePostProcessDEMCMD)
    
    if topoCorrect:
        replaceSceneNameTopoCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + topoCorrectionTemplate + ' > ' + topoCorrectScript
        os.system(replaceSceneNameTopoCMD)
        
    if genAlphaEntropy:
        replaceHaCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + generateHalphaTemplate + ' > ' + alphaEntropyScript
        replaceHaGeoCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + geoHalphaTemplate + ' > ' + geocodeAlphaEntropyScript
        os.system(replaceHaCMD)
        os.system(replaceHaGeoCMD)
    
    # Remove Temp Files
    rmTempCMD = 'rm temp*csh'
    os.system(rmTempCMD)
    
    # Run SLC
    print '----------------------------------'
    print '3) Running script to generate SLC...'
    runSLCCMD = 'csh ' + rawSLCScript + ' > slc.log'
    os.system(runSLCCMD)
        
    # Alpha-Entropy
    if genAlphaEntropy:
        print ' Generating alpha-Entropy image...'
        runAlphaEntropyCMD = 'csh ' + alphaEntropyScript + ' > alphaEntropy.log'
        os.system(runAlphaEntropyCMD)
        
    # Run GEO
    print '----------------------------------'
    print '4) Running script to geocode SLC...'
    
    # Subset DEM if required.
    if subsetDEM:
        print ' a) creating SRTM subset...'
        subDEM = SubsetDEM()
        srtmSub = dataDIR + '/' + scene + '_srtm_sub'
        srtmSubHeader = srtmSub + '.hdr'
        srtmSubPar = srtmSub + '_par'
        gammaCornerFile = dataDIR + '/' + scene + '.hh.slc.corners'
        subDEM.run(srtm, srtmSub, gammaCornerFile, llProjFile, utmProjFile, res)
        genPar = GenerateDEMParFile()
        genPar.run(srtmSubHeader, srtmSubPar)
        print ' b) post-processing SRTM...'
        runPostProcessDEMCMD = 'csh ' + postProcessDEMScript + ' > dem.log'
        os.system(runPostProcessDEMCMD)
        print ' c) starting geocoding...'
    
    if subsetPAN:
        print ' a) creating PAN subset...'
        subPAN = SubsetPAN()
        panSub = dataDIR + '/' + scene + '_pan_sub'
        panSubHeader = panSub + '.hdr'
        panSubPar = panSub + '_par'
        gammaCornerFile = dataDIR + '/' + scene + '.hh.slc.corners'
        subPAN.run(pan, panSub, gammaCornerFile, llProjFile, utmProjFile, res)
        genPar = GenerateDEMParFile()
        genPar.run(panSubHeader, panSubPar)
        print ' b) post-processing PAN...'
        runPostProcessPANCMD = 'csh ' + postProcessPANScript + ' > dem.log'
        os.system(runPostProcessPANCMD)
        print ' c) starting geocoding...'
    
    runGEOCMD = 'csh ' + slcGeoScript + ' > geo.log'
    os.system(runGEOCMD)
    
    if genAlphaEntropy: 
        print ' Geocoding alpha-Entropy image...' # Geocode alpha entropy image
        runAlphaEntropyCMD = 'csh ' + geocodeAlphaEntropyScript + ' > geoAlphaEntropy.log'
        os.system(runAlphaEntropyCMD)
    
    if topoCorrect:
        print ' d) topographically correcting data...'
        runTopoCorrectCMD = 'csh ' + topoCorrectScript + ' > topo.log'
        os.system(runTopoCorrectCMD)
              
    # Generate ENVI Header
    print '----------------------------------'
    print '5) Generating ENVI Header'
    if zone == 'LatLong' or zone == 'LL':
        header = GenerateENVIHeaderLatLong()
        header.run('spatial', dataDIR, 'utm')
        header.run('spatial', dataDIR, 'inc')
        header.run('spatial', dataDIR, 'pix')
    else:
        header = GenerateENVIHeader()
        header.run('spatial', dataDIR, 'utm')
        header.run('spatial', dataDIR, 'inc')
        header.run('spatial', dataDIR, 'pix')
    
    print '----------------------------------'
    print '6) Generating QuickLooks'
    quickLook = CreateQuickLook()
    quickLook.run(dataDIR, dataDIR, 'utm')
            
    # If no output directory is set don't remove files or copy back to server
    if outDIR != '-':
        # Sort data and copy back to server
        print '----------------------------------'
        print '7) Sorting data and copying back to server'
        
        # Move data back a level
        cmdmvdata = 'mv ' +  dataDIR + '/*utm ' + sceneDIR 
        cmdmvhdr = 'mv ' +   dataDIR + '/*hdr ' + sceneDIR
        cmdmvinc = 'mv '+ dataDIR + '/*inc ' + sceneDIR
        cmdmvpix = 'mv '+ dataDIR + '/*pix ' + sceneDIR
        cmdmverror =  'mv ' +   dataDIR + '/*geocode_error.txt ' + sceneDIR
        cmdmvdempar = 'mv ' +   dataDIR + '/*.dem.par ' + sceneDIR
        cmdmvscripts = 'mv ' +   dataDIR + '/*.csh ' + sceneDIR
        cmdmvlogs = 'mv ' +   dataDIR + '/*.log ' + sceneDIR
        cmdmvql = 'mv ' +   dataDIR + '/*.png ' + sceneDIR
    
        os.system(cmdmvdata)
        os.system(cmdmvhdr)
        os.system(cmdmvinc)
        os.system(cmdmvpix)
        os.system(cmdmverror)
        os.system(cmdmvdempar)
        os.system(cmdmvscripts)
        os.system(cmdmvlogs)
        os.system(cmdmvql)
    
        # Remove all other data! 
        os.chdir(processDIR)
        cmdrmexcess = 'rm -fr ' + dataDIR
        os.system(cmdrmexcess)
        
        # Rename data from level 1 to level 1_5
        fileList = os.listdir(sceneDIR)
        for fileName in fileList:
            newFileName = fileName.replace('lev1','lev1_5')
            renamecmd = 'mv ' + sceneDIR + fileName + ' ' + sceneDIR + newFileName
            os.system(renamecmd)
       
        # Rename Directory
        newSceneDIR = re.sub('lev1','lev1_5',sceneDIR)
        cmdrenamedir = 'mv ' + sceneDIR + ' ' + newSceneDIR
        os.system(cmdrenamedir)
        
        # Create metadata file
        meta = BatchGammaMeta(newSceneDIR, "FBD")
        meta.writeMetaText()
        
        # Copy back
        cpcmd = 'cp -r ' + newSceneDIR + ' ' + outDIR + '/'
        os.system(cpcmd)
        
        # Delete data from processing DIR
        rmcmd = 'rm -fr ' + newSceneDIR
        os.system(rmcmd)
