/*
 *  ImagePyramid.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 09/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "ImagePyramid.h"

ImagePyramid::ImagePyramid()
{
	
}

void ImagePyramid::constructImagePyramid(GDALDataset *imageA, 
										 GDALDataset *imageB, 
										 int numLevels, 
										 float *levelScales,
										 int *windowLevel,
										 int imageABand,
										 int imageBBand,
										 const char *outputPath)
	throw(ImageNotAvailableException, 
		  ImageProcessingException,
		  ImageOutputException)
{
		Interpolation interpolation;
		const char *format = "GTIFF";
		pyramid = new PyramidLevel[numLevels];
		this->numberOfLevels = numLevels;
		
		/******************** Check inputs are correct ****************/
		if(imageA == NULL)
		{
			throw ImageNotAvailableException("Image A was NULL.", 
											 error_codes::reference_image);
		}
		else if(imageB == NULL)
		{
			throw ImageNotAvailableException("Image B was NULL.", 
											 error_codes::floating_image);
		}
		else
		{
			//Images OK continue..
		}
		
		if(imageABand > imageA->GetRasterCount())
		{
			throw ImageProcessingException("Not enough bands in image A ", 
										   error_codes::insufficent_num_bands, 
										   error_codes::reference_image);
		}
		else
		{
			// Image A Got sufficent bands, continue..
		}
		
		if(imageBBand > imageB->GetRasterCount())
		{
			throw ImageProcessingException("Not enough bands in Image B", 
										   error_codes::insufficent_num_bands, 
										   error_codes::floating_image);
		}
		else
		{
			// Image B Got sufficent bands, continue..
		}
		
		/**********************************************************************/
		
		/************************ Get Image Resolutions ***********************/
		double imgAXPixelRes = 0;
		double imgAYPixelRes = 0;
		double imgBXPixelRes = 0;
		double imgBYPixelRes = 0;
		
		double *trans1 = new double[6];
		imageA->GetGeoTransform(trans1);	
		if(trans1[1] < 0)
		{
			trans1[1] = trans1[1]*(-1);
		}
		if(trans1[5] < 0)
		{
			trans1[5] = trans1[5]*(-1);
		}
		double *trans2 = new double[6];
		imageB->GetGeoTransform(trans2);	
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
		/**********************************************************************/
		
		double baseResX = 0;
		double baseResY = 0;
		
		bool imageAHighestXRes = true;
		bool imageAHighestYRes = true;
		bool equalImageReg = false;
		
		if( imgAXPixelRes == imgBXPixelRes &
			imgAYPixelRes == imgBYPixelRes)
		{
			equalImageReg= true;
			baseResX = imgAXPixelRes;
			baseResY = imgAYPixelRes;
		}
		else
		{
			equalImageReg = false;
			if(imgAXPixelRes < imgBXPixelRes)
			{
				imageAHighestXRes = true;
				baseResX = imgAXPixelRes;
			}
			else
			{
				imageAHighestXRes = false;
				baseResX = imgBXPixelRes;
			}
			
			if(imgAYPixelRes < imgBYPixelRes)
			{
				imageAHighestYRes = true;
				baseResY = imgAYPixelRes;
			}
			else
			{
				imageAHighestYRes = false;
				baseResY = imgBYPixelRes;
			}
			
			if(imageAHighestXRes != imageAHighestYRes)
			{
				throw new ImageProcessingException("Highest resolution axis are in different images",
												   error_codes::xy_resolutions_different, -1);
			}
		}
		
		char tmpFilePath[3000];
		pyramid[0].level = 0;
		pyramid[0].windowSize = windowLevel[0];
		if(equalImageReg)
		{
			// Copy band from Image A
			strcpy(tmpFilePath, outputPath);
			strcat(tmpFilePath, "imageA_0.tif");
			pyramid[0].imageA = interpolation.copyImageBand(imageA, tmpFilePath, format, imageABand);
			
			// Copy band from Image B
			strcpy(tmpFilePath, outputPath);
			strcat(tmpFilePath, "imageB_0.tif");
			pyramid[0].imageB = interpolation.copyImageBand(imageB, tmpFilePath, format, imageBBand);
		}
		else
		{
			if(imageAHighestXRes)
			{
				// Copy band from Image A
				strcpy(tmpFilePath, outputPath);
				strcat(tmpFilePath, "imageA_0.tif");
				pyramid[0].imageA = interpolation.copyImageBand(imageA, tmpFilePath, format, imageABand);
				
				// Interpolate band from Image B
				strcpy(tmpFilePath, outputPath);
				strcat(tmpFilePath, "imageB_0.tif");
				pyramid[0].imageB = interpolation.createNewImage(imageB, baseResX, baseResY, tmpFilePath, format, imageBBand);
			}
			else
			{
				// Copy band from Image B
				strcpy(tmpFilePath, outputPath);
				strcat(tmpFilePath, "imageB_0.tif");
				pyramid[0].imageB = interpolation.copyImageBand(imageB, tmpFilePath, format, imageBBand);
				
				// Interpolate band from Image A
				strcpy(tmpFilePath, outputPath);
				strcat(tmpFilePath, "imageA_0.tif");
				pyramid[0].imageA =interpolation.createNewImage(imageA, baseResX, baseResY, tmpFilePath, format, imageABand);
			}
		}
		
		pyramid[0].imgOverlap = new ImageOverlap(pyramid[0].imageA, pyramid[0].imageB);
		pyramid[0].imageRes = baseResX;
		
		double currentXRes = baseResX;
		double currentYRes = baseResY;
		
		double newResX = 0;
		double newResY = 0;
		
		char numerator[4];
		
		for( int i = 1; i < numLevels; i++)
		{
			pyramid[i].level = i;
			pyramid[i].windowSize = windowLevel[i];
			
			newResX = currentXRes * levelScales[i];
			newResY = currentYRes * levelScales[i];
			
			pyramid[i].imageRes = newResX;
			
			// Interpolate band from Image A
			strcpy(tmpFilePath, outputPath);
			strcat(tmpFilePath, "imageA_");
			sprintf(numerator, "%d", i);
			strcat(tmpFilePath, numerator);
			strcat(tmpFilePath, ".tif");
			pyramid[i].imageA = interpolation.createNewImage(imageA, 
															  newResX, 
															  newResY, 
															  tmpFilePath, 
															  format, 
															  imageABand);
			
			// Interpolate band from Image B
			strcpy(tmpFilePath, outputPath);
			strcat(tmpFilePath, "imageB_");
			sprintf(numerator, "%d", i);
			strcat(tmpFilePath, numerator);
			strcat(tmpFilePath, ".tif");
			pyramid[i].imageB = interpolation.createNewImage(imageB, 
															  newResX, 
															  newResY, 
															  tmpFilePath, 
															  format, 
															  imageBBand);
			
			pyramid[i].imgOverlap = new ImageOverlap(pyramid[i].imageA, pyramid[i].imageB);
			currentXRes = newResX;
			currentYRes = newResY;
		}
		
		if(trans1 != NULL)
		{
			delete trans1;
		}
		if(trans2 != NULL)
		{
			delete trans2;
		}
}

