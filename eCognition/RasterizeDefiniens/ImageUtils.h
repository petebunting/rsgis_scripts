/*
 *  ImageUtils.h
 *  CCWProject
 *
 *  Created by Pete Bunting on 14/01/2008.
 *  Copyright 2008 Aberystwyth University. All rights reserved.
 *
 */

#ifndef ImageUtils_H
#define ImageUtils_H

#include "gdal_priv.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <string>
#include <sstream>

struct AttribStruct
{
	int objID;
	float *attributes;
};

class ImageUtils
	{
	public: 
		ImageUtils();
		void rasterizeDefiniens(GDALDataset *input, const char *outputFile, const char *fileAttribs, int numAttributes, int ignorelines);
		void rasterizeDefiniensImageBand(GDALRasterBand *inputBand, GDALRasterBand *outputBand, std::vector<AttribStruct> *attributes, int band);
		void readAttributes(const char *attributesFile, std::vector<AttribStruct> *attributes, int ignorelines, int numAttributes);
		void printAttributes(std::vector<AttribStruct> *attributes, int numAttributes);
		void convertLineToAttribute(std::string *line, AttribStruct *attribute, int numAttributes);
		int countNumLines(const char *attributesFile);
		~ImageUtils();
	};
#endif
