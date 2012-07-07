/*
 *  CorrelationMeasures.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/04/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "CorrelationMeasures.h"

CorrelationMeasures::CorrelationMeasures()
{
	
}

double CorrelationMeasures::calcCorrelationCoefficient(GDALDataset *ref, 
													   GDALDataset *floating, 
													   int refBand, 
													   int floatBand, 
													   ImageOverlap *imgOverlap,
													   double xShift,
													   double yShift)
	throw(ImageNotAvailableException, ImageProcessingException)
{
		Interpolation interpolation;
		MathUtils mathUtils;
		
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
		xShiftz = mathUtils.findFloatingPointComponent(xShift, &b4floatingpoint);
		yShiftz = mathUtils.findFloatingPointComponent(yShift, &b4floatingpoint);
		
		if(xShiftz == 0 & yShiftz == 0)
		{
			return this->calcCorrelationCoefficient(ref, floating, refBand, floatBand, imgOverlap);
		}
		else
		{
			// There is a floating point shift use the function...
			//std::cout << "calcCorrelationCoefficient WITH SHIFT!!\n";
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
		
		if(imageASizeX < 1)
		{
			std::cout << "Image A Size X: " << imageASizeX << std::endl;
			std::cout << "Image A Size Y: " << imageASizeY << std::endl;
			std::cout << "Image B Size X: " << imageBSizeX << std::endl;
		}
		if(imageASizeY < 1)
		{
			std::cout << "Image A Size X: " << imageASizeX << std::endl;
			std::cout << "Image A Size Y: " << imageASizeY << std::endl;
			std::cout << "Image B Size X: " << imageBSizeX << std::endl;
		}
		if(imageBSizeX < 1)
		{
			std::cout << "Image A Size X: " << imageASizeX << std::endl;
			std::cout << "Image A Size Y: " << imageASizeY << std::endl;
			std::cout << "Image B Size X: " << imageBSizeX << std::endl;
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
		
		// Pixel Values for Calculations.
		double referencePixel = 0;
		double floatingPixel = 0;
		double pixels[4];
		
		double correlationCoefficient = 0;
		double sumRef = 0;
		double sumFloat = 0;
		double sumRefFloat = 0;
		double sumSQRef = 0;
		double sumSQFloat = 0;
		double counter = 0;
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
				
				floatingPixel = interpolation.bilinear(xfloatingShift, 
														yfloatingShift, 
														pixels);	
				
				sumRef += referencePixel;
				sumFloat += floatingPixel;
				sumRefFloat += referencePixel * floatingPixel;
				sumSQRef += referencePixel*referencePixel;
				sumSQFloat += floatingPixel*floatingPixel;
				
				counter++;
			}
		}
		/***************************************************************/
		
		correlationCoefficient = ((counter * sumRefFloat) - (sumRef * sumFloat)) /
			sqrt(((counter * sumSQRef)-(sumRef*sumRef))*
				 ((counter * sumSQFloat)-(sumFloat*sumFloat)));
		
		
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
		return correlationCoefficient;
}

