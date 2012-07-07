/*
 *  JointHistogram.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 05/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "JointHistogram.h"


JointHistogram::JointHistogram()
{
	// Default Constructor 
	// Sets number of Bins to a default 100;
	this->numberbins = 100;
}

JointHistogram::JointHistogram(int numBins)
{
	this->numberbins = numBins;
}

JointHistogram::JointHistogram(GDALDataset *ref, 
							   GDALDataset *floating, 
							   int refBand, 
							   int floatBand, 
							   int numBins, 
							   ImageOverlap *imgOverlap)
throw(ImageNotAvailableException, ImageProcessingException)
{
	this->numberbins = numBins;
	try
	{
		this->generateJointHistogram(ref,floating,refBand,floatBand, imgOverlap);
	}
	catch(ImageNotAvailableException e)
	{
		throw e;
	}
	catch(ImageProcessingException e)
	{
		throw e;
	}
}

bool JointHistogram::generateJointHistogram(GDALDataset *ref, 
											GDALDataset *floating, 
											int refBand, 
											int floatBand, 
											ImageOverlap *imgOverlap)
	throw(ImageNotAvailableException, ImageProcessingException)
{
	/******************** Check inputs are correct ****************/
	if(ref == NULL)
	{
		throw ImageNotAvailableException("Reference Image was NULL.", 
										 error_codes::reference_image);
	}
	else if(floating == NULL)
	{
		throw ImageNotAvailableException("Floating Image was NULL.", 
										 error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Datasets are not null.\n";
	}
	
	if(imgOverlap == NULL)
	{
		throw ImageProcessingException("Image Overlap is NULL.", 
									   error_codes::no_image_overlap, 0);
	}
	else
	{
		//std::cout << "OK: Got overlapping areas.\n";
	}
	
	if(refBand > ref->GetRasterCount())
	{
		throw ImageProcessingException("Not enough bands in reference image", 
									   error_codes::insufficent_num_bands, 
									   error_codes::reference_image);
	}
	else
	{
		//std::cout << "OK: Sufficient bands in reference image.\n";
	}
	
	if(floatBand > floating->GetRasterCount())
	{
		throw ImageProcessingException("Not enough bands in floating image", 
									   error_codes::insufficent_num_bands, 
									   error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Sufficient bands in floating image.\n";
	}
	
	/**********************************************************************/
	
	/******* Retrieve overlapping areas and setup local variables *********/
	int *refImagePixels;
	int *floatImagePixels;
	double *geoCorners;
	refImagePixels = imgOverlap->getImageAPixelCoords();
	floatImagePixels = imgOverlap->getImageBPixelCoords();
	geoCorners = imgOverlap->getOverlapGeoCoords();
	/*****************************************************************/
	
	/***************** Test: Print overlapping areas: *********************
	std::cout << "Image A Pixels: (" << refImagePixels[0] << "," 
		<< refImagePixels[1] << ") ("
		<< refImagePixels[2] << "," << refImagePixels[3] << ")\n";
	std::cout << "Image B Pixels: (" << floatImagePixels[0] << "," 
		<< floatImagePixels[1] << ") ("
		<< floatImagePixels[2] << "," << floatImagePixels[3] << ")\n";
	std::cout << "Geo Coords of Overlap: (" << geoCorners[0] << "," 
		<< geoCorners[1] << ") ("
		<< geoCorners[2] << "," << geoCorners[3] << ")\n";
	/**********************************************************************/
		
	/************************ Set up data variables ****************/
	int imageASizeX = imgOverlap->getSizeXPixelsA();
	int imageASizeY = imgOverlap->getSizeYPixelsA();
	int imageBSizeX = imgOverlap->getSizeXPixelsB();
	int imageBSizeY = imgOverlap->getSizeYPixelsB();
	
	if(imageBSizeX <= 0 | imageBSizeY <= 0)
	{
		frequency = NULL;
		return false;
	}
	
	float *refScanline;
	float *floatScanline;
	
	refScanline = (float *) CPLMalloc(sizeof(float)*imageASizeX);
	floatScanline = (float *) CPLMalloc(sizeof(float)*imageASizeX);
	
	GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
	GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
	
	refMax = 0;
	refMin = 0;
	floatMax = 0;
	floatMin = 0;
	/***************************************************************/
	
	/********** Find Max and Min Values for both images ************/
	for(int i=0; i < imageASizeY; i++)
	{
		// Get data
		refRasterband->RasterIO(GF_Read, 
								refImagePixels[0], 
								(refImagePixels[1]+i), 
								imageASizeX, 
								1, 
								refScanline, 
								imageASizeX, 
								1, 
								GDT_Float32, 
								0, 
								0);
		
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+i), 
								  imageASizeX, 
								  1, 
								  floatScanline, 
								  imageASizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		
		for(int j=0; j<imageASizeX; j++)
		{
			// Set Initial values
			if(i == 0 & j == 0)
			{
				refMax = refMin = refScanline[0];
				floatMax = floatMin = floatScanline[0];
			}
			// Reference Image
			if(refScanline[j] > refMax)
			{
				refMax = refScanline[j];
			}
			else if(refScanline[j] < refMin)
			{
				refMin = refScanline[j];
			}
			// Floating Image
			if(floatScanline[j] > floatMax)
			{
				floatMax = floatScanline[j];
			}
			else if(floatScanline[j] < floatMin)
			{
				floatMin = floatScanline[j];
			}
		}
	}
	/***************************************************************/
	
	/******** TEST: Print out MIN and MAX values for both images **********
	
	std::cout << "refMax: " << refMax << std::endl;
	std::cout << "refMin: " << refMin << std::endl;
	std::cout << "floatMax: " << floatMax << std::endl;
	std::cout << "floatMin: " << floatMin << std::endl;
	
	**********************************************************************/
	
	double *refRanges;
	double *floatRanges;
	
	/********* Identify Bin Ranges for reference and floating image ************/
	// Reference Image
	refRanges = new double[this->numberbins + 1];
	double refDifference = (refMax - refMin) / numberbins;
	refRanges[0] = refMin;
	for(int i = 1; i < numberbins; i++)
	{
		refRanges[i] = refRanges[i-1] + refDifference;
	}
	refRanges[numberbins] = refMax;
	// Floating Image
	floatRanges = new double[this->numberbins + 1];
	double floatDifference = (floatMax - floatMin) / numberbins;
	floatRanges[0] = floatMin;
	for(int i = 1; i < numberbins; i++)
	{
		floatRanges[i] = floatRanges[i-1] + floatDifference;
	}
	floatRanges[numberbins] = floatMax;
	/****************************************************************************/
	
	/************ TEST: Print out ranges **************************************
	
	for(int i = 0; i < numberbins; i++)
	{
		std::cout << i << ": " << refRanges[i] << " - " << refRanges[i+1] << std::endl;
	}
	
	for(int i = 0; i < numberbins; i++)
	{
		std::cout << i << ": " << floatRanges[i] << " - " << floatRanges[i+1] << std::endl;
	}
	
	*************************************************************************/
	
	/*********************** Populate join Histogram ***************************/
	int refIndex = 0;
	int floatIndex = 0;
	
	int **tmpfrequency = NULL;
	tmpfrequency = new int* [numberbins];
	for(int i = 0; i < numberbins; i++)
	{
		tmpfrequency[i] = new int[numberbins];
		for(int j = 0; j < numberbins; j++)
		{
			tmpfrequency[i][j] = 0;
		}
	}
	
	for(int i=0; i < imageASizeY; i++)
	{
		// Get data
		refRasterband->RasterIO(GF_Read, 
								refImagePixels[0], 
								(refImagePixels[1]+i), 
								imageASizeX, 
								1, 
								refScanline, 
								imageASizeX, 
								1, 
								GDT_Float32, 
								0, 
								0);
		
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+i), 
								  imageASizeX, 
								  1, 
								  floatScanline, 
								  imageASizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		
		for(int j=0; j<imageASizeX; j++)
		{
			refIndex = 0;
			floatIndex = 0;
			// Find index for reference Image.
			for(int k = 0; k < numberbins; k++)
			{
				if(refScanline[j] >= refRanges[k] & refScanline[j] <= refRanges[k+1])
				{
					refIndex = k;
					break;
				}
			}
			for(int k = 0; k < numberbins; k++)
			{
				if(floatScanline[j] >= floatRanges[k] & floatScanline[j] <= floatRanges[k+1])
				{
					floatIndex = k;
					break;
				}
			}
			/*if(refIndex != floatIndex)
			{
				std::cout << "refIndex and floatIndex not the same! refIdex: " << refIndex 
				          << " floatIndex: " << floatIndex 
				          << " ref: "  << refScanline[j] 
				          << " floating: " << floatScanline[j]
						  << std::endl;
			}*/
			//std::cout << "Incrementing frequency[" << refIndex << "][" << floatIndex << "]\n";
			tmpfrequency[refIndex][floatIndex]++;
		}
	}
	/***************************************************************************/
	
	/**************** Put Result into frequency attribute ******************/
	
	int jointHistLength = numberbins*numberbins;
	frequency = new double[jointHistLength];
	 int counter = 0;
	 for(int n = 0; n < numberbins; n++)
	 {
		 for(int m = 0; m < numberbins; m++)
		 {
			 frequency[counter++] = tmpfrequency[n][m];
		 }
	 }
	 /*************************************************************************/
	 
	 /**************** TEST: print out join histogram ******************
	 for(int i = 0; i < jointHistLength; i++)
	 {
		 std::cout << frequency[i] << ", ";
		 if(i % numberbins == 0)
		 {
			 std::cout << std::endl;
		 }
	 }
	 std::cout << std::endl;
	 *************************************************************************/
	 
	 //Free Memory
	 if(tmpfrequency != NULL)
	 {
		 for(int i = 0; i < numberbins; i++)
		 {
			 delete tmpfrequency[i];
		 }
		 delete tmpfrequency;
		 //std::cout << "delete tmpfrequency;\n";
	 }
	 
	 if( refRasterband != NULL )
	 {
		 refRasterband->FlushCache();
		 //std::cout << "refRasterband->FlushCache();\n";
	 }
	 
	 if( floatRasterband != NULL )
	 {
		 floatRasterband->FlushCache();
		 //std::cout << "floatRasterband->FlushCache();\n";
	 }
	 
	 if( refScanline != NULL )
	 {
		 CPLFree(refScanline);
		 //std::cout << "CPLFree(refScanline);\n";
	 }
	 
	 if ( floatScanline != NULL )
	 {
		 CPLFree(floatScanline);
		 //std::cout << "CPLFree(floatScanline);\n";
	 }
	 
	 if( refRanges != NULL )
	 {
		 delete refRanges;
	 }
	 
	 if ( floatRanges != NULL )
	 {
		 delete floatRanges;
	 }
	 
	 return true;
}

