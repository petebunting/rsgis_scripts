/*
 *  Interpolation.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 25/03/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "Interpolation.h"

Interpolation::Interpolation()
{
	
}

double Interpolation::areaBasedBilinear(double xShift, double yShift, double *pixels)
{
	/************ Calculate New Pixel Value ************/
	double pixelValue = 0;
	
	pixelValue = ((1-xShift) * (1-yShift) * pixels[0]) + 
		(xShift * (1-yShift) * pixels[1]) +
		((1-xShift) * yShift * pixels[2]) +
		(xShift * yShift * pixels[3]);
	/*****************************************************/
	
	return pixelValue;
}

double Interpolation::bilinear(double xShift, double yShift, double *pixels)
{
	/************ Calculate New Pixel Value ************/
	double pixelValue = 0;
	double x1Linear = 0;
	double x2Linear = 0;
	
	x1Linear = ((1-xShift)*pixels[0]) + (xShift*pixels[1]);
	x2Linear = ((1-xShift)*pixels[2]) + (xShift*pixels[3]);
	
	pixelValue = ((1-yShift)*x1Linear)+(yShift * x2Linear);
	/*****************************************************/

	return pixelValue;
}

double Interpolation::nearestNeighbour(double xShift, double yShift, double *pixels) 
{
	ArrayUtils *arrayUtil;
	arrayUtil = new ArrayUtils;
	
	/************ Calculate New Pixel Value ************/
	double pixelValue = 0;
	int pixelIndex = 0;
	
	double pixelOverlaps [4];
	
	pixelOverlaps[0] = (1-xShift) * (1-yShift);
	pixelOverlaps[1] = xShift * (1-yShift);
	pixelOverlaps[2] = (1-xShift) * yShift;
	pixelOverlaps[3] = xShift * yShift;
	
	pixelIndex = arrayUtil->findIndexOfMax(pixelOverlaps, 4);
	
	pixelValue = pixels[pixelIndex];
	
	/*****************************************************/
	
	if(arrayUtil != NULL)
	{
		delete arrayUtil;
	}
	
	return pixelValue;
}

double Interpolation::triangleAverage(double xShift, double yShift, double *pixels)
{	
	/********** Calc pixels which create triangle ************/
	double newPixelValue1 = this->triangle(xShift, yShift, pixels, true);
	double newPixelValue2 = this->triangle(xShift, yShift, pixels, false);
	/**********************************************************/
	
	/*********** Calculate final Pixel Value ******************/
	double pixelValue = 0;
	pixelValue = (newPixelValue1 + newPixelValue2) /2;
	/***********************************************************/
	
	return pixelValue;
}

/***
 * triangulation: TRUE = ABC and FALSE = BDC
 */
double Interpolation::triangle(double xShift, 
							   double yShift, 
							   double *pixels, 
							   bool triangulation)
{	
	/********** Calc pixels which create triangle ************/
	
	double a = 0;
	double b = 0;
	double c = 0;
	
	////////////////////// Triangulation 1 //////////////////////
	double newPixelValue1 = 0;
	
	if( xShift + yShift <= 1)
	{
		c = pixels[0];
		a = pixels[1] - c;
		b = pixels[2] - c;
		
		newPixelValue1 = (a*xShift) + (b*yShift) + c;
	}
	else if( xShift + yShift > 1 )
	{
		a = pixels[3] - pixels[2];
		b = pixels[3] - pixels[1];
		c = pixels[1] - a;
		
		newPixelValue1 = (a*xShift) + (b*yShift) + c;
	}
	//////////////////////////////////////////////////////////////
	
	////////////////////// Triangulation 2 //////////////////////
	double newPixelValue2 = 0;
	a = 0;
	b = 0;
	c = 0;
	
	if( xShift - yShift >= 0 )
	{
		c = pixels[0];
		a = pixels[1] - c;
		b = pixels[3] - (a+c);
		
		newPixelValue2 = (a*xShift) + (b*yShift) + c;
	}
	else if( xShift - yShift < 0 )
	{
		c = pixels[0];
		b = pixels[2] - c;
		a = pixels[3] - (b+c);
		
		newPixelValue2 = (a*xShift) + (b*yShift) + c;
	}
	//////////////////////////////////////////////////////////////
	
	/**********************************************************/
	
	/*********** Calculate final Pixel Value ******************/
	double pixelValue = 0;
	if(triangulation)
	{
		pixelValue = newPixelValue1;
	}
	else
	{
		pixelValue = newPixelValue2;
	}
	/***********************************************************/
	
	return pixelValue;
}