double CorrelationMeasures::calcCorrelationCoefficient(GDALDataset *ref, 
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
	**********************************************************************/
	
	/************************ Set up data variables ****************/
	
	// Image Size.
	int imageASizeX = imgOverlap->getSizeXPixelsA();
	int imageASizeY = imgOverlap->getSizeYPixelsA();
	int imageBSizeX = imgOverlap->getSizeXPixelsB();
	int imageBSizeY = imgOverlap->getSizeYPixelsB();
	
	double correlationCoefficient = 0;
	
	if(imageBSizeX <= 0 | imageBSizeY <= 0)
	{
		correlationCoefficient = -999;
	}
	else
	{
		// Image Data Stores.
		float *refScanline1;
		float *floatScanline1;
		
		refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
		floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
		
		GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
		GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
		
		// Pixel Values for Calculations.
		double referencePixel = 0;
		double floatingPixel = 0;
		
		double sumRef = 0;
		double sumFloat = 0;
		double sumRefFloat = 0;
		double sumSQRef = 0;
		double sumSQFloat = 0;
		double counter = 0;
		/***************************************************************/
		
		/********** Find Max and Min Values for both images ************/
		for(int i=0; i < imageASizeY-1; i++)
		{ 
			//std::cout << "Going to read data\t";
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
			//std::cout << "Read reference band\t";
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
			//std::cout << "Read Floating band\n";
			for(int j=0; j< imageASizeX-1; j++)
			{
				referencePixel = refScanline1[j];
				floatingPixel = floatScanline1[j];	
				
				sumRef += referencePixel;
				sumFloat += floatingPixel;
				sumRefFloat += referencePixel * floatingPixel;
				sumSQRef += referencePixel*referencePixel;
				sumSQFloat += floatingPixel*floatingPixel;
								
				counter++;
			}
		}
		/***************************************************************/
		/*std::cout << "sumRef = " << sumRef << std::endl;
		std::cout << "sumFloat = " << sumFloat << std::endl;
		std::cout << "sumRefFloat = " << sumRefFloat << std::endl;
		std::cout << "sumSQRef = " << sumSQRef << std::endl;
		std::cout << "sumSQFloat = " << sumSQFloat << std::endl;
		std::cout << "counter = " << counter << std::endl;*/
		
		correlationCoefficient = ((counter * sumRefFloat) - (sumRef * sumFloat)) /
								sqrt(((counter * sumSQRef) - (sumRef*sumRef))*
									 ((counter * sumSQFloat) - (sumFloat*sumFloat)));

		if(refScanline1 != NULL)
		{
			delete refScanline1;
		}
		if(floatScanline1 != NULL)
		{
			delete floatScanline1;
		}
	}
	return correlationCoefficient;
}

double CorrelationMeasures::calcDiffResolutionCorrelationCoefficient(GDALDataset *ref, 
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
	
	/************************ Get Image Resolutions ***********************/
	double refXPixelRes = 0;
	double refYPixelRes = 0;
	double floatXPixelRes = 0;
	double floatYPixelRes = 0;
	
	refXPixelRes = imgOverlap->getRefPixelXRes();
	refYPixelRes = imgOverlap->getRefPixelYRes();
	floatXPixelRes = imgOverlap->getFloatPixelXRes();
	floatYPixelRes = imgOverlap->getFloatPixelYRes();
	
	if(refXPixelRes != refYPixelRes)
	{
		throw ImageProcessingException("X and Y resolutions are different", 
									   error_codes::xy_resolutions_different, 
									   error_codes::reference_image);
	}
	else if(floatXPixelRes != floatYPixelRes)
	{
		throw ImageProcessingException("X and Y resolutions are different", 
									   error_codes::xy_resolutions_different, 
									   error_codes::floating_image);
	}
	
	if(refXPixelRes == floatXPixelRes)
	{
		return this->calcCorrelationCoefficient(ref, 
												floating, 
												refBand, 
												floatBand, 
												imgOverlap);
	}
	else if(refXPixelRes < floatXPixelRes)
	{
		return this->calcDiffResolutionCorrelationCoefficientRefHigh(ref, 
																	 floating, 
																	 refBand,
																	 floatBand,
																	 imgOverlap);
	}
	//else if(refXPixelRes > floatXPixelRes)
	return this->calcDiffResolutionCorrelationCoefficientFloatHigh(ref, 
																   floating, 
																   refBand,
																   floatBand,
																   imgOverlap);
	/*********************************************************************/
	
}

