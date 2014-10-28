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

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", nargs='+',type=str, help="Input Files(s)")
parser.add_argument("--dtm", action='store_true', default=False, help="Create DTM")
parser.add_argument("--dsm", action='store_true', default=False, help="Create DSM")
parser.add_argument("--hillshade", action='store_true', default=False, help="Create Hillshade from DTM/DSM")
parser.add_argument("--wkt", type=str, default=None, help="WKT file providing projection (Default = From LAS)")
parser.add_argument("--interpolation", type=str, default="NATURAL_NEIGHBOR", help="Interpolation algorithm for DTM/DSM (Default = NATURAL_NEIGHBOR)")
args = parser.parse_args() 

for lasfile in args.inputfile:
   print('\n***Converting: {}***\n'.format(lasfile))
   basefile = os.path.splitext(lasfile)[0]
   temp_dir = tempfile.mkdtemp()
   spdtmppath = os.path.join(temp_dir, 'spd_tmp')
   spdfile = basefile + '.spd'
   spdfile_grd = basefile + '_grd.spd'
   spdfile_grd_tmp = basefile + '_grd_tmp.spd'
   outstats = basefile + '_stats.kea'
   outdsm = basefile + '_dsm.kea'
   outdsm_hillshade = basefile + '_dsm_hillshade.kea'
   outdtm = basefile + '_dtm.kea'
   outdtm_hillshade = basefile + '_dtm_hillshade.kea'

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
   exit()

   # If required create DSM
   if args.dtm or args.dsm:
      if args.dtm:

         print('DTM requested - classifying ground returns') 
         print(' Running Progressive Morphology Filter')
         pmfCMD = ['spdpmfgrd', '-c','50','-r','50','-b','1','--grd','1',
         '-i',spdfile,'-o',spdfile_grd_tmp]
         subprocess.call(pmfCMD)

         print(' Running Multi-scale Curvature Algorithm')
         mccCMD = ['spdmccgrd', '-c','50','-r','50','-b','1','--class','3',
         '--initcurvetol','1',
         '-i',spdfile_grd_tmp,'-o',spdfile_grd]
         subprocess.call(mccCMD)

         # Remove PMF only ground classification
         os.remove(spdfile_grd_tmp)

         print('Creating DTM')
         dtmCMD = ['spdinterp','--dtm','--topo',
               '--in',args.interpolation,
               '-f','KEA','-b','1','-i',spdfile_grd,'-o',outdtm]
         subprocess.call(dtmCMD)
         if haveRSGISLib:
            imageutils.popImageStats(outdtm,True,0.,True)

         if args.hillshade:
            print('Creating DTM Hillshade')
            hillshadeCMD = ['gdaldem','hillshade','-of','KEA',
               outdtm, outdtm_hillshade]
            subprocess.call(hillshadeCMD)
            if haveRSGISLib:
               imageutils.popImageStats(outdtm_hillshade,True,0.,True)

      if args.dsm: 
         if not args.dtm:
            spdfile_grd = spdfile

         print('Creating DSM')
         dsmCMD = ['spdinterp','--dsm','--topo',
               '--in',args.interpolation,
               '-f','KEA','-b','1','-i',spdfile_grd,'-o',outdsm]
         subprocess.call(dsmCMD)
         if haveRSGISLib:
            imageutils.popImageStats(outdsm,True,0.,True)

         if args.hillshade:
            print('Creating DTM Hillshade')
            hillshadeCMD = ['gdaldem','hillshade','-of','KEA',
               outdsm, outdsm_hillshade]
            subprocess.call(hillshadeCMD)
            if haveRSGISLib:
               imageutils.popImageStats(outdsm_hillshade,True,0.,True)

