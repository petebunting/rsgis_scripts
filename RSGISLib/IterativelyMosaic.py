import rsgislib
from rsgislib import imageutils
import glob
import shutil

# Search for all files with the extension 'kea'
inputList = glob.glob('./Tropics/*.kea')
outImage = './Landsat_HansenTropics_GFC2013.kea'
tmpImageFileName = './Landsat_HansenTropics_GFC2013_tmp.kea'
tmpImage = ''
backgroundVal = 0.0
skipVal = 0.0
skipBand = 1
overlapBehaviour = 0
format = 'KEA'
dataType = rsgislib.TYPE_8UINT

tmpImage = inputList.pop() # Remove first element in the list.
for image in inputList:
	print("Processing ", image,)
	imageList = []
	imageList.append(tmpImage)
	imageList.append(image)
	
	print(imageList)
	imageutils.createImageMosaic(imageList, outImage, backgroundVal, skipVal, skipBand, overlapBehaviour, format, dataType)
	shutil.copy2(outImage, tmpImageFileName)
	tmpImage = tmpImageFileName
	print("   COMPLETED.")
print("Mosaic Complete")
	