double Interpolation::cubic(double xShift, double yShift, double *pixels)
{
	double pixelValue = 0;
	
	double *newPixels = new double[3];
	double *tmpPixels = new double[3];
	tmpPixels[0] = pixels[0];
	tmpPixels[1] = pixels[3];
	tmpPixels[2] = pixels[6];
	newPixels[0] = estimateNewValueFromCurve(tmpPixels, yShift);
	
	tmpPixels[0] = pixels[1];
	tmpPixels[1] = pixels[4];
	tmpPixels[2] = pixels[7];
	newPixels[1] = estimateNewValueFromCurve(tmpPixels, yShift);
	
	tmpPixels[0] = pixels[2];
	tmpPixels[1] = pixels[5];
	tmpPixels[2] = pixels[8];
	newPixels[2] = estimateNewValueFromCurve(tmpPixels, yShift);

	pixelValue = estimateNewValueFromCurve(newPixels, xShift);	
	
	if(newPixels != NULL)
	{
		delete newPixels;
	}
	if(tmpPixels != NULL)
	{
		delete tmpPixels;
	}
	return pixelValue;
}

double Interpolation::estimateNewValueFromCurve(double *pixels, double shift)
{
	double newValue = 0;
	////////////// Fit line /////////////////////
	double ax = 0;
	double bx = 0;
	double cx = 0;
	
	cx = pixels[1];
	bx = ((pixels[2]-pixels[1])-(pixels[0]-pixels[1]))/2;
	ax = pixels[2] - (cx + bx);
	
	//std::cout << "ax = " << ax << " bx = " << bx << " cx = " << cx << std::endl;
	
	///////////////////////////////////////////////
	
	/////////////// Find new value /////////////
	
	newValue = (shift*shift)*ax + shift*bx + cx;
	
	///////////////////////////////////////////
	
	return newValue;
}

