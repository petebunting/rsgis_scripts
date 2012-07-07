/*
 *  ImageOverlap.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 06/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "ImageOverlap.h"

ImageOverlap::ImageOverlap()
{
	
}

ImageOverlap::ImageOverlap(GDALDataset *imgA, GDALDataset *imgB)
	throw(ImageNotAvailableException, ImageProcessingException)
{
	try
	{
		this->calcOverlappingAreaWithShift(imgA, imgB, 0, 0);
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

void ImageOverlap::calcOverlappingAreaWithDiffResolutions(GDALDataset *imgA, 
														  GDALDataset *imgB)
throw(ImageNotAvailableException, ImageProcessingException)
{
	MathUtils mathUtils;
	
	/******************* Checking Images are NOT NULL ********************/
	if(imgA == NULL)
	{
		throw ImageNotAvailableException("Image A is not availble.", error_codes::reference_image);
	}
	else if(imgB == NULL)
	{
		throw ImageNotAvailableException("Image B is not availble.", error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Got images\n";
	}
	/**********************************************************************/
	
	/********** Getting Georeferencing info for reference Image ***********/
	double refGeoinfo[6];
	if(imgA->GetGeoTransform(refGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Reference Image has geo info.\n";
		std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image A does not have any geoinfo", 
									   error_codes::no_projection, error_codes::reference_image);
	}
	/*****************************************************************************/
	
	/************ Getting Georeferencing info for floating Image ***************/
	double floatGeoinfo[6];
	if(imgB->GetGeoTransform(floatGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Floating Image has geo info.\n";
		std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image B does not have any geoinfo", 
									   error_codes::no_projection, error_codes::floating_image);
	}
	/*******************************************************************************/
	
	/****************** Checking  pixel resolution is the same ********************/
	if(refGeoinfo[1] != floatGeoinfo[1] | refGeoinfo[5] != floatGeoinfo[5])
	{
		//std::cout << "Pixel Resolution is different" << std::endl;
	}
	
	
	// Image A.
	// X
	if(refGeoinfo[1] < 0)
	{
		refGeoinfo[1] = refGeoinfo[1]*(-1);
	}
	// Y
	if(refGeoinfo[5] < 0)
	{
		refGeoinfo[5] = refGeoinfo[5]*(-1);
	}
	//Image B
	// X
	if(floatGeoinfo[1] < 0)
	{
		floatGeoinfo[1] = floatGeoinfo[1]*(-1);
	}
	// Y
	if(floatGeoinfo[5] < 0)
	{
		floatGeoinfo[5] = floatGeoinfo[5]*(-1);
	}
	this->refPixelXres = refGeoinfo[1];
	this->refPixelYres = refGeoinfo[5];
	this->floatPixelXres = floatGeoinfo[1];
	this->floatPixelYres = floatGeoinfo[5];
	/*********************************************************************/
	
	/******************** TEST: Print GeoInfo for Both Images ********************
		std::cout << "After negative check.\n";
	std::cout << "Image A:.\n";
	std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
	std::cout << "Image B: \n";
	std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
	****************************************************************************/
	
	/**************** Checking  image rotation is the same ****************/
	if(refGeoinfo[2] != floatGeoinfo[2] | refGeoinfo[4] != floatGeoinfo[4])
	{
		throw ImageProcessingException("Pixel Resolution is different", 
									   error_codes::difference_rotation, 0);
	}
	else
	{
		//std::cout << "OK: Image rotation is the same in both images\n";
	}
	/************************************************************************/		
	
	/************** Calculate Images TL and BR Coords **********************/	
	// Coords for Image A:
	double imageACoords[4];
	int imageAPixels[4];
	double imageAXSize = imgA->GetRasterXSize() * refPixelXres;
	double imageAYSize = imgA->GetRasterYSize() * refPixelYres;
	
	imageACoords[0] = refGeoinfo[0];
	imageACoords[1] = refGeoinfo[3];
	imageACoords[2] = refGeoinfo[0] + imageAXSize;
	imageACoords[3] = refGeoinfo[3] - imageAYSize;
	
	imageAPixels[0] = 0;
	imageAPixels[1] = 0;
	imageAPixels[2] = imgA->GetRasterXSize();
	imageAPixels[3] = imgA->GetRasterYSize();
	
	// Coords for Image B:
	double imageBCoords[4];
	int imageBPixels[4];
	double imageBXSize = imgB->GetRasterXSize() * floatPixelXres;
	double imageBYSize = imgB->GetRasterYSize() * floatPixelYres;
	
	imageBCoords[0] = floatGeoinfo[0];
	imageBCoords[1] = floatGeoinfo[3];
	imageBCoords[2] = floatGeoinfo[0] + imageBXSize;
	imageBCoords[3] = floatGeoinfo[3] - imageBYSize;
	
	imageBPixels[0] = 0;
	imageBPixels[1] = 0;
	imageBPixels[2] = imgB->GetRasterXSize();
	imageBPixels[3] = imgB->GetRasterYSize();
	/************************************************************************/
	/****************** Find over lapping areas *****************************/
	
	// Find MAX X coord which gives X coord for top left
	if(refGeoinfo[0] >= floatGeoinfo[0])
	{
		this->overlapCoords[0] = refGeoinfo[0];
	}
	else
	{
		this->overlapCoords[0] = floatGeoinfo[0];
	}
	
	// Find MIN Y coord which gives Y coord for top left
	if(refGeoinfo[3] <= floatGeoinfo[3])
	{
		this->overlapCoords[1] = refGeoinfo[3];
	}
	else
	{
		this->overlapCoords[1] = floatGeoinfo[3];
	}
	// Find coords for the bottom right corner of each image
	// Image A:
	//    1) Distance in metres across image.
	double imgA_Xsize_metres = imgA->GetRasterXSize() * refPixelXres;
	double imgA_Ysize_metres = imgA->GetRasterYSize() * refPixelYres;
	//    2) Add to opposite corner coords.
	double imgA_BottomRight_X = refGeoinfo[0] + imgA_Xsize_metres;
	double imgA_BottomRight_Y = refGeoinfo[3] - imgA_Ysize_metres;
	
	//Image B:
	//    1) Distance in metres across image.
	double imgB_Xsize_metres = imgB->GetRasterXSize() * floatPixelXres;
	double imgB_Ysize_metres = imgB->GetRasterYSize() * floatPixelYres;
	//    2) Add to opposite corner coords.
	double imgB_BottomRight_X = floatGeoinfo[0] + imgB_Xsize_metres;
	double imgB_BottomRight_Y = floatGeoinfo[3] - imgB_Ysize_metres;
	
	// Find MIN X coord which gives X coord for bottom right
	if(imgA_BottomRight_X <= imgB_BottomRight_X)
	{
		this->overlapCoords[2] = imgA_BottomRight_X;
	}
	else
	{
		this->overlapCoords[2] = imgB_BottomRight_X;
	}
	
	// Find MAX Y coord which gives Y coord for bottom right
	if(imgA_BottomRight_Y >= imgB_BottomRight_Y)
	{
		this->overlapCoords[3] = imgA_BottomRight_Y;
	}
	else
	{
		this->overlapCoords[3] = imgB_BottomRight_Y;
	}
	/****************************************************************************/
	
	/*************** Find Pixels associated with those coordinates ********************/
	
	// Image A:
	// 1) Top Left
	double imgA_dist_X_TL = overlapCoords[0] - refGeoinfo[0];
	imgAPixelCoords[0] = mathUtils.round(imgA_dist_X_TL / refPixelXres);
	double imgA_dist_Y_TL = refGeoinfo[3] - overlapCoords[1];
	imgAPixelCoords[1] = mathUtils.round(imgA_dist_Y_TL / refPixelYres);
	// 2) Bottom Right
	double imgA_dist_X_BR = imgA_BottomRight_X - overlapCoords[2];
	imgAPixelCoords[2] =  imgA->GetRasterXSize() - mathUtils.round(imgA_dist_X_BR / refPixelXres);
	double imgA_dist_Y_BR = overlapCoords[3] - imgA_BottomRight_Y;
	imgAPixelCoords[3] = imgA->GetRasterYSize() - mathUtils.round(imgA_dist_Y_BR / refPixelYres);
	
	// Image B:
	// 1) Top Left
	double imgB_dist_X_TL = overlapCoords[0] - floatGeoinfo[0];
	imgBPixelCoords[0] = mathUtils.round(imgB_dist_X_TL / floatPixelXres);
	double imgB_dist_Y_TL = floatGeoinfo[3] - overlapCoords[1];
	imgBPixelCoords[1] = mathUtils.round(imgB_dist_Y_TL / floatPixelYres);
	// 2) Bottom Right
	double imgB_dist_X_BR = imgB_BottomRight_X - overlapCoords[2];
	imgBPixelCoords[2] =  imgB->GetRasterXSize() - mathUtils.round(imgB_dist_X_BR / floatPixelXres);
	double imgB_dist_Y_BR = overlapCoords[3] - imgB_BottomRight_Y;
	imgBPixelCoords[3] = imgB->GetRasterYSize() - mathUtils.round(imgB_dist_Y_BR / floatPixelYres);
	
	/********************************************************************************/
}

