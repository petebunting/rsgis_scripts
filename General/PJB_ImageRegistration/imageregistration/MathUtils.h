/*
 *  MathUtils.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 25/03/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */


#ifndef MathUtils_H
#define MathUtils_H

#include "gdal_priv.h"
#include "ImageTiling.h"
#include "ImageOverlap.h"
#include <cstdlib>

class MathUtils
{
public:
	MathUtils();
	double findFloatingPointComponent(double floatingPointNum, int *integer);
	double sumVector(double *vector, int size);
	int sumIntArray(int *array, int size);
	int roundDown(double number);
	int roundUp(double number);
	int round(double number);
	double absoluteValue(double number);
	double tileMean(TileCoords *tile, GDALDataset *image, bool imageA, int band);
	double tileStandardDeviation(TileCoords *tile, GDALDataset *image, bool imageA, int band);
	double tileVariation(TileCoords *tile, GDALDataset *image, bool imageA, int band);
	double tileRangePercentage(TileCoords *tile, GDALDataset *image, bool imageA, int band, double imageRange);
	double tileRange(TileCoords *tile, GDALDataset *image, bool imageA, int band);
	double imageRange(GDALDataset *image, int band);
	int randomWithinRange(int lower, int upper);

	~MathUtils();
};

#endif
