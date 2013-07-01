###################################################
# run_zonalStats.py
# Runs zonal stats for all kea files in a directory
# 
# Dan Clewley (daniel.clewley@gmail.com) - 26/02/2013
#
###################################################

import os, sys, subprocess

fileExt = 'kea'

zonalStatsTemplate = os.path.join(os.sys.path[0], 'zonalStatsTemplate.xml')

if len(sys.argv) != 3:
    print('''Not enough parameters provided:
Usage:
    run_zonalStats_all.py inDIR inROIFile
''')
    exit()

inDIR = os.path.abspath(sys.argv[1]) # Use absolute path (needed for RSGISLib)
inROIFile = os.path.abspath(sys.argv[2]) 

command='find ' + inDIR + ' -name *.' + fileExt

out = subprocess.Popen(command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(stdout, stderr) = out.communicate()
stdout
fileList = stdout.split('\n')

for file in fileList:
    if file == '':
        pass
    else:
        outPath = os.path.split(file)[0]
        outName = os.path.split(file)[1]
        outBaseName = outName.replace('.' + fileExt,'')

        zonalStatsDir = os.path.join(outPath, 'ZonalStats')

        # Check if directory exists and create if it doesn't
        if os.path.isdir(zonalStatsDir) == False:
            os.mkdir(zonalStatsDir)

        createXMLcmd = '''rsgislibcmdxml.py --input %s -o %s/%s_zonalStats.xml \
-b %s \
-p %s \
-f %s \
    '''%(zonalStatsTemplate, zonalStatsDir, outBaseName, outBaseName, outPath, inROIFile)
        os.system(createXMLcmd)
        os.system('rsgisexe -x ' + zonalStatsDir + '/' + outBaseName + '_zonalStats.xml')





