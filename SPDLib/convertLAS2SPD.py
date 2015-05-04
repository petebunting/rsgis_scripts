#!/usr/bin/env python
"""
Convert LAS files to SPD format and create:

- DSM
- DTM
- Hillshade images (for visualisation)

Dan Clewley (dac@pml.ac.uk)
"""
import glob, argparse, os
import subprocess
import shutil, tempfile
try:
   from rsgislib import imageutils
   haveRSGISLib=True
except ImportError:
   haveRSGISLib=False

def printCommand(commandList):
   """ Print list of commands provided to
       subprocess as a single string.
   """
   outStr = ''
   for arg in commandList:
      outStr += str(arg) + ' ' 
   print(outStr)
    
def getFileExtension(gdalformat):
    """
    A function to get the extension for a given file format 
    (NOTE, currently only KEA, GTIFF, HFA, PCI and ENVI are supported).
    """
    if gdalformat.lower() == "kea":
        ext = ".kea"
    elif gdalformat.lower() == "gtiff":
        ext = ".tif"
    elif gdalformat.lower() == "hfa":
        ext = ".img"
    elif gdalformat.lower() == "envi":
        ext = ".dem"
    elif gdalformat.lower() == "pcidsk":
        ext = ".pix"
    else:
        raise RSGISPyException("The extension for the gdalformat specified is unknown.")
    return ext
 
parser = argparse.ArgumentParser()
parser.add_argument("inputfile", nargs='+',type=str, help="Input Files(s)")
parser.add_argument("--dtm", action='store_true', default=False, help="Create DTM")
parser.add_argument("--dsm", action='store_true', default=False, help="Create DSM")
parser.add_argument("--hillshade", action='store_true', default=False, help="Create Hillshade from DTM/DSM")
parser.add_argument("--wkt", type=str, default=None, help="WKT file providing projection (Default = From LAS)")
parser.add_argument("--interpolation", type=str, default="NATURAL_NEIGHBOR", help="Interpolation algorithm for DTM/DSM (Default = NATURAL_NEIGHBOR)")
parser.add_argument("--of", type=str, default="KEA", help="Output format for rasters (Default = KEA)")
args = parser.parse_args() 

fileext = getFileExtension(args.of)

for lasfile in args.inputfile:
   print('\n***Converting: {}***\n'.format(lasfile))
   basefile = os.path.splitext(lasfile)[0]
   temp_dir = tempfile.mkdtemp()
   spdtmppath = os.path.join(temp_dir, 'spd_tmp')
   spdfile = basefile + '.spd'
   spdfile_grd = basefile + '_grd.spd'
   spdfile_grd_tmp = basefile + '_grd_tmp.spd'
   outdsm = basefile + '_dsm' + fileext
   outdsm_hillshade = basefile + '_dsm_hillshade' + fileext
   outdtm = basefile + '_dtm' + fileext
   outdtm_hillshade = basefile + '_dtm_hillshade' + fileext

   spdCMD = ['spdtranslate','--if','LAS','--of','SPD','-b',
               '1','-x','LAST_RETURN',
               '--temppath',spdtmppath,
               '-i',lasfile,'-o',spdfile]
   if args.wkt is not None:
     spdCMD = spdCMD + ['--input_proj',args.wkt, '--output_proj', args.wkt]
   print('Running:')
   printCommand(spdCMD)
   subprocess.call(spdCMD)

   shutil.rmtree(temp_dir)

   # If required create DSM
   if args.dtm or args.dsm:
      if args.dtm:

         print('DTM requested - classifying ground returns') 
         print(' Running Progressive Morphology Filter')
         pmfCMD = ['spdpmfgrd', 
                  '-r','50',
                  '--overlap','10',
                  '--maxfilter','14', 
                  '-i',spdfile,'-o',spdfile_grd]
         subprocess.call(pmfCMD)

         print('Creating DTM')
         dtmCMD = ['spdinterp','--dtm','--topo',
               '--in',args.interpolation,
               '-f',args.of,'-b','1','-i',spdfile_grd,'-o',outdtm]
         subprocess.call(dtmCMD)
         if haveRSGISLib and args.of == 'KEA':
            imageutils.popImageStats(outdtm,True,0.,True)

         if args.hillshade:
            print('Creating DTM Hillshade')
            hillshadeCMD = ['gdaldem','hillshade','-of',args.of,
               outdtm, outdtm_hillshade]
            subprocess.call(hillshadeCMD)
            if haveRSGISLib and args.of == 'KEA':
               imageutils.popImageStats(outdtm_hillshade,True,0.,True)

      if args.dsm: 
         if not args.dtm:
            spdfile_grd = spdfile

         print('Creating DSM')
         dsmCMD = ['spdinterp','--dsm','--topo',
               '--in',args.interpolation,
               '-f',args.of,'-b','1','-i',spdfile_grd,'-o',outdsm]

         subprocess.call(dsmCMD)
         if haveRSGISLib and args.of == 'KEA':
            imageutils.popImageStats(outdsm,True,0.,True)

         if args.hillshade:
            print('Creating DTM Hillshade')
            hillshadeCMD = ['gdaldem','hillshade','-of',args.of,
               outdsm, outdsm_hillshade]
            subprocess.call(hillshadeCMD)
            if haveRSGISLib and args.of == 'KEA':
               imageutils.popImageStats(outdsm_hillshade,True,0.,True)

