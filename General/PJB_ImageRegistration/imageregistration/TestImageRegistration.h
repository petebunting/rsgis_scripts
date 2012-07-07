/*
 *  TestImageRegistration.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 10/01/2006.
 *  Copyright 2006  Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */


#ifndef Test_IR_H
#define Test_IR_H

#include "ImageNotAvailableException.h"
#include "gdal_priv.h"
#include "ErrorCodes.h"
#include "ImageOverlap.h"
#include "JointHistogram.h"
#include "MutualInformation.h"
#include <iostream>
#include "VectorImageMeasures.h"

class TestImageRegistration{
public: 
	TestImageRegistration();
	void testImageOverlap(const int scenario, 
						  const char *referenceImage, 
						  const char *floatingImage);
	void getImage4Read(const char *fileRef, const char *fileFloat)  
		throw(ImageNotAvailableException);
	void testMIValues(const char *referenceImage, 
					  const char *floatingImage);
	void testImageInterpolation();
	void testTriangularImageInterpolation();
	void testEuclideanDistanceUsingSmallImages(const char *filepath, double shift, int pixelMovement, int imageBand);
	double findEuclideanDistance(float *image, double xShift, double yShift, int imagexSize, int imageYSize);
	~TestImageRegistration();
protected:
	GDALDataset *reference;
	GDALDataset *floating;
};

#endif