Transform Interpolation::calcateSubPixelTranformationXYCurve(double *surface, 
															 int *valid, 
															 double steps, 
															 bool minmax)
{
	/************* Setup output transform *****************/
	Transform subPixelTransform;
	
	subPixelTransform.shiftX = 0;
	subPixelTransform.shiftY = 0;
	/*********************************************************/
	
	/*********** TEST Valid array **************
	for(int i = 0; i < 9; i++)
	{
		std::cout << valid[i] << ", ";
		if(i == 2 | i == 5 | i == 8)
		{
			std::cout << std::endl;
		}
	}
	*****************************************/
	
	/**************** Check surface is valid ****************/
	MathUtils mathUtils;
	
	int sumValid = mathUtils.sumIntArray(valid, 9);
	
	if(sumValid != 0)
	{
		return subPixelTransform;
	}
	
	/*********************************************************/
	
	/************** TEST: Print surface ***********************
	
	for(int i = 0; i < 9; i++)
	{
		if(valid[i] != -1)
		{
			std::cout << surface[i] << ", ";
		}
		else
		{
			std::cout << "(-1), ";
		}
		
		if(i == 2 | i == 5 | i == 8)
		{
			std::cout << std::endl;
		}
	}
	***********************************************/
	
	/**************** X Axis ***********************/
	
	////////////// Fit line /////////////////////
	double ax = 0;
	double bx = 0;
	double cx = 0;
	
	cx = surface[4];
	bx = ((surface[5]-surface[4])-(surface[3]-surface[4]))/2;
	ax = surface[5] - (cx + bx);
	
	//std::cout << "ax = " << ax << " bx = " << bx << " cx = " << cx << std::endl;
	
	///////////////////////////////////////////////
	
	//////////////// Find Subpixel shift //////////
	int totalSteps = mathUtils.roundUp((2/steps) + 1);
	
	double valueX = -1;
	double max = 0;
	double min = 0;
	double maxX = 0;
	double minX = 0;
	double surfaceValue = 0;
	
	
	for(int i = 0; i < totalSteps; i++)
	{
		surfaceValue = ((valueX*valueX)*ax) + (bx*valueX) + cx;
		//std::cout << surfaceValue << ", ";
		
		if(valueX == -1)
		{
			max = surfaceValue;
			maxX = valueX;
			min = surfaceValue;
			minX = valueX;
		}
		else if(surfaceValue > max)
		{
			max = surfaceValue;
			maxX = valueX;
		}
		else if(surfaceValue < min)
		{
			min = surfaceValue;
			minX = valueX;
		}
		
		valueX = valueX + steps;
	}
	//std::cout << std::endl;
	if(minmax)
	{
		subPixelTransform.shiftX = maxX;
	}
	else
	{
		subPixelTransform.shiftX = minX;
	}
	
	///////////////////////////////////////////////
	
	/***********************************************/
	
	/**************** Y Axis ***********************/
	
	double ay = 0;
	double by = 0;
	double cy = 0;
	
	cy = surface[4];
	by = ((surface[7]-surface[4])-(surface[1]-surface[4]))/2;
	ay = surface[7] - (cy + by);
	
	//std::cout << "ay = " << ay << " by = " << by << " cy = " << cy << std::endl;
	
	//////////////// Find Subpixel shift //////////
	totalSteps = mathUtils.roundUp((2/steps) + 1);
	
	double valueY = -1;
	max = 0;
	min = 0;
	double maxY = 0;
	double minY = 0;
	surfaceValue = 0;
	
	for(int i = 0; i < totalSteps; i++)
	{
		surfaceValue = ((valueY*valueY)*ay) + (by*valueY) + cy;
		//std::cout << surfaceValue << ", ";
		if(valueY == -1)
		{
			max = surfaceValue;
			maxY = valueY;
			min = surfaceValue;
			minY = valueY;
		}
		else if(surfaceValue > max)
		{
			max = surfaceValue;
			maxY = valueY;
		}
		else if(surfaceValue < min)
		{
			min = surfaceValue;
			minY = valueY;
		}
		
		valueY = valueY + steps;
	}
	
	//std::cout << std::endl;
	
	if(minmax)
	{
		subPixelTransform.shiftY = maxY;
	}
	else
	{
		subPixelTransform.shiftY = minY;
	}
	
	///////////////////////////////////////////////
	
	/***********************************************/
	
	
	//std::cout << "SubPixel [" << subPixelTransform.shiftX << ", " 
	//<< subPixelTransform.shiftY << "]" << std::endl;
	
	return subPixelTransform;
}

GDALDataset* Interpolation::createNewImage(GDALDataset *data, 
										   double outputXResolution,
										   double outputYResolution,
										   const char *filename, 
										   const char *format, 
										   int band)
