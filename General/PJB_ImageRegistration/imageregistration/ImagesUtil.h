/*
 *  ImagesUtil.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 05/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef ImagesUtil_H
#define ImagesUtil_H

#include "gdal_priv.h"
#include "JointHistogram.h"
#include "ImageOverlap.h"
#include "RegisterImages.h"
#include "Interpolation.h"
#include <iostream>
#include "ErrorCodes.h"
#include "ImageNotAvailableException.h"
#include "ImageProcessingException.h"
#include "ImageRegistrationException.h"
#include "ImageOutputException.h"
#include "ImagePyramid.h"
#include "ImageNetwork.h"

class ImagesUtil
{
public:
	ImagesUtil();
	ImagesUtil(const char *fileRef, 
			   const char *fileFloat,
			   bool printOut)
	throw(ImageNotAvailableException);
	void generateJointHistogram(int refBand, 
								int floatBand,
								const char *outfilename, 
								int bins)
	throw(ImageNotAvailableException, ImageRegistrationException);
	void getImage4Read(const char *fileRef, 
					   const char *fileFloat,
					   bool printOut) 
		 throw(ImageNotAvailableException);
	void registerImages(int buffer, 
						const char *outfilename, 
						int bins, 
						int refBand, 
						int floatBand)
		throw(ImageRegistrationException);
	double calcMI(int bins, 
				  int refBand, 
				  int floatBand)
	throw(ImageRegistrationException);
	void printOverlap(bool singleLine) throw(ImageRegistrationException);
	void registerImagesNonLinearTransformation(int buffer, 
											   int bins, 
											   int refBand, 
											   int floatBand,
											   int minTileSize)
		throw(ImageRegistrationException);
	void registerImagesNonLinearTransformationSubPixel(const char *outfilename, 
													   int buffer, 
													   int bins, 
													   int refBand, 
													   int floatBand,
													   int minTileSize,
													   double tileMovement,
													   int measure)
		throw(ImageRegistrationException);
	void registerImagesMultiResolutionNonLinearTransformationEstimateSubPixel(const char *ptsOutputFile,
																			  int searchBuffer,
																			  int jhBins,
																			  int refBand,
																			  int floatBand,
																			  int minTileSize,
																			  int distanceMeasure)
		throw(ImageRegistrationException);
	void registerAllImagesSubPixelDiffResolutions(const char *ptsOutputFile,
												  const char *tmpPath,
												  int searchBuffer,
												  int jhBins,
												  int refBand,
												  int floatBand,
												  int minTileSize,
												  int distanceMeasure,
												  int search,
												  int numWalks,
												  int tmax,
												  int tdecrease,
												  int successful,
												  int unsuccessful,
												  bool image2image,
												  bool image2imageScaled,
												  bool map2image,
												  bool map2imageScaled,
												  bool errorCorrection,
												  float measureThreshold)
		throw(ImageRegistrationException);
	void registerImagesNonLinearTransformationEstimateSubPixel(const char *ptsOutputFile,
															   int searchBuffer,
															   int jhBins,
															   int refBand,
															   int floatBand,
															   int minTileSize,
															   int distanceMeasure)
		throw(ImageRegistrationException);
	
	
	void findControlPointsNetwork(const char *tmpPath,
								  const char *ptsOutput,
								  int refBand,
								  int floatBand,
								  int distanceMeasure,
								  int searchAlgor,
								  int searchArea,
								  int jhBins,
								  int numWalks,
								  int tmax,
								  int tdecrease,
								  int successful,
								  int unsuccessful,
								  float thresholdMeasure,
								  int numLevels,
								  int xPixelStep,
								  int yPixelStep,
								  float *levelScales,
								  int *windowLevel,
								  int numberIterations,
								  int networkDistanceThreshold,
								  double* networkUpdateWeights,
								  int* distanceSteps,
								  int numberOfSteps,
								  int correctionStdDev,
								  double tilePercentageRangeThreshold,
								  bool image2image,
								  bool image2imageScaled,
								  bool map2image,
								  bool map2imageScaled)
		throw(ImageRegistrationException);

	void findSimilarityStrip(int *origin, 
							 int refband,
							 int floatband,
							 int axis, 
							 int length, 
							 int windowSize, 
							 int measure, 
							 int bins,
							 const char *outputFile)
		throw(ImageRegistrationException);
	
	
	~ImagesUtil()throw();
protected:
	GDALDataset *reference;
	GDALDataset *floating;
};
#endif
