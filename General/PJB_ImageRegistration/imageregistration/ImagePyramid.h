/*
 *  ImagePyramid.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 09/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef ImagePyramid_H
#define ImagePyramid_H

#include "ImageNotAvailableException.h"
#include "ImageProcessingException.h"
#include "ImageOutputException.h"
#include "ErrorCodes.h"
#include "MathUtils.h"
#include "Interpolation.h"
#include "ImageOverlap.h"
#include "ImageNetworkStructures.h"
#include "ErrorCodes.h"
#include "ImageTiling.h"
#include "gdal_priv.h"
#include <iostream>

struct PyramidLevel
{
	GDALDataset *imageA;
	GDALDataset *imageB;
	ImageOverlap *imgOverlap;
	int windowSize;
	double imageRes;
	int level;
};

class ImagePyramid
{
public: 
	ImagePyramid();
	void constructImagePyramid(GDALDataset *imageA, 
							   GDALDataset *imageB, 
							   int numLevels, 
							   float *levelScales,
							   int *windowLevel,
							   int imageABand,
							   int imageBBand,
							   const char *outputPath)
		throw (ImageNotAvailableException, 
			  ImageProcessingException,
			   ImageOutputException);
	PyramidLevel* getLevel(int level);
	int getNumberOfLevels();
	void getTileCoords4PointWindow(ImageNetworkNode *networkNode,
								   int level,
								   TileCoords* tile);
	~ImagePyramid();
private:
	int numberOfLevels;
	PyramidLevel *pyramid;
};

#endif

