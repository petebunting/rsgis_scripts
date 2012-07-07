/*
 *  CorrelationMeasures.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/04/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef CorrelationMeasures_H
#define CorrelationMeasures_H

#include "ImageOverlap.h"
#include "gdal_priv.h"
#include "ImageNotAvailableException.h"
#include "ImageProcessingException.h"
#include <iostream>
#include "Interpolation.h"
#include "MathUtils.h"

class CorrelationMeasures
{
public:
	CorrelationMeasures();
	double calcCorrelationCoefficient(GDALDataset *ref, 
									  GDALDataset *floating, 
									  int refBand, 
									  int floatBand, 
									  ImageOverlap *imgOverlap,
									  double xShift,
									  double yShift)
	throw(ImageNotAvailableException, ImageProcessingException);
	double calcCorrelationCoefficient(GDALDataset *ref, 
									  GDALDataset *floating, 
									  int refBand, 
									  int floatBand, 
									  ImageOverlap *imgOverlap)
		throw(ImageNotAvailableException, ImageProcessingException);
	double calcDiffResolutionCorrelationCoefficient(GDALDataset *ref, 
									  GDALDataset *floating, 
									  int refBand, 
									  int floatBand, 
									  ImageOverlap *imgOverlap)
		throw(ImageNotAvailableException, ImageProcessingException);
	
	double calcDiffResolutionCorrelationCoefficientRefHigh(GDALDataset *ref, 
														   GDALDataset *floating, 
														   int refBand, 
														   int floatBand, 
														   ImageOverlap *imgOverlap);
	
	double calcDiffResolutionCorrelationCoefficientFloatHigh(GDALDataset *ref, 
															 GDALDataset *floating, 
															 int refBand, 
															 int floatBand, 
															 ImageOverlap *imgOverlap);
	
	~CorrelationMeasures();
protected:	
		enum
	{
		NegShift = 0,
		PosShift = 1
	};
};


#endif
