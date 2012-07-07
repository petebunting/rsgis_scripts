/*
 *  MathUtils.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 25/03/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "MathUtils.h"

MathUtils::MathUtils()
{
	
}

double MathUtils::findFloatingPointComponent(double floatingPointNum, int *integer)
{
	//std::cout << "Starting find floating point\n";
	*integer = 0;
	bool negative = false;
	if(floatingPointNum < 0)
	{
		floatingPointNum = floatingPointNum * (-1);
		negative = true;
	}
	
	int reduction = 100000000;
	
	while(floatingPointNum > 1)
	{
		while(floatingPointNum > reduction & reduction != 0)
		{
			//std::cout << "floatingPointNum = " << floatingPointNum << " reduction = " << reduction << std::endl;
			floatingPointNum = floatingPointNum - reduction;
			*integer = *integer + reduction;
		}
		//std::cout << "Adjust reduction: floatingPointNum = " << floatingPointNum << std::endl;
		reduction = reduction / 10;
	}
	if(floatingPointNum > -0.000000001 & floatingPointNum < 0.000000001)
	{
		floatingPointNum = 0;
	}
	if(floatingPointNum > 0.999999999 & floatingPointNum < 1.000000001)
	{
		floatingPointNum = 0;
		*integer = *integer + 1;
	}
	
	if( negative )
	{
		*integer = (*integer) * (-1);
	}
	//std::cout << "finished floating point\n";
	return floatingPointNum;
}

double MathUtils::sumVector(double *vector, int size)
{
	double sum = 0;
	for(int i = 0; i< size; i++)
	{
		sum  = sum + vector[i];
	}
	return sum;
}

int MathUtils::sumIntArray(int *array, int size)
{
	int sum = 0;
	for(int i = 0; i< size; i++)
	{
		sum  = sum + array[i];
	}
	return sum;
}

int MathUtils::roundDown(double number)
{
	double afterfloatingpoint = 0;
	int b4floatingpoint = 0;
	if( number > 0 )
	{
		afterfloatingpoint = this->findFloatingPointComponent(number, &b4floatingpoint);
	}
	else if( number < 0 )
	{
		afterfloatingpoint = this->findFloatingPointComponent(number, &b4floatingpoint);
		if( afterfloatingpoint != 0 )
		{
			b4floatingpoint--;
		}
	}
	else
	{
		b4floatingpoint = 0;
	}
	return b4floatingpoint;
}

int MathUtils::round(double number)
{
	double afterfloatingpoint = 0;
	int b4floatingpoint = 0;
	int rounded = 0;

	if(number > 0)
	{
		afterfloatingpoint = this->findFloatingPointComponent(number, &b4floatingpoint);
		if(afterfloatingpoint < 0.5)
		{
			rounded = b4floatingpoint;
		}
		else 
		{
			rounded = b4floatingpoint+1;
		}
	}
	else if(number < 0)
	{
		afterfloatingpoint = this->findFloatingPointComponent(number, &b4floatingpoint);
		if(afterfloatingpoint < 0.5)
		{
			rounded = b4floatingpoint;
		}
		else 
		{
			rounded = b4floatingpoint-1;
		}
	}
	else
	{
		rounded = 0;
	}
		
	
	return rounded;
}

int MathUtils::roundUp(double number)
{
	double afterfloatingpoint = 0;
	int b4floatingpoint = 0;
	if(number > 0)
	{
		afterfloatingpoint = this->findFloatingPointComponent(number, &b4floatingpoint);
		if( afterfloatingpoint != 0 )
		{
			b4floatingpoint++;
		}
	}
	else if(number < 0)
	{
		afterfloatingpoint = this->findFloatingPointComponent(number, &b4floatingpoint);
	}
	else
	{
		b4floatingpoint = 0;
	}
	return b4floatingpoint;
}

double MathUtils::absoluteValue(double number)
{
	if(number < 0)
	{
		number = number *-1;
	}
	return number;
}

double MathUtils::tileMean(TileCoords *tile, GDALDataset *image, bool imageA, int band)
{
	int imageSizeX = 0;
	int imageSizeY = 0;
	int xStart = 0;
	int yStart = 0;
	int counter = 0;
	double mean = 0;
	double sum = 0;
	if(imageA)
	{
		imageSizeX = tile->imgABRX - tile->imgATLX;
		imageSizeY = tile->imgABRY - tile->imgATLY;
		xStart = tile->imgATLX;
		yStart = tile->imgATLY;
	}
	else
	{
		imageSizeX = tile->imgBBRX - tile->imgBTLX;
		imageSizeY = tile->imgBBRY - tile->imgBTLY;
		xStart = tile->imgBTLX;
		yStart = tile->imgBTLY;
	}
	
	float *imageScanline;
	imageScanline = (float *) CPLMalloc(sizeof(float)*imageSizeX);
	GDALRasterBand *rasterband = image->GetRasterBand(band);
	for(int i=0; i < (imageSizeY-1); i++)
	{
		rasterband->RasterIO(GF_Read, 
								xStart, 
								(yStart+i), 
								imageSizeX, 
								1, 
								imageScanline, 
								imageSizeX, 
								1, 
								GDT_Float32, 
								0, 
								0);
		for(int j=0; j<(imageSizeX-1); j++)
		{
			sum += imageScanline[j];
			counter++;
		}
	}
	
	mean = sum/counter;
	return mean;
}

double MathUtils::tileStandardDeviation(TileCoords *tile, 
										GDALDataset *image, 
										bool imageA, 
										int band)
{
	int imageXSize = image->GetRasterXSize();
	int imageYSize = image->GetRasterYSize();
	//std::cout << "image Size: [" << imageXSize << ", " << imageYSize << "]" << std::endl;
	if(imageA)
	{
		//std::cout << "tile A: [" << tile->imgATLX << ", " << tile->imgATLY << "][" 
		//<< tile->imgABRX << ", " << tile->imgABRY << "]" << std::endl;
		if(tile->imgATLX < 0)
		{
			tile->imgATLX = 0;
		}
		if(tile->imgATLY < 0)
		{
			tile->imgATLY = 0;
		}
		if(tile->imgABRX > imageXSize)
		{
			tile->imgABRX = imageXSize;
		}
		if(tile->imgABRY > imageYSize)
		{
			tile->imgABRY = imageYSize;
		}
	}
	else
	{
		//std::cout << "tile B: [" << tile->imgBTLX << ", " << tile->imgBTLY << "][" 
		//<< tile->imgBBRX << ", " << tile->imgBBRY << "]" << std::endl;
		if(tile->imgBTLX < 0)
		{
			tile->imgBTLX = 0;
		}
		if(tile->imgBTLY < 0)
		{
			tile->imgBTLY = 0;
		}
		if(tile->imgBBRX > imageXSize)
		{
			tile->imgBBRX = imageXSize;
		}
		if(tile->imgBBRY > imageYSize)
		{
			tile->imgBBRY = imageYSize;
		}
	}
	
	int tileSizeX = 0;
	int tileSizeY = 0;
	int xStart = 0;
	int yStart = 0;
	int counter = 0;
	
	double mean = this->tileMean(tile, image, imageA, band);
	double sum = 0;
	double stddev = 0;
	if(imageA)
	{
		tileSizeX = tile->imgABRX - tile->imgATLX;
		tileSizeY = tile->imgABRY - tile->imgATLY;
		xStart = tile->imgATLX;
		yStart = tile->imgATLY;
	}
	else
	{
		tileSizeX = tile->imgBBRX - tile->imgBTLX;
		tileSizeY = tile->imgBBRY - tile->imgBTLY;
		xStart = tile->imgBTLX;
		yStart = tile->imgBTLY;
	}
	//std::cout << "Tile Size: [" << tileSizeX << ", " << tileSizeY << "]\n";
	float *imageScanline;
	imageScanline = (float *) CPLMalloc(sizeof(float)*tileSizeX);
	GDALRasterBand *rasterband = image->GetRasterBand(band);
	for(int i=0; i < (tileSizeY-1); i++)
	{
		rasterband->RasterIO(GF_Read, 
							 xStart, 
							 (yStart+i), 
							 tileSizeX, 
							 1, 
							 imageScanline, 
							 tileSizeX, 
							 1, 
							 GDT_Float32, 
							 0, 
							 0);
		for(int j=0; j<(tileSizeX-1); j++)
		{
			sum += ((imageScanline[j]-mean)*(imageScanline[j]-mean));
			counter++;
		}
	}
	sum = sqrt(sum);
	stddev = sum/(counter-1);
	return stddev;
}

double MathUtils::tileVariation(TileCoords *tile, GDALDataset *image, bool imageA, int band)
{
	int imageXSize = image->GetRasterXSize();
	int imageYSize = image->GetRasterYSize();
	if(imageA)
	{
		if(tile->imgATLX < 0)
		{
			tile->imgATLX = 0;
		}
		if(tile->imgATLY < 0)
		{
			tile->imgATLY = 0;
		}
		if(tile->imgABRX > imageXSize)
		{
			tile->imgABRX = imageXSize;
		}
		if(tile->imgABRY > imageYSize)
		{
			tile->imgABRY = imageYSize;
		}
	}
	else
	{
		if(tile->imgBTLX < 0)
		{
			tile->imgBTLX = 0;
		}
		if(tile->imgBTLY < 0)
		{
			tile->imgBTLY = 0;
		}
		if(tile->imgBBRX > imageXSize)
		{
			tile->imgBBRX = imageXSize;
		}
		if(tile->imgBBRY > imageYSize)
		{
			tile->imgBBRY = imageYSize;
		}
	}
	
	int tileSizeX = 0;
	int tileSizeY = 0;
	int xStart = 0;
	int yStart = 0;
	int counter = 0;
	
	double mean = this->tileMean(tile, image, imageA, band);
	double sum = 0;
	double var = 0;
	if(imageA)
	{
		tileSizeX = tile->imgABRX - tile->imgATLX;
		tileSizeY = tile->imgABRY - tile->imgATLY;
		xStart = tile->imgATLX;
		yStart = tile->imgATLY;
	}
	else
	{
		tileSizeX = tile->imgBBRX - tile->imgBTLX;
		tileSizeY = tile->imgBBRY - tile->imgBTLY;
		xStart = tile->imgBTLX;
		yStart = tile->imgBTLY;
	}
	
	float *imageScanline;
	imageScanline = (float *) CPLMalloc(sizeof(float)*tileSizeX);
	GDALRasterBand *rasterband = image->GetRasterBand(band);
	for(int i=0; i < (tileSizeY-1); i++)
	{
		rasterband->RasterIO(GF_Read, 
							 xStart, 
							 (yStart+i), 
							 tileSizeX, 
							 1, 
							 imageScanline, 
							 tileSizeX, 
							 1, 
							 GDT_Float32, 
							 0, 
							 0);
		for(int j=0; j<(tileSizeX-1); j++)
		{
			sum += this->absoluteValue(imageScanline[j]-mean);
			counter++;
		}
	}
	var = sum/(counter);
	
	return var;
}

//if < 0 is inputted as the Range the range will be calculated!
double MathUtils::tileRangePercentage(TileCoords *tile, 
									  GDALDataset *image, 
									  bool imageA, 
									  int band, 
									  double imageRange)
{
	if(imageRange < 0)	
	{
		imageRange = this->imageRange(image, band);
	}
	double tileRange = this->tileRange(tile, image, imageA, band);
	double rangePercentage = tileRange/imageRange;
	return rangePercentage;
}

double MathUtils::tileRange(TileCoords *tile, GDALDataset *image, bool imageA, int band)
{
	//std::cout << "[" << tile->imgATLX << ", " << tile->imgATLY << "][" 
	//<< tile->imgABRX << ", " << tile->imgABRY << "]\n";
	//std::cout << "[" << tile->imgBTLX << ", " << tile->imgBTLY << "][" 
	//<< tile->imgBBRX << ", " << tile->imgBBRY << "]\n";
	//std::cout << "[" << tile->eastingTL << ", " << tile->northingTL << "][" 
	//<< tile->eastingBR << ", " << tile->northingBR << "]\n";
	
	
	int imageXSize = image->GetRasterXSize();
	int imageYSize = image->GetRasterYSize();
	if(imageA)
	{
		
		//std::cout << "Using Image A\n";
		if(tile->imgATLX < 0)
		{
			tile->imgATLX = 0;
		}
		if(tile->imgATLY < 0)
		{
			tile->imgATLY = 0;
		}
		if(tile->imgABRX > imageXSize)
		{
			tile->imgABRX = imageXSize;
		}
		if(tile->imgABRY > imageYSize)
		{
			tile->imgABRY = imageYSize;
		}
	}
	else
	{
		//std::cout << "Using Image B\n";
		if(tile->imgBTLX < 0)
		{
			tile->imgBTLX = 0;
		}
		if(tile->imgBTLY < 0)
		{
			tile->imgBTLY = 0;
		}
		if(tile->imgBBRX > imageXSize)
		{
			tile->imgBBRX = imageXSize;
		}
		if(tile->imgBBRY > imageYSize)
		{
			tile->imgBBRY = imageYSize;
		}
	}
	
	int tileSizeX = 0;
	int tileSizeY = 0;
	int xStart = 0;
	int yStart = 0;
	
	double max = 0;
	double min = 0;
	double range = 0;
	if(imageA)
	{
		tileSizeX = tile->imgABRX - tile->imgATLX;
		tileSizeY = tile->imgABRY - tile->imgATLY;
		xStart = tile->imgATLX;
		yStart = tile->imgATLY;
	}
	else
	{
		tileSizeX = tile->imgBBRX - tile->imgBTLX;
		tileSizeY = tile->imgBBRY - tile->imgBTLY;
		xStart = tile->imgBTLX;
		yStart = tile->imgBTLY;
	}
	
	//std::cout << "TileSizeX = " << tileSizeX << " TileSizeY = " << tileSizeY <<std::endl;
	//std::cout << "xStart = " << xStart << " yStart = " << yStart << std::endl;
	
	float *imageScanline;
	//std::cout << "Allocating memory sizeof(float)*tileSizeX = " 
	//<< sizeof(float)*tileSizeX << std::endl;
	imageScanline = (float *) CPLMalloc(sizeof(float)*tileSizeX);
	GDALRasterBand *rasterband = image->GetRasterBand(band);
	for(int i=0; i < (tileSizeY-1); i++)
	{
		rasterband->RasterIO(GF_Read, 
							 xStart, 
							 (yStart+i), 
							 tileSizeX, 
							 1, 
							 imageScanline, 
							 tileSizeX, 
							 1, 
							 GDT_Float32, 
							 0, 
							 0);
		for(int j=0; j<(tileSizeX-1); j++)
		{
			if( (imageScanline[j] < 100000000000000000.0 
				 & imageScanline[j] > -10000000000000000000.0))
			{
				if(i == 0 & j == 0)
				{
					min = imageScanline[j];
					max = imageScanline[j];
				}
				if(imageScanline[j] > max)
				{
					max  = imageScanline[j];
				}
				if( imageScanline[j] < min)
				{
					min = imageScanline[j];
				}
			}
		}
	}
	range = max - min;
	if(imageScanline != NULL)
	{
		CPLFree(imageScanline);
	}
	return range;
}

double MathUtils::imageRange(GDALDataset *image, int band)
{
	int imageXSize = image->GetRasterXSize();
	int imageYSize = image->GetRasterYSize();
	
	double min = 0;
	double max = 0;
	double range = 0;
	
	float *imageScanline;
	imageScanline = (float *) CPLMalloc(sizeof(float)*imageXSize);
	GDALRasterBand *rasterband = image->GetRasterBand(band);
	
	for(int i=0; i < imageYSize; i++)
	{
		rasterband->RasterIO(GF_Read, 
							 0, 
							 i, 
							 imageXSize, 
							 1, 
							 imageScanline, 
							 imageXSize, 
							 1, 
							 GDT_Float32, 
							 0, 
							 0);
		for(int j=0; j<imageXSize; j++)
		{
			if( (imageScanline[j] < 100000000000000000.0 & 
				 imageScanline[j] > -10000000000000000000.0))
			{
				if(i == 0 & j == 0)
				{
					min = imageScanline[j];
					max = imageScanline[j];
				}
				if(imageScanline[j] > max)
				{
					max  = imageScanline[j];
				}
				if( imageScanline[j] < min)
				{
					min = imageScanline[j];
				}
			}
		}
	}
	
	range = max - min;
	if(imageScanline != NULL)
	{
		CPLFree(imageScanline);
	}
	return range;
}

int MathUtils::randomWithinRange(int lower, int upper)
{
	int value = 0;
	int diff = this->round(this->absoluteValue(upper - lower));
	//std::cout << "Lower = " << lower << " Upper = " << upper << std::endl;
	//std::cout << "Difference = " << diff << std::endl;
	double random = rand();
	//std::cout << "Random = " << random << std::endl;
	double randomZeroOne = random/(RAND_MAX-1);
	//std::cout << "Random (range 0-1) = " << randomZeroOne << std::endl;
	double b4Round = (diff * randomZeroOne) + lower;
	//std::cout << "Before round = " << b4Round << std::endl;
	value = this->round(b4Round);
	//std::cout << "Random (range " << lower << "-" << upper << ") = " << value << std::endl << std::endl;
	return value;
}

MathUtils::~MathUtils()
{
	
}