bool JointHistogram::generateSubPixelJointHistogram(GDALDataset *ref, 
													GDALDataset *floating, 
													int refBand, 
													int floatBand, 
													ImageOverlap *imgOverlap,
													double xShift,
													double yShift)
throw(ImageNotAvailableException, ImageProcessingException)
{	
	MathUtils *mathUtils = NULL;
	mathUtils = new MathUtils;
	Interpolation *interpolation = NULL;
	interpolation = new Interpolation;
	/******************** Check inputs are correct ****************/
	if(ref == NULL)
	{
		throw ImageNotAvailableException("Reference Image was NULL.", 
										 error_codes::reference_image);
	}
	else if(floating == NULL)
	{
		throw ImageNotAvailableException("Floating Image was NULL.", 
										 error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Datasets are not null.\n";
	}
	
	if(imgOverlap == NULL)
	{
		throw ImageProcessingException("Image Overlap is NULL.", 
									   error_codes::no_image_overlap, 0);
	}
	else
	{
		//std::cout << "OK: Got overlapping areas.\n";
	}
	
	if(refBand > ref->GetRasterCount())
	{
		throw ImageProcessingException("Not enough bands in reference image", 
									   error_codes::insufficent_num_bands, 
									   error_codes::reference_image);
	}
	else
	{
		//std::cout << "OK: Sufficient bands in reference image.\n";
	}
	
	if(floatBand > floating->GetRasterCount())
	{
		throw ImageProcessingException("Not enough bands in floating image", 
									   error_codes::insufficent_num_bands, 
									   error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Sufficient bands in floating image.\n";
	}
	
	/**********************************************************************/
	
	/******* Retrieve overlapping areas and setup local variables *********/
	int *refImagePixels;
	int *floatImagePixels;
	double *geoCorners;
	refImagePixels = imgOverlap->getImageAPixelCoords();
	floatImagePixels = imgOverlap->getImageBPixelCoords();
	geoCorners = imgOverlap->getOverlapGeoCoords();
	/*****************************************************************/
	
	/***************** Test: Print overlapping areas: *********************
	std::cout << "ShiftX = " << xShift << " ShiftY = " << yShift << std::endl;
	std::cout << "Image A Pixels: (" << refImagePixels[0] << "," 
		<< refImagePixels[1] << ") ("
		<< refImagePixels[2] << "," << refImagePixels[3] << ")\n";
	std::cout << "Image B Pixels: (" << floatImagePixels[0] << "," 
		<< floatImagePixels[1] << ") ("
		<< floatImagePixels[2] << "," << floatImagePixels[3] << ")\n";
	std::cout << "Geo Coords of Overlap: (" << geoCorners[0] << "," 
		<< geoCorners[1] << ") ("
		<< geoCorners[2] << "," << geoCorners[3] << ")\n";
	/**********************************************************************/
	
	/************************ Set up data variables ****************/
	// Find floating component z of w.z
	double xShiftz = 0;
	double yShiftz = 0;
	int b4floatingpoint = 0; // Not used just to compile with interface
	xShiftz = mathUtils->findFloatingPointComponent(xShift, &b4floatingpoint);
	yShiftz = mathUtils->findFloatingPointComponent(yShift, &b4floatingpoint);
	
	// If no floating point to shift use non shift funcation.
	if(xShiftz == 0 & yShiftz == 0)
	{
		return this->generateJointHistogram(ref, floating, refBand, floatBand, imgOverlap);
	}
	else
	{
		// There is a floating point shift use this funcation..
	}
	
	// Negative or Positive Shift.
	int xShiftDirection = 0;
	int yShiftDirection = 0;
	
	if( xShift > 0 )
	{
		xShiftDirection = PosShift;
	}
	else
	{
		xShiftDirection = NegShift;
	}
	
	if( yShift > 0 )
	{
		yShiftDirection = PosShift;
	}
	else
	{
		yShiftDirection = NegShift;
	}
	
	// Calculate Floating Point increment per interation
	double xfloatingShift = 0;
	if( xShiftDirection == PosShift | xShiftz == 0 )
	{
		xfloatingShift = xShiftz;
	}
	else if( xShiftDirection == NegShift & xShiftz != 0 )
	{
		xfloatingShift = 1 - xShiftz;
	}
	else
	{
		//nothing!
	}
	double yfloatingShift = 0;
	if( yShiftDirection == PosShift | yShiftz == 0  )
	{
		yfloatingShift = yShiftz;
	}
	else if( yShiftDirection == NegShift & yShiftz != 0)
	{
		yfloatingShift = 1 - yShiftz;
	}
	else
	{
		//nothing!
	}
	
	// Image Size.
	int imageASizeX = imgOverlap->getSizeXPixelsA();
	int imageASizeY = imgOverlap->getSizeYPixelsA();
	int imageBSizeX = imgOverlap->getSizeXPixelsB();
	int imageBSizeY = imgOverlap->getSizeYPixelsB();
	
	if(imageBSizeX <= 0 | imageBSizeY <= 0)
	{
		frequency = NULL;
		return false;
	}
	
	// Image Data Stores.
	float *refScanline1;
	float *floatScanline1;
	float *floatScanline2;
	
	refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
	floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	floatScanline2 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	
	GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
	GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
	
	// Max and Min Areas
	refMax = 0;
	refMin = 0;
	floatMax = 0;
	floatMin = 0;
	
	// Pixel Values for Calculations.
	double referencePixel = 0;
	double floatingPixel = 0;
	double pixels[4];
	/***************************************************************/
	
	/******************* TEST: Print Shifts ***********************
	std::cout << "JH xShift = " << xShift << std::endl;
	std::cout << "JH yShift = " << yShift << std::endl;
	std::cout << "xShiftz = " << xShiftz << std::endl;
	std::cout << "yShiftz = " << yShiftz << std::endl;
	std::cout << "xfloatingShift = " << xfloatingShift << std::endl;
	std::cout << "yfloatingShift = " << yfloatingShift << std::endl;
	/**************************************************************/
	
	/********** Find Max and Min Values for both images ************/
	for(int i=0; i < (imageASizeY-1); i++)
	{
		//std::cout << "i = " << i << std::endl;
		// Get data
		refRasterband->RasterIO(GF_Read, 
								refImagePixels[0], 
								(refImagePixels[1]+i), 
								imageASizeX, 
								1, 
								refScanline1, 
								imageASizeX, 
								1, 
								GDT_Float32, 
								0, 
								0);
		//std::cout << "Read in Line from reference Image" << std::endl;
		floatRasterband->RasterIO(GF_Read, 
								   floatImagePixels[0], 
								   (floatImagePixels[1]+i), 
								   imageBSizeX, 
								   1, 
								   floatScanline1, 
								   imageBSizeX, 
								   1, 
								   GDT_Float32, 
								   0, 
								   0);
		//std::cout << "Read in Line from floating Image" << std::endl;
		
		floatRasterband->RasterIO(GF_Read, 
									floatImagePixels[0], 
									(floatImagePixels[1]+(i+1)), 
									imageBSizeX, 
									1, 
									floatScanline2, 
									imageBSizeX, 
									1, 
									GDT_Float32, 
									0, 
									0);
		//std::cout << "Read in extra Line from floating Image" << std::endl;
		
		for(int j=0; j<(imageASizeX-1); j++)
		{
			referencePixel = refScanline1[j];
			pixels[0] = floatScanline1[j];
			pixels[1] = floatScanline1[j+1];
			pixels[2] = floatScanline2[j];
			pixels[3] = floatScanline2[j+1];
			floatingPixel = interpolation->bilinear(xfloatingShift, 
												   yfloatingShift, 
												   pixels);
			
			// Set Initial values
			if(i == 0 & j == 0)
			{
				refMax = refMin = referencePixel;
				floatMax = floatMin = floatingPixel;
			}
			// Reference Image
			if(referencePixel > refMax)
			{
				refMax = referencePixel;
			}
			else if(referencePixel < refMin)
			{
				refMin = referencePixel;
			}
			// Floating Image
			if(floatingPixel > floatMax)
			{
				floatMax = floatingPixel;
			}
			else if(floatingPixel < floatMin)
			{
				floatMin = floatingPixel;
			}
		}
	}
	/***************************************************************/
	
	/******** TEST: Print out MIN and MAX values for both images **********
	std::cout << "refMax: " << refMax << std::endl;
	std::cout << "refMin: " << refMin << std::endl;
	std::cout << "floatMax: " << floatMax << std::endl;
	std::cout << "floatMin: " << floatMin << std::endl;
	**********************************************************************/
	
	double *refRanges;
	double *floatRanges;
	
	/********* Identify Bin Ranges for reference and floating image ************/
	// Reference Image
	refRanges = new double[this->numberbins + 1];
	double refDifference = (refMax - refMin) / numberbins;
	refRanges[0] = refMin;
	for(int i = 1; i < numberbins; i++)
	{
		refRanges[i] = refRanges[i-1] + refDifference;
	}
	refRanges[numberbins] = refMax;
	// Floating Image
	floatRanges = new double[this->numberbins + 1];
	double floatDifference = (floatMax - floatMin) / numberbins;
	floatRanges[0] = floatMin;
	for(int i = 1; i < numberbins; i++)
	{
		floatRanges[i] = floatRanges[i-1] + floatDifference;
	}
	floatRanges[numberbins] = floatMax;
	/****************************************************************************/
	
	/************ TEST: Print out ranges **************************************
	for(int i = 0; i < numberbins; i++)
	{
		std::cout << i << ": " << refRanges[i] << " - " << refRanges[i+1] << std::endl;
	}
	
	for(int i = 0; i < numberbins; i++)
	{
		std::cout << i << ": " << floatRanges[i] << " - " << floatRanges[i+1] << std::endl;
	}
	*************************************************************************/
	
	/*********************** Populate join Histogram ***************************/
	int refIndex = 0;
	int floatIndex = 0;
	
	int **tmpfrequency = NULL;
	tmpfrequency = new int* [numberbins];
	for(int i = 0; i < numberbins; i++)
	{
		tmpfrequency[i] = new int[numberbins];
		for(int j = 0; j < numberbins; j++)
		{
			tmpfrequency[i][j] = 0;
		}
	}
	
	for(int i=0; i < (imageASizeY-1); i++)
	{
		// Get data
		refRasterband->RasterIO(GF_Read, 
								refImagePixels[0], 
								(refImagePixels[1]+i), 
								imageASizeX, 
								1, 
								refScanline1, 
								imageASizeX, 
								1, 
								GDT_Float32, 
								0, 
								0);
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+i), 
								  imageBSizeX, 
								  1, 
								  floatScanline1, 
								  imageBSizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		

			floatRasterband->RasterIO(GF_Read, 
									  floatImagePixels[0], 
									  (floatImagePixels[1]+(i+1)), 
									  imageBSizeX, 
									  1, 
									  floatScanline2, 
									  imageBSizeX, 
									  1, 
									  GDT_Float32, 
									  0, 
									  0);

		for(int j=0; j<imageASizeX-1; j++)
		{
			referencePixel = refScanline1[j];
			pixels[0] = floatScanline1[j];
			pixels[1] = floatScanline1[j+1];
			pixels[2] = floatScanline2[j];
			pixels[3] = floatScanline2[j+1];
			
			floatingPixel = interpolation->bilinear(xfloatingShift, 
												   yfloatingShift, 
												   pixels);
			
			refIndex = 0;
			floatIndex = 0;
			// Find index for reference Image.
			for(int k = 0; k < numberbins; k++)
			{
				if(referencePixel >= refRanges[k] & referencePixel <= refRanges[k+1])
				{
					refIndex = k;
					break;
				}
			}
			for(int k = 0; k < numberbins; k++)
			{
				if(floatingPixel >= floatRanges[k] & floatingPixel <= floatRanges[k+1])
				{
					floatIndex = k;
					break;
				}
			}
			/*if(refIndex != floatIndex)
			{
				std::cout << "refIndex and floatIndex not the same! refIdex: " << refIndex 
				<< " floatIndex: " << floatIndex 
				<< " ref: "  << refScanline[j] 
				<< " floating: " << floatScanline[j]
				<< std::endl;
			}*/
			//std::cout << "Incrementing frequency[" << refIndex << "][" << floatIndex << "]\n";
			tmpfrequency[refIndex][floatIndex]++;
		}
	}
	/***************************************************************************/
	
	/**************** Put Result into frequency attribute ******************/
	
	int jointHistLength = numberbins*numberbins;
	frequency = new double[jointHistLength];
	int counter = 0;
	for(int n = 0; n < numberbins; n++)
	{
		for(int m = 0; m < numberbins; m++)
		{
			frequency[counter++] = tmpfrequency[n][m];
		}
	}
	/*************************************************************************/
	
	/**************** TEST: print out join histogram ******************
		for(int i = 0; i < jointHistLength; i++)
	{
			std::cout << frequency[i] << ", ";
			if(i % numberbins == 0)
			{
				std::cout << std::endl;
			}
	}
	std::cout << std::endl;
	*************************************************************************/
	
	//Free Memory
	if(tmpfrequency != NULL)
	{
		for(int i = 0; i < numberbins; i++)
		{
			delete tmpfrequency[i];
		}
		delete tmpfrequency;
	}
	if( refScanline1 != NULL )
	{
		CPLFree(refScanline1);
	}
	
	if ( floatScanline1 != NULL )
	{
		CPLFree(floatScanline1);
	}
	
	if ( floatScanline2 != NULL )
	{
		CPLFree(floatScanline2);
	}
	
	if( refRanges != NULL )
	{
		delete refRanges;
	}
	
	if ( floatRanges != NULL )
	{
		delete floatRanges;
	}
	
	return true;
}

bool JointHistogram::generateSubPixelJointHistogramWithInterp(GDALDataset *ref, 
															  GDALDataset *floating, 
															  int refBand, 
															  int floatBand, 
															  ImageOverlap *imgOverlap,
															  double xShift,
															  double yShift)
throw(ImageNotAvailableException, ImageProcessingException)
{	
	MathUtils *mathUtils = NULL;
	mathUtils = new MathUtils;
	
	/******************** Check inputs are correct ****************/
	if(ref == NULL)
	{
		throw ImageNotAvailableException("Reference Image was NULL.", 
										 error_codes::reference_image);
	}
	else if(floating == NULL)
	{
		throw ImageNotAvailableException("Floating Image was NULL.", 
										 error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Datasets are not null.\n";
	}
	
	if(imgOverlap == NULL)
	{
		throw ImageProcessingException("Image Overlap is NULL.", 
									   error_codes::no_image_overlap, 0);
	}
	else
	{
		//std::cout << "OK: Got overlapping areas.\n";
	}
	
	if(refBand > ref->GetRasterCount())
	{
		throw ImageProcessingException("Not enough bands in reference image", 
									   error_codes::insufficent_num_bands, 
									   error_codes::reference_image);
	}
	else
	{
		//std::cout << "OK: Sufficient bands in reference image.\n";
	}
	
	if(floatBand > floating->GetRasterCount())
	{
		throw ImageProcessingException("Not enough bands in floating image", 
									   error_codes::insufficent_num_bands, 
									   error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Sufficient bands in floating image.\n";
	}
	
	/**********************************************************************/
	
	/******* Retrieve overlapping areas and setup local variables *********/
	int *refImagePixels;
	int *floatImagePixels;
	double *geoCorners;
	refImagePixels = imgOverlap->getImageAPixelCoords();
	floatImagePixels = imgOverlap->getImageBPixelCoords();
	geoCorners = imgOverlap->getOverlapGeoCoords();
	/*****************************************************************/
	
	/***************** Test: Print overlapping areas: *********************
		std::cout << "ShiftX = " << xShift << " ShiftY = " << yShift << std::endl;
	std::cout << "Image A Pixels: (" << refImagePixels[0] << "," 
		<< refImagePixels[1] << ") ("
		<< refImagePixels[2] << "," << refImagePixels[3] << ")\n";
	std::cout << "Image B Pixels: (" << floatImagePixels[0] << "," 
		<< floatImagePixels[1] << ") ("
		<< floatImagePixels[2] << "," << floatImagePixels[3] << ")\n";
	std::cout << "Geo Coords of Overlap: (" << geoCorners[0] << "," 
		<< geoCorners[1] << ") ("
		<< geoCorners[2] << "," << geoCorners[3] << ")\n";
	/**********************************************************************/
	
	/************************ Set up data variables ****************/
	// Find floating component z of w.z
	double xShiftz = 0;
	double yShiftz = 0;
	int b4floatingpoint = 0; // Not used just to compile with interface
	xShiftz = mathUtils->findFloatingPointComponent(xShift, &b4floatingpoint);
	yShiftz = mathUtils->findFloatingPointComponent(yShift, &b4floatingpoint);
	
	// If no floating point to shift use non shift funcation.
	if(xShiftz == 0 & yShiftz == 0)
	{
		return this->generateJointHistogram(ref, floating, refBand, floatBand, imgOverlap);
	}
	else
	{
		// There is a floating point shift use this funcation..
	}
	
	// Negative or Positive Shift.
	int xShiftDirection = 0;
	int yShiftDirection = 0;
	
	if( xShift > 0 )
	{
		xShiftDirection = PosShift;
	}
	else
	{
		xShiftDirection = NegShift;
	}
	
	if( yShift > 0 )
	{
		yShiftDirection = PosShift;
	}
	else
	{
		yShiftDirection = NegShift;
	}
	
	// Calculate Floating Point increment per interation
	double xfloatingShift = 0;
	if( xShiftDirection == PosShift | xShiftz == 0 )
	{
		xfloatingShift = xShiftz;
	}
	else if( xShiftDirection == NegShift & xShiftz != 0 )
	{
		xfloatingShift = 1 - xShiftz;
	}
	else
	{
		//nothing!
	}
	double yfloatingShift = 0;
	if( yShiftDirection == PosShift | yShiftz == 0  )
	{
		yfloatingShift = yShiftz;
	}
	else if( yShiftDirection == NegShift & yShiftz != 0)
	{
		yfloatingShift = 1 - yShiftz;
	}
	else
	{
		//nothing!
	}
	
	// Image Size.
	int imageASizeX = imgOverlap->getSizeXPixelsA();
	int imageASizeY = imgOverlap->getSizeYPixelsA();
	int imageBSizeX = imgOverlap->getSizeXPixelsB();
	int imageBSizeY = imgOverlap->getSizeYPixelsB();
	
	if(imageBSizeX <= 0 | imageBSizeY <= 0)
	{
		frequency = NULL;
		return false;
	}
	//std::cout << "imageASizeX = " << imageASizeX << " imageBAizeY = " << imageASizeY << std::endl;
	//std::cout << "imageBSizeX = " << imageBSizeX << " imageBSizeY = " << imageBSizeY << std::endl;
	
	// Image Data Stores.
	float *refScanline1;
	float *floatScanline1;
	float *floatScanline2;
	
	refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
	floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	floatScanline2 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	
	GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
	GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
	
	// Max and Min Areas
	refMax = 0;
	refMin = 0;
	floatMax = 0;
	floatMin = 0;
	
	// Pixel Values for Calculations.
	double referencePixel = 0;
	double floatingPixel = 0;
	double pixels[4];
	/***************************************************************/
	
	/******************* TEST: Print Shifts ***********************
		std::cout << "JH xShift = " << xShift << std::endl;
	std::cout << "JH yShift = " << yShift << std::endl;
	std::cout << "xShiftz = " << xShiftz << std::endl;
	std::cout << "yShiftz = " << yShiftz << std::endl;
	std::cout << "xfloatingShift = " << xfloatingShift << std::endl;
	std::cout << "yfloatingShift = " << yfloatingShift << std::endl;
	/**************************************************************/
	
	/********** Find Max and Min Values for both images ************/
	for(int i=0; i < (imageASizeY-1); i++)
	{
		//std::cout << "i = " << i << std::endl;
		// Get data
		refRasterband->RasterIO(GF_Read, 
								refImagePixels[0], 
								(refImagePixels[1]+i), 
								imageASizeX, 
								1, 
								refScanline1, 
								imageASizeX, 
								1, 
								GDT_Float32, 
								0, 
								0);
		//std::cout << "Read in Line from reference Image" << std::endl;
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+i), 
								  imageBSizeX, 
								  1, 
								  floatScanline1, 
								  imageBSizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		//std::cout << "Read in Line from floating Image" << std::endl;
		
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+(i+1)), 
								  imageBSizeX, 
								  1, 
								  floatScanline2, 
								  imageBSizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		//std::cout << "Read in extra Line from floating Image" << std::endl;
		
		for(int j=0; j<(imageASizeX-1); j++)
		{
			referencePixel = refScanline1[j];
			floatingPixel = floatScanline1[j];
			
			// Set Initial values
			if(i == 0 & j == 0)
			{
				refMax = refMin = referencePixel;
				floatMax = floatMin = floatingPixel;
			}
			// Reference Image
			if(referencePixel > refMax)
			{
				refMax = referencePixel;
			}
			else if(referencePixel < refMin)
			{
				refMin = referencePixel;
			}
			// Floating Image
			if(floatingPixel > floatMax)
			{
				floatMax = floatingPixel;
			}
			else if(floatingPixel < floatMin)
			{
				floatMin = floatingPixel;
			}
		}
		//std::cout << "Processed Line\n";
	}
	/***************************************************************/
	
	/******** TEST: Print out MIN and MAX values for both images **********
		std::cout << "refMax: " << refMax << std::endl;
	std::cout << "refMin: " << refMin << std::endl;
	std::cout << "floatMax: " << floatMax << std::endl;
	std::cout << "floatMin: " << floatMin << std::endl;
	**********************************************************************/
	
	double *refRanges;
	double *floatRanges;
	
	/********* Identify Bin Ranges for reference and floating image ************/
	// Reference Image
	refRanges = new double[this->numberbins + 1];
	double refDifference = (refMax - refMin) / numberbins;
	refRanges[0] = refMin;
	for(int i = 1; i < numberbins; i++)
	{
		refRanges[i] = refRanges[i-1] + refDifference;
	}
	refRanges[numberbins] = refMax;
	// Floating Image
	floatRanges = new double[this->numberbins + 1];
	double floatDifference = (floatMax - floatMin) / numberbins;
	floatRanges[0] = floatMin;
	for(int i = 1; i < numberbins; i++)
	{
		floatRanges[i] = floatRanges[i-1] + floatDifference;
	}
	floatRanges[numberbins] = floatMax;
	/****************************************************************************/
	
	/************ TEST: Print out ranges **************************************
		for(int i = 0; i < numberbins; i++)
	{
			std::cout << i << ": " << refRanges[i] << " - " << refRanges[i+1] << std::endl;
	}
	
	for(int i = 0; i < numberbins; i++)
	{
		std::cout << i << ": " << floatRanges[i] << " - " << floatRanges[i+1] << std::endl;
	}
	*************************************************************************/
	
	/*********************** Populate join Histogram ***************************/
	int refIndex = 0;
	int floatIndex = 0;
	
	double **tmpfrequency = NULL;
	tmpfrequency = new double* [numberbins];
	for(int i = 0; i < numberbins; i++)
	{
		tmpfrequency[i] = new double[numberbins];
		for(int j = 0; j < numberbins; j++)
		{
			tmpfrequency[i][j] = 0;
		}
	}
	
	for(int i=0; i < (imageASizeY-1); i++)
	{
		// Get data
		refRasterband->RasterIO(GF_Read, 
								refImagePixels[0], 
								(refImagePixels[1]+i), 
								imageASizeX, 
								1, 
								refScanline1, 
								imageASizeX, 
								1, 
								GDT_Float32, 
								0, 
								0);
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+i), 
								  imageBSizeX, 
								  1, 
								  floatScanline1, 
								  imageBSizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		
		
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+(i+1)), 
								  imageBSizeX, 
								  1, 
								  floatScanline2, 
								  imageBSizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		
		for(int j=0; j<imageASizeX; j++)
		{
			referencePixel = refScanline1[j];
			pixels[0] = floatScanline1[j];
			pixels[1] = floatScanline1[j+1];
			pixels[2] = floatScanline2[j];
			pixels[3] = floatScanline2[j+1];
			
			refIndex = 0;
			floatIndex = 0;
			// Find index for reference Image.
			for(int k = 0; k < numberbins; k++)
			{
				if(referencePixel >= refRanges[k] & referencePixel <= refRanges[k+1])
				{
					refIndex = k;
					break;
				}
			}
			for(int k = 0; k < numberbins; k++)
			{
				if(pixels[0] >= floatRanges[k] & pixels[0] <= floatRanges[k+1])
				{
					floatIndex = k;
					tmpfrequency[refIndex][floatIndex] += ((1-xfloatingShift) * (1-yfloatingShift));
					break;
				}
			}
			for(int k = 0; k < numberbins; k++)
			{
				if(pixels[1] >= floatRanges[k] & pixels[1] <= floatRanges[k+1])
				{
					floatIndex = k;
					tmpfrequency[refIndex][floatIndex] += (xfloatingShift * (1-yfloatingShift));
					break;
				}
			}
			for(int k = 0; k < numberbins; k++)
			{
				if(pixels[2] >= floatRanges[k] & pixels[2] <= floatRanges[k+1])
				{
					floatIndex = k;
					tmpfrequency[refIndex][floatIndex] += ((1-xfloatingShift) * yfloatingShift);
					break;
				}
			}
			for(int k = 0; k < numberbins; k++)
			{
				if(pixels[3] >= floatRanges[k] & pixels[3] <= floatRanges[k+1])
				{
					floatIndex = k;
					tmpfrequency[refIndex][floatIndex] += (xfloatingShift * yfloatingShift);
					break;
				}
			}
		}
	}
	/***************************************************************************/
	
	/**************** Put Result into frequency attribute ******************/
	
	int jointHistLength = numberbins*numberbins;
	frequency = new double[jointHistLength];
	int counter = 0;
	for(int n = 0; n < numberbins; n++)
	{
		for(int m = 0; m < numberbins; m++)
		{
			frequency[counter++] = mathUtils->round(tmpfrequency[n][m]);
		}
	}
	/*************************************************************************/
	
	/**************** TEST: print out join histogram ******************
		for(int i = 0; i < jointHistLength; i++)
	{
			std::cout << frequency[i] << ", ";
			if(i % numberbins == 0)
			{
				std::cout << std::endl;
			}
	}
	std::cout << std::endl;
	*************************************************************************/
	
	//Free Memory
	if(tmpfrequency != NULL)
	{
		for(int i = 0; i < numberbins; i++)
		{
			delete tmpfrequency[i];
		}
		delete tmpfrequency;
	}
	if( refScanline1 != NULL )
	{
		CPLFree(refScanline1);
	}
	if ( floatScanline1 != NULL )
	{
		CPLFree(floatScanline1);
	}
	
	if ( floatScanline2 != NULL )
	{
		CPLFree(floatScanline2);
	}
	
	if( refRanges != NULL )
	{
		delete refRanges;
	}
	
	if ( floatRanges != NULL )
	{
		delete floatRanges;
	}
	return true;
}


