/*
 *  ImageUtil.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "ImageUtil.h"


ImageUtil::ImageUtil()
{
	
}

/**
 * Constructor takes in filepath on which all operations will be performed within this class.
 */
ImageUtil::ImageUtil(const char *filepath)
{
	// Get dataset
	this->getImage4Read(filepath);
}

void ImageUtil::generateHistogram(ImageHistogram &imageHistogram) 
{
	// Check whether dataset is null before proceeding.
	if(dataset == NULL)
	{
		std::cout<<"Data is null before trying to create histogram\n";
		return;
	}
	// Generate Histogram.
	imageHistogram.calcHistogram(dataset,1);
}

/**
 * Funcation for getting hold of the image..
 */
void ImageUtil::getImage4Read(const char *filepath)
{
	// Register the drivers for the supported file formats.
	GDALAllRegister();
	//Get Datasete
	dataset = (GDALDataset *) GDALOpen(filepath, GA_ReadOnly);
	// Check read in correctly.
	if(dataset == NULL)
	{
		std::cout << "Bugger could not open Image so throwing an Exception..";
	}
	else
	{
		//std::cout << "Data from " << filepath << " has been read in OK!\n";
	}
}

void ImageUtil::interpolateImage(const char *outputFilepath, const char *format, double xRes, double yRes, int band)
{
	Interpolation interpolation;
	
	interpolation.createNewImage(dataset, xRes, yRes, outputFilepath, format, band);
}

ImageUtil::~ImageUtil()
{
	delete this->dataset;
}
