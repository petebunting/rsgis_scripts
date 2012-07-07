/*
 *  ImagesUtil.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 05/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "ImagesUtil.h"

ImagesUtil::ImagesUtil()
{
	
}

ImagesUtil::ImagesUtil(const char *fileRef, const char *fileFloat, bool printOut)
	throw(ImageNotAvailableException)
{
	// Get Images
	try
	{
		this->getImage4Read(fileRef, fileFloat, printOut);
	}
	catch( ImageNotAvailableException e )
	{
		if(floating != NULL)
		{
			delete floating;
		}
		if( reference != NULL )
		{
			delete reference;
		}
		throw e;
	}
}

void ImagesUtil::getImage4Read(const char *fileRef, const char *fileFloat, bool printOut)  
     throw(ImageNotAvailableException)
{
	GDALAllRegister();
	//Get Datasete
	reference = (GDALDataset *) GDALOpen(fileRef, GA_ReadOnly);
	// Check read in correctly.
	if(reference == NULL)
	{
		std::cout << "Bugger could not open Image " << fileRef << std::endl;
		throw ImageNotAvailableException("Could not Open Image.", error_codes::reference_image);
	}
	else
	{
		if(printOut)
		{
			std::cout << "Data from " << fileRef << " has been read in OK!\n";
		}
	}
	
	floating = (GDALDataset *) GDALOpen(fileFloat, GA_ReadOnly);
	// Check read in correctly.
	if(floating == NULL)
	{
		std::cout << "Bugger could not open Image " << fileFloat << std::endl;
		throw ImageNotAvailableException("Could not Open Image.", error_codes::floating_image);
	}
	else
	{
		if(printOut)
		{
			std::cout << "Data from " << fileFloat << " has been read in OK!\n";
		}
	}
}

void ImagesUtil::generateJointHistogram(int refBand, 
										int floatBand,
										const char *outfilename, 
										int bins)
     throw(ImageNotAvailableException, ImageRegistrationException)
{
	// Check whether dataset is null before proceeding.
	if(reference == NULL)
	{
		std::cout<<"Reference data is null. Cannot continue to generate joint histogram\n";
		throw ImageNotAvailableException("Image has not been read in.", error_codes::reference_image);
	}
	// Check whether dataset is null before proceeding.
	if(floating == NULL)
	{
		std::cout<<"Floating data is null. Cannot continue to generate joint histogram\n";
		throw ImageNotAvailableException("Image has not been read in.", error_codes::reference_image);
	}
	
	ImageOverlap *imgOverlap = NULL;	 
	JointHistogram *jointHis = NULL;
	try
	{
		// Find Image Overlap from initial georefencing	
		imgOverlap = new ImageOverlap(reference, floating);
	
		//Generate Joint Histogram
		jointHis = new JointHistogram(bins);
	
		jointHis->generateJointHistogram(reference, floating, refBand, floatBand, imgOverlap);
		//Export Joint Histogram
		jointHis->exportAsImage(outfilename, "GTiff");
		//jointHis->printTextJointHistogram();
	}
	catch(ImageRegistrationException e)
	{
		if(imgOverlap != NULL)
		{
			delete imgOverlap;
		}
		if(jointHis != NULL )
		{
			delete jointHis;
		}
		throw e;
	}

	//Free Memory
	if(imgOverlap != NULL)
	{
		delete imgOverlap;
	}
	if(jointHis != NULL )
	{
		delete jointHis;
	}
}

void ImagesUtil::printOverlap(bool singleLine)
throw(ImageRegistrationException)
{
	ImageOverlap *imgOverlap = NULL;
	try
	{
		imgOverlap = new ImageOverlap(reference, floating);
		imgOverlap->printOverlappingArea(singleLine);
	}
	catch(ImageRegistrationException e)
	{
		if( imgOverlap != NULL )
		{
			delete imgOverlap;
		}
		throw e;
	}
	
	if( imgOverlap != NULL )
	{
		delete imgOverlap;
	}
}

void ImagesUtil::registerImages(int buffer, 
								const char *outfilename, 
								int bins, 
								int refBand, 
								int floatBand)
throw(ImageRegistrationException)
{
	RegisterImages *regImages = NULL;
	try
	{
		regImages = new RegisterImages;
		regImages->registerImagesSearchBuffer(reference, 
											  floating, 
											  buffer, 
											  outfilename, 
											  bins,
											  refBand, 
											  floatBand);
	}
	catch(ImageRegistrationException e)
	{
		if(regImages != NULL)
		{
			delete regImages;
		}
		throw e;
	}
	
	if(regImages != NULL)
	{
		delete regImages;
	}
}

double ImagesUtil::calcMI(int bins, int refBand, int floatBand)
throw(ImageRegistrationException)
{
	ImageOverlap *imgOverlap = NULL;
	JointHistogram *jointHistogram = NULL;
	MutualInformation *mi = NULL;
	double mi_value = 0;
	try
	{
		/******************* Calc Image Overlap ***************************/
		imgOverlap = new ImageOverlap(reference, floating);
		/************************************************************************/
	
		/******************* Generate Joint Histogram ***************************/
		jointHistogram = new JointHistogram(bins);
		jointHistogram->generateJointHistogram(reference, floating, refBand, floatBand, imgOverlap);
		/************************************************************************/
	
		/************************** Calculate MI *******************************/
		mi = new MutualInformation;
		mi_value = mi->calcMutualInformation(*jointHistogram);
		/************************************************************************/
		//std::cout << "mi: " << mi_value << std::endl;
	}
	catch(ImageRegistrationException e)
	{
		if( imgOverlap != NULL )
		{
			delete imgOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		if( mi != NULL )
		{
			delete mi;
		}
		throw e;
	}
	// Free Memory
	if( imgOverlap != NULL )
	{
		delete imgOverlap;
	}
	if( jointHistogram != NULL )
	{
		delete jointHistogram;
	}
	if( mi != NULL )
	{
		delete mi;
	}
	
	return mi_value;	
}

