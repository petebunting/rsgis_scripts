#! /usr/bin/env python

#########################################################################################
#########################################################################################
## BatchGammaFBD.py
##
## A python script to process
## ALOS data using GAMMA
## Takes template files containing
## GAMMA commands and creates new file
## to process individual scene
## Author: Dan Clewley 
## Email: ddc06@aber.ac.uk
## Date 15/02/2010
##
## Input parameters
## 1) inDIR: directory containing raw, gzipped, data
## 2) inSceneList: text file containing scenes to be processed, type '-' to process all scenes in inDIR
## 3) processDIR: directory to process files
## 4) outDIRL: directory to copy files back to, type '-' to skip copying back
## 5) zone + north or south e.g. 55n (enter LatLong or ll for lat long)
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
#########################################################################################
#########################################################################################

import os, sys, string, re
from time import gmtime, strftime

print '''Script to process FBD ALOS scenes
python BatchGammaFBD.py <inDIR> <inSceneList> <processDIR> <outDIR> <zone>
 Input parameters:
 1) inDIR: directory containing raw, gzipped, data
 2) inSceneList: text file containing scenes to be processed, type '-' to process all scenes in inDIR
 3) processDIR: directory to process files
 4) outDIR: directory to copy files back to, type '-' to skip copying back
 5) zone + north or south e.g. 55n (enter LatLong or LL for lat long)'''

#########################################################################################
# SET FILE PATHS BASED ON ZONE

# Check for the correct number of parameters
numArgs = len(sys.argv)
if numArgs != 6:
    print "Not enough parameters supplied!"
    exit()

zone = sys.argv[5].strip()

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
generateHalphaTemplate = scriptsPath + 'CSHTemplates/PolSARPro/generate_Halpha_FBD.csh'
geoHalphaTemplate = scriptsPath + 'CSHTemplates/PolSARPro/geocode_Halpha.csh'

if zone == '54N' or zone == '54S' or zone == '54':
    rawSLCTemplate = scriptsPath + 'CSHTemplates/Australia/FBD_raw_to_SLC_Australia_template.csh'
    slcGeoTemplate = scriptsPath + 'CSHTemplates/Australia/FBD_SLC_to_GEO_Australia_template.csh'
    srtm = '/data/Australia/Basedata/SRTM/shraem_aus_20000211_ac0g0.tif'
    pan = '/data/Australia/Basedata/LandsatPan/l7tmpa_aus_y2002_db9a2.tif'
    llProjFile = scriptsPath + 'Projection/LL_WGS84.wkt'
    utmProjFile = scriptsPath + 'Projection/utm_z54.wkt'

elif zone == '55N' or zone == '55S' or zone == '55':
    srtm = '/data/Australia/Basedata/SRTM/shraem_aus_20000211_ac0g0.tif'
    pan = '/data/Australia/Basedata/LandsatPan/l7tmpa_aus_y2002_db9a2.tif'
    llProjFile = scriptsPath + 'Projection/LL_WGS84.wkt'
    utmProjFile = scriptsPath + 'Projection/utm_z55.wkt'
    rawSLCTemplate = scriptsPath + 'CSHTemplates/Australia/FBD_raw_to_SLC_Australia_template.csh'
    slcGeoTemplate = scriptsPath + 'CSHTemplates/Australia/FBD_SLC_to_GEO_Australia_template.csh'

elif zone =='56' or zone == '56N' or zone == '56S':
    srtm = '/data/Australia/Basedata/SRTM/shraem_aus_20000211_ac0g0.tif'
    pan = '/data/Australia/Basedata/LandsatPan/l7tmpa_aus_y2002_db9a2.tif'
    llProjFile = scriptsPath + 'Projection/LL_WGS84.wkt'
    utmProjFile = scriptsPath + 'Projection/utm_z56.wkt'
    rawSLCTemplate = scriptsPath + 'CSHTemplates/Australia/FBD_raw_to_SLC_Australia_template.csh'
    slcGeoTemplate = scriptsPath + 'CSHTemplates/Australia/FBD_SLC_to_GEO_Australia_template.csh'

elif zone =='46N' or zone == '46n':
    srtm = '/data/temp/SonaliALOS/DEM/astdem_mosaic.env'
    pan = '/data/temp/SonaliALOS/PAN/L4TM_1989_B1_mos.env'
    llProjFile = scriptsPath + 'Projection/LL_WGS84.wkt'
    utmProjFile = scriptsPath + 'Projection/utm_z46n.wkt'
    rawSLCTemplate = scriptsPath + 'CSHTemplates/General/FBD_raw_to_SLC_template.csh'
    slcGeoTemplate = scriptsPath + 'CSHTemplates/General/FBD_SLC_to_GEO_withPAN_template.csh'
    res = 90

