/*
 *  VectorImageMeasures.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 23/01/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "VectorImageMeasures.h"


VectorImageMeasures::VectorImageMeasures()
{
}

double VectorImageMeasures::calcEuclideanDistance(double *imageA, 
												  double *imageB, 
												  int sizeX, 
												  int sizeY)
{
	double euclideanDistance = 0;
	double tmp = 0;
	int totalSize = sizeX * sizeY;
	for(int i = 0; i < totalSize; i++)
	{
		tmp = imageA[i] - imageB[i];
		euclideanDistance = euclideanDistance + (tmp * tmp);
	}
	
	euclideanDistance = sqrt(euclideanDistance);
	return euclideanDistance;
}

double VectorImageMeasures::calcManhattenDistance(double *imageA, 
												  double *imageB, 
												  int sizeX, 
												  int sizeY)
{
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	double calcManhattenDistance = 0;
	double tmp = 0;
	int totalSize = sizeX * sizeY;
	for(int i = 0; i < totalSize; i++)
	{
		tmp = imageA[i] - imageB[i];
		tmp = mathUtils->absoluteValue(tmp);
		calcManhattenDistance = calcManhattenDistance + tmp;
	}
	calcManhattenDistance = sqrt(calcManhattenDistance);
	if(mathUtils != NULL)
	{
		delete mathUtils;
	}
	return calcManhattenDistance;
}

double VectorImageMeasures::calcManhattenIncrementDistanceWithInterpolation(double imageA, 
																			double xShift, 
																			double yShift, 
																			double *pixels)
{	
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	double calcManhattenDistance = 0;
	double tmp = 0;

	tmp = imageA - pixels[0];
	tmp = mathUtils->absoluteValue(tmp);
	tmp = tmp * ((1-xShift) * (1-yShift));
	calcManhattenDistance = calcManhattenDistance + tmp;
	
	tmp = 0;
	tmp = imageA - pixels[1];
	tmp = mathUtils->absoluteValue(tmp);
	tmp = tmp * (xShift * (1-yShift));
	calcManhattenDistance = calcManhattenDistance + tmp;
	
	tmp = 0;
	tmp = imageA - pixels[2];
	tmp = mathUtils->absoluteValue(tmp);
	tmp = tmp * ((1-xShift) * yShift);
	calcManhattenDistance = calcManhattenDistance + tmp;
	
	tmp = 0;
	tmp = imageA - pixels[3];
	tmp = mathUtils->absoluteValue(tmp);
	tmp = tmp * (xShift * yShift);
	calcManhattenDistance = calcManhattenDistance + tmp;
	
	if(mathUtils != NULL)
	{
		delete mathUtils;
	}
	return calcManhattenDistance;
}


double VectorImageMeasures::calcChebyshevDistance(double *imageA, 
												  double *imageB, 
												  int sizeX, 
												  int sizeY)
{
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	double ChebyshevDistance = 0;
	double tmp = 0;
	int totalSize = sizeX * sizeY;
	for(int i = 0; i < totalSize; i++)
	{
		tmp = imageA[i] - imageB[i];
		tmp = mathUtils->absoluteValue(tmp);
		tmp = mathUtils->roundUp(tmp);
		ChebyshevDistance = ChebyshevDistance + tmp;
	}
	if(mathUtils != NULL)
	{
		delete mathUtils;
	}
	return ChebyshevDistance;
}

double VectorImageMeasures::calcEuclideanDistance(GDALDataset *ref, 
												  GDALDataset *floating, 
												  int refBand, 
												  int floatBand, 
												  ImageOverlap *imgOverlap,
												  double xShift,
												  double yShift)
	throw(ImageNotAvailableException, ImageProcessingException)
{	
		Interpolation *interpolation;
		interpolation = new Interpolation;
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
		
		if(xShiftz == 0 & yShiftz == 0)
		{
			//std::cout << "xShiftz: " << xShiftz << " yShiftz: " << yShiftz << std::endl;
			return this->calcEuclideanDistance(ref, floating, refBand, floatBand, imgOverlap);
		}
		else
		{
			// There is a floating point shift use the function...
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
			//nothing
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
			//nothing
		}
		
		// Image Size.
		int imageASizeX = imgOverlap->getSizeXPixelsA();
		int imageASizeY = imgOverlap->getSizeYPixelsA();
		int imageBSizeX = imgOverlap->getSizeXPixelsB();
		
		// Image Data Stores.
		float *refScanline1;
		float *floatScanline1;
		float *floatScanline2;
		
		refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
		floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
		floatScanline2 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
		
		GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
		GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
		
		// Pixel Values for Calculations.
		double referencePixel = 0;
		double floatingPixel = 0;
		double pixels[4];
		
		double euclideanDistance = 0;
		/***************************************************************/
		
		/******************* TEST: Print Shifts ***********************
		std::cout << " xShift = " << xShift << std::endl;
		std::cout << " yShift = " << yShift << std::endl;
		std::cout << "xShiftz = " << xShiftz << std::endl;
		std::cout << "yShiftz = " << yShiftz << std::endl;
		std::cout << "xfloatingShift = " << xfloatingShift << std::endl;
		std::cout << "yfloatingShift = " << yfloatingShift << std::endl;
		/**************************************************************/
		
		/********** Find Max and Min Values for both images ************/
		for(int i=0; i < imageASizeY-1; i++)
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
			
			for(int j=0; j< imageASizeX-1; j++)
			{
				referencePixel = refScanline1[j];
				pixels[0] = floatScanline1[j];
				pixels[1] = floatScanline1[j+1];
				pixels[2] = floatScanline2[j];
				pixels[3] = floatScanline2[j+1];
				
				floatingPixel = interpolation->bilinear(xfloatingShift, 
														yfloatingShift, 
														pixels);	
			
				euclideanDistance = euclideanDistance + 
					((referencePixel - floatingPixel)*(referencePixel - floatingPixel));
				
			}
		}
		/***************************************************************/
		euclideanDistance = euclideanDistance / (imageASizeX*imageASizeY);
		euclideanDistance = sqrt(euclideanDistance);
		
		if(refScanline1 != NULL)
		{
			delete refScanline1;
		}
		if(floatScanline1 != NULL)
		{
			delete floatScanline1;
		}
		if(floatScanline2 != NULL)
		{
			delete floatScanline2;
		}
		if(interpolation != NULL)
		{
			delete interpolation;
		}
		if(mathUtils != NULL)
		{
			delete mathUtils;
		}
		
	return euclideanDistance;
}