throw(FileOutputException, ImageOutputException)
{
	// Image Data Stores.
	float *scanline0 = NULL;
	float *scanline1 = NULL;
	float *scanline2 = NULL;
	double *transformation = NULL;
	float *newLine = NULL;
	double *pixels = NULL;
	GDALDataset *outputtmp = NULL;
	try
	{
		MathUtils mathUtils;
		GDALDataset *output;
		/********************** Calculate Scaling *************************/
		transformation = new double[6];
		data->GetGeoTransform(transformation);	
		
		int dataXSize = data->GetRasterXSize();
		int dataYSize = data->GetRasterYSize();
		
		double inputXResolution = transformation[1];
		if(inputXResolution < 0)
		{
			inputXResolution = inputXResolution * (-1);
		}
		double inputYResolution = transformation[5];
		if(inputYResolution < 0)
		{
			inputYResolution = inputYResolution * (-1);
		}
		
		double xScale = inputXResolution/outputXResolution;
		double yScale = inputYResolution/outputYResolution;
		
		int xSize = mathUtils.round(dataXSize*xScale);
		int ySize = mathUtils.round(dataYSize*yScale);;
		int bands = 1;
		
		transformation[1] = outputXResolution;
		transformation[5] = outputYResolution;
		/*******************************************************************/

		/********************** TEST output info ************************
		std::cout << "DataXSize = " << dataXSize << " DataYSize = " << dataYSize << std::endl;
		std::cout << "inputXResolution = " << inputXResolution << " inputYResolution = " 
			<< inputYResolution << std::endl;
		std::cout << "xSize = " << xSize << " ySize = " << ySize << std::endl;
		std::cout << "xScale = " << xScale << " yScale = " << yScale << std::endl;
		/******************************************************************/
		
		/*************** Prepare for outputing image ************************/
		GDALDriver *poDriver;
		char **papazMetadata;
		
		GDALAllRegister();
		
		poDriver = GetGDALDriverManager()->GetDriverByName(format);
		if(poDriver == NULL)
		{
			throw ImageOutputException("Could not find driver", error_codes::no_driver);
		}
		else
		{
			//std::cout << "OK: Got driver\n";
		}
		
		papazMetadata = poDriver->GetMetadata();
		if(CSLFetchBoolean(papazMetadata, GDAL_DCAP_CREATE, FALSE))
		{
			//std::cout << "Driver "<< format <<" supports CreateCopy() method\n";
		}
		else
		{
			throw ImageOutputException("Driver does not support create on that format", 
									   error_codes::unsupported_format);
		}
		/*******************************************************************/
		
		/************ Output Image with the New registration *******************/   
		output = poDriver->Create(filename, xSize, ySize, bands, GDT_Float32, papazMetadata);
		output->SetGeoTransform(transformation);
		output->SetProjection(data->GetProjectionRef());
		GDALRasterBand *outputRasterBand = output->GetRasterBand(1);
		
		scanline0 = (float *) CPLMalloc(sizeof(float)*dataXSize);
		scanline1 = (float *) CPLMalloc(sizeof(float)*dataXSize);
		scanline2 = (float *) CPLMalloc(sizeof(float)*dataXSize);
		
		GDALRasterBand *rasterband = data->GetRasterBand(band);
		
		//std::cout << "New Interpolated File Size: [" << ySize << "," << xSize << "]\n";
		
		//float image[ySize][xSize];
		
		newLine = (float *)CPLMalloc(sizeof(float)*xSize);
		pixels = new double[9];
		
		int column = 0;
		int row = 0;
		double xShift = 0;
		double yShift = 0;
		
		for( int i = 0; i < ySize; i++)
		{
			yShift = mathUtils.findFloatingPointComponent(((i*outputYResolution)/inputYResolution),
														  &row);
			if(row == 0)
			{
				//std::cout << "Row == 0\n";
				rasterband->RasterIO(GF_Read, 
										0, 
										row, 
										dataXSize, 
										1, 
										scanline0, 
										dataXSize, 
										1, 
										GDT_Float32, 
										0, 
										0);
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row, 
									 dataXSize, 
									 1, 
									 scanline1, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row+1, 
									 dataXSize, 
									 1, 
									 scanline2, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
			}
			else if(row == (dataYSize-1))
			{
				//std::cout << "(row == (dataYSize-1)\n";
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row-1, 
									 dataXSize, 
									 1, 
									 scanline0, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row, 
									 dataXSize, 
									 1, 
									 scanline1, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row, 
									 dataXSize, 
									 1, 
									 scanline2, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
			}
			else
			{
				//std::cout << "Row = " << row << std::endl;
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row-1, 
									 dataXSize, 
									 1, 
									 scanline0, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row, 
									 dataXSize, 
									 1, 
									 scanline1, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
				rasterband->RasterIO(GF_Read, 
									 0, 
									 row+1, 
									 dataXSize, 
									 1, 
									 scanline2, 
									 dataXSize, 
									 1, 
									 GDT_Float32, 
									 0, 
									 0);
			}
			for(int j = 0; j < xSize; j++)
			{
				xShift = mathUtils.findFloatingPointComponent(((j*outputXResolution)/inputXResolution), 
															  &column);
				if(column == 0)
				{
					//std::cout << "Column == 0 \n";
					//Column 1
					pixels[0] = scanline0[column];
					pixels[3] = scanline1[column];
					pixels[6] = scanline2[column];
					//Column 2
					pixels[1] = scanline0[column];
					pixels[4] = scanline1[column];
					pixels[7] = scanline2[column];
					//Column 1
					pixels[2] = scanline0[column+1];
					pixels[5] = scanline1[column+1];
					pixels[8] = scanline2[column+1];
				}
				else if(column == (dataXSize-1))
				{
					//std::cout << "column == (dataXSize-1)\n";
					//Column 1
					pixels[0] = scanline0[column-1];
					pixels[3] = scanline1[column-1];
					pixels[6] = scanline2[column-1];
					//Column 2
					pixels[1] = scanline0[column];
					pixels[4] = scanline1[column];
					pixels[7] = scanline2[column];
					//Column 1
					pixels[2] = scanline0[column];
					pixels[5] = scanline1[column];
					pixels[8] = scanline2[column];
				}
				else
				{
					//std::cout << "column = " << column << " row = " << row << std::endl;
					//Column 1
					pixels[0] = scanline0[column-1];
					pixels[3] = scanline1[column-1];
					pixels[6] = scanline2[column-1];
					//Column 2
					pixels[1] = scanline0[column];
					pixels[4] = scanline1[column];
					pixels[7] = scanline2[column];
					//Column 1
					pixels[2] = scanline0[column+1];
					pixels[5] = scanline1[column+1];
					pixels[8] = scanline2[column+1];
				}
				
				//std::cout << "xShift = " << xShift << " yShift = " << yShift << std::endl;
				
				//std::cout << "[" << pixels[0] << "," << pixels[1] << "," << pixels[2] << "]\n";
				//std::cout << "[" << pixels[3] << "," << pixels[4] << "," << pixels[5] << "]\n";
				//std::cout << "[" << pixels[6] << "," << pixels[7] << "," << pixels[8] << "]\n";
				
				newLine[j] = this->cubic(xShift,yShift,pixels);
				//image[i][j] = newLine[j];
				//std::cout << newLine[j] << std::endl;
			}
			outputRasterBand->RasterIO(GF_Write, 0, i, xSize, 1, newLine, xSize, 1, GDT_Float32, 0, 0);
		}
		GDALClose(output);
		
		outputtmp = (GDALDataset *) GDALOpen(filename, GA_ReadOnly);
		// Check read in correctly.
		if(outputtmp == NULL)
		{
			throw ImageNotAvailableException("Could not Open Image.", error_codes::other_image);
		}
		else
		{
		//	std::cout << "Output Image is not NULL when leaving interpolation. output x size = " 
		//	<< output->GetRasterXSize() << "\n";
		}
	}
	catch(ImageNotAvailableException e)
	{
		if( transformation != NULL )
		{
			delete transformation;
		}
		if(newLine != NULL)
		{
			delete newLine;
		}
		if( pixels != NULL )
		{
			delete pixels;
		}
		if( scanline0 != NULL )
		{
			delete scanline0;
		}
		if( scanline1 != NULL )
		{
			delete scanline1;
		}
		if( scanline2 != NULL )
		{
			delete scanline2;
		}
		throw e;
	}
	catch(ImageOutputException e)
	{
		if( transformation != NULL )
		{
			delete transformation;
		}
		if(newLine != NULL)
		{
			delete newLine;
		}
		if( pixels != NULL )
		{
			delete pixels;
		}
		if( scanline0 != NULL )
		{
			delete scanline0;
		}
		if( scanline1 != NULL )
		{
			delete scanline1;
		}
		if( scanline2 != NULL )
		{
			delete scanline2;
		}
		throw e;
	}
		
	if( transformation != NULL )
	{
		delete transformation;
	}
	if(newLine != NULL)
	{
		delete newLine;
	}
	if( pixels != NULL )
	{
		delete pixels;
	}
	if( scanline0 != NULL )
	{
		delete scanline0;
	}
	if( scanline1 != NULL )
	{
		delete scanline1;
	}
	if( scanline2 != NULL )
	{
		delete scanline2;
	}
	/************************************************************************/
	return outputtmp;
}