void ImagesUtil::registerImagesNonLinearTransformation(int buffer, 
													   int bins, 
													   int refBand, 
													   int floatBand,
													   int minTileSize)
throw(ImageRegistrationException)
{
	RegisterImages *regImages = NULL;
	try
	{
		regImages = new RegisterImages;
		regImages->constructNonusImageTree(reference, 
										   floating, 
										   buffer, 
										   bins, 
										   refBand, 
										   floatBand, 
										   minTileSize);
		
		/*regImages->findNonLinearTransformation(reference, 
											   floating, 
											   outfilename, 
											   buffer, 
											   bins, 
											   refBand, 
											   floatBand);*/
	}
	catch(ImageRegistrationException e)
	{
		if(regImages != NULL)
		{
			delete regImages;
		}
		throw e;
	}
	if(regImages != NULL)
	{
		delete regImages;
	}
}

void ImagesUtil::registerImagesNonLinearTransformationSubPixel(const char *outfilename, 
															   int buffer, 
															   int bins, 
															   int refBand, 
															   int floatBand,
															   int minTileSize,
															   double tileMovement,
															   int measure)
	throw(ImageRegistrationException)
{
	//std::cout << "ENTERED ImageUtil subpixel" << std::endl;
	RegisterImages *regImages = NULL;
	try
	{
		regImages = new RegisterImages;
		regImages->constructSubPixelNonusImageTree(reference, 
												   floating, 
												   outfilename,
												   buffer, 
												   bins, 
												   refBand, 
												   floatBand, 
												   minTileSize, 
												   tileMovement,
												   measure);
	}
	catch(ImageRegistrationException e)
	{
		if(regImages != NULL)
		{
			delete regImages;
		}
		throw e;
	}
	if(regImages != NULL)
	{
		delete regImages;
	}
}

void ImagesUtil::registerImagesNonLinearTransformationEstimateSubPixel(const char *ptsOutputFile,
																	   int searchBuffer,
																	   int jhBins,
																	   int refBand,
																	   int floatBand,
																	   int minTileSize,
																	   int distanceMeasure)
	throw(ImageRegistrationException)
{
		RegisterImages *regImages = NULL;
		try
		{
			regImages = new RegisterImages;
			regImages->constructPixel_EstimateSubPixelNonusImageTree(reference, 
																	 floating, 
																	 ptsOutputFile,
																	 searchBuffer,
																	 jhBins, 
																	 refBand, 
																	 floatBand, 
																	 minTileSize, 
																	 distanceMeasure);
		}
		catch(ImageRegistrationException e)
		{
			if(regImages != NULL)
			{
				delete regImages;
			}
			throw e;
		}
		if(regImages != NULL)
		{
			delete regImages;
		}
}

void ImagesUtil::registerImagesMultiResolutionNonLinearTransformationEstimateSubPixel(const char *ptsOutputFile,
																					 int searchBuffer,
																					 int jhBins,
																					 int refBand,
																					 int floatBand,
																					 int minTileSize,
																					 int distanceMeasure)