double VectorImageMeasures::calcEuclideanDistance(GDALDataset *ref, 
												  GDALDataset *floating, 
												  int refBand, 
												  int floatBand, 
												  ImageOverlap *imgOverlap)
throw(ImageNotAvailableException, ImageProcessingException)
{	
	//std::cout << "VectorImageMeasures::calcEuclideanDistance\n";
	
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
	
	// Image Size.
	int imageASizeX = imgOverlap->getSizeXPixelsA();
	int imageASizeY = imgOverlap->getSizeYPixelsA();
	int imageBSizeX = imgOverlap->getSizeXPixelsB();
	// Image Data Stores.
	
	double euclideanDistance = 0;
	
	if(imageBSizeX <= 0 | imageASizeX <= 0)
	{
		euclideanDistance = 999;
	}
	else
	{
	
		//std::cout << "imageASizeX: " << imageASizeX << " imageBSizeX: " << imageBSizeX << std::endl;
		float *refScanline1;
		float *floatScanline1;
		
		refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
		floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
		
		GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
		GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
		
		// Pixel Values for Calculations.
		double referencePixel = 0;
		double floatingPixel = 0;
		
		
		/***************************************************************/
		
		/********** Find Max and Min Values for both images ************/
		for(int i=0; i < imageASizeY; i++)
		{
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
			
			for(int j=0; j< imageASizeX; j++)
			{
				referencePixel = refScanline1[j];
				floatingPixel = floatScanline1[j];	
				
				euclideanDistance = euclideanDistance + 
					((referencePixel - floatingPixel)*(referencePixel - floatingPixel));
				
			}
		}
		/***************************************************************/
		euclideanDistance = euclideanDistance / (imageASizeX*imageASizeY);
		euclideanDistance = sqrt(euclideanDistance);
		
		if(refScanline1 != NULL)
		{
			delete refScanline1;
		}
		if(floatScanline1 != NULL)
		{
			delete floatScanline1;
		}
		
	}
	
	if(mathUtils != NULL)
	{
		delete mathUtils;
	}
	
	return euclideanDistance;
}


double VectorImageMeasures::calcEuclideanDistanceCubicInterpolation(GDALDataset *ref, 
																	GDALDataset *floating, 
																	int refBand, 
																	int floatBand, 
																	ImageOverlap *imgOverlap,
																	double xShift,
																	double yShift)
