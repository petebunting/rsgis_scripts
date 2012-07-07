/*
 *  ImageOverlap.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 06/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef ImageOverlap_H
#define ImageOverlap_H

#include "gdal_priv.h"
#include <iostream>
#include "ImageNotAvailableException.h"
#include "MathUtils.h"
#include "ImageProcessingException.h"
#include "ImageRegistrationException.h"
#include "ErrorCodes.h"
#include "math.h"
#include "ArrayUtils.h"

class ImageOverlap
{
public:
	ImageOverlap();
	ImageOverlap(GDALDataset *imgA, GDALDataset *imgB)
		throw(ImageNotAvailableException, ImageProcessingException);
	void calcOverlappingAreaWithShift(GDALDataset *imgA, 
									  GDALDataset *imgB, 
									  int xShift, 
									  int yShift)
		throw(ImageNotAvailableException, ImageProcessingException);

	
	void calcOverlappingAreaWithDiffResolutions(GDALDataset *imgA, 
												GDALDataset *imgB)
		throw(ImageNotAvailableException, ImageProcessingException);
	
	void calcOverlappingAreaWithinTileWithFloatShift(GDALDataset *imgA, 
													 GDALDataset *imgB, 
													 double xShift, 
													 double yShift, 
													 TileCoords *tile)
		throw(ImageNotAvailableException, ImageProcessingException);
	void calcOverlappingAreaWithDiffResolutionsTileWithFloatShift(GDALDataset *imgA, 
																  GDALDataset *imgB, 
																  double xShiftFloat, 
																  double yShiftFloat, 
																  TileCoords *tile)
		throw(ImageNotAvailableException, ImageProcessingException);
	void printOverlappingArea(bool singleLine);
	void findtiles(TileCoords *tile, TileCoords *tiles);
	int* getImageAPixelCoords();
	int* getImageBPixelCoords();
	double* getOverlapGeoCoords();
	int getSizeXPixelsA();
	int getSizeYPixelsA();
	int getSizeXPixelsB();
	int getSizeYPixelsB();
	int getNumPixels();
	double getRefPixelXRes();
	double getRefPixelYRes();
	double getFloatPixelXRes();
	double getFloatPixelYRes();
	double getPixelXRes();
	double getPixelYRes();
	void findtiles(TileCoords *tile, TileCoords *tiles, Transform transform);
	void findtilesDiffResolution(TileCoords *tile, TileCoords *tiles, Transform transform);
	~ImageOverlap();
protected:
	int imgAPixelCoords[4];
	int imgBPixelCoords[4];
	double overlapCoords[4];
	double pixelXres;
	double pixelYres;
	double refPixelXres;
	double refPixelYres;
	double floatPixelXres;
	double floatPixelYres;
};


#endif
