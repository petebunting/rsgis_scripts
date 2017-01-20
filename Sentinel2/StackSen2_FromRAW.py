import rsgislib
from rsgislib import imageutils
from rsgislib import imagecalibration

imageList = ['./RAW/B02.jp2', './RAW/B03.jp2', './RAW/B04.jp2']
bandNamesList = ['Blue','Green', 'Red']
outputImageBGR = './Sen2_BGR.kea'
imageutils.stackImageBands(imageList, bandNamesList, outputImageBGR, None, 0, 'KEA', rsgislib.TYPE_16UINT)

imageList = ['./RAW/B08.jp2']
bandNamesList = ['NIR']
outputImageNIR = './Sen2_NIR.kea'
imageutils.stackImageBands(imageList, bandNamesList, outputImageNIR, None, 0, 'KEA', rsgislib.TYPE_16UINT)

imageList = ['./RAW/B05.jp2', './RAW/B06.jp2', './RAW/B07.jp2', './RAW/B8A.jp2']
bandNamesList = ['RedEdge_B5','RedEdge_B6', 'RedEdge_B7', 'RedEdge_B8A']
outputImageRedEdge = './Sen2_RedEdge.kea'
imageutils.stackImageBands(imageList, bandNamesList, outputImageRedEdge, None, 0, 'KEA', rsgislib.TYPE_16UINT)

imageList = ['./RAW/B11.jp2', './RAW/B12.jp2']
bandNamesList = ['SWIR_B11', 'SWIR_B12']
outputImageSWIR = './Sen2_SWIR.kea'
imageutils.stackImageBands(imageList, bandNamesList, outputImageSWIR, None, 0, 'KEA', rsgislib.TYPE_16UINT)



outputImageRedEdge10m = './Sen2_RedEdge_10m.kea'
rsgislib.imageutils.resampleImage2Match(outputImageBGR, outputImageRedEdge, outputImageRedEdge10m, 'KEA', 'cubic', datatype=None)
outputImageSWIR10m = './Sen2_SWIR_10m.kea'
rsgislib.imageutils.resampleImage2Match(outputImageBGR, outputImageSWIR, outputImageSWIR10m, 'KEA', 'cubic', datatype=None)



imageList = [outputImageBGR, outputImageRedEdge10m, outputImageNIR, outputImageSWIR10m]
outputImageTOA = './Sen2_10m_Tile.kea'
imageutils.stackImageBands(imageList, None, outputImage, None, 0, 'KEA', rsgislib.TYPE_16UINT)

bandNames = ['Blue','Green','Red','RedEdge_B5','RedEdge_B6', 'RedEdge_B7', 'RedEdge_B8A', 'NIR','SWIR_B11', 'SWIR_B12']
imageutils.setBandNames(outputImage, bandNames)

outputImageDOS = './Sen2_10m_Tile_DOS.kea'

imagecalibration.performDOSCalc(outputImageTOA, outputImageDOS, gdalFormat='KEA', nonNegative=True, noDataVal=0, darkObjReflVal=0, darkObjPercentile=0.01, copyBandNames=True, calcStatsPyd=True)



