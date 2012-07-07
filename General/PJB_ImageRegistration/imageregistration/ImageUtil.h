/*
 *  ImageUtil.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef ImageUtil_H
#define ImageUtil_H

#include "gdal_priv.h"
#include "ImageHistogram.h"
#include "Interpolation.h"
#include <iostream>


class ImageUtil
{
public:
	ImageUtil();
	ImageUtil(const char *filepath);
	void generateHistogram(ImageHistogram &imageHistogram);
	void getImage4Read(const char *filepath);
	void interpolateImage(const char *outputFilepath, const char *format, double xRes, double yRes, int band);
	~ImageUtil();
protected:
	GDALDataset *dataset;
};
#endif
