import sys
from rios import rat
import osgeo.gdal as gdal
import numpy as np
import argparse
import rsgislib
from rsgislib import rastergis

parser = argparse.ArgumentParser()
parser.add_argument("--rat", type=str, required=True, help="Raster attribute table to copy classification to")
parser.add_argument("--txt", type=str, required=True, help="Text file containing classification")
parser.add_argument("--outraster", type=str, required=False, default=None, help="Output Raster classification")
parser.add_argument("--name", type=str, required=False, default='Classification', help="Outname for column in RAT. Defaults to 'Classification'")

args = parser.parse_args()    
 
print('Reading in Classification')
classification = np.genfromtxt(args.txt,dtype=int, skip_header=1)

print('Opening RAT')
inRatFile = args.rat
ratDataset = gdal.Open(inRatFile, gdal.GA_Update)

# Read in column names
colnames = rat.getColumnNames(inRatFile)

# Read in one column
# (just need to check same number as rows as classification)
testCol = rat.readColumn(ratDataset, colnames[0]) 

if testCol.shape[0] != classification.shape[0]:
    raise Exception("The classification file doesn't contain the same number of rows as the RAT")

rat.writeColumn(ratDataset, args.name, classification)
ratDataset = None

if args.outraster is not None:
    rastergis.exportCols2GDALImage(args.rat, args.outraster, 'KEA', rsgislib.TYPE_8INT, [args.name])
