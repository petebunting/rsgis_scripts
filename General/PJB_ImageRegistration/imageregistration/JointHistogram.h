/*
 *  JointHistogram.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 05/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef JointHistogram_H
#define JointHistogram_H

#include "gdal_priv.h"
#include "ImageOverlap.h"
#include <iostream>
#include "ImageNotAvailableException.h"
#include "ImageProcessingException.h"
#include "ErrorCodes.h"
#include "ImageRegistrationException.h"
#include "ImageOutputException.h"
#include "MathUtils.h"
#include "Interpolation.h"

class JointHistogram
{
public:
	JointHistogram();
	JointHistogram(int numBins);
	JointHistogram(GDALDataset *ref, 
				   GDALDataset *floating, 
				   int refBand, 
				   int floatBand, 
				   int numBins, 
				   ImageOverlap *imgOverlap)
		throw(ImageNotAvailableException, ImageProcessingException);
	bool generateJointHistogram(GDALDataset *ref, 
								GDALDataset *floating, 
								int refBand, 
								int floatBand, 
								ImageOverlap *imgOverlap)
		throw(ImageNotAvailableException, ImageProcessingException);
	bool generateSubPixelJointHistogram(GDALDataset *ref, 
										GDALDataset *floating, 
										int refBand, 
										int floatBand, 
										ImageOverlap *imgOverlap,
										double xShift,
										double yShift)
		throw(ImageNotAvailableException, ImageProcessingException);
	bool generateSubPixelJointHistogramWithInterp(GDALDataset *ref, 
												  GDALDataset *floating, 
												  int refBand, 
												  int floatBand, 
												  ImageOverlap *imgOverlap,
												  double xShift,
												  double yShift)
		throw(ImageNotAvailableException, ImageProcessingException);
		
	double getFloatingMax();
	double getFloatMin();
	double getReferenceMax();
	double getReferenceMin();
	void setNumberBins(int numBins);
	int getNumberBins();
	void printTextJointHistogram();
	void getJointHistogramImage(double *jointHisto);	
	void exportAsImage(const char *filename, const char *format)
		throw(ImageOutputException);
	~JointHistogram();
protected:
	int numberbins;
	double *frequency;
	double range;
	double refMax;
	double floatMax;
	double refMin;
	double floatMin;
	enum
	{
		NegShift = 0,
		PosShift = 1
	};
};
#endif