throw(ImageNotAvailableException, ImageProcessingException)
{	
	Interpolation *interpolation;
	interpolation = new Interpolation;
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
	else
	{
		xfloatingShift = 1 - xShiftz;
	}
	double yfloatingShift = 0;
	if( yShiftDirection == PosShift | yShiftz == 0  )
	{
		yfloatingShift = yShiftz;
	}
	else 
	{
		yfloatingShift = 1 - yShiftz;
	}
	
	// Image Size.
	int imageASizeX = imgOverlap->getSizeXPixelsA();
	int imageASizeY = imgOverlap->getSizeYPixelsA();
	int imageBSizeX = imgOverlap->getSizeXPixelsB();
	
	// Image Data Stores.
	float *refScanline1;
	float *floatScanline0;
	float *floatScanline1;
	float *floatScanline2;
	float *floatScanline3;
	
	refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
	floatScanline0 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	floatScanline2 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	floatScanline3 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	
	GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
	GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
	
	// Pixel Values for Calculations.
	double referencePixel = 0;
	double floatingPixel = 0;
	double pixels[16];
	
	double euclideanDistance = 0;
	/***************************************************************/
	
	/******************* TEST: Print Shifts ***********************
		std::cout << " xShift = " << xShift << std::endl;
	std::cout << " yShift = " << yShift << std::endl;
	std::cout << "xShiftz = " << xShiftz << std::endl;
	std::cout << "yShiftz = " << yShiftz << std::endl;
	std::cout << "xfloatingShift = " << xfloatingShift << std::endl;
	std::cout << "yfloatingShift = " << yfloatingShift << std::endl;
	/**************************************************************/
	
	/********** Find Max and Min Values for both images ************/
	for(int i=1; i < imageASizeY-2; i++)
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
								  (floatImagePixels[1]+i-1), 
								  imageBSizeX, 
								  1, 
								  floatScanline0, 
								  imageBSizeX, 
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
		
		floatRasterband->RasterIO(GF_Read, 
								  floatImagePixels[0], 
								  (floatImagePixels[1]+(i+2)), 
								  imageBSizeX, 
								  1, 
								  floatScanline3, 
								  imageBSizeX, 
								  1, 
								  GDT_Float32, 
								  0, 
								  0);
		
		for(int j=1; j< imageASizeX-2; j++)
		{
			referencePixel = refScanline1[j];
			pixels[0] = floatScanline0[j-1];
			pixels[1] = floatScanline0[j];
			pixels[2] = floatScanline0[j+1];
			pixels[3] = floatScanline0[j+2];
			
			pixels[4] = floatScanline1[j-1];
			pixels[5] = floatScanline1[j];
			pixels[6] = floatScanline1[j+1];
			pixels[7] = floatScanline1[j+2];
			
			pixels[8] = floatScanline2[j-1];
			pixels[9] = floatScanline2[j];
			pixels[10] = floatScanline2[j+1];
			pixels[11] = floatScanline2[j+2];
			
			pixels[12] = floatScanline3[j-1];
			pixels[13] = floatScanline3[j];
			pixels[14] = floatScanline3[j+1];
			pixels[15] = floatScanline3[j+2];
			
			floatingPixel = interpolation->cubic(xfloatingShift, 
												 yfloatingShift, 
												 pixels);	
			euclideanDistance = euclideanDistance + 
				((referencePixel - floatingPixel)*(referencePixel - floatingPixel));
		}
	}
	/***************************************************************/
	euclideanDistance = euclideanDistance / (imageASizeX*imageASizeY);
	euclideanDistance = sqrt(euclideanDistance);
	
	if(refScanline1 != NULL)
	{
		delete refScanline1;
	}
	if(floatScanline1 != NULL)
	{
		delete floatScanline1;
	}
	if(floatScanline2 != NULL)
	{
		delete floatScanline2;
	}
	if(interpolation != NULL)
	{
		delete interpolation;
	}
	
	return euclideanDistance;
}


double VectorImageMeasures::calcManhattanDistance(GDALDataset *ref, 
												  GDALDataset *floating, 
												  int refBand, 
												  int floatBand, 
												  ImageOverlap *imgOverlap,
												  double xShift,
												  double yShift)
{
	Interpolation *interpolation;
	interpolation = new Interpolation;
	
	MathUtils *mathUtils;
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
	
	// Image Data Stores.
	float *refScanline1;
	float *floatScanline1;
	float *floatScanline2;
	
	refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
	floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	floatScanline2 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	
	GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
	GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
	
	// Pixel Values for Calculations.
	double referencePixel = 0;
	double floatingPixel = 0;
	double pixels[4];
	
	double manhattanDistance = 0;
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
			manhattanDistance = manhattanDistance + 
				mathUtils->absoluteValue(referencePixel - floatingPixel);
		}
	}
	/***************************************************************/
	
	manhattanDistance = manhattanDistance/(imageASizeY*imageASizeX);
	
	manhattanDistance = sqrt(manhattanDistance);
	
	if(refScanline1 != NULL)
	{
		delete refScanline1;
	}
	if(floatScanline1 != NULL)
	{
		delete floatScanline1;
	}
	if(floatScanline2 != NULL)
	{
		delete floatScanline2;
	}
	if(interpolation != NULL)
	{
		delete interpolation;
	}
	if(mathUtils != NULL)
	{
		delete mathUtils;
	}
	
	return manhattanDistance;
}