double JointHistogram::getFloatingMax()
{
	return this->floatMax;
}

double JointHistogram::getFloatMin()
{
	return this->floatMin;
}

double JointHistogram::getReferenceMax()
{
	return this->refMax;
}

double JointHistogram::getReferenceMin()
{
	return this->refMin;
}

void JointHistogram::setNumberBins(int numBins)
{
	this->numberbins = numBins;
}

/**
 * Print out to console a text based version of the joint histogram.
 */
void JointHistogram::printTextJointHistogram()
{
	int jointHistLength = numberbins * numberbins;
	std::cout << frequency[0] << ", ";
	for(int i = 1; i < jointHistLength; i++)
	{
		std::cout << frequency[i] << ", ";
		if(i % numberbins == 0)
		{
			std::cout << std::endl;
		}
	}
	std::cout << std::endl;
}

void JointHistogram::exportAsImage(const char *filename, const char *format)
	throw(ImageOutputException)
{
	MathUtils *mathUtils = NULL;
	mathUtils = new MathUtils;
		
	GDALDriver *poDriver;
	char **papazMetadata;
	
	GDALAllRegister();
	
	poDriver = GetGDALDriverManager()->GetDriverByName(format);
	if(poDriver == NULL)
	{
		throw ImageOutputException("Driver no found.", error_codes::no_driver);
	}
	papazMetadata = poDriver->GetMetadata();
	if(CSLFetchBoolean(papazMetadata, GDAL_DCAP_CREATE, FALSE))
	{
		//std::cout << "Driver "<< format <<" supports Create() method\n";
	}
	else
	{
		throw ImageOutputException("Driver cannot create a new file.", 
								   error_codes::unsupported_format);
	}
	GDALDataset *dataset;       
    char **papszOptions = NULL;
	
    dataset = poDriver->Create(filename, 
							   this->numberbins, 
							   this->numberbins, 
							   1, 
							   GDT_Float32, 
							   papszOptions);
	
	GDALRasterBand *poBand;
	int jointHistLength = numberbins * numberbins;
	int *raster;
	raster = new int[jointHistLength];
	int tmpInt = 0;
	
	for(int i=0; i<jointHistLength; i++)
	{
		
		mathUtils->findFloatingPointComponent(this->frequency[i], &tmpInt);
		
		raster[i] = tmpInt;
		
		/*if(raster[i] == 0)
		{
			std::cout << "index " << i << " is "<<  raster[i] 
					<<" frequency[" << i << "] = " << this->frequency[i] 
					<< std::endl;
		}*/
	}
	
	poBand = dataset->GetRasterBand(1);
    poBand->RasterIO( GF_Write, 
					  0, 
					  0, 
					  numberbins, 
					  numberbins, 
					  raster, 
					  numberbins, 
					  numberbins, 
					  GDT_Float32, 
					  0, 
					  0 );    
	if(raster != NULL)
	{
		delete raster;
	}
	if(dataset != NULL)
	{
		delete dataset;
	}
}

int JointHistogram::getNumberBins()
{
	return this->numberbins;
}

void JointHistogram::getJointHistogramImage(double *jointHisto)
{
	//std::cout << "JointHistogram::getJointHistogramImage(double *jointHisto)\n";
	int histogramLength = numberbins*numberbins;
	for(int i = 0; i< histogramLength; i++)
	{
		jointHisto[i] = this->frequency[i];
	}
}

JointHistogram::~JointHistogram()
{
	//std::cout << "JointHistogram::~JointHistogram()\n";
	/*if( refRanges != NULL )
	{
		delete [] refRanges;
		std::cout << "delete [] refRanges;\n";
	}
	if( floatRanges != NULL )
	{
		delete [] floatRanges;
		std::cout << "delete [] floatRanges;\n";
	}*/
	if( frequency != NULL )
	{
		delete [] frequency;
		//std::cout << "delete [] frequency;\n";
	}
}
