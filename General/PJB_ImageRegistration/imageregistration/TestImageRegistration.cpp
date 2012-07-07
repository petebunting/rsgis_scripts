/*
 *  TestImageRegistration.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 10/01/2006.
 *  Copyright 2006  Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "TestImageRegistration.h"

TestImageRegistration::TestImageRegistration()
{
	
}

void TestImageRegistration::testImageOverlap(const int scenario, 
											 const char *referenceImage, 
											 const char *floatingImage)
{
	TileCoords *tile = new TileCoords;
	ImageOverlap *imgOverlap = new ImageOverlap;
	switch(scenario)
	{
		case 0:
		{
			try
			{
				std::cout << "\nRunning scenario 0...  shift(0, 0)" << std::endl;
				
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 0;
				double shiftY = 0;
				tile->imgATLX = 50;
				tile->imgATLY = 50;
				tile->imgABRX = 100;
				tile->imgABRY = 100;
				tile->imgBTLX = 50;
				tile->imgBTLY = 50;
				tile->imgBBRX = 100;
				tile->imgBBRY = 100;
				tile->eastingTL = 539599;
				tile->northingTL = 7147626;
				tile->eastingBR = 539649;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 50)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 50)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 100)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 100)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 1:
		{
			try
			{
				std::cout << "\nRunning scenario 1...  shift(0, 1) TEST Y" << std::endl;
				
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 0;
				double shiftY = 1;
				tile->imgATLX = 50;
				tile->imgATLY = 50;
				tile->imgABRX = 100;
				tile->imgABRY = 100;
				tile->imgBTLX = 50;
				tile->imgBTLY = 50;
				tile->imgBBRX = 100;
				tile->imgBBRY = 100;
				tile->eastingTL = 539599;
				tile->northingTL = 7147626;
				tile->eastingBR = 539649;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 50)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 51)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 100)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 101)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 2:
		{
			try
			{
				std::cout << "\nRunning scenario 2...  shift(0, -1) TEST Y" << std::endl;
			
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 0;
				double shiftY = -1;
				tile->imgATLX = 50;
				tile->imgATLY = 50;
				tile->imgABRX = 100;
				tile->imgABRY = 100;
				tile->imgBTLX = 50;
				tile->imgBTLY = 50;
				tile->imgBBRX = 100;
				tile->imgBBRY = 100;
				tile->eastingTL = 539599;
				tile->northingTL = 7147626;
				tile->eastingBR = 539649;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 50)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 49)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 100)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 99)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 3:
		{
			try
			{
				std::cout << "\nRunning scenario 3...  shift(1, 0) TEST X" << std::endl;
			
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 1;
				double shiftY = 0;
				tile->imgATLX = 50;
				tile->imgATLY = 50;
				tile->imgABRX = 100;
				tile->imgABRY = 100;
				tile->imgBTLX = 50;
				tile->imgBTLY = 50;
				tile->imgBBRX = 100;
				tile->imgBBRY = 100;
				tile->eastingTL = 539599;
				tile->northingTL = 7147626;
				tile->eastingBR = 539649;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 51)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 50)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 101)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 100)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}			
		case 4:
		{
			try
			{
				std::cout << "\nRunning scenario 4...  shift(-1, 0) TEST X" << std::endl;
				
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = -1;
				double shiftY = 0;
				tile->imgATLX = 50;
				tile->imgATLY = 50;
				tile->imgABRX = 100;
				tile->imgABRY = 100;
				tile->imgBTLX = 50;
				tile->imgBTLY = 50;
				tile->imgBBRX = 100;
				tile->imgBBRY = 100;
				tile->eastingTL = 539599;
				tile->northingTL = 7147626;
				tile->eastingBR = 539649;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 49)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 50)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 99)
				{
					std::cout << "Image B BRX Pixel value is *** *** INCORRECT *** ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 100)
				{
					std::cout << "Image B BRY Pixel value is *** *** INCORRECT *** ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** *** INCORRECT *** ***!!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}	
		case 5:
		{
			try
			{
				std::cout << "\nRunning scenario 5... shift(-1, 0) TEST X BORDER" << std::endl;
				
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = -1;
				double shiftY = 0;
				tile->imgATLX = 0;
				tile->imgATLY = 50;
				tile->imgABRX = 100;
				tile->imgABRY = 100;
				tile->imgBTLX = 0;
				tile->imgBTLY = 50;
				tile->imgBBRX = 100;
				tile->imgBBRY = 100;
				tile->eastingTL = 539549;
				tile->northingTL = 7147626;
				tile->eastingBR = 539649;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 1)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 0)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 50)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 99)
				{
					std::cout << "Image B BRX Pixel value is *** *** INCORRECT *** ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 100)
				{
					std::cout << "Image B BRY Pixel value is *** *** INCORRECT *** ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539550)
				{
					std::cout << "Geo-Coords TLX value is *** *** INCORRECT *** ***!!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 6:
		{
			try
			{
				std::cout << "\nRunning scenario 6... shift(1, 0) TEST X BORDER" << std::endl;
			
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 1;
				double shiftY = 0;
				tile->imgATLX = 450;
				tile->imgATLY = 50;
				tile->imgABRX = 500;
				tile->imgABRY = 100;
				tile->imgBTLX = 450;
				tile->imgBTLY = 50;
				tile->imgBBRX = 500;
				tile->imgBBRY = 100;
				tile->eastingTL = 539999;
				tile->northingTL = 7147626;
				tile->eastingBR = 540049;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 450)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 499)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 451)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 50)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 500)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 100)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539999)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 540048)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 7:
		{
			try
			{
				std::cout << "\nRunning scenario 7... shift(0, 1) TEST Y BORDER" << std::endl;
			
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 0;
				double shiftY = 1;
				tile->imgATLX = 50;
				tile->imgATLY = 100;
				tile->imgABRX = 100;
				tile->imgABRY = 150;
				tile->imgBTLX = 50;
				tile->imgBTLY = 100;
				tile->imgBBRX = 100;
				tile->imgBBRY = 150;
				tile->eastingTL = 539599;
				tile->northingTL = 7147576;
				tile->eastingBR = 540049;
				tile->northingBR = 7147526;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 100)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 149)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 50)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 101)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 100)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 150)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
				}
				else if(overlapCoords[1] != 7147576)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 540049)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147527)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 8:
		{
			try
			{
				std::cout << "\nRunning scenario 8... shift(0, -1) TEST Y BORDER" << std::endl;
			
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 0;
				double shiftY = -1;
				tile->imgATLX = 50;
				tile->imgATLY = 0;
				tile->imgABRX = 100;
				tile->imgABRY = 50;
				tile->imgBTLX = 50;
				tile->imgBTLY = 0;
				tile->imgBBRX = 100;
				tile->imgBBRY = 50;
				tile->eastingTL = 539599;
				tile->northingTL = 7147676;
				tile->eastingBR = 539649;
				tile->northingBR = 7147626;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 1)
				{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 50)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 50)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 0)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 100)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 49)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
				}
				else if(overlapCoords[1] != 7147675)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147626)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 9:
		{
			try
			{
				std::cout << "\nRunning scenario 9... shift(1.2,0) TEST Sub-pixel" << std::endl;
			
				this->getImage4Read(referenceImage, floatingImage);
				double shiftX = 1.2;
				double shiftY = 0;
				tile->imgATLX = 50;
				tile->imgATLY = 50;
				tile->imgABRX = 100;
				tile->imgABRY = 100;
				tile->imgBTLX = 50;
				tile->imgBTLY = 50;
				tile->imgBBRX = 100;
				tile->imgBBRY = 100;
				tile->eastingTL = 539599;
				tile->northingTL = 7147626;
				tile->eastingBR = 539649;
				tile->northingBR = 7147576;
				imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
				imgOverlap->printOverlappingArea(false);
				int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
				int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
				double *overlapCoords = imgOverlap->getOverlapGeoCoords();
				//Test Image A Pixel Coords
				if(imgAPixelCoords[0] != 50)
				{
					std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[1] != 50)
				{
					std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[2] != 100)
				{
					std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgAPixelCoords[3] != 100)
				{
					std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image A Pixel values are correct!! :)" << std::endl;
				}
				//Test Image B Pixel Coords
				if(imgBPixelCoords[0] != 51)
				{
					std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[1] != 50)
				{
					std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[2] != 102)
				{
					std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else if(imgBPixelCoords[3] != 100)
				{
					std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image B Pixel values are correct!! :)" << std::endl;
				}
				//Test Geo-Coords
				if(overlapCoords[0] != 539599)
				{
					std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
				}
				else if(overlapCoords[1] != 7147626)
				{
					std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[2] != 539649)
				{
					std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
				}
				else if(overlapCoords[3] != 7147576)
				{
					std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
				}
				else
				{
					std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
				}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 10:
		{
			try
			{
			std::cout << "\nRunning scenario 10... shift(-1.2,0) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = -1.2;
			double shiftY = 0;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 48)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 50)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 99)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 100)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}		
		case 11:
		{
			try
			{
			std::cout << "\nRunning scenario 11... shift(0, 1.2) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 0;
			double shiftY = 1.2;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 50)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 51)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 100)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 102)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 12:
		{
			try
			{
			std::cout << "\nRunning scenario 12... shift(0, -1.2) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 0;
			double shiftY = -1.2;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 50)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 48)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 100)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 99)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 13:
		{
			try
		{
			std::cout << "\nRunning scenario 13... shift(1, 1)" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 1;
			double shiftY = 1;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 51)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 51)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 101)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 101)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
		case 14:
		{
			try
		{
			std::cout << "\nRunning scenario 14... shift(1.7,0) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 1.7;
			double shiftY = 0;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 51)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 50)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 102)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 100)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
		}
			catch(ImageNotAvailableException e)
		{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
		}
			break;
		}
		case 15:
		{
			try
		{
			std::cout << "\nRunning scenario 15... shift(-1.7,0) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = -1.7;
			double shiftY = 0;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 48)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 50)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 99)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 100)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
		}
			catch(ImageNotAvailableException e)
		{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
		}
			break;
		}		
		case 16:
		{
			try
		{
			std::cout << "\nRunning scenario 16... shift(0, 1.7) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 0;
			double shiftY = 1.7;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 50)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 51)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 100)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 102)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
		}
			catch(ImageNotAvailableException e)
		{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
		}
			break;
		}
		case 17:
		{
			try
		{
			std::cout << "\nRunning scenario 17... shift(0, -1.7) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 0;
			double shiftY = -1.7;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 50)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 48)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 100)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 99)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
		}
			catch(ImageNotAvailableException e)
		{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
		}
			break;
		}
		case 18:
		{
			try
		{
			std::cout << "\nRunning scenario 18... shift(0.5, 0) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 0.5;
			double shiftY = 0;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 50)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 50)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 101)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 100)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
		}
			catch(ImageNotAvailableException e)
		{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
		}
			break;
		}	
		case 19:
		{
			try
		{
			std::cout << "\nRunning scenario 19... shift(4.9, 0) TEST Sub-pixel" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 4.9;
			double shiftY = 0;
			tile->imgATLX = 50;
			tile->imgATLY = 50;
			tile->imgABRX = 100;
			tile->imgABRY = 100;
			tile->imgBTLX = 50;
			tile->imgBTLY = 50;
			tile->imgBBRX = 100;
			tile->imgBBRY = 100;
			tile->eastingTL = 539599;
			tile->northingTL = 7147626;
			tile->eastingBR = 539649;
			tile->northingBR = 7147576;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 50)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 50)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 100)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 100)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 54)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 50)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 105)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 100)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539599)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147626)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 539649)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147576)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
		}
			catch(ImageNotAvailableException e)
		{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
		}
			break;
		}	
		case 20:
		{
			try
			{
			std::cout << "\nRunning scenario 20... shift(0, 0) TEST Whole Image" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = 0;
			double shiftY = 0;
			tile->imgATLX = 0;
			tile->imgATLY = 0;
			tile->imgABRX = 500;
			tile->imgABRY = 150;
			tile->imgBTLX = 0;
			tile->imgBTLY = 0;
			tile->imgBBRX = 500;
			tile->imgBBRY = 150;
			tile->eastingTL = 539549;
			tile->northingTL = 7147676;
			tile->eastingBR = 540049;
			tile->northingBR = 7147826;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 0)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 0)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 500)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 150)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 0)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 0)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 500)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 150)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539549)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147676)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 540049)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147826)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}	
		case 21:
		{
			try
			{
			std::cout << "\nRunning scenario 21... shift(-1, -1) TEST Whole Image" << std::endl;
			
			this->getImage4Read(referenceImage, floatingImage);
			double shiftX = -1;
			double shiftY = -1;
			tile->imgATLX = 0;
			tile->imgATLY = 0;
			tile->imgABRX = 500;
			tile->imgABRY = 150;
			tile->imgBTLX = 0;
			tile->imgBTLY = 0;
			tile->imgBBRX = 500;
			tile->imgBBRY = 150;
			tile->eastingTL = 539549;
			tile->northingTL = 7147676;
			tile->eastingBR = 540049;
			tile->northingBR = 7147826;
			imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
			imgOverlap->printOverlappingArea(false);
			int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
			int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
			double *overlapCoords = imgOverlap->getOverlapGeoCoords();
			//Test Image A Pixel Coords
			if(imgAPixelCoords[0] != 1)
			{
				std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[1] != 1)
			{
				std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[2] != 500)
			{
				std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgAPixelCoords[3] != 150)
			{
				std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image A Pixel values are correct!! :)" << std::endl;
			}
			//Test Image B Pixel Coords
			if(imgBPixelCoords[0] != 0)
			{
				std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[1] != 0)
			{
				std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[2] != 499)
			{
				std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else if(imgBPixelCoords[3] != 149)
			{
				std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image B Pixel values are correct!! :)" << std::endl;
			}
			//Test Geo-Coords
			if(overlapCoords[0] != 539550)
			{
				std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
			}
			else if(overlapCoords[1] != 7147675)
			{
				std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[2] != 540049)
			{
				std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
			}
			else if(overlapCoords[3] != 7147826)
			{
				std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
			}
			else
			{
				std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
			}
			}
			catch(ImageNotAvailableException e)
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
			}
			break;
		}
	}
	
}

void TestImageRegistration::getImage4Read(const char *fileRef, const char *fileFloat)  
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
		//std::cout << "Data from " << fileRef << " has been read in OK!\n";
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
		//std::cout << "Data from " << fileFloat << " has been read in OK!\n";
	}
}


void TestImageRegistration::testMIValues(const char *referenceImage, const char *floatingImage)
{
	TileCoords *tile = new TileCoords;
	ImageOverlap *imgOverlap = new ImageOverlap;
	std::cout << "\n Shift(0, 0) TEST Whole Image" << std::endl;
	try
	{
		this->getImage4Read(referenceImage, floatingImage);
		double shiftX = 0;
		double shiftY = 0;
		tile->imgATLX = 0;
		tile->imgATLY = 0;
		tile->imgABRX = 500;
		tile->imgABRY = 150;
		tile->imgBTLX = 0;
		tile->imgBTLY = 0;
		tile->imgBBRX = 500;
		tile->imgBBRY = 150;
		tile->eastingTL = 539549;
		tile->northingTL = 7147676;
		tile->eastingBR = 540049;
		tile->northingBR = 7147826;
		imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
		imgOverlap->printOverlappingArea(false);
		int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
		int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
		double *overlapCoords = imgOverlap->getOverlapGeoCoords();
		//Test Image A Pixel Coords
		if(imgAPixelCoords[0] != 0)
		{
			std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[1] != 0)
		{
			std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[2] != 500)
		{
			std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[3] != 150)
		{
			std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image A Pixel values are correct!! :)" << std::endl;
		}
		//Test Image B Pixel Coords
		if(imgBPixelCoords[0] != 0)
		{
			std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[1] != 0)
		{
			std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[2] != 500)
		{
			std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[3] != 150)
		{
			std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image B Pixel values are correct!! :)" << std::endl;
		}
		//Test Geo-Coords
		if(overlapCoords[0] != 539549)
		{
			std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
		}
		else if(overlapCoords[1] != 7147676)
		{
			std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
		}
		else if(overlapCoords[2] != 540049)
		{
			std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
		}
		else if(overlapCoords[3] != 7147826)
		{
			std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
		}
		
		// Create a JointHistogram
		JointHistogram *jointHistogram = NULL;
		jointHistogram = new JointHistogram;
		jointHistogram->generateSubPixelJointHistogram(reference, floating, 16, 16, imgOverlap, shiftX, shiftY);
		
		// Find value of MI
		MutualInformation *mi = NULL;
		mi = new MutualInformation;
		double mivalue = 0;
		mivalue = mi->calcMutualInformation(*jointHistogram);
		
		std::cout << "MI Value: " << mivalue << std::endl;
	}
	catch(ImageNotAvailableException e)
	{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				std::exit(-1);
	}

	try
	{
		std::cout << "\n Shift(-1, -1) TEST Whole Image" << std::endl;
		
		this->getImage4Read(referenceImage, floatingImage);
		double shiftX = -1;
		double shiftY = -1;
		tile->imgATLX = 0;
		tile->imgATLY = 0;
		tile->imgABRX = 500;
		tile->imgABRY = 150;
		tile->imgBTLX = 0;
		tile->imgBTLY = 0;
		tile->imgBBRX = 500;
		tile->imgBBRY = 150;
		tile->eastingTL = 539549;
		tile->northingTL = 7147676;
		tile->eastingBR = 540049;
		tile->northingBR = 7147826;
		imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
		imgOverlap->printOverlappingArea(false);
		int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
		int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
		double *overlapCoords = imgOverlap->getOverlapGeoCoords();
		//Test Image A Pixel Coords
		if(imgAPixelCoords[0] != 1)
		{
			std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[1] != 1)
		{
			std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[2] != 500)
		{
			std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[3] != 150)
		{
			std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image A Pixel values are correct!! :)" << std::endl;
		}
		//Test Image B Pixel Coords
		if(imgBPixelCoords[0] != 0)
		{
			std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[1] != 0)
		{
			std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[2] != 499)
		{
			std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[3] != 149)
		{
			std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image B Pixel values are correct!! :)" << std::endl;
		}
		//Test Geo-Coords
		if(overlapCoords[0] != 539550)
		{
			std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
		}
		else if(overlapCoords[1] != 7147675)
		{
			std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
		}
		else if(overlapCoords[2] != 540049)
		{
			std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
		}
		else if(overlapCoords[3] != 7147826)
		{
			std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
		}
		// Create a JointHistogram
		JointHistogram *jointHistogram = NULL;
		jointHistogram = new JointHistogram;
		jointHistogram->generateSubPixelJointHistogram(reference , floating, 16, 16, imgOverlap, shiftX, shiftY);
		
		// Find value of MI
		MutualInformation *mi = NULL;
		mi = new MutualInformation;
		double mivalue = 0;
		mivalue = mi->calcMutualInformation(*jointHistogram);
		
		std::cout << "MI Value: " << mivalue << std::endl;
	}
	catch(ImageNotAvailableException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	try
	{
		std::cout << "\n Shift(-1, 0) TEST Whole Image" << std::endl;
		
		this->getImage4Read(referenceImage, floatingImage);
		double shiftX = -1;
		double shiftY = 0;
		tile->imgATLX = 0;
		tile->imgATLY = 0;
		tile->imgABRX = 500;
		tile->imgABRY = 150;
		tile->imgBTLX = 0;
		tile->imgBTLY = 0;
		tile->imgBBRX = 500;
		tile->imgBBRY = 150;
		tile->eastingTL = 539549;
		tile->northingTL = 7147676;
		tile->eastingBR = 540049;
		tile->northingBR = 7147826;
		imgOverlap->ImageOverlap::calcOverlappingAreaWithinTileWithFloatShift(reference, floating, shiftX, shiftY, tile);
		imgOverlap->printOverlappingArea(false);
		int *imgAPixelCoords = imgOverlap->getImageAPixelCoords();
		int *imgBPixelCoords = imgOverlap->getImageBPixelCoords();
		double *overlapCoords = imgOverlap->getOverlapGeoCoords();
		//Test Image A Pixel Coords
		if(imgAPixelCoords[0] != 1)
		{
			std::cout << "Image A TLX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[1] != 0)
		{
			std::cout << "Image A TLY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[2] != 500)
		{
			std::cout << "Image A BRX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgAPixelCoords[3] != 150)
		{
			std::cout << "Image A BRY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image A Pixel values are correct!! :)" << std::endl;
		}
		//Test Image B Pixel Coords
		if(imgBPixelCoords[0] != 0)
		{
			std::cout << "Image B TLX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[1] != 0)
		{
			std::cout << "Image B TLY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[2] != 499)
		{
			std::cout << "Image B BRX Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else if(imgBPixelCoords[3] != 150)
		{
			std::cout << "Image B BRY Pixel value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image B Pixel values are correct!! :)" << std::endl;
		}
		//Test Geo-Coords
		if(overlapCoords[0] != 539550)
		{
			std::cout << "Geo-Coords TLX value is *** INCORRECT *** !!" << std::endl;
		}
		else if(overlapCoords[1] != 7147676)
		{
			std::cout << "Geo-Coords TLY value is *** INCORRECT ***!!" << std::endl;
		}
		else if(overlapCoords[2] != 540049)
		{
			std::cout << "Geo-Coords BRX value is *** INCORRECT ***!!" << std::endl;
		}
		else if(overlapCoords[3] != 7147826)
		{
			std::cout << "Geo-Coords BRY value is *** INCORRECT ***!!" << std::endl;
		}
		else
		{
			std::cout << "Image Geo-Coords are correct!! :)" << std::endl;
		}
		// Create a JointHistogram
		JointHistogram *jointHistogram = NULL;
		jointHistogram = new JointHistogram;
		jointHistogram->generateSubPixelJointHistogram(reference , floating, 16, 16, imgOverlap, shiftX, shiftY);
		
		// Find value of MI
		MutualInformation *mi = NULL;
		mi = new MutualInformation;
		double mivalue = 0;
		mivalue = mi->calcMutualInformation(*jointHistogram);
		
		std::cout << "MI Value: " << mivalue << std::endl;
	}
	catch(ImageNotAvailableException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
}

void TestImageRegistration::testImageInterpolation()
{
	VectorImageMeasures *vecImageMeasures = NULL;
	vecImageMeasures = new VectorImageMeasures;
	MathUtils *mathUtils = NULL;
	mathUtils = new MathUtils;
	Interpolation *interpolation = NULL;
	interpolation = new Interpolation;
	
	double pixels1[4];
	double pixels2[4];
	double pixels3[4];
	double pixels4[4];
	
	pixels1[0] = 137.14;
	pixels1[1] = 159.82;
	pixels1[2] = 143.72;
	pixels1[3] = 155.63;
	
	pixels2[0] = 159.82;
	pixels2[1] = 160.67;
	pixels2[2] = 155.63;
	pixels2[3] = 158.47;
	
	pixels3[0] = 143.72;
	pixels3[1] = 155.63;
	pixels3[2] = 154.48;
	pixels3[3] = 151.55;
	
	pixels4[0] = 155.63;
	pixels4[1] = 158.47;
	pixels4[2] = 151.55;
	pixels4[3] = 150.85;
	
	std::cout << "Original Pixels:\n";
	std::cout << "pixels1[0]: " << pixels1[0] << std::endl;
	std::cout << "pixels1[1]: " << pixels1[1] << std::endl;
	std::cout << "pixels1[2]: " << pixels1[2] << std::endl;
	std::cout << "pixels1[3]: " << pixels1[3] << std::endl;
	
	double output = 0;
	double storeInterpolatedImage1[6][6];
	double storeInterpolatedImage2[6][6];
	double storeInterpolatedImage3[6][6];
	double storeInterpolatedImage4[6][6];
	int xCount = 0;
	int yCount = 0;
	
	std::cout << "Set 1:\n";
	
	for(double i = 0; i <= 1; i=i+0.2)
	{
		for(double j = 0; j<=1; j=j+0.2)
		{
			output = interpolation->bilinear(j,i,pixels1);
			std::cout << output << ",";
			storeInterpolatedImage1[xCount++][yCount] = output;
		}
		std::cout << "\n";
		yCount++;
		xCount = 0;
	}
	
	std::cout << "Set 2:\n";
	xCount = 0;
	yCount = 0;
	for(double i = 0; i <= 1; i=i+0.2)
	{
		for(double j = 0; j<=1; j=j+0.2)
		{
			output = interpolation->bilinear(j,i,pixels2);
			std::cout << output << ",";
			storeInterpolatedImage2[xCount++][yCount] = output;
		}
		std::cout << "\n";
		yCount++;
		xCount = 0;
	}
	
	std::cout << "Set 3:\n";
	xCount = 0;
	yCount = 0;
	for(double i = 0; i <= 1; i=i+0.2)
	{
		for(double j = 0; j<=1; j=j+0.2)
		{
			output = interpolation->bilinear(j,i,pixels3);
			std::cout << output << ",";
			storeInterpolatedImage3[xCount++][yCount] = output;
		}
		std::cout << "\n";
		yCount++;
		xCount = 0;
	}
	
	std::cout << "Set 4:\n";
	xCount = 0;
	yCount = 0;
	for(double i = 0; i <= 1; i=i+0.2)
	{
		for(double j = 0; j<=1; j=j+0.2)
		{
			output = interpolation->bilinear(j,i,pixels4);
			std::cout << output << ",";
			storeInterpolatedImage4[xCount++][yCount] = output;
		}
		std::cout << "\n";
		yCount++;
		xCount = 0;
	}
	
	
	double outputEuclideanDistance[6][6];
	double tmpB4Sqrt = 0;
	double set1 = 0;
	double set2 = 0;
	double set3 = 0;
	double set4 = 0;
	
	for(int i = 0; i < 6; i++)
	{
		for(int j = 0; j < 6; j++)
		{
			//std::cout << "i: " << i << " j: " << j << std::endl;
			//std::cout << "storeInterpolatedImage1[j][i]: " << storeInterpolatedImage1[j][i] << std::endl;
			//std::cout << "storeInterpolatedImage2[j][i]: " << storeInterpolatedImage2[j][i] << std::endl;
			//std::cout << "storeInterpolatedImage3[j][i]: " << storeInterpolatedImage3[j][i] << std::endl;
			//std::cout << "storeInterpolatedImage4[j][i]: " << storeInterpolatedImage4[j][i] << std::endl;
			
			set1 = (pixels1[0] - storeInterpolatedImage1[j][i])*(pixels1[0] - storeInterpolatedImage1[j][i]);
			set2 = (pixels1[1] - storeInterpolatedImage2[j][i])*(pixels1[1] - storeInterpolatedImage2[j][i]);
			set3 = (pixels1[2] - storeInterpolatedImage3[j][i])*(pixels1[2] - storeInterpolatedImage3[j][i]);
			set4 = (pixels1[3] - storeInterpolatedImage4[j][i])*(pixels1[3] - storeInterpolatedImage4[j][i]);
			
			//std::cout << "set1: " << set1 << std::endl;
			//std::cout << "set2: " << set2 << std::endl;
			//std::cout << "set3: " << set3 << std::endl;
			//std::cout << "set4: " << set4 << std::endl;
			
			tmpB4Sqrt = set1 + set2 + set3 + set4;
			
			//std::cout << "tmpB4Sqrt: " << tmpB4Sqrt << std::endl;
			
			outputEuclideanDistance[j][i] = sqrt(tmpB4Sqrt);
			if( outputEuclideanDistance[j][i] > -0.0000001 & outputEuclideanDistance[j][i] < 0.0000001 )
			{
				outputEuclideanDistance[j][i] = 0;
			}
		}
	}
	
	std::cout << "Euclidean Distance:\n";
	
	for(int i = 0; i < 6; i++)
	{
		for(int j = 0; j < 6; j++)
		{
			std::cout << outputEuclideanDistance[j][i] << ", ";
		}
		std::cout << std::endl;
	}
	
	if( vecImageMeasures != NULL)
	{
		delete vecImageMeasures;
	}
}

void TestImageRegistration::testEuclideanDistanceUsingSmallImages(const char *filepath, double shift, int pixelMovement, int imageBand)
{
	VectorImageMeasures *vecImageMeasures = NULL;
	vecImageMeasures = new VectorImageMeasures;
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	
	GDALAllRegister();
	//Get Dataset
	GDALDataset *inputImage = NULL;
	inputImage = (GDALDataset *) GDALOpen(filepath, GA_ReadOnly);
	// Check read in correctly.
	if(inputImage == NULL)
	{
		std::cout << "Bugger could not open Image " << filepath << std::endl;
		std::exit(-1);
	}
	else
	{
		std::cout << "Data from " << filepath << " has been read in OK!\n";
	} 
	
	int imageXSize = inputImage->GetRasterXSize();
	int imageYSize = inputImage->GetRasterYSize();
	
	int arrayImageSize = imageXSize * imageYSize;
	float *imageScanline;
	
	imageScanline = (float *) CPLMalloc(sizeof(float)*arrayImageSize);
	
	GDALRasterBand *inputImageBand = inputImage->GetRasterBand(imageBand);
	inputImageBand->RasterIO(GF_Read, 
							0, 
							0, 
							imageXSize, 
							imageYSize, 
							imageScanline, 
							imageXSize, 
							imageYSize, 
							GDT_Float32, 
							0, 
							0);
	for(int i = 0; i < arrayImageSize; i++)
	{
		std::cout << imageScanline[i] << ", ";
		if( i % imageXSize == imageXSize-1)
		{
			std::cout << std::endl;
		}
	}
	std::cout << std::endl;
	std::cout << std::endl;
	
	int bufferSize = ((mathUtils->roundUp(pixelMovement/shift))*2)+1;
	
	double **imageMovement = NULL;
	*imageMovement = new double[bufferSize];
	
	double xShift = pixelMovement * (-1);
	double yShift = pixelMovement;
	
	for(int i = (bufferSize-1); i >= 0; i--)
	{
		imageMovement[i] = new double[bufferSize];
		for(int j = 0; j < bufferSize; j++)
		{
			std::cout << "xShift: " << xShift << " yShift: " << yShift << std::endl;
			imageMovement[j][i] = this->findEuclideanDistance(imageScanline, xShift, yShift, imageXSize, imageYSize);
			xShift += shift;
			if(xShift > -0.0000001 & xShift < 0.0000001)
			{
				xShift = 0;
			}
		}
		yShift -= shift;
		if(yShift > -0.0000001 & yShift < 0.0000001)
		{
			yShift = 0;
		}
		xShift = pixelMovement * (-1);
	}
	
	
	std::cout << std::endl;
	std::cout << std::endl;
	
	for(int i = (bufferSize-1); i >= 0; i--)
	{
		for(int j = 0; j < bufferSize; j++)
		{
			std::cout << imageMovement[j][i] << ", ";
		}
		std::cout << std::endl;
	}
	
	if( vecImageMeasures != NULL)
	{
		delete vecImageMeasures;
	}
	if(imageMovement != NULL)
	{
		for(int i = 0; i < bufferSize; i++)
		{
			delete [] imageMovement[i];
		}
		delete [] imageMovement;
	}
}

double TestImageRegistration::findEuclideanDistance(float *image, double xShift, double yShift, int imageXSize, int imageYSize)
{
	double distanceMeasure = 0;
	VectorImageMeasures *vecImageMeasures = NULL;
	vecImageMeasures = new VectorImageMeasures;
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	Interpolation *interpolation;
	interpolation = new Interpolation;
	std::cout<< "imageXSize: " << imageXSize << " imageYSize: " << imageYSize << std::endl;
	int xShiftInt = 0;
	double xShiftFloatingPoint = mathUtils->findFloatingPointComponent(xShift, &xShiftInt);
	
	int yShiftInt = 0;
	double yShiftFloatingPoint = mathUtils->findFloatingPointComponent(yShift, &yShiftInt);
	
	std::cout << "xShiftFloatingPoint: " << xShiftFloatingPoint;
	std::cout << " yShiftFloatingPoint: " << yShiftFloatingPoint << std::endl;
	
	bool xShiftPos = true;
	if(xShift < 0)
	{
		xShiftPos = false;
		if(xShiftFloatingPoint != 0)
		{
			xShiftFloatingPoint = 1-xShiftFloatingPoint;
		}
	}
	bool yShiftPos = true;
	if(yShift < 0)
	{
		yShiftPos = false;
		if(yShiftFloatingPoint != 0)
		{
			yShiftFloatingPoint = 1-yShiftFloatingPoint;
		}
	}

	
	// Calculate Image Overlap after shift.
	int xMinFloating = 0;
	int xMaxFloating = imageXSize;
	int yMinFloating = 0;
	int yMaxFloating = imageYSize;
	int xMinOrig = 0;
	int xMaxOrig = imageXSize;
	int yMinOrig = 0;
	int yMaxOrig = imageYSize;
	
	double tmpXMin = xMinFloating + xShift;
	double tmpXMax = xMaxFloating + xShift;
	double tmpYMin = yMinFloating + yShift;
	double tmpYMax = yMaxFloating + yShift;
	
	if(xShiftPos)
	{
		xMinFloating = mathUtils->roundDown(tmpXMin);
		xMaxOrig = xMaxOrig - mathUtils->roundUp(xShift);
	}
	else
	{
		xMaxFloating = mathUtils->roundUp(tmpXMax);
		xMinOrig = xMinOrig - mathUtils->roundDown(xShift); 
	}
	
	if(yShiftPos)
	{
		yMinFloating = mathUtils->roundDown(tmpYMin);
		yMaxOrig = yMaxOrig - mathUtils->roundUp(yShift);
	}
	else
	{
		yMaxFloating = mathUtils->roundUp(tmpYMax);
		yMinOrig = yMinOrig - mathUtils->roundDown(yShift); 
	}
	
	std::cout << "Orig: [" << xMinOrig << "," << yMinOrig << "][" << xMaxOrig << "," << yMaxOrig << "]\n";
	std::cout << "Floating: [" << xMinFloating << "," << yMinFloating << "][" << xMaxFloating << "," << yMaxFloating << "]\n";
	
	// Used to store pixels for interpolation.
	double pixels[4];
	int shiftedXSize = xMaxOrig - xMinOrig;
	int shiftedYSize = yMaxOrig - yMinOrig;
	
	int totalNumPixels = shiftedXSize * shiftedYSize;
	int startingPointFloating = (yMinFloating * imageXSize) + xMinFloating;
	int startingPointOrig = (yMinOrig * imageXSize) + xMinOrig;
	
	std::cout << "ShiftedXSize: " << shiftedXSize;
	std::cout << " ShiftedYSize: " << shiftedYSize << std::endl;
	//std::cout << "totalNumPixels: " << totalNumPixels << std::endl;
	std::cout << "startingPointOrig: " << startingPointOrig << std::endl;
	std::cout << "startingPointFloating: " << startingPointFloating << std::endl;
	
	double *imageSubset = NULL;
	imageSubset = new double[totalNumPixels];
	double *interImage = NULL;
	interImage = new double[totalNumPixels];
	int imageArrayIndex = 0;
	int newImageArrayIndex = 0;
	int pixel0_index = 0;
	int pixel1_index = 0;
	int pixel2_index = 0;
	int pixel3_index = 0;
	double meanPixelValue = 0;
	
	double distanceMeasure4 = 0;
	
	//Populating interImage array
	for(int i = 0; i<shiftedYSize; i++)
	{
		for(int j = 0; j<shiftedXSize; j++)
		{
			imageArrayIndex = startingPointOrig + (i*imageXSize) + j;
			pixel0_index = startingPointFloating + (i*imageXSize) + j;
			pixel1_index = (startingPointFloating + (i*imageXSize) + j)+1;
			pixel2_index = (startingPointFloating + (i*imageXSize) + j)+imageXSize;
			pixel3_index = (startingPointFloating + (i*imageXSize) + j)+imageXSize + 1;
				
			//std::cout << "imageIndex: " << imageArrayIndex << std::endl;
			//std::cout << "index: " << newImageArrayIndex << std::endl;
			//std::cout << "[" << pixel0_index << "][" << pixel1_index << "]\n";
			//std::cout << "[" << pixel2_index << "][" << pixel3_index << "]\n";
			
			imageSubset[newImageArrayIndex] = image[imageArrayIndex];
			
			pixels[0] = image[pixel0_index];
			
			if(pixel1_index % shiftedXSize-1 == 0)
			{
				if( pixel2_index >= totalNumPixels)
				{
					pixels[1] = pixels[0];
				}
				else
				{
					meanPixelValue = (pixels[0] + image[pixel2_index])/2;
					pixels[1] = meanPixelValue;
				}
			}
			else
			{
				pixels[1] = image[pixel1_index];
			}
			
			if( pixel2_index >= totalNumPixels)
			{
				meanPixelValue = (image[pixel0_index]+image[pixel1_index])/2;
				pixels[2] = meanPixelValue;
				pixels[3] = meanPixelValue;
			}
			else
			{
				pixels[2] = image[pixel2_index];
				pixels[3] = image[pixel3_index];
			}
			
			//for(int k = 0; k < 4; k++)
			//{
			//	std::cout << "pixels[" << k << "] = " << pixels[k] << std::endl;
			//}
			
			interImage[newImageArrayIndex] = interpolation->bilinear(xShiftFloatingPoint,
																				yShiftFloatingPoint,
																				pixels);
			
			distanceMeasure4 = distanceMeasure4 + 
				vecImageMeasures->calcManhattenIncrementDistanceWithInterpolation(image[imageArrayIndex],
																				  xShiftFloatingPoint,
																				  yShiftFloatingPoint,
																				  pixels);
			
			newImageArrayIndex++;
		}
	}
	/*
	for(int i = 0; i < totalNumPixels; i++)
	{
		std::cout << imageSubset[i] << ",\t";
		if( i % shiftedXSize == shiftedXSize-1)
		{
			std::cout << std::endl;
		}
	}
	std::cout << std::endl;
	
	for(int i = 0; i < totalNumPixels; i++)
	{
		std::cout << interImage[i] << ",\t";
		//std::cout << i % shiftedXSize << "), ";
		if( i % shiftedXSize == shiftedXSize-1)
		{
			std::cout << std::endl;
		}
	}
	std::cout << std::endl;*/
	
	double imageSum = mathUtils->sumVector(imageSubset,totalNumPixels);
	double interSum = mathUtils->sumVector(interImage,totalNumPixels);
	std::cout << "image Sum: " << imageSum << std::endl;
	std::cout << "inter Sum: " << interSum << std::endl;
	
	double vectorDifference = mathUtils->absoluteValue(imageSum-interSum);
	
	distanceMeasure = vecImageMeasures->calcEuclideanDistance(imageSubset,interImage,shiftedXSize,shiftedYSize);
	double distanceMeasure2 = vecImageMeasures->calcManhattenDistance(imageSubset,interImage,shiftedXSize,shiftedYSize);
	double distanceMeasure3 = vecImageMeasures->calcChebyshevDistance(imageSubset,interImage,shiftedXSize,shiftedYSize);
	
	distanceMeasure4 = distanceMeasure4/totalNumPixels;
	distanceMeasure4 = sqrt(distanceMeasure4);
	
	std::cout << "Vector Difference: " << vectorDifference << std::endl;
	std::cout << "Euclidean Distance: " << distanceMeasure << std::endl;
	std::cout << "Manhattan Distance: " << distanceMeasure2 << std::endl;
	std::cout << "Chebyshev Distance: " << distanceMeasure3 << std::endl;
	std::cout << "Manhatten Interpolated Distance: " << distanceMeasure4 << std::endl<< std::endl;
	
	if( vecImageMeasures != NULL)
	{
		delete vecImageMeasures;
	}
	if( imageSubset != NULL )
	{
		delete imageSubset;
	}
	if( interImage != NULL)
	{
		delete interImage;
	}
	
	return distanceMeasure4;
}

