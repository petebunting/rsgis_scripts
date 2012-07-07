/*
 *  ImageUtils.cpp
 *  CCWProject
 *
 *  Created by Pete Bunting on 14/01/2008.
 *  Copyright 2008 Aberystwyth University. All rights reserved.
 *
 */

#include "ImageUtils.h"

ImageUtils::ImageUtils()
{
	
}

void ImageUtils::rasterizeDefiniens(GDALDataset *input, 
									const char *outputFile, 
									const char *fileAttribs, 
									int numAttributes, 
									int ignorelines)
{
	// Register GDAL
	GDALAllRegister();
	
	// Get statistics from original image
	int xSize = input->GetRasterXSize();
	int ySize = input->GetRasterYSize();
	
	double *transformation = NULL;
	transformation = new double[6];
	input->GetGeoTransform(transformation);	
	
	// Get Driver
	GDALDriver *poDriver;
	poDriver = GetGDALDriverManager()->GetDriverByName("GTIFF");
	if(poDriver == NULL)
	{
		std::cout << "Driver does not exists!";
		std::exit(-1);
	}
	
	// Create new file. 
	GDALDataset *outputImage;
	outputImage = poDriver->Create(outputFile, xSize, ySize, numAttributes, GDT_Float32, poDriver->GetMetadata());
	outputImage->SetGeoTransform(transformation);
	outputImage->SetProjection(input->GetProjectionRef());
	
	std::cout << "New image has size [" << xSize << "," << ySize << "] and " << numAttributes << " bands." << std::endl;
	
	GDALRasterBand *inputBand = input->GetRasterBand(1);
	std::vector<AttribStruct> *memAttribs = new std::vector<AttribStruct>();
	this->readAttributes(fileAttribs, memAttribs, ignorelines, numAttributes);
	std::cout << "Got " << memAttribs->size() << " attributes\n";
	
	// Iterate through the input file and calculate new file pixels on a per attribute(band) basis
	for(int i = 0; i < numAttributes; i++)
	{
		std::cout << "Processing Band " << i+1 << " of " << numAttributes << std::endl;
		//this->printAttributes(memAttribs, numAttributes);
		this->rasterizeDefiniensImageBand(inputBand, outputImage->GetRasterBand(i+1), memAttribs, (i+1));
	}
	
	// Clear memory and finish
	if(memAttribs != NULL)
	{
		delete memAttribs;
	}
	GDALClose(outputImage);
}


void ImageUtils::rasterizeDefiniensImageBand(GDALRasterBand *inputBand, 
											 GDALRasterBand *outputBand, 
											 std::vector<AttribStruct> *attributes,
											 int band)
{
	int xSize = inputBand->GetXSize();
	int ySize = inputBand->GetYSize();
	
	float *imgData = NULL;
	imgData = (float *) CPLMalloc(sizeof(float)*xSize);
	
	for(int i = 0; i < ySize; i++)
	{
		inputBand->RasterIO(GF_Read, 0, i, xSize, 1, imgData, xSize, 1, GDT_Float32, 0, 0);
		for(int j = 0; j < xSize; j++)
		{
			imgData[j] = attributes->at((imgData[j])).attributes[band-1];
		}
		outputBand->RasterIO(GF_Write, 0, i, xSize, 1, imgData, xSize, 1, GDT_Float32, 0, 0);
	}
	
	if(imgData != NULL)
	{
		delete imgData;
	}
}

void ImageUtils::readAttributes(const char *attributesFile, 
								std::vector<AttribStruct> *attributes, 
								int ignorelines, 
								int numAttributes)
{
	std::ifstream inFile;
	inFile.open(attributesFile);
	
	if(inFile.is_open())
	{
		int lineNum = 0;
		std::string strLine;
		
		while(!inFile.eof())
		{
			//std::cout << "LineNum: " << lineNum << std::endl;
			getline(inFile, strLine, '\n');
			if( lineNum > ignorelines)
			{
				AttribStruct *attribute = new AttribStruct;
				this->convertLineToAttribute(&strLine, attribute, numAttributes);
				attributes->push_back(*attribute);
			}
			lineNum++;
		}
	}
	else
	{
		std::cout << "Could not open file!\n";
	}
	
	inFile.close();
}

void ImageUtils::printAttributes(std::vector<AttribStruct> *attributes, 
								 int numAttributes)
{
	int numFeatures = (int)attributes->size();
	 for(int i = 0; i < numFeatures; i++)
	 {
		std::cout << i << " id = " << attributes->at(i).objID << "\t[";
		for(int j = 0; j < numAttributes; j++)
		{
			std::cout << attributes->at(i).attributes[j] << ", ";
		}
		std::cout << "]\n";
	 }
}

void ImageUtils::convertLineToAttribute(std::string *strLine, 
										AttribStruct *attribute, 
										int numAttributes)
{
	const char *line = strLine->c_str();
	int lineLength = 0;
	lineLength = (int)strLine->size();
	std::string word;
	word.clear();
	int j = 0;
	float wordFloat = 0.0;
	int wordInt = 0;
	const char *semiColon = ";";
	int numWords = 0;
	attribute->attributes = new float[numAttributes];
	for(int i = 0; i < numAttributes; i++)
	{
		attribute->attributes[i] = 0;
	}
	
	for(int i = 0; i < lineLength; i++)
	{
		if(*semiColon == line[i])
		{
			j = 0;
			wordFloat = (float)atof(word.c_str());
			if(numWords == 0)
			{
				wordInt = (int)wordFloat;
				attribute->objID = wordInt;
			}
			else
			{
				attribute->attributes[numWords-1] = wordFloat;
			}
			numWords++;
			word.clear();
		}
		else
		{
			word.append(&line[i]);
		}
	}
	wordFloat = (float)atof(word.c_str());
	attribute->attributes[numAttributes-1] = wordFloat;
}

int ImageUtils::countNumLines(const char *attributesFile)
{
	int i = 0;
	
	std::ifstream inFile;
	inFile.open(attributesFile);
	
	if(inFile.is_open())
	{

		while(!inFile.eof())
		{
			i++;
		}
	}
	inFile.close();
	return i;
}

ImageUtils::~ImageUtils()
{
	
}