void ImageOverlap::calcOverlappingAreaWithShift(GDALDataset *imgA, 
												GDALDataset *imgB, 
												int xShift, 
												int yShift)
	throw(ImageNotAvailableException, ImageProcessingException)
{	
	MathUtils mathUtils;
	/******************* Checking Images are NOT NULL ********************/
	if(imgA == NULL)
	{
		throw ImageNotAvailableException("Image A is not availble.", error_codes::reference_image);
	}
	else if(imgB == NULL)
	{
		throw ImageNotAvailableException("Image B is not availble.", error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Got images\n";
	}
	/**********************************************************************/
	
	/********** Getting Georeferencing info for reference Image ***********/
	double refGeoinfo[6];
	if(imgA->GetGeoTransform(refGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Reference Image has geo info.\n";
		std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image A does not have any geoinfo", 
									   error_codes::no_projection, error_codes::reference_image);
	}
	/*****************************************************************************/
	
	/************ Getting Georeferencing info for floating Image ***************/
	double floatGeoinfo[6];
	if(imgB->GetGeoTransform(floatGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Floating Image has geo info.\n";
		std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image B does not have any geoinfo", 
									   error_codes::no_projection, error_codes::floating_image);
	}
	/*******************************************************************************/
	// Image A.
	// X
	if(refGeoinfo[1] < 0)
	{
		refGeoinfo[1] = refGeoinfo[1]*(-1);
	}
	// Y
	if(refGeoinfo[5] < 0)
	{
		refGeoinfo[5] = refGeoinfo[5]*(-1);
	}
	//Image B
	// X
	if(floatGeoinfo[1] < 0)
	{
		floatGeoinfo[1] = floatGeoinfo[1]*(-1);
	}
	// Y
	if(floatGeoinfo[5] < 0)
	{
		floatGeoinfo[5] = floatGeoinfo[5]*(-1);
	}
	
	/****************** Checking  pixel resolution is the same ********************/
	if(refGeoinfo[1] != floatGeoinfo[1] | refGeoinfo[5] != floatGeoinfo[5])
	{
		throw ImageProcessingException("Pixel Resolution is different", 
									   error_codes::different_pixel_resolution, 0);
	}
	else
	{
		/**** Checking for negative values, if present convert to positive. *******/
		//std::cout << "OK: Pixel resolution the same in both images\n";
		
		this->pixelXres = refGeoinfo[1];
		this->pixelYres = refGeoinfo[5];
		//std::cout << "OK: Pixel resolution all positive values\n";
		/****************************************************************************/
	}
	/*********************************************************************/
	
	/******************** TEST: Print GeoInfo for Both Images ********************
	std::cout << "After negative check.\n";
	std::cout << "Image A:.\n";
	std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
	std::cout << "Image B: \n";
	std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
	/****************************************************************************/
	
	/**************** Checking  image rotation is the same ****************/
	if(refGeoinfo[2] != floatGeoinfo[2] | refGeoinfo[4] != floatGeoinfo[4])
	{
		throw ImageProcessingException("Pixel Resolution is different", 
									   error_codes::difference_rotation, 0);
	}
	else
	{
		//std::cout << "OK: Image rotation is the same in both images\n";
	}
	/************************************************************************/	
	
	/*********** Move Image using the shiftX and shiftY values **************/
	// Calc Shift in Metres
	double xShiftMetres = xShift * pixelXres;
	double yShiftMetres = yShift * pixelYres;
	
	//std::cout << "xShift in metres: " << xShiftMetres << std::endl;
	//std::cout << "yShift in metres: " << yShiftMetres << std::endl;
	
	//std::cout << "x TL (before)" << floatGeoinfo[0] << std::endl;
	//std::cout << "y TL (before)" << floatGeoinfo[3] << std::endl;
	
	// Add Shift to the to Top Left corner
	floatGeoinfo[0] += xShiftMetres;
	floatGeoinfo[3] += yShiftMetres;
	
	//std::cout << "x TL (after)" << floatGeoinfo[0] << std::endl;
	//std::cout << "y TL (after)" << floatGeoinfo[3] << std::endl;
	/*************************************************************************/
	
	/****************** Find over lapping areas *****************************/
	
	// Find MAX X coord which gives X coord for top left
	if(refGeoinfo[0] >= floatGeoinfo[0])
	{
		this->overlapCoords[0] = refGeoinfo[0];
	}
	else
	{
		this->overlapCoords[0] = floatGeoinfo[0];
	}
	
	// Find MIN Y coord which gives Y coord for top left
	if(refGeoinfo[3] <= floatGeoinfo[3])
	{
		this->overlapCoords[1] = refGeoinfo[3];
	}
	else
	{
		this->overlapCoords[1] = floatGeoinfo[3];
	}
	
	// Find coords for the bottom right corner of each image
	// Image A:
	//    1) Distance in metres across image.
	double imgA_Xsize_metres = imgA->GetRasterXSize() * refGeoinfo[1];
	double imgA_Ysize_metres = imgA->GetRasterYSize() * refGeoinfo[5];
	//    2) Add to opposite corner coords.
	double imgA_BottomRight_X = refGeoinfo[0] + imgA_Xsize_metres;
	double imgA_BottomRight_Y = refGeoinfo[3] - imgA_Ysize_metres;
	
	//Image B:
	//    1) Distance in metres across image.
	double imgB_Xsize_metres = imgB->GetRasterXSize() * floatGeoinfo[1];
	double imgB_Ysize_metres = imgB->GetRasterYSize() * floatGeoinfo[5];
	//    2) Add to opposite corner coords.
	double imgB_BottomRight_X = floatGeoinfo[0] + imgB_Xsize_metres;
	double imgB_BottomRight_Y = floatGeoinfo[3] - imgB_Ysize_metres;
	
	// Find MIN X coord which gives X coord for bottom right
	if(imgA_BottomRight_X <= imgB_BottomRight_X)
	{
		this->overlapCoords[2] = imgA_BottomRight_X;
	}
	else
	{
		this->overlapCoords[2] = imgB_BottomRight_X;
	}
	
	// Find MAX Y coord which gives Y coord for bottom right
	if(imgA_BottomRight_Y >= imgB_BottomRight_Y)
	{
		this->overlapCoords[3] = imgA_BottomRight_Y;
	}
	else
	{
		this->overlapCoords[3] = imgB_BottomRight_Y;
	}
	/****************************************************************************/
	/**************** TEST: Print coords ***************************
	std::cout << "OK: Found Top Left coords. (" << overlapCoords[0] 
	<< "," << overlapCoords[1] << ")\n";
	std::cout << "OK: Found Bottom Right coords. (" << overlapCoords[2] << ","
	<< overlapCoords[3] << ")\n";
	/****************************************************************************/
	
	/*************** Find Pixels associated with those coordinates ********************/
	
	// Image A:
	// 1) Top Left
	double imgA_dist_X_TL = overlapCoords[0] - refGeoinfo[0];
	imgAPixelCoords[0] = mathUtils.round(imgA_dist_X_TL / refGeoinfo[1]);
	double imgA_dist_Y_TL = refGeoinfo[3] - overlapCoords[1];
	imgAPixelCoords[1] = mathUtils.round(imgA_dist_Y_TL / refGeoinfo[5]);
	// 2) Bottom Right
	double imgA_dist_X_BR = imgA_BottomRight_X - overlapCoords[2];
	imgAPixelCoords[2] =  imgA->GetRasterXSize() - mathUtils.round(imgA_dist_X_BR / refGeoinfo[1]);
	double imgA_dist_Y_BR = overlapCoords[3] - imgA_BottomRight_Y;
	imgAPixelCoords[3] = imgA->GetRasterYSize() - mathUtils.round(imgA_dist_Y_BR / refGeoinfo[5]);
	
	// Image B:
	// 1) Top Left
	double imgB_dist_X_TL = overlapCoords[0] - floatGeoinfo[0];
	imgBPixelCoords[0] = mathUtils.round(imgB_dist_X_TL / floatGeoinfo[1]);
	double imgB_dist_Y_TL = floatGeoinfo[3] - overlapCoords[1];
	imgBPixelCoords[1] = mathUtils.round(imgB_dist_Y_TL / floatGeoinfo[5]);
	// 2) Bottom Right
	double imgB_dist_X_BR = imgB_BottomRight_X - overlapCoords[2];
	imgBPixelCoords[2] =  imgB->GetRasterXSize() - mathUtils.round(imgB_dist_X_BR / floatGeoinfo[1]);
	double imgB_dist_Y_BR = overlapCoords[3] - imgB_BottomRight_Y;
	imgBPixelCoords[3] = imgB->GetRasterYSize() - mathUtils.round(imgB_dist_Y_BR / floatGeoinfo[5]);
	
	/********************************************************************************/
	
	/********************* TEST: Print result *******************************
	std::cout << "OK: Found Image A pixels. (" << imgAPixelCoords[0] << "," 
	<< imgAPixelCoords[1] << ")" << "(" << imgAPixelCoords[2] << "," 
	<< imgAPixelCoords[3] << ")\n";
	std::cout << "OK: Found Image B pixels. (" << imgBPixelCoords[0] << "," 
		      << imgBPixelCoords[1] << ")" << "(" << imgBPixelCoords[2] << "," 
			<< imgBPixelCoords[3] << ")\n";
	std::cout << "Geo Coords: (" << overlapCoords[0] << "," << overlapCoords[1] << ")"
		      << "(" << overlapCoords[2] << "," << overlapCoords[3] << ")\n";
	/**************************************************************************/
}

void ImageOverlap::calcOverlappingAreaWithDiffResolutionsTileWithFloatShift(GDALDataset *imgA, 
																			GDALDataset *imgB, 
																			double xShiftFloat, 
																			double yShiftFloat, 
																			TileCoords *tile)
throw(ImageNotAvailableException, ImageProcessingException)
{
	MathUtils mathUtils;
	
	/******************* Checking Images are NOT NULL ********************/
	if(imgA == NULL)
	{
		throw ImageNotAvailableException("Image A is not availble.", error_codes::reference_image);
	}
	else if(imgB == NULL)
	{
		throw ImageNotAvailableException("Image B is not availble.", error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Got images\n";
	}
	/**********************************************************************/
	
	/********** Getting Georeferencing info for reference Image ***********/
	double refGeoinfo[6];
	if(imgA->GetGeoTransform(refGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Reference Image has geo info.\n";
		std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image A does not have any geoinfo", 
									   error_codes::no_projection, error_codes::reference_image);
	}
	/*****************************************************************************/
	
	/************ Getting Georeferencing info for floating Image ***************/
	double floatGeoinfo[6];
	if(imgB->GetGeoTransform(floatGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Floating Image has geo info.\n";
		std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image B does not have any geoinfo", 
									   error_codes::no_projection, error_codes::floating_image);
	}
	/*******************************************************************************/
	
	/****************** Checking  pixel resolution is the same ********************/
	if(refGeoinfo[1] != floatGeoinfo[1] | refGeoinfo[5] != floatGeoinfo[5])
	{
		//std::cout << "Pixel Resolution is different" << std::endl;
	}

		
	// Image A.
	// X
	if(refGeoinfo[1] < 0)
	{
		refGeoinfo[1] = refGeoinfo[1]*(-1);
	}
	// Y
	if(refGeoinfo[5] < 0)
	{
		refGeoinfo[5] = refGeoinfo[5]*(-1);
	}
	//Image B
	// X
	if(floatGeoinfo[1] < 0)
	{
		floatGeoinfo[1] = floatGeoinfo[1]*(-1);
	}
	// Y
	if(floatGeoinfo[5] < 0)
	{
		floatGeoinfo[5] = floatGeoinfo[5]*(-1);
	}
	this->refPixelXres = refGeoinfo[1];
	this->refPixelYres = refGeoinfo[5];
	this->floatPixelXres = floatGeoinfo[1];
	this->floatPixelYres = floatGeoinfo[5];
	/*********************************************************************/
	
	/******************** TEST: Print GeoInfo for Both Images ********************
		std::cout << "After negative check.\n";
	std::cout << "Image A:.\n";
	std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
	std::cout << "Image B: \n";
	std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
	****************************************************************************/
	
	/**************** Checking  image rotation is the same ****************/
	if(refGeoinfo[2] != floatGeoinfo[2] | refGeoinfo[4] != floatGeoinfo[4])
	{
		throw ImageProcessingException("Pixel Resolution is different", 
									   error_codes::difference_rotation, 0);
	}
	else
	{
		//std::cout << "OK: Image rotation is the same in both images\n";
	}
	/************************************************************************/		
	
	/************** Calculate Images TL and BR Coords **********************/	
	// Coords for Image A:
	double imageACoords[4];
	int imageAPixels[4];
	double imageAXSize = imgA->GetRasterXSize() * refPixelXres;
	double imageAYSize = imgA->GetRasterYSize() * refPixelYres;
	
	imageACoords[0] = refGeoinfo[0];
	imageACoords[1] = refGeoinfo[3];
	imageACoords[2] = refGeoinfo[0] + imageAXSize;
	imageACoords[3] = refGeoinfo[3] - imageAYSize;
	
	imageAPixels[0] = 0;
	imageAPixels[1] = 0;
	imageAPixels[2] = imgA->GetRasterXSize();
	imageAPixels[3] = imgA->GetRasterYSize();
	
	// Coords for Image B:
	double imageBCoords[4];
	int imageBPixels[4];
	double imageBXSize = imgB->GetRasterXSize() * floatPixelXres;
	double imageBYSize = imgB->GetRasterYSize() * floatPixelYres;
	
	imageBCoords[0] = floatGeoinfo[0];
	imageBCoords[1] = floatGeoinfo[3];
	imageBCoords[2] = floatGeoinfo[0] + imageBXSize;
	imageBCoords[3] = floatGeoinfo[3] - imageBYSize;
	
	imageBPixels[0] = 0;
	imageBPixels[1] = 0;
	imageBPixels[2] = imgB->GetRasterXSize();
	imageBPixels[3] = imgB->GetRasterYSize();
	/************************************************************************/
	
	/*std::cout << "imageCoords: [" << imageAPixels[0] << ", " << imageAPixels[1] << "]["
			  << imageAPixels[2] << ", "<< imageAPixels[3]<<"]\n";
	std::cout << "imageCoords: [" << imageBPixels[0] << ", "<< imageBPixels[1] << "]["
		<< imageBPixels[2] << ", "<< imageBPixels[3]<<"]\n";*/
	
	
	/********* Calculate Calculate the pixel shift for floating image **********/
	
	//Calculate which image has high resolution
	double shiftXFloatImage = 0;
	double shiftYFloatImage = 0;
	double floatPixels4refpixelY = 0;
	double floatPixels4refpixelX = 0;
	int compareImageXRes = 0;
	int compareImageYRes = 0;
	
	// X Axis.
	if(refPixelXres == floatPixelXres)
	{
		// they are equal.
		shiftXFloatImage = xShiftFloat;
		compareImageXRes = 0;
	}
	else if(refPixelXres < floatPixelXres)
	{
		// floating image is a lower resolution than reference image.
		floatPixels4refpixelX = refPixelXres/floatPixelXres;
		shiftXFloatImage = xShiftFloat * floatPixels4refpixelX;
		compareImageXRes = 1;
	}
	else if(refPixelXres > floatPixelXres)
	{
		// floating image is a high resolution than reference image.
		floatPixels4refpixelX = floatPixelXres/refPixelXres;
		shiftXFloatImage = xShiftFloat;
		compareImageXRes = -1;
	}
	// Y Axis.
	if(refPixelYres == floatPixelYres)
	{
		// they are equal.
		shiftYFloatImage = yShiftFloat;
		compareImageYRes = 0;
	}
	else if(refPixelYres < floatPixelYres)
	{
		// floating image is a lower resolution than reference image.
		floatPixels4refpixelY = refPixelYres/floatPixelYres;
		shiftYFloatImage = yShiftFloat * floatPixels4refpixelY;
		compareImageYRes = 1;
	}
	else if(refPixelYres > floatPixelYres)
	{
		// floating image is a high resolution than reference image.
		floatPixels4refpixelY = floatPixelYres/refPixelYres;
		shiftYFloatImage = yShiftFloat;
		compareImageYRes = -1;
	}
	
	/************************************************************************/
	
	/************ Apply the Shift and Round Floating Result *****************/
	// Apply Shift
	double tileImgBCoordsFloat[4];
	tileImgBCoordsFloat[0] = tile->imgBTLX + shiftXFloatImage;
	tileImgBCoordsFloat[1] = tile->imgBTLY + shiftYFloatImage;
	tileImgBCoordsFloat[2] = tile->imgBBRX + shiftXFloatImage;
	tileImgBCoordsFloat[3] = tile->imgBBRY + shiftYFloatImage;
	// Round the result to nearest approapriate pixel.
	int tileImgBCoords[4];
	tileImgBCoords[0] = mathUtils.roundDown(tileImgBCoordsFloat[0]); // Round Down
	tileImgBCoords[1] = mathUtils.roundDown(tileImgBCoordsFloat[1]); // Round Down
	tileImgBCoords[2] = mathUtils.roundUp(tileImgBCoordsFloat[2]); // Round Up
	tileImgBCoords[3] = mathUtils.roundUp(tileImgBCoordsFloat[3]); // Round Up
	/************************************************************************/
	
	/*************** TEST: Print Shifted and Rounded result ****************
	std::cout << "tileImgBCoords (Before Shift)[" << tile->imgBTLX << "," << tile->imgBTLY
		      << "][" << tile->imgBBRX << "," << tile->imgBBRY << "]" << std::endl;
	std::cout << "tileImgBCoordsFloat (Float Shift)[" << tileImgBCoordsFloat[0] << "," << tileImgBCoordsFloat[1]
		      << "][" << tileImgBCoordsFloat[2] << "," << tileImgBCoordsFloat[3] << "]" << std::endl;
	std::cout << "TileImageBCoords (Rounded) [" << tileImgBCoords[0] << "," << tileImgBCoords[1]
		      << "][" << tileImgBCoords[2] << "," << tileImgBCoords[3] << "]" << std::endl;
	/************************************************************************/
	
	/*************** Check Shifted Tile is still within image B **************/
	if( compareImageXRes == 0 & compareImageYRes == 0)
	{
		int diff = 0;
		if(tileImgBCoords[0] < imageBPixels[0])
		{
			diff = imageBPixels[0] - tileImgBCoords[0];
			imgAPixelCoords[0] = tile->imgATLX + diff;
			imgBPixelCoords[0] = imageBPixels[0];
			overlapCoords[0] = tile->eastingTL + (diff * pixelXres);
		}
		else
		{
			imgAPixelCoords[0] = tile->imgATLX;
			imgBPixelCoords[0] = tileImgBCoords[0];
			overlapCoords[0] = tile->eastingTL;
		}
		
		if(tileImgBCoords[1] < imageBPixels[1])
		{
			diff = imageBPixels[1] - tileImgBCoords[1];
			imgAPixelCoords[1] = tile->imgATLY + diff;
			imgBPixelCoords[1] = imageBPixels[1];
			overlapCoords[1] = tile->northingTL - (diff * pixelYres);
		}
		else
		{
			imgAPixelCoords[1] = tile->imgATLY;
			imgBPixelCoords[1] = tileImgBCoords[1];
			overlapCoords[1] = tile->northingTL;
		}
		
		if(tileImgBCoords[2] > imageBPixels[2])
		{
			diff = tileImgBCoords[2] - imageBPixels[2];
			imgAPixelCoords[2] = tile->imgABRX - diff;
			imgBPixelCoords[2] = imageBPixels[2];
			overlapCoords[2] = tile->eastingBR - (diff * pixelXres);
		}
		else
		{
			imgAPixelCoords[2] = tile->imgABRX;
			imgBPixelCoords[2] = tileImgBCoords[2];
			overlapCoords[2] = tile->eastingBR;
		}
		
		if(tileImgBCoords[3] > imageBPixels[3])
		{
			diff = tileImgBCoords[3] - imageBPixels[3];
			imgAPixelCoords[3] = tile->imgABRY - diff;
			imgBPixelCoords[3] = imageBPixels[3];
			overlapCoords[3] = tile->northingBR + (diff * pixelYres);
		}
		else
		{
			imgAPixelCoords[3] = tile->imgABRY;
			imgBPixelCoords[3] = tileImgBCoords[3];
			overlapCoords[3] = tile->northingBR;
		}
	}
	else if( compareImageXRes == 1 & compareImageYRes == 1)
	{
		int diff = 0;
		int diffImageAPixels = 0;
		if(tileImgBCoords[0] < imageBPixels[0])
		{
			diff = imageBPixels[0] - tileImgBCoords[0];
			diffImageAPixels = mathUtils.roundDown(diff / floatPixels4refpixelX);
			imgAPixelCoords[0] = tile->imgATLX + diffImageAPixels;
			imgBPixelCoords[0] = imageBPixels[0];
			overlapCoords[0] = tile->eastingTL + (diff * floatPixelXres);
		}
		else
		{
			imgAPixelCoords[0] = tile->imgATLX;
			imgBPixelCoords[0] = tileImgBCoords[0];
			overlapCoords[0] = tile->eastingTL;
		}
		
		if(tileImgBCoords[1] < imageBPixels[1])
		{
			diff = imageBPixels[1] - tileImgBCoords[1];
			diffImageAPixels = mathUtils.roundDown(diff / floatPixels4refpixelY);
			imgAPixelCoords[1] = tile->imgATLY + diffImageAPixels;
			imgBPixelCoords[1] = imageBPixels[1];
			overlapCoords[1] = tile->northingTL - (diff * floatPixelYres);
		}
		else
		{
			imgAPixelCoords[1] = tile->imgATLY;
			imgBPixelCoords[1] = tileImgBCoords[1];
			overlapCoords[1] = tile->northingTL;
		}
		
		if(tileImgBCoords[2] > imageBPixels[2])
		{
			diff = tileImgBCoords[2] - imageBPixels[2];
			diffImageAPixels = mathUtils.roundUp(diff / floatPixels4refpixelX);
			imgAPixelCoords[2] = tile->imgABRX - diffImageAPixels;
			imgBPixelCoords[2] = imageBPixels[2];
			overlapCoords[2] = tile->eastingBR - (diff * floatPixelXres);
		}
		else
		{
			imgAPixelCoords[2] = tile->imgABRX;
			imgBPixelCoords[2] = tileImgBCoords[2];
			overlapCoords[2] = tile->eastingBR;
		}
		
		if(tileImgBCoords[3] > imageBPixels[3])
		{
			diff = tileImgBCoords[3] - imageBPixels[3];
			diffImageAPixels = mathUtils.roundUp(diff / floatPixels4refpixelY);
			imgAPixelCoords[3] = tile->imgABRY - diffImageAPixels;
			imgBPixelCoords[3] = imageBPixels[3];
			overlapCoords[3] = tile->northingBR + (diff * floatPixelYres);
		}
		else
		{
			imgAPixelCoords[3] = tile->imgABRY;
			imgBPixelCoords[3] = tileImgBCoords[3];
			overlapCoords[3] = tile->northingBR;
		}
	}
	else if( compareImageXRes == -1 & compareImageYRes == -1)
	{
		int diff = 0;
		int diffImageAPixels = 0;
		if(tileImgBCoords[0] < imageBPixels[0])
		{
			diff = imageBPixels[0] - tileImgBCoords[0];
			diffImageAPixels = mathUtils.roundDown(diff / floatPixels4refpixelX);
			imgAPixelCoords[0] = tile->imgATLX + diffImageAPixels;
			imgBPixelCoords[0] = imageBPixels[0];
			overlapCoords[0] = tile->eastingTL + (diff * floatPixelXres);
		}
		else
		{
			imgAPixelCoords[0] = tile->imgATLX;
			imgBPixelCoords[0] = tileImgBCoords[0];
			overlapCoords[0] = tile->eastingTL;
		}
		
		if(tileImgBCoords[1] < imageBPixels[1])
		{
			diff = imageBPixels[1] - tileImgBCoords[1];
			diffImageAPixels = mathUtils.roundDown(diff / floatPixels4refpixelY);
			imgAPixelCoords[1] = tile->imgATLY + diffImageAPixels;
			imgBPixelCoords[1] = imageBPixels[1];
			overlapCoords[1] = tile->northingTL - (diff * floatPixelYres);
		}
		else
		{
			imgAPixelCoords[1] = tile->imgATLY;
			imgBPixelCoords[1] = tileImgBCoords[1];
			overlapCoords[1] = tile->northingTL;
		}
		
		if(tileImgBCoords[2] > imageBPixels[2])
		{
			diff = tileImgBCoords[2] - imageBPixels[2];
			diffImageAPixels = mathUtils.roundUp(diff / floatPixels4refpixelX);
			imgAPixelCoords[2] = tile->imgABRX - diffImageAPixels;
			imgBPixelCoords[2] = imageBPixels[2];
			overlapCoords[2] = tile->eastingBR - (diff * floatPixelXres);
		}
		else
		{
			imgAPixelCoords[2] = tile->imgABRX;
			imgBPixelCoords[2] = tileImgBCoords[2];
			overlapCoords[2] = tile->eastingBR;
		}
		
		if(tileImgBCoords[3] > imageBPixels[3])
		{
			diff = tileImgBCoords[3] - imageBPixels[3];
			diffImageAPixels = mathUtils.roundUp(diff / floatPixels4refpixelY);
			imgAPixelCoords[3] = tile->imgABRY - diffImageAPixels;
			imgBPixelCoords[3] = imageBPixels[3];
			overlapCoords[3] = tile->northingBR + (diff * floatPixelYres);
		}
		else
		{
			imgAPixelCoords[3] = tile->imgABRY;
			imgBPixelCoords[3] = tileImgBCoords[3];
			overlapCoords[3] = tile->northingBR;
		}
	}
	else
	{
		std::cout << "BUGGER Error!! X and Y axis on one of the images have a different" <<
					" resolution! No code has been written to deal with this yet!\n";
	}
	/*********************************************************************/
	
	/*************************** TEST: Print coords *********************************
		std::cout << "xShiftFloat: " << xShiftFloat << " yShiftFloat: " << yShiftFloat << std::endl;
	std::cout << "Image A pixels: (" << imgAPixelCoords[0] << "," << imgAPixelCoords[1] << ")"
		      << "(" << imgAPixelCoords[2] << "," << imgAPixelCoords[3] << ")\n";
	std::cout << "Image B pixels: (" << imgBPixelCoords[0] << "," << imgBPixelCoords[1] << ")"
		      << "(" << imgBPixelCoords[2] << "," << imgBPixelCoords[3] << ")\n";
	std::cout << "Geo Coords: (" << overlapCoords[0] << "," << overlapCoords[1] << ")"
		      << "(" << overlapCoords[2] << "," << overlapCoords[3] << ")\n";
	/*********************************************************************/  
}	

void ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(GDALDataset *imgA, 
															   GDALDataset *imgB, 
															   double xShiftFloat, 
															   double yShiftFloat, 
															   TileCoords *tile)
throw(ImageNotAvailableException, ImageProcessingException)
{
	MathUtils mathUtils;
	
	/******************* Checking Images are NOT NULL ********************/
	if(imgA == NULL)
	{
		throw ImageNotAvailableException("Image A is not availble.", error_codes::reference_image);
	}
	else if(imgB == NULL)
	{
		throw ImageNotAvailableException("Image B is not availble.", error_codes::floating_image);
	}
	else
	{
		//std::cout << "OK: Got images\n";
	}
	/**********************************************************************/
	
	/********** Getting Georeferencing info for reference Image ***********/
	double refGeoinfo[6];
	if(imgA->GetGeoTransform(refGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Reference Image has geo info.\n";
		std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image A does not have any geoinfo", 
									   error_codes::no_projection, error_codes::reference_image);
	}
	/*****************************************************************************/
	
	/************ Getting Georeferencing info for floating Image ***************/
	double floatGeoinfo[6];
	if(imgB->GetGeoTransform(floatGeoinfo) == CE_None)
	{
		/******************** TEST: Print out geoinfo ********************
		std::cout << "OK: Floating Image has geo info.\n";
		std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
		std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
		std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
		std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
		std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
		std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
		/*********************************************************************/
	}
	else
	{
		throw ImageProcessingException("Image B does not have any geoinfo", 
									   error_codes::no_projection, error_codes::floating_image);
	}
	/*******************************************************************************/
	// Image A.
	// X
	if(refGeoinfo[1] < 0)
	{
		refGeoinfo[1] = refGeoinfo[1]*(-1);
	}
	// Y
	if(refGeoinfo[5] < 0)
	{
		refGeoinfo[5] = refGeoinfo[5]*(-1);
	}
	//Image B
	// X
	if(floatGeoinfo[1] < 0)
	{
		floatGeoinfo[1] = floatGeoinfo[1]*(-1);
	}
	// Y
	if(floatGeoinfo[5] < 0)
	{
		floatGeoinfo[5] = floatGeoinfo[5]*(-1);
	}
	/****************** Checking  pixel resolution is the same ********************/
	if(refGeoinfo[1] != floatGeoinfo[1] | refGeoinfo[5] != floatGeoinfo[5])
	{
		throw ImageProcessingException("Pixel Resolution is different", 
									   error_codes::different_pixel_resolution, 0);
	}
	else
	{
		/**** Checking for negative values, if present convert to positive. *******/
		//std::cout << "OK: Pixel resolution the same in both images\n";
		
		
		this->pixelXres = refGeoinfo[1];
		this->pixelYres = refGeoinfo[5];
		//std::cout << "OK: Pixel resolution all positive values\n";
		/****************************************************************************/
	}
	/*********************************************************************/
	
	/******************** TEST: Print GeoInfo for Both Images ********************
		std::cout << "After negative check.\n";
	std::cout << "Image A:.\n";
	std::cout << "Top Left X coord: " << refGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << refGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << refGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << refGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << refGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << refGeoinfo[4] << std::endl;
	std::cout << "Image B: \n";
	std::cout << "Top Left X coord: " << floatGeoinfo[0] << std::endl;
	std::cout << "Top Left Y coord: " << floatGeoinfo[3] << std::endl;
	std::cout << "eastings pixel resolution: " << floatGeoinfo[1] << std::endl;
	std::cout << "northings pixel resolution: " << floatGeoinfo[5] << std::endl;
	std::cout << "rotation (e-w) (0 == NORTH): " << floatGeoinfo[2] << std::endl;
	std::cout << "rotation (n-s) (0 == NORTH): " << floatGeoinfo[4] << std::endl;
	****************************************************************************/
	
	/**************** Checking  image rotation is the same ****************/
	if(refGeoinfo[2] != floatGeoinfo[2] | refGeoinfo[4] != floatGeoinfo[4])
	{
		throw ImageProcessingException("Pixel Resolution is different", 
									   error_codes::difference_rotation, 0);
	}
	else
	{
		//std::cout << "OK: Image rotation is the same in both images\n";
	}
	/************************************************************************/		
	
	/************** Calculate Images TL and BR Coords **********************/	
	// Coords for Image A:
	double imageACoords[4];
	int imageAPixels[4];
	double imageAXSize = imgA->GetRasterXSize() * pixelXres;
	double imageAYSize = imgA->GetRasterYSize() * pixelYres;
	
	imageACoords[0] = refGeoinfo[0];
	imageACoords[1] = refGeoinfo[3];
	imageACoords[2] = refGeoinfo[0] + imageAXSize;
	imageACoords[3] = refGeoinfo[3] - imageAYSize;
	
	imageAPixels[0] = 0;
	imageAPixels[1] = 0;
	imageAPixels[2] = imgA->GetRasterXSize();
	imageAPixels[3] = imgA->GetRasterYSize();
	
	// Coords for Image B:
	double imageBCoords[4];
	int imageBPixels[4];
	double imageBXSize = imgB->GetRasterXSize() * pixelXres;
	double imageBYSize = imgB->GetRasterYSize() * pixelYres;
	
	imageBCoords[0] = floatGeoinfo[0];
	imageBCoords[1] = floatGeoinfo[3];
	imageBCoords[2] = floatGeoinfo[0] + imageBXSize;
	imageBCoords[3] = floatGeoinfo[3] - imageBYSize;
	
	imageBPixels[0] = 0;
	imageBPixels[1] = 0;
	imageBPixels[2] = imgB->GetRasterXSize();
	imageBPixels[3] = imgB->GetRasterYSize();
	/************************************************************************/
	
	/************* TEST: PRINT xShift and yShift ***************************
		std::cout << "xShiftFloat: " << xShiftFloat << " yShiftFloat: " << yShiftFloat << std::endl;
	/************************************************************************/
	
	/************ Apply the Shift and Round Floating Result *****************/
	// Apply Shift
	double tileImgBCoordsFloat[4];
	tileImgBCoordsFloat[0] = tile->imgBTLX + xShiftFloat;
	tileImgBCoordsFloat[1] = tile->imgBTLY + yShiftFloat;
	tileImgBCoordsFloat[2] = tile->imgBBRX + xShiftFloat;
	tileImgBCoordsFloat[3] = tile->imgBBRY + yShiftFloat;
	// Round the result to nearest approapriate pixel.
	int tileImgBCoords[4];
	tileImgBCoords[0] = mathUtils.roundDown(tileImgBCoordsFloat[0]); // Round Down
	tileImgBCoords[1] = mathUtils.roundDown(tileImgBCoordsFloat[1]); // Round Down
	tileImgBCoords[2] = mathUtils.roundUp(tileImgBCoordsFloat[2]); // Round Up
	tileImgBCoords[3] = mathUtils.roundUp(tileImgBCoordsFloat[3]); // Round Up
	/************************************************************************/
	
	/*************** TEST: Print Shifted and Rounded result ****************
	std::cout << "tileImgBCoords (Before Shift)[" << tile->imgBTLX << "," << tile->imgBTLY
		      << "][" << tile->imgBBRX << "," << tile->imgBBRY << "]" << std::endl;
	std::cout << "tileImgBCoordsFloat (Float Shift)[" << tileImgBCoordsFloat[0] << "," << tileImgBCoordsFloat[1]
		      << "][" << tileImgBCoordsFloat[2] << "," << tileImgBCoordsFloat[3] << "]" << std::endl;
	std::cout << "TileImageBCoords (Rounded) [" << tileImgBCoords[0] << "," << tileImgBCoords[1]
		      << "][" << tileImgBCoords[2] << "," << tileImgBCoords[3] << "]" << std::endl;
	/************************************************************************/
	
	/*************** Check Shifted Tile is still within image B **************/
	int diff = 0;
	if(tileImgBCoords[0] < imageBPixels[0])
	{
		diff = imageBPixels[0] - tileImgBCoords[0];
		imgAPixelCoords[0] = tile->imgATLX + diff;
		imgBPixelCoords[0] = imageBPixels[0];
		overlapCoords[0] = tile->eastingTL + (diff * pixelXres);
	}
	else
	{
		imgAPixelCoords[0] = tile->imgATLX;
		imgBPixelCoords[0] = tileImgBCoords[0];
		overlapCoords[0] = tile->eastingTL;
	}
	
	if(tileImgBCoords[1] < imageBPixels[1])
	{
		diff = imageBPixels[1] - tileImgBCoords[1];
		imgAPixelCoords[1] = tile->imgATLY + diff;
		imgBPixelCoords[1] = imageBPixels[1];
		overlapCoords[1] = tile->northingTL - (diff * pixelYres);
	}
	else
	{
		imgAPixelCoords[1] = tile->imgATLY;
		imgBPixelCoords[1] = tileImgBCoords[1];
		overlapCoords[1] = tile->northingTL;
	}
	
	if(tileImgBCoords[2] > imageBPixels[2])
	{
		diff = tileImgBCoords[2] - imageBPixels[2];
		imgAPixelCoords[2] = tile->imgABRX - diff;
		imgBPixelCoords[2] = imageBPixels[2];
		overlapCoords[2] = tile->eastingBR - (diff * pixelXres);
	}
	else
	{
		imgAPixelCoords[2] = tile->imgABRX;
		imgBPixelCoords[2] = tileImgBCoords[2];
		overlapCoords[2] = tile->eastingBR;
	}
	
	if(tileImgBCoords[3] > imageBPixels[3])
	{
		diff = tileImgBCoords[3] - imageBPixels[3];
		imgAPixelCoords[3] = tile->imgABRY - diff;
		imgBPixelCoords[3] = imageBPixels[3];
		overlapCoords[3] = tile->northingBR + (diff * pixelYres);
	}
	else
	{
		imgAPixelCoords[3] = tile->imgABRY;
		imgBPixelCoords[3] = tileImgBCoords[3];
		overlapCoords[3] = tile->northingBR;
	}
	/*********************************************************************/
	
	/*************************** TEST: Print coords *********************************
	std::cout << "xShiftFloat: " << xShiftFloat << " yShiftFloat: " << yShiftFloat << std::endl;
	std::cout << "Image A pixels: (" << imgAPixelCoords[0] << "," << imgAPixelCoords[1] << ")"
		      << "(" << imgAPixelCoords[2] << "," << imgAPixelCoords[3] << ")\n";
	std::cout << "Image B pixels: (" << imgBPixelCoords[0] << "," << imgBPixelCoords[1] << ")"
		      << "(" << imgBPixelCoords[2] << "," << imgBPixelCoords[3] << ")\n";
	std::cout << "Geo Coords: (" << overlapCoords[0] << "," << overlapCoords[1] << ")"
		      << "(" << overlapCoords[2] << "," << overlapCoords[3] << ")\n";
	/*********************************************************************/   
}

int* ImageOverlap::getImageAPixelCoords()
{
	return imgAPixelCoords;
}

int* ImageOverlap::getImageBPixelCoords()
{
	return imgBPixelCoords;
}

double* ImageOverlap::getOverlapGeoCoords()
{
	return overlapCoords;
}

int ImageOverlap::getNumPixels()
{
	return ((imgAPixelCoords[2] - imgAPixelCoords[0]) * (imgAPixelCoords[3] - imgAPixelCoords[1]));
}

int ImageOverlap::getSizeXPixelsA()
{
	return imgAPixelCoords[2] - imgAPixelCoords[0];
}

int ImageOverlap::getSizeYPixelsA()
{
	return imgAPixelCoords[3] - imgAPixelCoords[1];
}

int ImageOverlap::getSizeXPixelsB()
{
	return imgBPixelCoords[2] - imgBPixelCoords[0];
}

int ImageOverlap::getSizeYPixelsB()
{
	return imgBPixelCoords[3] - imgBPixelCoords[1];
}

void ImageOverlap::printOverlappingArea(bool singleLine)
{
	if(singleLine)
	{
		std::cout << "[" << imgAPixelCoords[0] << "," << imgAPixelCoords[1] << "," 
						<< imgAPixelCoords[2] << "," << imgAPixelCoords[3] << "]\n["
						<< imgBPixelCoords[0] << "," << imgBPixelCoords[1] << ","
						<< imgBPixelCoords[2] << "," << imgBPixelCoords[3] << "]\n";
	}
	else
	{
		std::cout << "Image A:\n";
		std::cout << "[" << imgAPixelCoords[0] << ", " << imgAPixelCoords[1] << "] ";
		std::cout << "[" << imgAPixelCoords[2] << ", " << imgAPixelCoords[3] << "]\n";
		
		std::cout << "Image B:\n";
		std::cout << "[" << imgBPixelCoords[0] << ", " << imgBPixelCoords[1] << "]";
		std::cout << "[" << imgBPixelCoords[2] << ", " << imgBPixelCoords[3] << "]\n";
		
		std::cout << "Geo Coords:\n";
		std::cout << "[" << overlapCoords[0] << ", " << overlapCoords[1] << "] ";
		std::cout << "[" << overlapCoords[2] << ", " << overlapCoords[3] << "]\n";
	}
}


void ImageOverlap::findtiles(TileCoords *tile, TileCoords *tiles)
{
	/************* Calc Image Size In Pixels **********************/
	int differenceX = tile->imgABRX - tile->imgATLX;
	int differenceY = tile->imgABRY - tile->imgATLY;
	/**************************************************************/
	
	/***************** TEST: Print Differences ********************
	std::cout << "Difference X: " << differenceX << std::endl;
	std::cout << "Difference Y: " << differenceY << std::endl;
	/*************************************************************/
	
	/************ Find Pixel coordinates for tiles **************/
	int tileWidth = differenceX/3;
	int tileHeight = differenceY/3;
	
	if(tileWidth*3 < differenceX) // Check for rounding down
	{
		tileWidth++;
	}
	if(tileHeight*3 < differenceY) //Check for rounding down
	{
		tileHeight++;
	}
	/*************************************************************/
	
	/**************** Calc tile width in metres *****************/
	double tileWidthMetres = tileWidth * pixelXres;
	double tileHeightMetres = tileHeight * pixelYres;
	/************************************************************/
	
	/************ TEST: Print tile Width and Heights ************
	std::cout << "\n\ntileWidth: " << tileWidth << std::endl;
	std::cout << "tileHeight: " << tileHeight << std::endl;
	
	std::cout << "tileWidth (metres): " << tileWidthMetres << std::endl;
	std::cout << "tileHeight (metres): " << tileHeightMetres << std::endl;
	/*************************************************************/
	
	/****************** Calc Pixel Tile Coords ******************/
	int counter = 0;
	for(int i = 0; i < 3; i++)
	{
		for(int j = 0; j < 3; j++)
		{
			// Top Left
			
			// X
			tiles[counter].imgATLX = tile->imgATLX + (j*tileWidth);
			tiles[counter].imgBTLX = tile->imgBTLX + (j*tileWidth);
			tiles[counter].eastingTL = tile->eastingTL + (j*tileWidthMetres);
			
			// Y
			tiles[counter].imgATLY = tile->imgATLY + (i*tileHeight);
			tiles[counter].imgBTLY = tile->imgBTLY + (i*tileHeight);
			tiles[counter].northingTL = tile->northingTL - (i*tileHeightMetres);
			
			
			// Bottom Right
			if( j == 2 ) // X
			{
				tiles[counter].imgABRX = tile->imgABRX;
				tiles[counter].imgBBRX = tile->imgBBRX;
				tiles[counter].eastingBR = tile->eastingBR;
			}
			else
			{
				tiles[counter].imgABRX = (tile->imgATLX+tileWidth) + (j*tileWidth);
				tiles[counter].imgBBRX = (tile->imgBTLX+tileWidth) + (j*tileWidth);
				tiles[counter].eastingBR = (tile->eastingTL+tileWidthMetres) + 
					(j*tileWidthMetres);
			}
			
			if( i == 2 )  // Y
			{
				tiles[counter].imgABRY = tile->imgABRY;
				tiles[counter].imgBBRY = tile->imgBBRY;
				tiles[counter].northingBR = tile->northingBR;
			}
			else
			{
				tiles[counter].imgABRY = (tile->imgATLY+tileHeight) + (i*tileHeight);
				tiles[counter].imgBBRY = (tile->imgBTLY+tileHeight) + (i*tileHeight);
				tiles[counter].northingBR = (tile->northingTL-tileHeightMetres) - 
					(i*tileHeightMetres);
			}
			counter++;
		}
	}
	/************************************************************/
	
	/*************** TEST: Print tile boundaries ****************
	for(int i= 0; i < 9; i++)
	{
			std::cout << "\n Tile " << i << ":\n";
			std::cout << " Image A:\n";
			std::cout << "[" << tiles[i].imgATLX << ", " << tiles[i].imgATLY << "] [" 
		          << tiles[i].imgABRX << ", " << tiles[i].imgABRY << "]\n";
			std::cout << " Image B:\n";
			std::cout << "[" << tiles[i].imgBTLX << ", " << tiles[i].imgBTLY << "] ["
		          << tiles[i].imgBBRX << ", " << tiles[i].imgBBRY << "]\n";
			std::cout << " Geo Coords:\n";
			std::cout << "[" << tiles[i].eastingTL << ", " << tiles[i].northingTL << "] [" 
			<< tiles[i].eastingBR << ", " << tiles[i].northingBR << "]\n";
	}
	/************************************************************/
}

void ImageOverlap::findtiles(TileCoords *tile, TileCoords *tiles, Transform transform)
{
	MathUtils mathUtils;
	/************* Calc Image Size In Pixels **********************/
	int differenceX = tile->imgABRX - tile->imgATLX;
	int differenceY = tile->imgABRY - tile->imgATLY;
	/**************************************************************/
	
	/***************** TEST: Print Differences ********************
		std::cout << "Difference X: " << differenceX << std::endl;
	std::cout << "Difference Y: " << differenceY << std::endl;
	/*************************************************************/
	
	/************ Find Pixel coordinates for tiles **************/
	int tileWidth = differenceX/3;
	int tileHeight = differenceY/3;
	
	if(tileWidth*3 < differenceX) // Check for rounding down
	{
		tileWidth++;
	}
	if(tileHeight*3 < differenceY) //Check for rounding down
	{
		tileHeight++;
	}
	/*************************************************************/
	
	/**************** Calc tile width in metres *****************/
	double tileWidthMetres = tileWidth * pixelXres;
	double tileHeightMetres = tileHeight * pixelYres;
	/************************************************************/
	
	/************ TEST: Print tile Width and Heights ************
		std::cout << "\n\ntileWidth: " << tileWidth << std::endl;
	std::cout << "tileHeight: " << tileHeight << std::endl;
	
	std::cout << "tileWidth (metres): " << tileWidthMetres << std::endl;
	std::cout << "tileHeight (metres): " << tileHeightMetres << std::endl;
	/*************************************************************/
	
	/****************** Calc Pixel Tile Coords ******************/
	int counter = 0;
	for(int i = 0; i < 3; i++)
	{
		for(int j = 0; j < 3; j++)
		{
			// Top Left
			
			// X
			tiles[counter].imgATLX = tile->imgATLX + (j*tileWidth);
			tiles[counter].imgBTLX = tile->imgBTLX + (j*tileWidth) 
									+ mathUtils.round(transform.shiftX);
			tiles[counter].eastingTL = tile->eastingTL + (j*tileWidthMetres);
			
			// Y
			tiles[counter].imgATLY = tile->imgATLY + (i*tileHeight);
			tiles[counter].imgBTLY = tile->imgBTLY + (i*tileHeight) 
									+ mathUtils.round(transform.shiftY);
			tiles[counter].northingTL = tile->northingTL - (i*tileHeightMetres);
			
			
			// Bottom Right
			if( j == 2 ) // X
			{
				tiles[counter].imgABRX = tile->imgABRX;
				tiles[counter].imgBBRX = tile->imgBBRX + mathUtils.round(transform.shiftX);
				tiles[counter].eastingBR = tile->eastingBR;
			}
			else
			{
				tiles[counter].imgABRX = (tile->imgATLX+tileWidth) + (j*tileWidth);
				tiles[counter].imgBBRX = (tile->imgBTLX+tileWidth) + (j*tileWidth) 
										+ mathUtils.round(transform.shiftX);
				tiles[counter].eastingBR = (tile->eastingTL+tileWidthMetres) + 
					(j*tileWidthMetres);
			}
			
			if( i == 2 )  // Y
			{
				tiles[counter].imgABRY = tile->imgABRY;
				tiles[counter].imgBBRY = tile->imgBBRY + mathUtils.round(transform.shiftY);
				tiles[counter].northingBR = tile->northingBR;
			}
			else
			{
				tiles[counter].imgABRY = (tile->imgATLY+tileHeight) + (i*tileHeight);
				tiles[counter].imgBBRY = (tile->imgBTLY+tileHeight) + (i*tileHeight) 
										+ mathUtils.round(transform.shiftY);
				tiles[counter].northingBR = (tile->northingTL-tileHeightMetres) - 
					(i*tileHeightMetres);
			}
			counter++;
		}
	}
	/************************************************************/
	
	/*************** TEST: Print tile boundaries ****************
		for(int i= 0; i < 9; i++)
	{
			std::cout << "\n Tile " << i << ":\n";
			std::cout << " Image A:\n";
			std::cout << "[" << tiles[i].imgATLX << ", " << tiles[i].imgATLY << "] [" 
		          << tiles[i].imgABRX << ", " << tiles[i].imgABRY << "]\n";
			std::cout << " Image B:\n";
			std::cout << "[" << tiles[i].imgBTLX << ", " << tiles[i].imgBTLY << "] ["
		          << tiles[i].imgBBRX << ", " << tiles[i].imgBBRY << "]\n";
			std::cout << " Geo Coords:\n";
			std::cout << "[" << tiles[i].eastingTL << ", " << tiles[i].northingTL << "] [" 
			<< tiles[i].eastingBR << ", " << tiles[i].northingBR << "]\n";
	}
	/************************************************************/
}

void ImageOverlap::findtilesDiffResolution(TileCoords *tile, TileCoords *tiles, Transform transform)
{
	//std::cout << "[" << tile->imgATLX << ", " << tile->imgATLY << "][" << tile->imgABRX << ", " << tile->imgABRY << "]\n";
	//std::cout << "[" << tile->imgBTLX << ", " << tile->imgBTLY << "][" << tile->imgBBRX << ", " << tile->imgBBRY << "]\n";
	//std::cout << "[" << tile->eastingTL << ", " << tile->northingTL << "][" << tile->eastingBR << ", " << tile->northingBR << "]\n";
	
	
	MathUtils mathUtils;
	/************* Calc Image Size In Pixels **********************/
	int imgADifferenceX = 0;
	int imgADifferenceY = 0;
	int imgBDifferenceX = 0;
	int imgBDifferenceY = 0;
	imgADifferenceX = tile->imgABRX - tile->imgATLX;
	imgADifferenceY = tile->imgABRY - tile->imgATLY;
	imgBDifferenceX = tile->imgBBRX - tile->imgBTLX;
	imgBDifferenceY = tile->imgBBRY - tile->imgBTLY;
	/**************************************************************/
	
	/***************** TEST: Print Differences ********************
	std::cout << "imgADifferenceX: " << imgADifferenceX << std::endl;
	std::cout << "imgADifferenceY: " << imgADifferenceY << std::endl;
	/*************************************************************/
	/***************** TEST: Print Differences ********************
	std::cout << "imgBDifferenceX: " << imgBDifferenceX << std::endl;
	std::cout << "imgBDifferenceY: " << imgBDifferenceY << std::endl;
	/*************************************************************/
	
	/************ Find Pixel coordinates for tiles **************/
	int imgAtileWidth = 0;
	int imgAtileHeight = 0;
	imgAtileWidth = imgADifferenceX/3;
	imgAtileHeight = imgADifferenceY/3;
	
	/************ TEST: Print tile Width and Heights ************
	std::cout << "BEFORE\nimgAtileWidth: " << imgAtileWidth << "imgAtileWidth*3 = " << imgAtileWidth*3 << std::endl;
	std::cout << "imgAtileHeight: " << imgAtileHeight << "imgAtileHeight*3  = " << imgAtileHeight*3 << std::endl;
	/*************************************************************/
	
	if(imgAtileWidth*3 < imgADifferenceX) // Check for rounding down
	{
		imgAtileWidth++;
	}
	if(imgAtileHeight*3 < imgADifferenceY) //Check for rounding down
	{
		imgAtileHeight++;
	}
	
	int imgBtileWidth = 0;
	int imgBtileHeight = 0;
	imgBtileWidth = imgBDifferenceX/3;
	imgBtileHeight = imgBDifferenceY/3;
	
	if(imgBtileWidth*3 < imgBDifferenceX) // Check for rounding down
	{
		imgBtileWidth++;
	}
	if(imgBtileHeight*3 < imgBDifferenceY) //Check for rounding down
	{
		imgBtileHeight++;
	}
	/*************************************************************/
	
	/************ Calc tile width and heightin metres ************/
	double imgAtileWidthMetres = 0;
	double imgAtileHeightMetres = 0;
	imgAtileWidthMetres = imgAtileWidth * refPixelXres;
	imgAtileHeightMetres = imgAtileHeight * refPixelYres;
	/************************************************************/
	
	/*********** Adjust Shift for image Resolution ***************/
	int xShift = 0;
	int yShift = 0;
	if(refPixelXres < floatPixelXres)
	{
		xShift = mathUtils.round((refPixelXres/floatPixelXres)*transform.shiftX);
		yShift = mathUtils.round((refPixelYres/floatPixelYres)*transform.shiftY);
	}
	else
	{
		xShift = mathUtils.round(transform.shiftX);
		yShift = mathUtils.round(transform.shiftY);
	}
	/*************************************************************/
	
	/************ TEST: Print tile Width and Heights ************
	std::cout << "imgAtileWidth: " << imgAtileWidth << std::endl;
	std::cout << "imgAtileHeight: " << imgAtileHeight << std::endl;
	std::cout << "imgBtileWidth: " << imgBtileWidth << std::endl;
	std::cout << "imgBtileHeight: " << imgBtileHeight << std::endl;
	
	std::cout << "tileWidth (metres): " << imgAtileWidthMetres << std::endl;
	std::cout << "tileHeight (metres): " << imgAtileHeightMetres << std::endl;
	/*************************************************************/
	
	/******************* Shifts ********************************
	std::cout << "Uncorrected Shift = [" << transform.shiftX << ", " << transform.shiftY << "]\n";
	std::cout << "Corrected Shift = [" << xShift << ", " << yShift << "]\n";
	/************************************************************/
	
	/****************** Calc Pixel Tile Coords ******************/
	int counter = 0;
	for(int i = 0; i < 3; i++)
	{
		for(int j = 0; j < 3; j++)
		{
			// Top Left
			
			// X
			tiles[counter].imgATLX = tile->imgATLX + (j*imgAtileWidth);
			tiles[counter].imgBTLX = tile->imgBTLX + (j*imgBtileWidth) 
				+ xShift;
			tiles[counter].eastingTL = tile->eastingTL + (j*imgAtileWidthMetres);
			
			// Y
			tiles[counter].imgATLY = tile->imgATLY + (i*imgAtileHeight);
			tiles[counter].imgBTLY = tile->imgBTLY + (i*imgBtileHeight) 
				+ yShift;
			tiles[counter].northingTL = tile->northingTL - (i*imgAtileHeightMetres);
			
			
			// Bottom Right
			if( j == 2 ) // X
			{
				tiles[counter].imgABRX = tile->imgABRX;
				tiles[counter].imgBBRX = tile->imgBBRX + xShift;
				tiles[counter].eastingBR = tile->eastingBR;
			}
			else
			{
				tiles[counter].imgABRX = (tile->imgATLX+imgAtileWidth) + (j*imgAtileWidth);
				tiles[counter].imgBBRX = (tile->imgBTLX+imgBtileWidth) + (j*imgBtileWidth) 
					+ xShift;
				tiles[counter].eastingBR = (tile->eastingTL+imgAtileWidthMetres) + 
					(j*imgAtileWidthMetres);
			}
			
			if( i == 2 )  // Y
			{
				tiles[counter].imgABRY = tile->imgABRY;
				tiles[counter].imgBBRY = tile->imgBBRY + yShift;
				tiles[counter].northingBR = tile->northingBR;
			}
			else
			{
				tiles[counter].imgABRY = (tile->imgATLY+imgAtileHeight) + (i*imgAtileHeight);
				tiles[counter].imgBBRY = (tile->imgBTLY+imgBtileHeight) + (i*imgBtileHeight) 
					+ yShift;
				tiles[counter].northingBR = (tile->northingTL-imgAtileHeightMetres) - 
					(i*imgAtileHeightMetres);
			}
			counter++;
		}
	}
	/************************************************************/
	
	/*************** TEST: Print tile boundaries ****************
		for(int i= 0; i < 9; i++)
	{
			std::cout << "\n Tile " << i << ":\n";
			std::cout << " Image A:\n";
			std::cout << "[" << tiles[i].imgATLX << ", " << tiles[i].imgATLY << "] [" 
		          << tiles[i].imgABRX << ", " << tiles[i].imgABRY << "]\n";
			std::cout << " Image B:\n";
			std::cout << "[" << tiles[i].imgBTLX << ", " << tiles[i].imgBTLY << "] ["
		          << tiles[i].imgBBRX << ", " << tiles[i].imgBBRY << "]\n";
			std::cout << " Geo Coords:\n";
			std::cout << "[" << tiles[i].eastingTL << ", " << tiles[i].northingTL << "] [" 
			<< tiles[i].eastingBR << ", " << tiles[i].northingBR << "]\n";
	}
	/************************************************************/
}

double ImageOverlap::getRefPixelXRes()
{
	return refPixelXres;
}

double ImageOverlap::getRefPixelYRes()
{
	return refPixelYres;
}

double ImageOverlap::getFloatPixelXRes()
{
	return floatPixelXres;
}

double ImageOverlap::getFloatPixelYRes()
{
	return floatPixelXres;
}

double ImageOverlap::getPixelXRes()
{
	return pixelXres;
}
double ImageOverlap::getPixelYRes()
{
	return pixelYres;
}

ImageOverlap::~ImageOverlap()
{
}
