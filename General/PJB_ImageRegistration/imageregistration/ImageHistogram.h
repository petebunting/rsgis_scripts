/*
 *  ImageHistogram.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */
#ifndef ImageHistogram_H
#define ImageHistogram_H

#include <iostream>
#include "gdal_priv.h"
#include "string.h"

class ImageHistogram
{
public:
	ImageHistogram();
	ImageHistogram(int numBins);
	ImageHistogram(GDALDataset *data, int band, int numBins);
	void calcHistogram(GDALDataset *data, int band);
	int getNumberBins();
	void getFrequencies(int *freq);
	void getBinRanges(double *ranges);
	double getBinRange();
	void setNumberBins(int numBins);
	double getMax();
	double getMin();
	void printTextHistogram();
	//void printImageHistogram(string filepath, int fileformat);
	~ImageHistogram();
private:
	int numBins;
	double max;
	double min;
	double difference;
	double binRange;
	int *frequencies;
	double *binRanges;
};

#endif