void TestImageRegistration::testTriangularImageInterpolation()
{
	VectorImageMeasures *vecImageMeasures = NULL;
	vecImageMeasures = new VectorImageMeasures;
	
	Interpolation *interpolation;
	interpolation = new Interpolation;
	
	double pixels1[4];
	
	pixels1[0] = 137.14;
	pixels1[1] = 159.82;
	pixels1[2] = 143.72;
	pixels1[3] = 155.63;
	
	std::cout << "Original Pixels:\n";
	std::cout << "pixels1[0]: " << pixels1[0] << std::endl;
	std::cout << "pixels1[1]: " << pixels1[1] << std::endl;
	std::cout << "pixels1[2]: " << pixels1[2] << std::endl;
	std::cout << "pixels1[3]: " << pixels1[3] << std::endl;
	
	double output = 0;
	double storeInterpolatedImage1[6][6];
	int xCount = 0;
	int yCount = 0;
	
	std::cout << "Set 1:\n";
	
	for(double i = 0; i <= 1; i=i+0.2)
	{
		for(double j = 0; j<=1; j=j+0.2)
		{
			output = interpolation->triangleAverage(j,i,pixels1);
			std::cout << output << ",";
			storeInterpolatedImage1[xCount++][yCount] = output;
		}
		std::cout << "\n";
		yCount++;
		xCount = 0;
	}
}	


TestImageRegistration::~TestImageRegistration()
{
	
}