GDALDataset* Interpolation::copyImageBand(GDALDataset *data, 
										  const char *filename, 
										  const char *format, 
										  int band)
throw(FileOutputException, ImageOutputException)
{
	// Image Data Stores.
	float *scanline0 = NULL;
	double *transformation = NULL;
	float *newLine = NULL;
	double *pixels = NULL;
	GDALDataset *outputtmp = NULL;
	try
	{
		MathUtils mathUtils;
		GDALDataset *output;
		/********************** Calculate Scaling *************************/
		transformation = new double[6];
		data->GetGeoTransform(transformation);	
		
		int dataXSize = data->GetRasterXSize();
		int dataYSize = data->GetRasterYSize();
		
		double inputXResolution = transformation[1];
		if(inputXResolution < 0)
		{
			inputXResolution = inputXResolution * (-1);
		}
		double inputYResolution = transformation[5];
		if(inputYResolution < 0)
		{
			inputYResolution = inputYResolution * (-1);
		}
		
		
		int xSize = dataXSize;
		int ySize = dataYSize;
		int bands = 1;
		
		transformation[1] = inputXResolution;
		transformation[5] = inputYResolution;
		/*******************************************************************/
		
		/*************** Prepare for outputing image ************************/
		GDALDriver *poDriver;
		char **papazMetadata;
		
		GDALAllRegister();
		
		poDriver = GetGDALDriverManager()->GetDriverByName(format);
		if(poDriver == NULL)
		{
			throw ImageOutputException("Could not find driver", error_codes::no_driver);
		}
		else
		{
			//std::cout << "OK: Got driver\n";
		}
		
		papazMetadata = poDriver->GetMetadata();
		if(CSLFetchBoolean(papazMetadata, GDAL_DCAP_CREATE, FALSE))
		{
			//std::cout << "Driver "<< format <<" supports CreateCopy() method\n";
		}
		else
		{
			throw ImageOutputException("Driver does not support create on that format", 
									   error_codes::unsupported_format);
		}
		/*******************************************************************/
		
		/************ Output Image with the New registration *******************/   
		output = poDriver->Create(filename, xSize, ySize, bands, GDT_Float32, papazMetadata);
		output->SetGeoTransform(transformation);
		output->SetProjection(data->GetProjectionRef());
		GDALRasterBand *outputRasterBand = output->GetRasterBand(1);
		
		scanline0 = (float *) CPLMalloc(sizeof(float)*dataXSize);
		
		GDALRasterBand *rasterband = data->GetRasterBand(band);
		
		//std::cout << "New File Size: [" << ySize << "," << xSize << "]\n";
		
		newLine = (float *)CPLMalloc(sizeof(float)*xSize);
		pixels = new double[9];
		
		for( int i = 0; i < ySize; i++)
		{
			rasterband->RasterIO(GF_Read, 
								 0, 
								 i, 
								 dataXSize, 
								 1, 
								 scanline0, 
								 dataXSize, 
								 1, 
								 GDT_Float32, 
								 0, 
								 0);
			
			for(int j = 0; j < xSize; j++)
			{
				newLine[j] = scanline0[j];
			}
			outputRasterBand->RasterIO(GF_Write, 0, i, xSize, 1, newLine, xSize, 1, GDT_Float32, 0, 0);
		}
		GDALClose(output);
		
		outputtmp = (GDALDataset *) GDALOpen(filename, GA_ReadOnly);
		// Check read in correctly.
		if(outputtmp == NULL)
		{
			throw ImageNotAvailableException("Could not Open Image.", error_codes::other_image);
		}
		else
		{
			//	std::cout << "Output Image is not NULL when leaving interpolation. output x size = " 
			//	<< output->GetRasterXSize() << "\n";
		}
	}
	catch(ImageNotAvailableException e)
	{
		if( transformation != NULL )
		{
			delete transformation;
		}
		if(newLine != NULL)
		{
			delete newLine;
		}
		if( pixels != NULL )
		{
			delete pixels;
		}
		if( scanline0 != NULL )
		{
			delete scanline0;
		}
		throw e;
	}
	catch(ImageOutputException e)
	{
		if( transformation != NULL )
		{
			delete transformation;
		}
		if(newLine != NULL)
		{
			delete newLine;
		}
		if( pixels != NULL )
		{
			delete pixels;
		}
		if( scanline0 != NULL )
		{
			delete scanline0;
		}
		throw e;
	}
	
	if( transformation != NULL )
	{
		delete transformation;
	}
	if(newLine != NULL)
	{
		delete newLine;
	}
	if( pixels != NULL )
	{
		delete pixels;
	}
	if( scanline0 != NULL )
	{
		delete scanline0;
	}
	/************************************************************************/
	return outputtmp;	
}

Interpolation::~Interpolation()
{
	
}
