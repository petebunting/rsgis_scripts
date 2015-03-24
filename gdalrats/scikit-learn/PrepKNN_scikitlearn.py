from rsgislib import rastergis
import rsgislib

from rios import rat
import numpy
import osgeo.gdal as gdal


clumpsImg='./N00E103_10_grid_knn_skl.kea'


rastergis.histoSampling(clumps=clumpsImg, varCol='HH', outSelectCol='HHSamplingWater', propOfSample=0.02, binWidth=0.01, classColumn='Class', classVal='1')
rastergis.histoSampling(clumps=clumpsImg, varCol='HH', outSelectCol='HHSamplingMang', propOfSample=0.1, binWidth=0.01, classColumn='Class', classVal='2')
rastergis.histoSampling(clumps=clumpsImg, varCol='HH', outSelectCol='HHSamplingOther', propOfSample=0.05, binWidth=0.01, classColumn='Class', classVal='3')

rastergis.histoSampling(clumps=clumpsImg, varCol='NDVI', outSelectCol='NDVISamplingWater', propOfSample=0.02, binWidth=0.01, classColumn='Class', classVal='1')
rastergis.histoSampling(clumps=clumpsImg, varCol='NDVI', outSelectCol='NDVISamplingMang', propOfSample=0.1, binWidth=0.01, classColumn='Class', classVal='2')
rastergis.histoSampling(clumps=clumpsImg, varCol='NDVI', outSelectCol='NDVISamplingOther', propOfSample=0.05, binWidth=0.01, classColumn='Class', classVal='3')


print("Open GDAL Dataset")
ratDataset = gdal.Open( clumpsImg, gdal.GA_Update )
HHSamplingWater = rat.readColumn(ratDataset, "HHSamplingWater")
HHSamplingMang = rat.readColumn(ratDataset, "HHSamplingMang")
HHSamplingOther = rat.readColumn(ratDataset, "HHSamplingOther")
NDVISamplingWater = rat.readColumn(ratDataset, "NDVISamplingWater")
NDVISamplingMang = rat.readColumn(ratDataset, "NDVISamplingMang")
NDVISamplingOther = rat.readColumn(ratDataset, "NDVISamplingOther")
Training = numpy.empty_like(HHSamplingWater, dtype=int)
Training[...] = 0
Training = numpy.where(((HHSamplingWater==1) | (HHSamplingMang == 1) | (HHSamplingOther == 1) | (NDVISamplingWater == 1) | (NDVISamplingMang == 1) | (NDVISamplingOther == 1)) , 1, Training)
# Export column to RAT
rat.writeColumn(ratDataset, "Training", Training)
ratDataset = None