throw(ImageRegistrationException)
{
	RegisterImages *regImages = NULL;
	try
	{
		regImages = new RegisterImages;
		regImages->constructDiffResolutionPixel_EstimateSubPixelNonusImageTree(reference, 
																			   floating, 
																			   ptsOutputFile,
																			   searchBuffer,
																			   jhBins, 
																			   refBand, 
																			   floatBand, 
																			   minTileSize, 
																			   distanceMeasure);
	}
	catch(ImageRegistrationException e)
	{
		if(regImages != NULL)
		{
			delete regImages;
		}
		throw e;
	}
	if(regImages != NULL)
	{
		delete regImages;
	}
}

void ImagesUtil::registerAllImagesSubPixelDiffResolutions(const char *ptsOutputFile,
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
throw(ImageRegistrationException)
{
	RegisterImages *regImages = NULL;
	NonusImageTree *nonusImageTree = NULL;
	Interpolation interpolation;
	try
	{
		double xScale = 0;
		double yScale = 0;
		regImages = new RegisterImages;

		double *trans1 = new double[6];
		reference->GetGeoTransform(trans1);	
		if(trans1[1] < 0)
		{
			trans1[1] = trans1[1]*(-1);
		}
		if(trans1[5] < 0)
		{
			trans1[5] = trans1[5]*(-1);
		}
		double *trans2 = new double[6];
		floating->GetGeoTransform(trans2);	
		if(trans2[1] < 0)
		{
			trans2[1] = trans2[1]*(-1);
		}
		if(trans2[5] < 0)
		{
			trans2[5] = trans2[5]*(-1);
		}
		
		if(trans1[1] != trans2[1] & trans1[5] != trans2[5])
		{
			GDALDataset *interpolatedImage;
			// Images not equal resolution so interpolate lower resolution image.
			if(trans1[1] < trans2[1] & trans1[5] < trans2[5])
			{
				interpolatedImage = interpolation.createNewImage(floating, 
																 trans1[1], 
																 trans1[5], 
																 tmpPath, 
																 "GTiff",
																 floatBand);
				
				if(interpolatedImage == NULL)
				{
					throw ImageRegistrationException("Image Scalling has gone wrong!! No new image was returned.",
													  error_codes::other_image);
				}
				
				std::cout << "Image interpolated to equivlent resolution. Now going to register...";
				nonusImageTree = regImages->constructNonusImageTreeSubPixel(reference, 
																			interpolatedImage, 
																			searchBuffer,
																			jhBins, 
																			refBand, 
																			1, 
																			minTileSize, 
																			distanceMeasure,
																			search,
																			numWalks,
																			tmax,
																			tdecrease,
																			successful,
																			unsuccessful,
																			errorCorrection,
																			measureThreshold);
				std::cout << "Found registration now going to output...\n";
				xScale = trans1[1]/trans2[1];
				yScale = trans1[5]/trans2[5];
			}
			else if(trans1[1] > trans2[1] & trans1[5] > trans2[5])
			{
				interpolatedImage = interpolation.createNewImage(reference, 
																 trans2[1], 
																 trans2[5], 
																 tmpPath, 
																 "GTiff",
																 refBand);
				
				if(interpolatedImage == NULL)
				{
					std::cout << "interpolated image is NULL!!\n";
					throw ImageRegistrationException("Image Scalling has gone wrong!! No new image was returned.",
													 error_codes::other_image);
				}
				std::cout << "Image interpolated to equivlent resolution. Now going to register...";
				
				nonusImageTree = regImages->constructNonusImageTreeSubPixel(interpolatedImage, 
																			floating, 
																			searchBuffer,
																			jhBins, 
																			1, 
																			floatBand, 
																			minTileSize, 
																			distanceMeasure,
																			search,
																			numWalks,
																			tmax,
																			tdecrease,
																			successful,
																			unsuccessful,
																			errorCorrection,
																			measureThreshold);
				std::cout << "Found registration now going to output...\n";
				xScale = 0;
				yScale = 0;
			}
			else
			{
				throw new ImageRegistrationException("Image have different compared resolutions in x and y axis'",
													 error_codes::other_image);
			}
		}
		else
		{
			// Images equal resolution so register.
			nonusImageTree = regImages->constructNonusImageTreeSubPixel(reference, 
																		floating, 
																		searchBuffer,
																		jhBins, 
																		refBand, 
																		floatBand, 
																		minTileSize, 
																		distanceMeasure,
																		search,
																		numWalks,
																		tmax,
																		tdecrease,
																		successful,
																		unsuccessful,
																		errorCorrection,
																		measureThreshold);
			std::cout << "Found registration now going to output...\n";
			xScale = 0;
			yScale = 0;
		}
		
		/********** Scale and output control points *************************/
		
		char tmpFilePath[1000];
		if(image2image)
		{
			strcpy(tmpFilePath, ptsOutputFile);
			strcat(tmpFilePath, "_image2image.pts");
			nonusImageTree->write2EnviGcpsFile(tmpFilePath, -1);
			std::cout << "Outputted image to image control points...\n";
		}
		
		if(image2imageScaled)
		{
			strcpy(tmpFilePath, ptsOutputFile);
			strcat(tmpFilePath, "_scaled_image2image.pts");
			nonusImageTree->write2EnviGcpsFile(tmpFilePath, -1, xScale, yScale);
			std::cout << "Outputted scaled image to image control points...\n";
		}
		
		if(map2image)
		{
			strcpy(tmpFilePath, ptsOutputFile);
			strcat(tmpFilePath, "_map2image.pts");
			nonusImageTree->writeMap2Image2EnviGcpsFile(tmpFilePath, -1);
			std::cout << "Outputted map to image control points...\n";
		}
		
		if(map2imageScaled)
		{
			strcpy(tmpFilePath, ptsOutputFile);
			strcat(tmpFilePath, "_scaled_map2image.pts");
			nonusImageTree->writeMap2Image2EnviGcpsFile(tmpFilePath, -1, xScale, yScale);
			std::cout << "Outputted scaled map to image control points...\n";
		}
		
		
		//nonusImageTree->printTree();
		
		
		/*********************************************************************/
		
		std::cout << "Finished Registration \n";
	}
	catch(ImageRegistrationException e)
	{
		if(regImages != NULL)
		{
			delete regImages;
		}
		if(nonusImageTree != NULL)
		{
			delete nonusImageTree;
		}
		throw e;
	}
	if(regImages != NULL)
	{
		delete regImages;
	}
	if(nonusImageTree != NULL)
	{
		delete nonusImageTree;
	}
}

void ImagesUtil::findControlPointsNetwork(const char *tmpPath,
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
throw(ImageRegistrationException)
{		
	ImagePyramid *imagePyramid = NULL;
	ImageNetwork *imageNetwork = NULL;
	RegisterImages *registerImagesObj = NULL;
	char tmpFilePath[1000];
	try
	{
		// Construct Image Pyramid.
		imagePyramid = new ImagePyramid;
		imagePyramid->constructImagePyramid(reference, 
											floating, 
											numLevels, 
											levelScales,
											windowLevel,
											refBand,
											floatBand,
											tmpPath);
		
		// Construct the Network..
		imageNetwork = new ImageNetwork;
		imageNetwork->constructNetwork(imagePyramid, 
									   numLevels,
									   xPixelStep,
									   yPixelStep,
									   windowLevel,
									   levelScales);
		
		for(int i = numLevels-1; i >= 0; i--)
		{
			std::cout << "Level " << i << " has " << imageNetwork->getNetworkLevel(i)->numNodes << " nodes\n"; 
		}
		registerImagesObj = new RegisterImages();
		// Identify transformations...
		registerImagesObj->registerImageNetwork(imagePyramid,
											imageNetwork, 
											distanceMeasure,
											searchAlgor,
											searchArea,
											jhBins,
											numWalks,
											tmax,
											tdecrease,
											successful,
											unsuccessful,
											thresholdMeasure,
											numberIterations,
											networkDistanceThreshold,
											levelScales,
											networkUpdateWeights,
											distanceSteps,
											numberOfSteps,
											windowLevel,
											correctionStdDev,
											tilePercentageRangeThreshold,
												ptsOutput);
		
		
		/************************ Get Image Resolutions ***********************/
		double imgAXPixelRes = 0;
		double imgAYPixelRes = 0;
		double imgBXPixelRes = 0;
		double imgBYPixelRes = 0;
		
		double *trans1 = new double[6];
		reference->GetGeoTransform(trans1);	
		if(trans1[1] < 0)
		{
			trans1[1] = trans1[1]*(-1);
		}
		if(trans1[5] < 0)
		{
			trans1[5] = trans1[5]*(-1);
		}
		double *trans2 = new double[6];
		floating->GetGeoTransform(trans2);	
		if(trans2[1] < 0)
		{
			trans2[1] = trans2[1]*(-1);
		}
		if(trans2[5] < 0)
		{
			trans2[5] = trans2[5]*(-1);
		}
		
		imgAXPixelRes = trans1[1];
		imgAYPixelRes = trans1[5];
		imgBXPixelRes = trans2[1];
		imgBYPixelRes = trans2[5];
		if(trans1 != NULL)
		{
			delete trans1;
		}
		if(trans2 != NULL)
		{
			delete trans2;
		}
		/**********************************************************************/
		
		// Output Control Points..
		if(image2image)
		{
			strcpy(tmpFilePath, ptsOutput);
			strcat(tmpFilePath, "_image2image.pts");
			imageNetwork->exportENVIControlPointsImage2Image(0, tmpFilePath);
			strcpy(tmpFilePath, ptsOutput);
			strcat(tmpFilePath, "networkOutput.txt");
			imageNetwork->exportNetworkAsText(0,tmpFilePath);
		}
		if(image2imageScaled)
		{
			double xScale = imgAXPixelRes / imgBXPixelRes;
			double yScale = imgAYPixelRes / imgBYPixelRes;
			strcpy(tmpFilePath, ptsOutput);
			strcat(tmpFilePath, "_image2image_scaled.pts");
			imageNetwork->exportENVIControlPointsImage2ImageScaled(0, tmpFilePath, xScale, yScale);
		}
		if(map2image)
		{
			strcpy(tmpFilePath, ptsOutput);
			strcat(tmpFilePath, "_map2image.pts");
			imageNetwork->exportENVIControlPointsMap2Image(0, tmpFilePath);
		}
		if(map2imageScaled)
		{
			double xScale = imgAXPixelRes / imgBXPixelRes;
			double yScale = imgAYPixelRes / imgBYPixelRes;
			strcpy(tmpFilePath, ptsOutput);
			strcat(tmpFilePath, "_map2image_scaled.pts");
			imageNetwork->exportENVIControlPointsMap2ImageScaled(0, tmpFilePath, xScale, yScale);
		}
	}
	catch(ImageRegistrationException e)
	{
		std::cout << "Caught ImageRegistration Exception freeing memory and throwing again\n";
		if(imagePyramid != NULL)
		{
			delete imagePyramid;
		}
		if(imageNetwork != NULL)
		{
			delete imageNetwork;
		}
		if(registerImagesObj != NULL)
		{
			delete registerImagesObj;
		}
		throw e;
	}
	if(imagePyramid != NULL)
	{
		delete imagePyramid;
	}
	if(imageNetwork != NULL)
	{
		delete imageNetwork;
	}
	if(registerImagesObj != NULL)
	{
		delete registerImagesObj;
	}
}

void ImagesUtil::findSimilarityStrip(int *origin, 
									 int refband,
									 int floatband,
									 int axis, 
									 int length, 
									 int windowSize, 
									 int measure, 
									 int bins,
									 const char *outputFile)
	throw(ImageRegistrationException)
{
	RegisterImages *registerImagesObj = NULL;
	ImageOverlap *imgOverlap = NULL;
	registerImagesObj = new RegisterImages();
	imgOverlap = new ImageOverlap(reference, floating);
	double xShift = 0;
	double yShift = 0;
	
	int stripLength = (length*2) +1;
	double *measureValues = NULL;
	measureValues = new double[stripLength];	
	int counter = 0;
	for( int i = (length*(-1)); i <= length; i++)
	{
		if(axis == 0)
		{
			xShift = i;
			yShift = 0;
		}
		else
		{
			xShift = 0;
			yShift = i;
		}
		measureValues[counter++] = registerImagesObj->findWindowMeasureWithOrigin(reference,
																	  floating,
																	  origin, 
																	  refband,
																	  floatband,
																	  windowSize, 
																	  measure, 
																	  bins,
																	  xShift,
																	  yShift,
																	  imgOverlap);
		std::cout << i;
		if(length != i)
		{
			std::cout << ",";
		}
		else
		{
			std::cout << std::endl;
		}
	}
	
	for(int i = 0; i < stripLength; i++)
	{
		std::cout << measureValues[i];
		if(i != (stripLength-1))
		{
			std::cout << ",";
		}
		else
		{
			std::cout << std::endl;
		}
	}
	
}

ImagesUtil::~ImagesUtil() throw()
{
	if(floating != NULL)
	{
		delete floating;
	}
	if( reference != NULL )
	{
		delete reference;
	}
}


