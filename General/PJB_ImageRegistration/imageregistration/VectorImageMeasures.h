/*
 *  VectorImageMeasures.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 23/01/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef VectorImageMeasures_H
#define VectorImageMeasures_H

#include "ImageOverlap.h"
#include "gdal_priv.h"
#include "ImageNotAvailableException.h"
#include "ImageProcessingException.h"
#include <iostream>
#include <fstream>
#include "ArrayUtils.h"
#include "Interpolation.h"
#include "MathUtils.h"

class VectorImageMeasures 
{
public:
	VectorImageMeasures();
	double calcEuclideanDistance(GDALDataset *ref, 
								 GDALDataset *floating, 
								 int refBand, 
								 int floatBand, 
								 ImageOverlap *imgOverlap,
								 double xShift,
								 double yShift)
		throw(ImageNotAvailableException, ImageProcessingException);
	double calcEuclideanDistance(GDALDataset *ref, 
								 GDALDataset *floating, 
								 int refBand, 
								 int floatBand, 
								 ImageOverlap *imgOverlap)
		throw(ImageNotAvailableException, ImageProcessingException);
	
	double calcManhattanDistance(GDALDataset *ref, 
								 GDALDataset *floating, 
								 int refBand, 
								 int floatBand, 
								 ImageOverlap *imgOverlap,
								 double xShift,
								 double yShift);
	
	double calcEuclideanDistance(double *imageA, 
								 double *imageB, 
								 int sizeX, 
								 int sizeY);
	
	double calcManhattenDistance(double *imageA, 
								 double *imageB, 
								 int sizeX, 
								 int sizeY);
	
	double calcChebyshevDistance(double *imageA, 
								 double *imageB, 
								 int sizeX, 
								 int sizeY);
	
	double calcManhattenIncrementDistanceWithInterpolation(double imageA, 
														   double xShift, 
														   double yShift, 
														   double *pixels);
	double calcEuclideanDistanceCubicInterpolation(GDALDataset *ref, 
												   GDALDataset *floating, 
												   int refBand, 
												   int floatBand, 
												   ImageOverlap *imgOverlap,
												   double xShift,
												   double yShift)
		throw(ImageNotAvailableException, ImageProcessingException);
	
protected:	
	enum
	{
		NegShift = 0,
		PosShift = 1
	};
};

#endif