PyramidLevel* ImagePyramid::getLevel(int level)
{
	return &pyramid[level];
}

int ImagePyramid::getNumberOfLevels()
{
	return numberOfLevels;
}

void ImagePyramid::getTileCoords4PointWindow(ImageNetworkNode *networkNode,
											 int level,
											 TileCoords* tile)
{
	MathUtils mathUtils;
	tile->imgABRX = 0;
	tile->imgABRY = 0;
	tile->imgATLX = 0;
	tile->imgATLY = 0;
	tile->imgBBRX = 0;
	tile->imgBBRX = 0;
	tile->imgBBRY = 0;
	tile->imgBTLX = 0;
	tile->imgBTLY = 0;
	tile->eastingTL = 0;
	tile->northingTL = 0;
	tile->eastingBR = 0;
	tile->northingBR = 0;
	int windowDimensions[4] = {0};
	
	int *refImagePixels = pyramid[level].imgOverlap->getImageAPixelCoords();
	int *floatImagePixels = pyramid[level].imgOverlap->getImageBPixelCoords();
	
	/*std::cout << "Centre Point: ImageA = [" << networkNode->imageA->x << ", "
			  << networkNode->imageA->y << "] Image B = [" << networkNode->imageB->x << ", "
			  << networkNode->imageB->y << "]\n";*/
	
	
	int tmpdifferenceA = 0;
	int tmpdifferenceB = 0;
	
	tile->imgATLX = networkNode->imageA->x - networkNode->windowSize;
	tile->imgATLY = networkNode->imageA->y - networkNode->windowSize;
	tile->imgABRX = networkNode->imageA->x + networkNode->windowSize;
	tile->imgABRY = networkNode->imageA->y + networkNode->windowSize;
	
	tile->imgBTLX = (networkNode->imageB->x + mathUtils.round(networkNode->transform->shiftX)) 
				  - networkNode->windowSize;
	tile->imgBTLY = (networkNode->imageB->y + mathUtils.round(networkNode->transform->shiftY)) 
		          - networkNode->windowSize;
	tile->imgBBRX = (networkNode->imageB->x + mathUtils.round(networkNode->transform->shiftX)) 
		          + networkNode->windowSize;
	tile->imgBBRY = (networkNode->imageB->y + mathUtils.round(networkNode->transform->shiftY)) 
			      + networkNode->windowSize;
	
/*	std::cout << "\nBefore Triming Image A: ";
	std::cout << "[" << tile->imgATLX << ", " << tile->imgATLY << "] [" 
		<< tile->imgABRX << ", " << tile->imgABRY << "]\n";
	std::cout << "Before Triming Image B: ";
	std::cout << "[" << tile->imgBTLX << ", " << tile->imgBTLY << "] ["
		<< tile->imgBBRX << ", " << tile->imgBBRY << "]\n";
	
	std::cout << "Transform = [" << networkNode->transform->shiftX << ", " 
			  << networkNode->transform->shiftY << "]\n";*/
	
	/*std::cout << "tile->imgATLX = " << tile->imgATLX << " refImagePixels[0] = " << refImagePixels[0]
			  << " tile->imgBTLX = " << tile->imgBTLX << " floatImagePixels[0] = " << floatImagePixels[0]
			  << std::endl;*/
	if(tile->imgATLX < refImagePixels[0] | tile->imgBTLX < floatImagePixels[0])
	{
		//TLX
		tmpdifferenceA = refImagePixels[0] - tile->imgATLX; 
		tmpdifferenceB = floatImagePixels[0] - tile->imgBTLX; 
		//std::cout << "tmpdifferenceA = " << tmpdifferenceA << " tmpdifferenceB = " << tmpdifferenceB << std::endl;
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[0] = networkNode->windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[0] = networkNode->windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[0] = networkNode->windowSize;
	}
	
	/*std::cout << "tile->imgATLY = " << tile->imgATLY << " refImagePixels[0] = " << refImagePixels[0]
			  << " tile->imgBTLY = " << tile->imgBTLY << " floatImagePixels[1] = " << floatImagePixels[1]
			  << std::endl;*/
	if(tile->imgATLY < refImagePixels[1] | tile->imgBTLY < floatImagePixels[1])
	{
		//TLY
		tmpdifferenceA = refImagePixels[1] - tile->imgATLY;
		tmpdifferenceB = floatImagePixels[1] - tile->imgBTLY;
		//std::cout << "tmpdifferenceA = " << tmpdifferenceA << " tmpdifferenceB = " << tmpdifferenceB << std::endl;
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[1] = networkNode->windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[1] = networkNode->windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[1] = networkNode->windowSize;
	}
	
	/*std::cout << "tile->imgABRX = " << tile->imgABRX << " refImagePixels[2] = "
			  << refImagePixels[2] << " tile->imgBBRX = " << tile->imgBBRX 
			  << " floatImagePixels[2] = " << floatImagePixels[2] << std::endl;*/
	if(tile->imgABRX > refImagePixels[2] | tile->imgBBRX > floatImagePixels[2])
	{
		//BRX
		tmpdifferenceA = tile->imgABRX - refImagePixels[2];
		tmpdifferenceB = tile->imgBBRX - floatImagePixels[2];
		//std::cout << "tmpdifferenceA = " << tmpdifferenceA << " tmpdifferenceB = " << tmpdifferenceB << std::endl;
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[2] = networkNode->windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[2] = networkNode->windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[2] = networkNode->windowSize;
	}
	
	/*std::cout << "tile->imgABRY = " << tile->imgABRY << " refImagePixels[3] = "
			  << refImagePixels[3] << " tile->imgBBRY = " << tile->imgBBRY
			  << " floatImagePixels[3] = " << floatImagePixels[3] << std::endl;*/
	if(tile->imgABRY > refImagePixels[3] | tile->imgBBRY > floatImagePixels[3])
	{
		//BRY
		tmpdifferenceA = tile->imgABRY - refImagePixels[3]; 
		tmpdifferenceB = tile->imgBBRY - floatImagePixels[3]; 
		//std::cout << "tmpdifferenceA = " << tmpdifferenceA << " tmpdifferenceB = " << tmpdifferenceB << std::endl;
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[3] = networkNode->windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[3] = networkNode->windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[3] = networkNode->windowSize;
	}
	
	tile->imgATLX = networkNode->imageA->x - windowDimensions[0];
	tile->imgATLY = networkNode->imageA->y - windowDimensions[1];
	tile->imgABRX = networkNode->imageA->x + windowDimensions[2];
	tile->imgABRY = networkNode->imageA->y + windowDimensions[3];
	
	tile->imgBTLX = (networkNode->imageB->x + mathUtils.round(networkNode->transform->shiftX)) 
				  - windowDimensions[0];
	tile->imgBTLY = (networkNode->imageB->y + mathUtils.round(networkNode->transform->shiftY)) 
				  - windowDimensions[1];
	tile->imgBBRX = (networkNode->imageB->x + mathUtils.round(networkNode->transform->shiftX)) 
				  + windowDimensions[2];
	tile->imgBBRY = (networkNode->imageB->y + mathUtils.round(networkNode->transform->shiftY)) 
				  + windowDimensions[3];
	
	tile->eastingTL = networkNode->geoPosition->eastings - 
		(double(windowDimensions[0]) / pyramid[level].imageRes);
	tile->northingTL = networkNode->geoPosition->northings + 
		(double(windowDimensions[1]) / pyramid[level].imageRes);
	tile->eastingBR = networkNode->geoPosition->eastings + 
		(double(windowDimensions[2]) / pyramid[level].imageRes);
	tile->northingBR = networkNode->geoPosition->northings -
		(double(windowDimensions[3]) / pyramid[level].imageRes);
}

ImagePyramid::~ImagePyramid()
{
	
}