elif zone =='Belize':
    srtm = '/data/ALOS/Belize/SRTM/SRTM_Belize_DEM.ieee'
    llProjFile = scriptsPath + 'Projection/LL_WGS84.wkt'
    utmProjFile = scriptsPath + 'Projection/utm_z56.wkt'
    rawSLCTemplate = scriptsPath + 'CSHTemplates/SouthAmerica/FBD_raw_to_SLC_belize_template.csh'
    slcGeoTemplate = scriptsPath + 'CSHTemplates/SouthAmerica/FBD_SLC_to_GEO_belize_template.csh'
    zone='LatLong'
    res = 90
    
elif zone =='UK':
    srtm = '/data/Wales/Basedata/Elevation/Wales_fltg_grtr0'
    llProjFile = scriptsPath + 'Projection/LL_WGS84.wkt'
    utmProjFile = scriptsPath + 'Projection/utm_z30n.wkt'
    rawSLCTemplate = scriptsPath + 'CSHTemplates/UK/FBD_raw_to_SLC_UK_template.csh'
    slcGeoTemplate = scriptsPath + 'CSHTemplates/UK/FBD_SLC_to_GEO_UK_template.csh'
    subsetPAN = False
    zone='BNG'
    res = 5
                
else:
    print 'Zone is not 54, 55, or 56.\nAssuming Lat-Long.\nSetting all paths relative to this script\n'  
    sys.path.append('../GenerateHeader/')
    sys.path.append('../QuickLook/')
    sys.path.append('../SubsetDEM/')
    sys.path.append('../GeneratePAR/')
    srtm = raw_input('Please enter the location of the elevation data:\n')
    rawSLCTemplate = raw_input('Please enter CSHTemplate to create SLC image:\n')
    slcGeoTemplate = raw_input('Please enter CSHTemplate to geocode SLC image:\n')
    topoCorrectQuestion = raw_input('Would you like the data to be topographically corrected? (enter y or n):\n')
    if topoCorrectQuestion == 'y':
        topoCorrectionTemplate = raw_input('Please enter CSHTemplate for topographic correction:\n')
    else:
        topoCorrect = False
    subsetDEM = False
    genAlphaEntropy = False

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
       if fileName[0:4] == 'alps':
           processScenes.append(re.sub('.tar.gz','',fileName))

else: #When using a list of files, checks for default name begining with alps, need to change this line if using non-AU names.
    inSceneList = open(inSceneListFile, 'r')
    for line in inSceneList:
        #if line[0:4] == 'alps':
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
                
    print 'Data DIR = ' + dataDIR
    os.chdir(dataDIR)
    
    # Create temp output files
    temp1 = 'temp1.csh'
    temp2 = 'temp2.csh'
    temp3 = 'temp3.csh'
    rawSLCScript = 'raw_to_SLC.csh'
    slcGeoScript = 'SLC_to_GEO.csh'
    postProcessDEMScript = 'PostProcessDEM.csh'
    postProcessPANScript = 'PostProcessPAN.csh'
    topoCorrectScript = 'TopoCorrect.csh'
    alphaEntropyScript = 'genAlphaEntropy.csh'
    geocodeAlphaEntropyScript = 'geoAlphaEntropy.csh'
    
    print '----------------------------------'
    print '2) Creating GAMMA scripts...'
    # Replace Leader file Name
    findLEDCMD = 'ls LED*'
    out = os.popen(findLEDCMD)
    LEDFile = re.sub('\n','',str(out.readline()))
    out.close()
    replaceLEDCMD = 'sed \'s/LEDFILENAME/' + LEDFile + '/g\' ' + rawSLCTemplate + ' > ' + temp1
    os.system(replaceLEDCMD)
    
    # Replace IMG-HH file Name
    findHHCMD = 'ls IMG-HH*'
    out = os.popen(findHHCMD)
    HHFile = re.sub('\n','',str(out.readline()))
    out.close()
    replaceHHCMD = 'sed \'s/HHFILENAME/' + HHFile + '/g\' ' + temp1 + ' > ' + temp2
    os.system(replaceHHCMD)
    
    # Replace IMG-HV file Name
    findHVCMD = 'ls IMG-HV*'
    out = os.popen(findHVCMD)
    HVFile = re.sub('\n','',str(out.readline()))
    out.close()
    replaceHVCMD = 'sed \'s/HVFILENAME/' + HVFile + '/g\' ' + temp2 + ' > ' + temp3
    os.system(replaceHVCMD)
    
    # Replace Scenename
    replaceSceneNameSLCCMD = 'sed \'s/SCENENAME/' + scene + '/g\' ' + temp3 + ' > ' + rawSLCScript
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
