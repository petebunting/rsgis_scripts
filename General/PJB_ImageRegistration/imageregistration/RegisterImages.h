/*
 *  RegisterImages.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 09/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */
#ifndef RegisterImages_H
#define RegisterImages_H

#include "JointHistogram.h"
#include "MutualInformation.h"
#include "ImageOverlap.h"
#include "gdal_priv.h"
#include <iostream>
#include "NonusImageTree.h"
#include "NonusTreeNode.h"
#include "Queue.h"
#include "VectorImageMeasures.h"
#include "ImageMeasures.h"
#include "ImageTiling.h"
#include "CorrelationMeasures.h"
#include <cstdlib>
#include <ctime>
#include "TransformsTable.h"
#include "ImageNetwork.h"
#include "ImageNetworkStructures.h"
#include "ImagePyramid.h"
#include "JointHistogramImageMeasures.h"

struct SurfacePosition {
	double xShift;
	double yShift;
	double measure;
};

class RegisterImages
{
public:
	RegisterImages();
	void registerImagesSearchBuffer(GDALDataset *ref, 
									GDALDataset *floating, 
									int pixelBuffer, 
									const char *outfilename, 
									int bins, 
									int refBand, 
									int floatBand)
		throw(ImageRegistrationException, ImageOutputException);
	double calcMIImagesPixelShift(GDALDataset *ref, 
								  GDALDataset *floating, 
								  int xShift, 
								  int yShift, 
								  int bins, 
								  int refBand, 
								  int floatBand)
		throw(ImageRegistrationException);
	void saveImageWithNewGeoReference(GDALDataset *floating, 
									  int xShift, 
									  int yShift, 
									  const char *filename, 
									  const char *format)
		throw(ImageOutputException);
	void findNonLinearTransformation(GDALDataset *ref, 
									 GDALDataset *floating,
									 int pixelBuffer, 
									 int bins, 
									 int refBand, 
									 int floatBand)
		throw(ImageRegistrationException);
	Transform registerTileSearchBuffer(GDALDataset *ref, 
									   GDALDataset *floating, 
									   int pixelBuffer, 
									   int bins, 
									   int refBand, 
									   int floatBand,
									   TileCoords *tile)
		throw(ImageRegistrationException);
	Transform findExtremaInSurface(GDALDataset *ref, 
								   GDALDataset *floating, 
								   int pixelBuffer, 
								   int refBand, 
								   int floatBand,
								   TileCoords *tile,
								   int measure,
								   int startX,
								   int startY,
								   int bins,
								   bool max)
		throw(ImageRegistrationException);
	Transform findExtremaInSurfaceSimulatedAnnealing(GDALDataset *ref, 
													 GDALDataset *floating, 
													 int pixelBuffer, 
													 int refBand, 
													 int floatBand,
													 TileCoords *tile,
													 int measure,
													 int startX,
													 int startY,
													 int bins,
													 bool max,
													 int tmax,
													 int tdecrease,
													 int successful,
													 int unsuccessful)
		throw(ImageRegistrationException);
	double calcMIImagesTilePixelShift(GDALDataset *ref, 
									  GDALDataset *floating, 
									  int xShift, 
									  int yShift, 
									  int bins, 
									  int refBand, 
									  int floatBand,
									  TileCoords *tile)
		throw(ImageRegistrationException);
	void constructNonusImageTree(GDALDataset *ref, 
								 GDALDataset *floating,
								 int pixelBuffer, 
								 int bins, 
								 int refBand, 
								 int floatBand,
								 int minTileSize)
		throw(ImageRegistrationException);
	void constructSubPixelNonusImageTree(GDALDataset *ref, 
										 GDALDataset *floating,
										 const char *ctrlptsOutputFile,
										 int pixelBuffer, 
										 int bins, 
										 int refBand, 
										 int floatBand,
										 int minTileSize,
										 double tileMovement,
										 int measure)
		throw(ImageRegistrationException);
	
	void constructPixel_SubPixelNonusImageTree(GDALDataset *ref, 
										  GDALDataset *floating,
										  const char *ctrlptsOutputFile,
										  int pixelBuffer, 
										  int bins, 
										  int refBand, 
										  int floatBand,
										  int minTileSize,
										  double tileMovement,
										  int measure)
		throw(ImageRegistrationException);
	
		
	void constructDiffResolutionPixel_EstimateSubPixelNonusImageTree(GDALDataset *ref, 
																	  GDALDataset *floating,
																	  const char *ctrlptsOutputFile,
																	  int pixelBuffer, 
																	  int bins, 
																	  int refBand, 
																	  int floatBand,
																	  int minTileSize,
																	  int measure)
		throw(ImageRegistrationException);
	
	void constructPixel_EstimateSubPixelNonusImageTree(GDALDataset *ref, 
													   GDALDataset *floating,
													   const char *ctrlptsOutputFile,
													   int pixelBuffer, 
													   int bins, 
													   int refBand, 
													   int floatBand,
													   int minTileSize,
													   int measure)
		throw(ImageRegistrationException);
	
	Transform registerTileSubPixelSearchBuffer(GDALDataset *ref, 
											   GDALDataset *floating, 
											   int pixelBuffer, 
											   int bins, 
											   int refBand, 
											   int floatBand,
											   TileCoords *tile,
											   double tileMovement,
											   int measure)
		throw(ImageRegistrationException);
	
