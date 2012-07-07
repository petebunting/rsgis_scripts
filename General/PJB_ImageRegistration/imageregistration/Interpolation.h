/*
 *  Interpolation.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 25/03/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef Interpolation_H
#define Interpolation_H

#include "ArrayUtils.h"
#include "ImageOverlap.h"
#include "MathUtils.h"
#include <iostream>
#include <fstream>
#include "gdal_priv.h"
#include "FileOutputException.h"
#include "ImageOutputException.h"

class Interpolation
{
public:
	Interpolation();
	double areaBasedBilinear(double xShift, double yShift, double *pixels); 
	double bilinear(double xShift, double yShift, double *pixels); 
	double nearestNeighbour(double xShift, double yShift, double *pixels); 
	double triangleAverage(double xShift, double yShift, double *pixels); 
	double triangle(double xShift, double yShift, double *pixels, bool triangulation);
	double cubic(double xShift, double yShift, double *pixels); 
	double estimateNewValueFromCurve(double *pixels, double shift);
	Transform calcateSubPixelTranformationXYCurve(double *surface, int *valid, double steps, bool minmax);
	GDALDataset* createNewImage(GDALDataset *data, 
								double outputXResolution, 
								double outputYResolution, 
								const char *filename, 
								const char *format, 
								int band)
		throw(FileOutputException, ImageOutputException);
	GDALDataset* copyImageBand(GDALDataset *data, 
							   const char *filename, 
							   const char *format, 
							   int band)
		throw(FileOutputException, ImageOutputException);
	~Interpolation();
};

#endif
