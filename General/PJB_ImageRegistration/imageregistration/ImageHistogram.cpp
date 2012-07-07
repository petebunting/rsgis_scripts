/*
 *  ImageHistogram.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/11/2005.
 *  Copyright 2005 University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "ImageHistogram.h"


/*
 * Default constructor sets the number of bins to 100 by default. 
 * If you wish to change this use setNumberBins() or another constructor
 */
ImageHistogram::ImageHistogram()
{
	this->numBins=100;
}

/*
 * Constructor which allows the number of bins to be set.
 */
ImageHistogram::ImageHistogram(int numBinslocal)
{
	this->numBins = numBinslocal;
}

/*
 * Constructor which does everything. Take in data, band to be proceeded and number of bins.
 * Also runs method to create histogram.
 */
ImageHistogram::ImageHistogram(GDALDataset *data, int band, int numBinslocal)
{
	this->numBins = numBinslocal;
	this->calcHistogram(data, band);
}

/*
 * Performs calculation to generate the histogram and set other values.
 *
 */
void ImageHistogram::calcHistogram(GDALDataset *data, int band)
{
	if(data == NULL)
	{
		std::cout<<"Error data NULL\n";
		return;
	}
	
	if(band > data->GetRasterCount())
	{
		std::cout<<"Not enough bands in image to complete request\n";
		return;
	}
	
	GDALRasterBand *rasterband = data->GetRasterBand(band);
	
	int xSize = rasterband->GetXSize();
	int ySize = rasterband->GetYSize();
	
	this->max = this->min = 0;
	
	float *scanline;
	scanline = (float *) CPLMalloc(sizeof(float)*xSize);
	for(int i=0; i<ySize; i++)
	{
		rasterband->RasterIO(GF_Read, 0, i, xSize, 1, scanline, xSize, 1, GDT_Float32, 0, 0);
		for(int j=0; j<xSize; j++)
		{
			if(i==0 & j==0)
			{
				this->max = this->min = scanline[j];
			}
			else if(scanline[j] > max)
			{
				this->max = scanline[j];
			}
			else if(scanline[j] < min)
			{
				this->min = scanline[j];
			}
		}
		
	}
	
	difference = this->max - this->min;
	this->binRange = difference/this->numBins;
	
	this->binRanges = new double[this->numBins+1];
	this->getBinRanges(this->binRanges);

	this->frequencies = new int[this->numBins];
	for(int i=0; i<this->numBins; i++)
	{
		this->frequencies[i] = 0;
	}
	
	for(int i=0; i<ySize; i++)
	{
		rasterband->RasterIO(GF_Read, 0, i, xSize, 1, scanline, xSize, 1, GDT_Float32, 0, 0);
		for(int j=0; j<xSize; j++)
		{
			for(int k=1; k<numBins+1; k++)
			{
				if(scanline[j] >= this->binRanges[k-1] & scanline[j] <= this->binRanges[k])
				{
					this->frequencies[k-1]++;
					break;
				}
			}
		}
	}
}

int ImageHistogram::getNumberBins()
{
	return numBins;
}

void ImageHistogram::getFrequencies(int *freq)
{
	freq = frequencies;
}

void ImageHistogram::getBinRanges(double *ranges)
{
	ranges[0] = this->min;
	for(int i=1; i<this->numBins; i++)
	{
		ranges[i] = ranges[i-1] + this->binRange;
	}
	ranges[numBins] = this->max;
}

double ImageHistogram::getBinRange()
{
	return binRange;
}

void ImageHistogram::setNumberBins(int numBinslocal)
{
	this->numBins = numBinslocal;
}

double ImageHistogram::getMax()
{
	return this->max;
}

double ImageHistogram::getMin()
{
	return this->min;
}


/*
 * Function which converts the histogram in text and prints to the console.
 */
void ImageHistogram::printTextHistogram()
{
	std::cout << "MAX: " << this->max << "\nMIN: " << this->min << std::endl;
	std::cout<< "Histogram:" << std::endl;
	for(int i=0; i<this->numBins; i++)
	{
		std::cout<< this->binRanges[i] << " - " << this->binRanges[i+1] << " : " << this->frequencies[i] << std::endl;
	}
}

/*
 * Function which converts the histogram in an image outputs to file.
 *
void ImageHistogram::printImageHistogram(string filepath, int fileformat)
{
	std::cout<< "NOT IMPLEMENTED YET!!! ...ImageHistogram::printImageHistogram(string filepath, int fileformat)\n";
}*/

ImageHistogram::~ImageHistogram()
{
	delete this->frequencies;
	delete this->binRanges;
}