	Transform registerTilePixel_SubPixelSearchBuffer(GDALDataset *ref, 
											   GDALDataset *floating,  
											   int pixelBuffer, 
											   int bins, 
											   int refBand, 
											   int floatBand,
											   TileCoords *tile,
											   double tileMovement,
											   int measure)
		throw(ImageRegistrationException);
	
	Transform registerTilePixel_EstimateSubPixelSearchBuffer(GDALDataset *ref, 
															 GDALDataset *floating, 
															 int pixelBuffer, 
															 int bins, 
															 int refBand, 
															 int floatBand,
															 TileCoords *tile,
															 int tileMovement,
															 int measure)
		throw(ImageRegistrationException);
	
	Transform registerTileDiffResolutionPixel_EstimateSubPixelSearchBuffer(GDALDataset *ref, 
																			GDALDataset *floating, 
																			int pixelBuffer, 
																			int bins, 
																			int refBand, 
																			int floatBand,
																			TileCoords *tile,
																			int tileMovement,
																			int measure)
		throw(ImageRegistrationException);
	
	Transform registerTileSubPixelSurfaceWalking(GDALDataset *ref, 
											   GDALDataset *floating,  
											   int bins, 
											   int refBand, 
											   int floatBand,
											   TileCoords *tile,
											   double tileMovement,
											   int measure)
		throw(ImageRegistrationException);
	
	double calcMIImagesTileSubPixelShift(GDALDataset *ref, 
										 GDALDataset *floating, 
										 double xShift, 
										 double yShift, 
										 int bins, 
										 int refBand, 
										 int floatBand,
										 TileCoords *tile)
		throw(ImageRegistrationException);
	
	double calcMeasureImagesTilePixelShift(GDALDataset *ref, 
										   GDALDataset *floating, 
										   double xShift, 
										   double yShift, 
										   int bins, 
										   int refBand, 
										   int floatBand,
										   TileCoords *tile,
										   int measure)
		throw(ImageRegistrationException);
	
	double calcMeasureImagesTilePixelSubShift(GDALDataset *ref, 
										   GDALDataset *floating, 
										   double xShift, 
										   double yShift, 
										   int bins, 
										   int refBand, 
										   int floatBand,
										   TileCoords *tile,
										   int measure)
		throw(ImageRegistrationException);
	
	double calcMeasureDiffResolutionImagesTilePixelShift(GDALDataset *ref, 
														  GDALDataset *floating, 
														  double xShift, 
														  double yShift, 
														  int bins, 
														  int refBand, 
														  int floatBand,
														  TileCoords *tile,
														  int measure,
														  VectorImageMeasures *vecImageMeasures)
		throw(ImageRegistrationException);
	
	NonusImageTree* constructNonusImageTreeSubPixel(GDALDataset *ref, 
													GDALDataset *floating,
													int pixelBuffer, 
													int bins, 
													int refBand, 
													int floatBand,
													int minTileSize,
													int measure,
													int search,
													int numWalks,
													int tmax,
													int tdecrease,
													int successful,
													int unsuccessful,
													bool errorCorrection,
													float measureThreshold)
		throw(ImageRegistrationException);
	
	Transform findTileTransformation(GDALDataset *ref, 
									 GDALDataset *floating, 
									 int pixelBuffer,
									 int refBand, 
									 int floatBand,
									 TileCoords *tile,
									 int measure,
									 int bins,
									 int search,
									 int numWalks,
									 int tmax,
									 int tdecrease,
									 int successful,
									 int unsuccessful,
									 float measureThreshold,
									 int possStartX,
									 int possStartY,
									 bool randomStart)
		throw(ImageRegistrationException);
	
	void correctErrors(NonusTreeNode *parent,
					   GDALDataset *ref, 
					   GDALDataset *floating,
					   int pixelBuffer, 
					   int bins, 
					   int refBand, 
					   int floatBand,
					   int measure,
					   int errorThreshold)
		throw(ImageRegistrationException);
	
	void registerImageNetwork(ImagePyramid *imagePyramid,
							  ImageNetwork *imageNetwork,
							  int distanceMeasure,
							  int searchAlgor,
							  int searchArea,
							  int bins,
							  int numWalks,
							  int tmax,
							  int tdecrease,
							  int successful,
							  int unsuccessful,
							  float measureThreshold,
							  int levelIterations,
							  double distanceThreshold,
							  float *levelScales,
							  double* networkUpdateWeights,
							  int* distanceSteps,
							  int numberOfSteps,
							  int *windowLevel,
							  int correctionStdDev,
							  double tilePercentageRangeThreshold,
							  const char *ptsOutput)
		throw(ImageRegistrationException);
	
	
	double findWindowMeasureWithOrigin(GDALDataset *ref,
									   GDALDataset *floating,
									   int *origin, 
									   int refband,
									   int floatband,
									   int windowSize, 
									   int measure, 
									   int bins,
									   double xShift,
									   double yShift,
									   ImageOverlap *imgOverlap)
		throw(ImageRegistrationException);
	
	~RegisterImages();
};
#endif