double CorrelationMeasures::calcDiffResolutionCorrelationCoefficientRefHigh(GDALDataset *ref, 
																			GDALDataset *floating, 
																			int refBand, 
																			int floatBand, 
																			ImageOverlap *imgOverlap)
{
	Interpolation *interpolation;
	interpolation = new Interpolation;
	MathUtils *mathUtils = NULL;
	mathUtils = new MathUtils;
	
	/************************ Get Image Resolutions ***********************/
	double refXPixelRes = 0;
	double refYPixelRes = 0;
	double floatXPixelRes = 0;
	double floatYPixelRes = 0;
	
	refXPixelRes = imgOverlap->getRefPixelXRes();
	refYPixelRes = imgOverlap->getRefPixelYRes();
	floatXPixelRes = imgOverlap->getFloatPixelXRes();
	floatYPixelRes = imgOverlap->getFloatPixelYRes();
	/*********************************************************************/
	
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
	
	// Image Size.
	int imageASizeX = imgOverlap->getSizeXPixelsA();
	int imageASizeY = imgOverlap->getSizeYPixelsA();
	int imageBSizeX = imgOverlap->getSizeXPixelsB();
	
	//std::cout << "image A Size X: " << imageASizeX << std::endl;
	//std::cout << "image A Size Y: " << imageASizeY << std::endl;
	//std::cout << "image B Size X: " << imageBSizeX << std::endl;
	
	// Image Data Stores.
	float *refScanline1;
	float *floatScanline1;
	float *floatScanline2;
	
	//std::cout << "Allocating refscanline1: "<< sizeof(float)*imageASizeX <<" \n";
	refScanline1 = (float *) CPLMalloc(sizeof(float)*imageASizeX);
	//std::cout << "Allocating floatScanline1: "<< sizeof(float)*imageBSizeX <<"\n";
	floatScanline1 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	//std::cout << "Allocating floatScanline2: "<< sizeof(float)*imageBSizeX <<"\n";
	floatScanline2 = (float *) CPLMalloc(sizeof(float)*imageBSizeX);
	//std::cout << "All memory allocated\n";
	
	GDALRasterBand *refRasterband = ref->GetRasterBand(refBand);
	GDALRasterBand *floatRasterband = floating->GetRasterBand(floatBand);
	
	// Pixel Values for Calculations.
	double referencePixel = 0;
	double floatingPixel = 0;
	double pixels[4];
	
	double correlationCoefficient = 0;
	double sumRef = 0;
	double sumFloat = 0;
	double sumRefFloat = 0;
	double sumSQRef = 0;
	double sumSQFloat = 0;
	double counter = 0;
	double xShift4Interpolation = 0;
	double yShift4Interpolation = 0;
	int xPixel = 0;
	int yPixel = 0;
	/***************************************************************/
	
	/********** Find Max and Min Values for both images ************/
	for(int i=0; i < imageASizeY-1; i++)
	{
		// Y Axis
		yShift4Interpolation = mathUtils->findFloatingPointComponent((refYPixelRes*i)/floatYPixelRes, &yPixel);
		
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
								  (floatImagePixels[1]+yPixel), 
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
								  (floatImagePixels[1]+(yPixel+1)), 
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

			//Identify Shift for interpolation taking into account image resolution
			//xShift4Interpolation
			
			// X Axis
			xShift4Interpolation = mathUtils->findFloatingPointComponent((refXPixelRes*j)/floatXPixelRes, &xPixel);

			referencePixel = refScanline1[j];
			pixels[0] = floatScanline1[xPixel];
			pixels[1] = floatScanline1[xPixel+1];
			pixels[2] = floatScanline2[xPixel];
			pixels[3] = floatScanline2[xPixel+1];
			
			floatingPixel = interpolation->bilinear(xShift4Interpolation, 
													yShift4Interpolation, 
													pixels);	
			
			sumRef += referencePixel;
			sumFloat += floatingPixel;
			sumRefFloat += referencePixel * floatingPixel;
			sumSQRef += referencePixel*referencePixel;
			sumSQFloat += floatingPixel*floatingPixel;
			
			counter++;
		}
	}
	/***************************************************************/
	
	correlationCoefficient = ((counter * sumRefFloat) - (sumRef * sumFloat)) /
		sqrt(((counter * sumSQRef) - (sumRef*sumRef))*
			 ((counter * sumSQFloat) - (sumFloat*sumFloat)));
	
	//std::cout << "Correlation = " << correlationCoefficient << std::endl;
	
	if(refScanline1 != NULL)
	{
		CPLFree(refScanline1);
	}
	if(floatScanline1 != NULL)
	{
		CPLFree(floatScanline1);
	}
	if(floatScanline2 != NULL)
	{
		CPLFree(floatScanline2);
	}
	if(interpolation != NULL)
	{
		delete interpolation;
	}
	if(mathUtils != NULL)
	{
		delete mathUtils;
	}
	
	return correlationCoefficient;
}

double CorrelationMeasures::calcDiffResolutionCorrelationCoefficientFloatHigh(GDALDataset *ref, 
																			GDALDataset *floating, 
																			int refBand, 
																			int floatBand, 
																			ImageOverlap *imgOverlap)
{
	return -1;
}


CorrelationMeasures::~CorrelationMeasures()
{
	
}
