#! /usr/bin/env python

#######################################
# convertSSURGO2RAT.py
# A script for converting selected attributes for
# SSURGO soil data to a raster attribute table
# and optionally a standard raster (one band
# per attribute)
# 
# Requires:
# rios (https://bitbucket.org/chchrsc/rios/overview)
# RSGISLib (http://www.rsgislib.org/doku.php)
# kealib (https://bitbucket.org/chchrsc/kealib/overview)
# and dependencies for these libraries
#
# Dan Clewley (daniel.clewley@gmail.com)
# 09/10/2012
#######################################


import os, sys, csv, glob
from rios import rat
import tempfile as tempfile

if len(sys.argv) == 4:
    inDIRName = sys.argv[1] 
    outColName = sys.argv[2] 
    outColNum = int(sys.argv[3]) 
    outRes = '30' # Set default to 30 m
elif len(sys.argv) >= 5:
    inDIRName = sys.argv[1] 
    outColName = sys.argv[2] 
    outColNum = int(sys.argv[3]) 
    outRes = str(sys.argv[4])
else:
    print '''Create Raster Atttribute Table (RAT) in KEA format from SSURGO data.
If the KEA file exists, new attributes are appended to the RAT.

Usage:
    python convertSSURGO2RAT.py inBaseDIR outColName outColNum [outRes]
Where outColName and outColNum are the required attributes in the table 'chorizon'
The output resolution defaults to 30, assuming the input projection is in m.
'''
    exit()

# CREATE RASTER ATTRIBUTE TABLE
inSpatialDIR = os.path.join(inDIRName,'spatial')
inSHPName = glob.glob(inSpatialDIR + '/soilmu_a_*.shp')[0]
inSHPFile = os.path.join(inSpatialDIR,inSHPName)
 
outKEAFile = inSHPFile.replace('.shp','_raster.kea')
# Set up name for standard raster file
outRasterImage = inSHPFile.replace('.shp','_raster_' + outColName + '.env')
outRasterImageScript = outRasterImage.replace('soilmu_a','run')
outRasterImageScript = outRasterImageScript.replace('.env','.xml')

# Check if KEA file exists or needs creating - assume if it exists it has the attribute table already
if os.path.exists(outKEAFile) == False: 
    # Rasterize polygon using gdal
    print 'Creating raster'
    rasterizeCommand = 'gdal_rasterize -of KEA -ot UInt32 -tr 30 30 -a MUKEY ' + inSHPFile + ' ' + outKEAFile + ' > /dev/null'
    os.system(rasterizeCommand)
    
    print 'Converting to RAT'
    # Convert to RAT using RSGIS
    outRSGISText = '''<rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">
        <rsgis:command algor="rastergis" option="popattributestats" clumps="%s" input="%s" >
                <rsgis:band band="1" min="mukey" />
        </rsgis:command>
    </rsgis:commands>'''%(outKEAFile, outKEAFile)
    
    # Create temp file for XML
    (osHandle, outXMLName) = tempfile.mkstemp(suffix='.xml')
    outXMLFile = open(outXMLName, 'w')
    outXMLFile.write(outRSGISText)
    outXMLFile.close()
    # Run RSGISLib
    os.system('rsgisexe -x ' + outXMLName + ' > /dev/null')
    # Remove temp file
    os.remove(outXMLName)

# JOIN ATTRIBUTES FROM TEXT FILE
print 'Adding ' + outColName + ' (column ' + str(outColNum) + ') to RAT'
# Open SSURGO text files
componentFileName = os.path.join(inDIRName, 'tabular','comp.txt')
chorizonFileName = os.path.join(inDIRName, 'tabular','chorizon.txt')

componentFile = open(componentFileName,'rU')
chorizonFile = open(chorizonFileName,'rU')

componentTxt = csv.reader(componentFile,delimiter='|')
chorizonTxt = csv.reader(chorizonFile,delimiter='|')

# Get mukey column from input file
mukeyCol = rat.readColumn(outKEAFile, 'mukey')

# Set up blank columns for output (one for each layer)
outColH1 = mukeyCol - mukeyCol 
outColH2 = mukeyCol - mukeyCol
outColH3 = mukeyCol - mukeyCol 
outColH4 = mukeyCol - mukeyCol 
outColH5 = mukeyCol - mukeyCol 
outColH6 = mukeyCol - mukeyCol 

# Set columns for mukey and cokey in componentTxt
compMUKEYCol = 107
compCOKEYCol = 108

chorizonCOKEYCol = 169
chorizonHZNAMECol = 0

for i in range(len(mukeyCol)):
    mukey = mukeyCol[i]
    if mukey > 0:
        componentFile.seek(0) # Reset position in CSV file
        for component in componentTxt:
            if int(component[compMUKEYCol]) == int(mukey):
                cokey = component[compCOKEYCol]
                chorizonFile.seek(0) # Reset position in CSV file
                for chorizon in chorizonTxt:
                    if (chorizon[chorizonCOKEYCol] == cokey) and (chorizon[outColNum] != ''):
                        if chorizon[chorizonHZNAMECol] == 'H1':
                            outColH1[i] = chorizon[outColNum]
                        elif chorizon[chorizonHZNAMECol] == 'H2':
                            outColH2[i] = chorizon[outColNum]
                        elif chorizon[chorizonHZNAMECol] == 'H3':
                            outColH3[i] = chorizon[outColNum]
                        elif chorizon[chorizonHZNAMECol] == 'H4':
                            outColH4[i] = chorizon[outColNum]
                        elif chorizon[chorizonHZNAMECol] == 'H5':
                            outColH5[i] = chorizon[outColNum]
                        elif chorizon[chorizonHZNAMECol] == 'H6':
                            outColH6[i] = chorizon[outColNum]

rat.writeColumn(outKEAFile, outColName + '_H1', outColH1)
rat.writeColumn(outKEAFile, outColName + '_H2', outColH2)
rat.writeColumn(outKEAFile, outColName + '_H3', outColH3)
rat.writeColumn(outKEAFile, outColName + '_H4', outColH4)
rat.writeColumn(outKEAFile, outColName + '_H5', outColH5)
rat.writeColumn(outKEAFile, outColName + '_H6', outColH6)

# Create RSGISLib script to convert to standard raster
outRSGISText = '''<rsgis:commands xmlns:rsgis="http://www.rsgislib.org/xml/">
    <rsgis:command algor="rastergis" option="exportcols2raster" clumps="%s" output="%s" format="ENVI" datatype="Float32" >
        <rsgis:field name="%s_H1" />
        <rsgis:field name="%s_H2" />
        <rsgis:field name="%s_H3" />
        <rsgis:field name="%s_H4" />
        <rsgis:field name="%s_H5" />
        <rsgis:field name="%s_H6" />
    </rsgis:command>

</rsgis:commands>'''%(outKEAFile, outRasterImage, outColName, outColName, outColName, outColName, outColName, outColName)

outXMLFile = open(outRasterImageScript, 'w')
outXMLFile.write(outRSGISText)
outXMLFile.close()

print 'Finished. 
print 'If you have viewer installed, you can view the data using:'
print ' viewer ' + outKEAFile
print 'To create a standard raster, with a seperate band for each layer, run:'
print ' rsgisexe -x ' + outRasterImageScript


