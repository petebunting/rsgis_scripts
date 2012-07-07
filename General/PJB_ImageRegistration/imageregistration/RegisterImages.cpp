/*
 *  RegisterImages.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 09/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "RegisterImages.h"

RegisterImages::RegisterImages()
{
}

void RegisterImages::registerImageNetwork(ImagePyramid *imagePyramid,
										  ImageNetwork *imageNetwork,
										  int distanceMeasure,
										  int searchAlgor,
										  int searchArea,
										  int bins,
										  int numWalks,
										  int tmax,
										  int tdecrease,
										  int successful,
										  int unsuccessful,
										  float measureThreshold,
										  int levelIterations,
										  double distanceThreshold,
										  float *levelScales,
										  double* networkUpdateWeights,
										  int* distanceSteps,
										  int numberOfSteps,
										  int *windowLevel,
										  int correctionStdDev,
										  double tilePercentageRangeThreshold,
										  const char *ptsOutput)
throw(ImageRegistrationException)
{
	MathUtils mathUtils;
	
	char tmpOutPath[1000];
	char numerator[5];
	int numLevels = imageNetwork->getNumberOfLevels();
	PyramidLevel *pyramidLevel = NULL;
	ImageResolutionLevel *networkLevel = NULL;
	Transform transform;
	bool change = true;
	int iterationCounter = 0;
	int startX = 0;
	int startY = 0;
	
	int numWindowSizes = 11;
	int windowSizes[11] = {0};
	int windowIncrement = 0;
	Transform windowTransformations[11];
	Transform maxCorrelationTransform;
	maxCorrelationTransform.shiftX = 0;
	maxCorrelationTransform.shiftY = 0;
	maxCorrelationTransform.measureValue = 0;
	Transform tmpTransform;
	tmpTransform.shiftX = 0;
	tmpTransform.shiftY = 0;
	tmpTransform.measureValue = 0;
	int maxCorrelationWindowSize = 0;
	int countNumTimesNodeReset = 0;
	TileCoords tile;
	double totalXShift = 0;
	double totalYShift = 0;
	double meanXShift = 0;
	double meanYShift = 0;
	int numNodes = 0;
	double prevMeanXShift = 0;
	double prevMeanYShift = 0;
	double xGradient = 10000;
	double yGradient = 10000;
	bool gradientOK = false;
	bool meanShiftOK = false;
	int startWindowSize = 0;
	//double tmpTileRange = 0;
	double sumShift[2] ={0};
	double meanShift[2] = {0};
	int j = 0;
	
	for(int i = (numLevels-1); i >= 0; i--)
	{
		pyramidLevel = imagePyramid->getLevel(i);
		networkLevel = imageNetwork->getNetworkLevel(i);
		
		// Calculate new window sizes
		windowIncrement = windowLevel[i]/10;
		startWindowSize = windowLevel[i] + (windowIncrement * ((numWindowSizes-1)/2));
		
		//std::cout << "windowlevel[i] = " << windowLevel[i] << std::endl;
		//std::cout << "startWindowSize: " << startWindowSize << std::endl;
		//std::cout << "windowIncrement: " << windowIncrement << std::endl;
		
		for(j = 0; j < numWindowSizes; j++)
		{
			windowSizes[j] = startWindowSize - (windowIncrement * j);
			//std::cout << "Window Size: " << windowSizes[j] << std::endl;
		}
		
		
		/* Calculate Large Window Size.
		windowSizes[0] = windowLevel[i]/2 + windowLevel[i];
		numWindowSizes = 1;
		tmpWindowIncrement = windowLevel[i]/10;
		for(int j = 0; j < 9; j++)
		{
			windowSizes[j+1] = windowLevel[i] - (tmpWindowIncrement * j);
			if(windowSizes[j+1] > 2)
			{
				numWindowSizes++;
			}
			else
			{
				break;
			}
		}*/
		
		xGradient = 100000;
		yGradient = 100000;
		gradientOK = false;
		meanShiftOK = false;
		iterationCounter = 0;
		change = true;
		while(change == true & iterationCounter < levelIterations & gradientOK == false & meanShiftOK == false)
		{
			std::cout << "Iterating Level " << i << " with " << networkLevel->numNodes 
					  << " nodes for the " << iterationCounter << " time\n";
			
			change = false;
			for(j = 0; j < networkLevel->numNodes; j++)
			{
				//std::cout << "Finding Transformation for Node " << j << std::endl;
				if(networkLevel->nodes[j]->percentageRange < tilePercentageRangeThreshold)
				{
					transform.shiftX = 0;
					transform.shiftY = 0;
					transform.measureValue = -1;
				}
				else
				{
					startX = networkLevel->nodes[j]->imageB->x + mathUtils.round(networkLevel->nodes[j]->transform->shiftX);
					startY = networkLevel->nodes[j]->imageB->y + mathUtils.round(networkLevel->nodes[j]->transform->shiftY);
					imagePyramid->getTileCoords4PointWindow(networkLevel->nodes[j], i, &tile);
					transform = this->findTileTransformation(pyramidLevel->imageA,
															 pyramidLevel->imageB,
															 searchArea,
															 1,
															 1,
															 &tile,
															 distanceMeasure, 
															 bins, 
															 searchAlgor,
															 numWalks,
															 tmax,
															 tdecrease,
															 successful,
															 unsuccessful,
															 measureThreshold,
															 0,
															 0,
															 false);
					//std::cout << "Found Transformation for Node " << j << std::endl
					
					if(distanceMeasure == image_measures::correlationCoefficient)
					{
						
						if(transform.measureValue < -1 | transform.measureValue > 1)
						{
							transform.measureValue = -1;
							transform.shiftX = 0;
							transform.shiftY = 0;
						}
						else if(isnan(transform.measureValue) != 0)
						{
							transform.measureValue = -1;
							transform.shiftX = 0;
							transform.shiftY = 0;
						}
						else if(transform.measureValue < measureThreshold)
						{
							//std::cout << "Insufficent Correlation for Node " << j << std::endl;
							//std::cout << "Image Measure is below threshold\n";
							countNumTimesNodeReset = 0;
							sumShift[0] = 0;
							sumShift[1] = 0;
							for(int k = 0; k < numWindowSizes; k++)
							{
								//std::cout << "Trying window size " << windowSizes[k] << std::endl;
								networkLevel->nodes[j]->windowSize = windowSizes[k];
								imagePyramid->getTileCoords4PointWindow(networkLevel->nodes[j], i, &tile);
								//tmpTileRange = mathUtils.tileRangePercentage(&tile, pyramidLevel->imageA, true, 1, -1);
								
								tmpTransform = this->findTileTransformation(pyramidLevel->imageA,
																			pyramidLevel->imageB,
																			searchArea,
																			1,
																			1,
																			&tile,
																			distanceMeasure, 
																			bins, 
																			searchAlgor,
																			numWalks,
																			tmax,
																			tdecrease,
																			successful,
																			unsuccessful,
																			measureThreshold,
																			0,
																			0,
																			false);
								windowTransformations[k] = tmpTransform;
								//std::cout << "Found transformation for window size " << windowSizes[k] << std::endl;
								
								if(tmpTransform.measureValue < -1 | tmpTransform.measureValue > 1)
								{
									//std::cout << "Measure Value = " << tmpTransform.measureValue << std::endl;
									tmpTransform.measureValue = -1;
									tmpTransform.shiftX = 0;
									tmpTransform.shiftY = 0;
								}
								else if(isnan(tmpTransform.measureValue) != 0)
								{
									//std::cout << "Measure Value is not a number. " << std::endl;
									tmpTransform.measureValue = -1;
									tmpTransform.shiftX = 0;
									tmpTransform.shiftY = 0;
								}
								
								if(tmpTransform.measureValue < 0)
								{
									countNumTimesNodeReset++;
								}
								
								/*std::cout << k << ") Trying window size " << networkLevel->nodes[j]->windowSize 
										  << " transformation [" << tmpTransform.shiftX << ", " << tmpTransform.shiftY 
										  << "] with correlation = " << tmpTransform.measureValue << " and tile Range "
										  << tmpTileRange << " was returned\n";*/
								
								sumShift[0] += tmpTransform.shiftX;
								sumShift[1] += tmpTransform.shiftY;
								
								if(k == 0)
								{
									maxCorrelationTransform = tmpTransform;
									maxCorrelationWindowSize = windowSizes[k];
								}
								else if(tmpTransform.measureValue >= maxCorrelationTransform.measureValue)
								{
									//std::cout << "Updating max Correlation\n";
									maxCorrelationTransform = tmpTransform;
									maxCorrelationWindowSize = windowSizes[k];
								}
							}
							
							meanShift[0] = sumShift[0]/numWindowSizes;
							meanShift[1] = sumShift[1]/numWindowSizes;
							
							double diffX = 0;
							double diffY = 0;
							double diffXSqu = 0;
							double diffYSqu = 0;
							double sumXDev = 0;
							double sumYDev = 0;
							
							for(int k = 0; k < numWindowSizes; k++)
							{
								diffX = windowTransformations[k].shiftX - meanShift[0];
								diffY = windowTransformations[k].shiftY - meanShift[1];
								diffXSqu = diffX * diffX;
								diffYSqu = diffY * diffY;
								sumXDev += diffXSqu;
								sumYDev += diffYSqu;
							}
							
							double stddevX = sqrt(sumXDev/numWindowSizes);
							double stddevY = sqrt(sumYDev/numWindowSizes);
							double xRange[2] = {0};
							double yRange[2] = {0};
							
							xRange[0] = meanShift[0] - stddevX;
							xRange[1] = meanShift[0] + stddevX;
							
							yRange[0] = meanShift[1] - stddevY;
							yRange[1] = meanShift[1] + stddevY;
							/*
							std::cout << "\n Mean Shift: [" << meanShift[0] << ", " << meanShift[1] << "]\n";
							std::cout << "Standard Deviation: [" << stddevX << "," << stddevY << "]\n";
							
							std::cout << "X Axis range within 1 deviation: [" << xRange[0]
									  << "," << xRange[1] << "]\n";
							std::cout << "Y Axis range within 1 deviation: [" << yRange[0] 
								<< "," << yRange[1] << "]\n";
							*/
							int meanCounterX = 0;
							int meanCounterY = 0;
							double meanSumX = 0;
							double meanSumY = 0;
							
							
							for(int k = 0; k < numWindowSizes; k++)
							{
								if(windowTransformations[k].shiftX > xRange[0] &
								   windowTransformations[k].shiftX < xRange[1])
								{
									meanSumX += windowTransformations[k].shiftX;
									meanCounterX++;
								}
								
								if(windowTransformations[k].shiftY > yRange[0] &
								   windowTransformations[k].shiftY < yRange[1])
								{
									meanSumY += windowTransformations[k].shiftY;
									meanCounterY++;
								}
							}
							
							double newMeanX = 0;
							double newMeanY = 0;
							if(meanCounterX == 0)
							{
								newMeanX = meanShift[0];
							}
							else
							{
								newMeanX = meanSumX/meanCounterX;
							}
							
							if(meanCounterY == 0)
							{
								newMeanY = meanShift[1];
							}
							else
							{
								newMeanY = meanSumY/meanCounterY;
							}
							
							
							//std::cout << "Transformation: [" << newMeanX << "," << newMeanY << "]\n";
							
							//std::cout << "Tried other window sizes for node " << j << std::endl;
							//transform = maxCorrelationTransform;
							transform.shiftX = newMeanX;
							transform.shiftY = newMeanY;
							transform.measureValue = 2;
							networkLevel->nodes[j]->windowSize = windowLevel[i];
							
							//std::cout << "Final window size = " << maxCorrelationWindowSize << " with transformation [" 
							//	<< transform.shiftX << ", " << transform.shiftY << "] and measure = " << transform.measureValue << std::endl;							
							//	}
						}
					}
				}
				//std::cout << "Applying Update to Node " << j << std::endl;
				//std::cout << std::endl;
				imageNetwork->updateNode(networkLevel->nodes[j], 
										 i, 
										 &transform, 
										 distanceThreshold, 
										 levelScales, 
										 networkUpdateWeights,
										 distanceSteps,
										 numberOfSteps);
				//std::cout << std::endl;
				if(transform.measureValue > measureThreshold | 
				   distanceMeasure != image_measures::correlationCoefficient)
				{
					totalXShift += transform.shiftX;
					totalYShift += transform.shiftY;
					numNodes++;
				}
				//std::cout << "Applied Update to Node " << j << std::endl;

				if(!(transform.shiftX > -0.0000000001 
					 & transform.shiftX < -0.0000000001 
					 & transform.shiftY > -0.0000000001 
					 & transform.shiftY < -0.0000000001))
				{
					change = true;
				}
			}
			
			strcpy(tmpOutPath, ptsOutput);
			strcat(tmpOutPath, "_nodesLevel0_");
			sprintf(numerator, "%d", i);
			strcat(tmpOutPath, numerator);
			sprintf(numerator, "%d", iterationCounter);
			strcat(tmpOutPath, numerator);
			strcat(tmpOutPath, ".txt");
			
			imageNetwork->exportNetworkAsText(0,tmpOutPath);
			
			prevMeanXShift = meanXShift;
			prevMeanXShift = meanYShift;
			
			meanXShift = totalXShift / numNodes;
			meanYShift = totalYShift / numNodes;
				
			if(iterationCounter > 0)
			{
				xGradient = mathUtils.absoluteValue(prevMeanXShift - meanXShift);
				yGradient = mathUtils.absoluteValue(prevMeanYShift - meanYShift);
				if(xGradient < 0.3 & yGradient < 0.3)
				{
					gradientOK = true;
				}
			}
			
			if(meanXShift < 0.2 & meanXShift > -0.2 & meanYShift < 0.2 & meanYShift > -0.2)
			{
				meanShiftOK = true;
			}
			
			std::cout << "Mean X Shift = " << meanXShift << " (" << totalXShift << ") on level " << i << " iteration " 
					  << iterationCounter << std::endl;
			std::cout << "Mean Y Shift = " << meanYShift << " (" << totalYShift << ") on level " << i << " iteration " 
				<< iterationCounter << std::endl;
			
			
			totalXShift = 0;
			totalYShift = 0;
			numNodes = 0;
			iterationCounter++;
			if(change == true & iterationCounter < levelIterations & gradientOK == false & meanShiftOK == false)
			{
				//std::cout << "Running smoothing on movements on level " << i << std::endl;
				imageNetwork->checkNodeNeighboringMovements(i);
				//std::cout << "Ran smoothing on movements on level " << i << std::endl;
			}
		}
		
		
		
		imageNetwork->exportNetworkAsText(0, tmpOutPath);
		
		std::cout << "\n\nLevel " << i << " required " << iterationCounter << " iterations resulting in a mean shift ["
				  << meanXShift << ", " << meanYShift << "] and change gradients [" << xGradient << ", " << yGradient << "]\n\n"; 
		
		//std::cout << "Checking movements on level " << i << std::endl;
		imageNetwork->checkNodeMovementsAtLevel(i,
												correctionStdDev,
												distanceThreshold, 
												levelScales, 
												networkUpdateWeights,
												distanceSteps,
												numberOfSteps);
		//std::cout << "Checked movements on level " << i << std::endl;
		
		/*strcpy(tmpFilePath, outputPath);
		strcat(tmpFilePath, "_nodesOnLevel0_afterprocessing");
		sprintf(numerator, "%d", i);
		strcat(tmpFilePath, numerator);
		strcat(tmpFilePath, ".txt");
		imageNetwork->exportNodeTransformationsAtlevel(0, tmpFilePath);
		strcpy(tmpFilePath, outputPath);
		strcat(tmpFilePath, "_nodesOnLevel1_afterprocessing");
		sprintf(numerator, "%d", i);
		strcat(tmpFilePath, numerator);
		strcat(tmpFilePath, ".txt");
		imageNetwork->exportNodeTransformationsAtlevel(1, tmpFilePath);
		strcpy(tmpFilePath, outputPath);
		strcat(tmpFilePath, "_nodesOnLevel2_afterprocessing");
		sprintf(numerator, "%d", i);
		strcat(tmpFilePath, numerator);
		strcat(tmpFilePath, ".txt");
		imageNetwork->exportNodeTransformationsAtlevel(2, tmpFilePath);*/
		//std::cout << "Completed Export on level " << i << std::endl << std::endl;
	}
}

void RegisterImages::registerImagesSearchBuffer(GDALDataset *ref, 
												GDALDataset *floating, 
												int pixelBuffer, 
												const char *outfilename,
												int bins, 
												int refBand, 
												int floatBand)
throw(ImageRegistrationException, ImageOutputException)
{
	int xShift = 0;
	int yShift = 0;
	int bufferSize = 0;
	double **bufferMIvalues = NULL;
	try
	{
		bufferSize = (pixelBuffer*2) + 1;
		*bufferMIvalues = new double[bufferSize];
		int xShiftInput = 0;
		int yShiftInput = pixelBuffer;
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			bufferMIvalues[i] = new double[bufferSize];
			xShiftInput = (pixelBuffer * (-1));
			
			for(int j = 0; j<bufferSize; j++)
			{
				//std::cout << "\n\ni: " << i << " j: " << j << std::endl;
				//std::cout << std::endl;
				bufferMIvalues[i][j] = calcMIImagesPixelShift(ref, 
															  floating, 
															  xShiftInput, 
															  yShiftInput, 
															  bins, 
															  refBand, 
															  floatBand);
				//std::cout << "shiftXInput: " << xShiftInput << " shiftYInput: " 
				//		  << yShiftInput << " MI = " << bufferMIvalues[i][j] << std::endl;
				xShiftInput++;
			}
			yShiftInput--;
		}
		/**********************************************************************************/
		
		/*********** TEST: Print out MI Buffer *************************/
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			for(int j=0; j < bufferSize; j++)
			{
				std::cout << bufferMIvalues[i][j] << ", ";
			}
			std::cout << std::endl;
		}
		/***************************************************************/
		
		/******************** Find MAX MI in Buffer ************************/
		double max = 0;
		
		xShiftInput = 0;
		yShiftInput = pixelBuffer;
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			xShiftInput = pixelBuffer * (-1);
			for(int j = 0; j<bufferSize; j++)
			{
				if(i == (bufferSize-1) & j == 0)
				{
					max = bufferMIvalues[i][j];
					xShift = xShiftInput;
					yShift = yShiftInput;
				}
				else if( bufferMIvalues[i][j] > max)
				{
					max = bufferMIvalues[i][j];
					xShift = xShiftInput;
					yShift = yShiftInput;
				}
				else
				{
					// DO NOTHING
				}
				xShiftInput++;
			}
			yShiftInput--;
		}
		/****************************************************************/
		
		/*************** Print MI value and transformation ***************/
		std::cout << "Max MI = " 
			<< max 
			<< " Meaning a shift in pixels of x: "
			<< xShift 
			<< " and y: " 
			<< yShift 
			<< std::endl;
		/****************************************************************/
		
		/************** Edit Geocoding in floating Image ********************/
		this->saveImageWithNewGeoReference(floating, xShift, yShift, outfilename, "GTiff");
		/*******************************************************************/
	}
	catch(ImageOutputException e)
	{
		if(bufferMIvalues != NULL)
		{
			for(int i = 0; i < bufferSize; i++)
			{
				if(bufferMIvalues[i] != NULL)
				{
					delete [] bufferMIvalues[i];
				}
			}
			delete bufferMIvalues;
		}
		throw e;
	}
	catch(ImageRegistrationException e)
	{
		if(bufferMIvalues != NULL)
		{
			for(int i = 0; i < bufferSize; i++)
			{
				if(bufferMIvalues[i] != NULL)
				{
					delete [] bufferMIvalues[i];
				}
			}
			delete bufferMIvalues;
		}
		throw e;
	}
	if(bufferMIvalues != NULL)
	{
		for(int i = 0; i < bufferSize; i++)
		{
			if(bufferMIvalues[i] != NULL)
			{
				delete [] bufferMIvalues[i];
			}
		}
		delete bufferMIvalues;
	}
}

double RegisterImages::calcMIImagesPixelShift(GDALDataset *ref, 
											  GDALDataset *floating, 
											  int xShift, 
											  int yShift, 
											  int bins, 
											  int refBand, 
											  int floatBand)
	throw(ImageRegistrationException)
{
	//std::cout << "RegisterImages::calcMIImagesPixelShift Has not yet been implemented!!!\n"; 
	double mi_value = 0;
	ImageOverlap *imageOverlap = NULL;
	JointHistogram *jointHistogram = NULL;
	MutualInformation *mi = NULL;
		
	try
	{
		/******** Calculate Image Overlap - Including possible shift ***********/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithShift(ref, floating, xShift, yShift);
		/***********************************************************************/

		/******************* Generate Joint Histogram ***************************/
		jointHistogram = new JointHistogram(bins);
		jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		/************************************************************************/
		
		/************************** Calculate MI *******************************/
		mi = new MutualInformation;
		mi_value = mi->calcMutualInformation(*jointHistogram);
		/************************************************************************/
		//std::cout << "mi: " << mi_value << std::endl;
	}
	catch(ImageRegistrationException e)
	{
		if( mi != NULL)
		{
			delete mi;
		}
		if(imageOverlap != NULL)
		{
			delete imageOverlap;
		}
		if(jointHistogram != NULL)
		{
			delete jointHistogram;
		}
		throw e;
	}
	
	// Free Memory
	if( mi != NULL)
	{
		delete mi;
	}
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( jointHistogram != NULL )
	{
		delete jointHistogram;
	}
	
	return mi_value;
}

void RegisterImages::saveImageWithNewGeoReference(GDALDataset *data,
												  int xShift, 
												  int yShift, 
												  const char *filename, 
												  const char *format)
	throw(ImageOutputException)
{
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
	if(CSLFetchBoolean(papazMetadata, GDAL_DCAP_CREATECOPY, FALSE))
	{
		//std::cout << "Driver "<< format <<" supports CreateCopy() method\n";
	}
	else
	{
		throw ImageOutputException("Driver does not support create on that format", 
								   error_codes::unsupported_format);
	}
	/*******************************************************************/
	
	/*************** Get current Transformation ************************/
	double *transformation;
	transformation = new double[6];
	data->GetGeoTransform(transformation);	
	/*******************************************************************/
	
	/***************** TEST: Print out current transformation ************/
	std::cout << "Transformation[0]: " << transformation[0] << std::endl;
	std::cout << "Transformation[1]: " << transformation[1] << std::endl;
	std::cout << "Transformation[2]: " << transformation[2] << std::endl;
	std::cout << "Transformation[3]: " << transformation[3] << std::endl;
	std::cout << "Transformation[4]: " << transformation[4] << std::endl;
	std::cout << "Transformation[5]: " << transformation[5] << std::endl;
	/********************************************************************/
	
	/************* Apply New transformation ****************************/
	double xPixel = transformation[1];
	double yPixel = transformation[5];
	
	if(xPixel < 0)
	{
		xPixel = xPixel*(-1);
	}
	if(yPixel < 0)
	{
		yPixel = yPixel*(-1);
	}
	transformation[1] = xPixel;
	transformation[5] = yPixel;
	
	
	double xShiftInMetres = (double)xShift * xPixel;
	double yShiftInMetres = (double)yShift * yPixel;
	
	transformation[0] += xShiftInMetres;
	transformation[3] += yShiftInMetres;
	
	/*********************************************************************/
	
	/***************** TEST: Print out current transformation ************/
	std::cout << "Transformation[0]: " << transformation[0] << std::endl;
	std::cout << "Transformation[1]: " << transformation[1] << std::endl;
	std::cout << "Transformation[2]: " << transformation[2] << std::endl;
	std::cout << "Transformation[3]: " << transformation[3] << std::endl;
	std::cout << "Transformation[4]: " << transformation[4] << std::endl;
	std::cout << "Transformation[5]: " << transformation[5] << std::endl;
	/********************************************************************/
	
	/************ Output Image with the New registration *******************/
	GDALDataset *outDataset;    
	
	outDataset = poDriver->CreateCopy(filename, data, FALSE, NULL, NULL, NULL);
	
	outDataset->SetGeoTransform(transformation);
	
	if(outDataset != NULL)
	{
		delete outDataset;
	}
	if( transformation != NULL )
	{
		delete transformation;
	}
	/************************************************************************/
}

void RegisterImages::findNonLinearTransformation(GDALDataset *ref, 
												 GDALDataset *floating,
												 int pixelBuffer, 
												 int bins, 
												 int refBand, 
												 int floatBand)
throw(ImageRegistrationException)
{
	ImageOverlap *imageOverlap = NULL;
	TileCoords *tiles = NULL;
	try
	{
		/************** Find Overlapping areas **********************/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithShift(ref, floating, 0, 0);
		int *refImagePixels;
		int *floatImagePixels;
		double *geoCorners;
		refImagePixels = imageOverlap->getImageAPixelCoords();
		floatImagePixels = imageOverlap->getImageBPixelCoords();
		geoCorners = imageOverlap->getOverlapGeoCoords();
	
		TileCoords imageCoords;
		imageCoords.imgATLX = refImagePixels[0];
		imageCoords.imgATLY = refImagePixels[1];
		imageCoords.imgABRX = refImagePixels[2];
		imageCoords.imgABRY = refImagePixels[3];
		imageCoords.imgBTLX = floatImagePixels[0];
		imageCoords.imgBTLY = floatImagePixels[1];
		imageCoords.imgBBRX = floatImagePixels[2];
		imageCoords.imgBBRY = floatImagePixels[3];
		imageCoords.eastingTL = geoCorners[0];
		imageCoords.northingTL = geoCorners[1];
		imageCoords.eastingBR = geoCorners[2];
		imageCoords.northingBR = geoCorners[3];
		/*************************************************************/
	
		/****************** TEST: Print out **************************
			imageOverlap->printOverlappingArea();
		*************************************************************/
	
		/****************** Calculate 9 tiles ************************/
		tiles = new TileCoords[9];
		imageOverlap->findtiles(&imageCoords, tiles);
		/*************************************************************/
	
		/******************* TEST: Print tile details ****************
			for(int i= 0; i < 9; i++)
		{
				std::cout << "\n Tile " << i << ":\n";
				std::cout << " Image A:\n";
				std::cout << "[" 
					<< tiles[i].imgATLX 
					<< ", " 
					<< tiles[i].imgATLY 
					<< "] [" 
					<< tiles[i].imgABRX 
					<< ", " 
					<< tiles[i].imgABRY 
					<< "]\n";
				std::cout << " Image B:\n";
				std::cout << "[" 
					<< tiles[i].imgBTLX 
					<< ", " 
					<< tiles[i].imgBTLY
					<< "] [" 
					<< tiles[i].imgBBRX 
					<< ", " 
					<< tiles[i].imgBBRY 
					<< "]\n";
				std::cout << " Geo Coords:\n";
				std::cout << "["
					<< tiles[i].eastingTL 
					<< ", " 
					<< tiles[i].northingTL 
					<< "] [" 
					<< tiles[i].eastingBR 
					<< ", " 
					<< tiles[i].northingBR 
					<< "]\n";
		}
		/*************************************************************/
	
		/****** Calculate linear transformation for each tile ********/
		Transform transformMatrix[9];
		for( int i = 0; i < 9; i++)
		{
			transformMatrix[i] = this->registerTileSearchBuffer(ref, 
																floating, 
																pixelBuffer, 
																bins, 
																refBand, 
																floatBand, 
																&tiles[i]);
		}
		/*************************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( tiles != NULL )
		{
			delete tiles;
		}
		throw e;
	}
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( tiles != NULL )
	{
		delete tiles;
	}
}

void RegisterImages::constructNonusImageTree(GDALDataset *ref, 
											 GDALDataset *floating,
											 int pixelBuffer, 
											 int bins, 
											 int refBand, 
											 int floatBand,
											 int minTileSize)
throw(ImageRegistrationException)
{	
	NonusImageTree *imageTree = NULL;
	ImageOverlap *imageOverlap = NULL;
	TileCoords *tiles = NULL;
	Queue *queue = NULL;
	
	try
	{
		/****************** Initilize Image Tree *********************/
		imageTree = new NonusImageTree;
		/*************************************************************/
		
		/************** Find Overlapping areas **********************/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithShift(ref, floating, 0, 0);
		int *refImagePixels;
		int *floatImagePixels;
		double *geoCorners;
		refImagePixels = imageOverlap->getImageAPixelCoords();
		floatImagePixels = imageOverlap->getImageBPixelCoords();
		geoCorners = imageOverlap->getOverlapGeoCoords();
	
		TileCoords imageCoords;
		imageCoords.imgATLX = refImagePixels[0];
		imageCoords.imgATLY = refImagePixels[1];
		imageCoords.imgABRX = refImagePixels[2];
		imageCoords.imgABRY = refImagePixels[3];
		imageCoords.imgBTLX = floatImagePixels[0];
		imageCoords.imgBTLY = floatImagePixels[1];
		imageCoords.imgBBRX = floatImagePixels[2];
		imageCoords.imgBBRY = floatImagePixels[3];
		imageCoords.eastingTL = geoCorners[0];
		imageCoords.northingTL = geoCorners[1];
		imageCoords.eastingBR = geoCorners[2];
		imageCoords.northingBR = geoCorners[3];
		/*************************************************************/
	
		/******** Perform Linear Registration of Images *************/
		Transform transform = registerTileSearchBuffer(ref, 
													   floating, 
													   pixelBuffer, 
													   bins, 
													   refBand, 
													   floatBand, 
													   &imageCoords);
		/*******************************************************************/
	
		/****************** Create Nonus Image Tree Root **************/
		TileCoords *tileCoords = imageTree->setRoot(transform, imageCoords, 0, 0);
		/************************************************************/
	
		/****************** Calculate 9 tiles ************************/
		tiles = new TileCoords[9]; 
		imageOverlap->findtiles(tileCoords, tiles);
		/*************************************************************/
	
		/****************** Create NonusImageTree *********************/
	
		//////// Create and Initialize Queue with Image tiles ////////////
		queue = new Queue;
		for(int i = 0; i < 9; i++)
		{
			queue->add(imageTree->addNode(&tiles[i], 0, 0));
		}
		/////////////////////////////////////////////////////////////////
	
		////////////// Initialize ////////////////////////////
		NonusTreeNode *currentNode;
		//////////////////////////////////////////////////////
	
		////////////////// Fill Nonus Tree //////////////////
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			/*------------------- Find transformation ----------------- */
			transform = registerTileSearchBuffer(ref, 
												 floating, 
												 pixelBuffer, 
												 bins, 
												 refBand, 
												 floatBand, 
												 currentNode->tileCoords);
			/*------------------------------------------------------------ */
		
			/*------------------- set transformation ----------------- */
			currentNode->TileTransformation->shiftX = transform.shiftX;
			currentNode->TileTransformation->shiftY = transform.shiftY;
			/*------------------------------------------------------------ */
		
			/*---------- Get Next level of tile and add to Queue -------------- */
			if((currentNode->tileCoords->imgABRX - currentNode->tileCoords->imgATLX) 
			   < (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else if((currentNode->tileCoords->imgABRY - currentNode->tileCoords->imgATLY) 
					< (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else
			{
				imageOverlap->findtiles(currentNode->tileCoords, tiles);
				for(int i = 0; i < 9; i++)
				{
					queue->add(imageTree->addNode(&tiles[i], 0, 0));
				}
			}
			/*----------------------------------------------------------------- */
		}
		/////////////////////////////////////////////////////////////////
		/*************************************************************/
	
		/********** Print NonusImageTree *************************/
		imageTree->printTree();
		/*********************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( tiles != NULL )
		{
			delete [] tiles;
		}
		if( queue != NULL )
		{
			delete queue;
		}
		if(imageTree != NULL )
		{
			delete imageTree; // NOT YET IMPLEMENTED :-s
		}
		throw e;
	}
		
	/************** Free Memory ************************/
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( tiles != NULL )
	{
		delete [] tiles;
	}
	if( queue != NULL )
	{
		delete queue;
	}
	if(imageTree != NULL )
	{
		delete imageTree; // NOT YET IMPLEMENTED :-s
	}
	/**************************************************/
	
}

Transform RegisterImages::registerTileSearchBuffer(GDALDataset *ref, 
												   GDALDataset *floating, 
												   int pixelBuffer, 
												   int bins, 
												   int refBand, 
												   int floatBand,
												   TileCoords *tile)
throw(ImageRegistrationException)
{
	int xShift = 0;
	int yShift = 0;
	double **bufferMIvalues = NULL;
	int bufferSize = 0;
	try
	{
		/********************* Calculate MI values for the Buffer ************************/
		bufferSize = ((pixelBuffer*2)+1);
		*bufferMIvalues = new double[bufferSize];
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			bufferMIvalues[i] = new double[bufferSize];
			for(int j = 0; j<bufferSize; j++)
			{
				bufferMIvalues[i][j] = calcMIImagesTilePixelShift(ref, 
																  floating, 
																  ((pixelBuffer*(-1))+j), 
																  ((pixelBuffer*(-1))+i), 
																  bins, 
																  refBand, 
																  floatBand, 
																  tile);
			}
		}
		/**********************************************************************************/
	
		/*********** TEST: Print out MI Buffer *************************/
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			for(int j=0; j < bufferSize; j++)
			{
				std::cout << bufferMIvalues[i][j] << ", ";
			}
			std::cout << std::endl;
		}
		/***************************************************************/
	
		/******************** Find MAX MI in Buffer ************************/
		double max = 0;
	
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			for(int j=0; j <bufferSize; j++)
			{
				if(i == (bufferSize-1) & j == 0)
				{
					max = bufferMIvalues[i][j];
					xShift = ((pixelBuffer*(-1))+j);
					yShift = ((pixelBuffer*(-1))+i);
				}
				else if( bufferMIvalues[i][j] > max)
				{
					max = bufferMIvalues[i][j];
					xShift = ((pixelBuffer*(-1))+j);
					yShift = ((pixelBuffer*(-1))+i);
				}
				else
				{
					// DO NOTHING
				}
			}
		}
		/****************************************************************/
	
		/*************** Print MI value and transformation ***************/
		std::cout << "Max MI = " 
			<< max 
			<< " Meaning a shift in pixels of x: "
			<< xShift 
			<< " and y: " 
			<< yShift 
			<< std::endl;
	/****************************************************************/
	}
	catch(ImageRegistrationException e)
	{
		throw e;
	}
	/************** Create Transform Struct and return *************/
	Transform transform;
	transform.shiftX = xShift;
	transform.shiftY = yShift;
	return transform;
	/****************************************************************/
}

double RegisterImages::calcMIImagesTilePixelShift(GDALDataset *ref, 
												  GDALDataset *floating, 
												  int xShift, 
												  int yShift, 
												  int bins, 
												  int refBand, 
												  int floatBand,
												  TileCoords *tile)
throw(ImageRegistrationException)
{
	double mi_value = 0;
	ImageOverlap *imageOverlap = NULL;
	JointHistogram *jointHistogram = NULL;
	MutualInformation *mi = NULL;
	
	try
	{
		/*************** TEST: Print out tile details **********************
		std::cout << "\nxShift: " << xShift << " yShift: " << yShift << " \n";
		std::cout << " Image A: ";
		std::cout << "[" << tile->imgATLX << ", " << tile->imgATLY << "] [" 
				<< tile->imgABRX << ", " << tile->imgABRY << "]\n";
		std::cout << " Image B: ";
		std::cout << "[" << tile->imgBTLX << ", " << tile->imgBTLY << "] [" 
				<< tile->imgBBRX << ", " << tile->imgBBRY << "]\n";
		std::cout << " Geo Coords: ";
		std::cout << "[" << tile->eastingTL << ", " << tile->northingTL << "] [" 
				<< tile->eastingBR << ", " << tile->northingBR << "]\n";
		/***************************************************************************/
	
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, floating, xShift, yShift, tile);
		/***************************************************************************/
	
		/******************* Generate Joint Histogram ***************************/
		jointHistogram = new JointHistogram(bins);
		jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		/************************************************************************/
	
		/************************** Calculate MI *******************************/
		mi = new MutualInformation;
		mi_value = mi->calcMutualInformation(*jointHistogram);
		/************************************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( mi != NULL)
		{
			delete mi;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		throw e;
	}
	
	/*********************** Free Memory ************************************/
	if( mi != NULL)
	{
		delete mi;
	}
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( jointHistogram != NULL )
	{
		delete jointHistogram;
	}
	/************************************************************************/
	return mi_value;
}

void RegisterImages::constructSubPixelNonusImageTree(GDALDataset *ref, 
													 GDALDataset *floating,
													 const char *ctrlptsOutputFile,
													 int pixelBuffer, 
													 int bins, 
													 int refBand, 
													 int floatBand,
													 int minTileSize,
													 double tileMovement,
													 int measure)
throw(ImageRegistrationException)
{
	NonusImageTree *imageTree = NULL;
	ImageOverlap *imageOverlap = NULL;
	TileCoords *tiles = NULL;
	Queue *queue = NULL;
	//std::cout << "Starting to construt subPixel nonus image tree" << std::endl;
	try
	{
		/***************** Init the NonusImageTree *****************/
		imageTree = new NonusImageTree;
		/***********************************************************/
		
		/************** Find Overlapping areas **********************/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithShift(ref, floating, 0, 0);
		int *refImagePixels;
		int *floatImagePixels;
		double *geoCorners;
		refImagePixels = imageOverlap->getImageAPixelCoords();
		floatImagePixels = imageOverlap->getImageBPixelCoords();
		geoCorners = imageOverlap->getOverlapGeoCoords();
		
		TileCoords imageCoords;
		imageCoords.imgATLX = refImagePixels[0];
		imageCoords.imgATLY = refImagePixels[1];
		imageCoords.imgABRX = refImagePixels[2];
		imageCoords.imgABRY = refImagePixels[3];
		imageCoords.imgBTLX = floatImagePixels[0];
		imageCoords.imgBTLY = floatImagePixels[1];
		imageCoords.imgBBRX = floatImagePixels[2];
		imageCoords.imgBBRY = floatImagePixels[3];
		imageCoords.eastingTL = geoCorners[0];
		imageCoords.northingTL = geoCorners[1];
		imageCoords.eastingBR = geoCorners[2];
		imageCoords.northingBR = geoCorners[3];
		/*************************************************************/
		
		/****** Perform Linear Subpixel Registration on the Images *********/
		Transform transform = registerTileSubPixelSearchBuffer(ref, 
															   floating, 
															   pixelBuffer, 
															   bins, 
															   refBand, 
															   floatBand, 
															   &imageCoords,
															   tileMovement,
															   measure);
		/*******************************************************************/
		
		/****************** Create Nonus Image Tree Root **************/
		TileCoords *tileCoords = imageTree->setRoot(transform, imageCoords, 0, 0);
		/************************************************************/
		
		
		
		/****************** Calculate 9 tiles ************************/
		tiles = new TileCoords[9]; 
		imageOverlap->findtiles(tileCoords, tiles);
		/*************************************************************/
		
		/****************** Create NonusImageTree *********************/
		
		//////// Create and Initialize Queue with Image tiles ////////////
		queue = new Queue;
		for(int i = 0; i < 9; i++)
		{
			queue->add(imageTree->addNode(&tiles[i], 0, 0));
		}
		/////////////////////////////////////////////////////////////////
		
		////////////// Initialize ////////////////////////////
		NonusTreeNode *currentNode;
		//////////////////////////////////////////////////////
		
		////////////////// Fill Nonus Tree //////////////////
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			/*------------------- Find transformation ----------------- */
			transform = registerTileSubPixelSearchBuffer(ref, 
														 floating, 
														 pixelBuffer, 
														 bins, 
														 refBand, 
														 floatBand, 
														 currentNode->tileCoords,
														 tileMovement,
														 measure);
			/*------------------------------------------------------------ */
			
			/*------------------- set transformation ----------------- */
			currentNode->TileTransformation->shiftX = transform.shiftX;
			currentNode->TileTransformation->shiftY = transform.shiftY;
			/*------------------------------------------------------------ */
			
			/*---------- Get Next level of tile and add to Queue -------------- */
			if((currentNode->tileCoords->imgABRX - currentNode->tileCoords->imgATLX) 
			   < (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else if((currentNode->tileCoords->imgABRY - currentNode->tileCoords->imgATLY) 
					< (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else
			{
				imageOverlap->findtiles(currentNode->tileCoords, tiles);
				for(int i = 0; i < 9; i++)
				{
					queue->add(imageTree->addNode(&tiles[i], 0, 0));
				}
			}
			/*----------------------------------------------------------------- */
		}
		/////////////////////////////////////////////////////////////////
		/*************************************************************/
		
		/********** Print NonusImageTree *************************/
		imageTree->printTree();
		/*********************************************************/
		
		/********* Output Control Points for ENVI ***************/
		imageTree->write2EnviGcpsFile(ctrlptsOutputFile, -1);
		/*******************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( tiles != NULL )
		{
			delete [] tiles;
		}
		if( queue != NULL )
		{
			delete queue;
		}
		if(imageTree != NULL )
		{
			delete imageTree; // NOT YET IMPLEMENTED :-s
		}
		throw e;
	}
	
	/************** Free Memory ************************/
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( tiles != NULL )
	{
		delete [] tiles;
	}
	if( queue != NULL )
	{
		delete queue;
	}
	if(imageTree != NULL )
	{
		delete imageTree; // NOT YET IMPLEMENTED :-s
	}
	/**************************************************/
}

void RegisterImages::constructPixel_EstimateSubPixelNonusImageTree(GDALDataset *ref, 
																   GDALDataset *floating,
																   const char *ctrlptsOutputFile,
																   int pixelBuffer, 
																   int bins, 
																   int refBand, 
																   int floatBand,
																   int minTileSize,
																   int measure)
throw(ImageRegistrationException)	
{
	MathUtils mathUtils;
	NonusImageTree *imageTree = NULL;
	ImageOverlap *imageOverlap = NULL;
	TileCoords *tiles = NULL;
	Queue *queue = NULL;
	double stddevref = 0;
	double stddevfloat = 0;
	try
	{
		/***************** Init the NonusImageTree *****************/
		imageTree = new NonusImageTree;
		/***********************************************************/
		
		/************** Find Overlapping areas **********************/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithShift(ref, floating, 0, 0);
		int *refImagePixels;
		int *floatImagePixels;
		double *geoCorners;
		refImagePixels = imageOverlap->getImageAPixelCoords();
		floatImagePixels = imageOverlap->getImageBPixelCoords();
		geoCorners = imageOverlap->getOverlapGeoCoords();
		
		TileCoords imageCoords;
		imageCoords.imgATLX = refImagePixels[0];
		imageCoords.imgATLY = refImagePixels[1];
		imageCoords.imgABRX = refImagePixels[2];
		imageCoords.imgABRY = refImagePixels[3];
		imageCoords.imgBTLX = floatImagePixels[0];
		imageCoords.imgBTLY = floatImagePixels[1];
		imageCoords.imgBBRX = floatImagePixels[2];
		imageCoords.imgBBRY = floatImagePixels[3];
		imageCoords.eastingTL = geoCorners[0];
		imageCoords.northingTL = geoCorners[1];
		imageCoords.eastingBR = geoCorners[2];
		imageCoords.northingBR = geoCorners[3];
		/*************************************************************/
		
		/****** Perform Linear Subpixel Registration on the Images *********/
		Transform transform = registerTilePixel_EstimateSubPixelSearchBuffer(ref, 
																			 floating, 
																			 pixelBuffer, 
																			 bins, 
																			 refBand, 
																			 floatBand, 
																			 &imageCoords,
																			 1,
																			 measure);
		/*******************************************************************/
		
		/*************** Print transformation ***************/
		std::cout << "ROOT - Transform of x: "
			<< transform.shiftX 
			<< " and y: " 
			<< transform.shiftY 
			<< std::endl;
		/***************************************************************/
			
		/****************** Create Nonus Image Tree Root **************/
		TileCoords *tileCoords = imageTree->setRoot(transform, imageCoords, 1, 1);
		/************************************************************/
		
		/****************** Calculate 9 tiles ************************/
		tiles = new TileCoords[9]; 
		imageOverlap->findtiles(tileCoords, tiles, transform);
		/*************************************************************/
		
		/****************** Create NonusImageTree *********************/
		
		//////// Create and Initialize Queue with Image tiles ////////////
		queue = new Queue;
		for(int i = 0; i < 9; i++)
		{
			queue->add(imageTree->addNode(&tiles[i], 0.5, 0.5));
		}
		/////////////////////////////////////////////////////////////////
		
		////////////// Initialize ////////////////////////////
		NonusTreeNode *currentNode;
		//////////////////////////////////////////////////////
		
		////////////////// Fill Nonus Tree //////////////////
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			
			if(currentNode->stddevtilefloat < 0.2 | currentNode->stddevtileref < 0.2)
			{
				transform.shiftX = 0;
				transform.shiftY = 0;
			}
			else
			{
				/*------------------- Find transformation ----------------- */
				transform = registerTilePixel_EstimateSubPixelSearchBuffer(ref, 
																		   floating, 
																		   pixelBuffer, 
																		   bins, 
																		   refBand, 
																		   floatBand, 
																		   currentNode->tileCoords,
																		   1,
																		   measure);
				/*------------------------------------------------------------ */
			}
			
			
			
			/*------------------- set transformation ----------------- */
			currentNode->TileTransformation->shiftX = transform.shiftX;
			currentNode->TileTransformation->shiftY = transform.shiftY;
			/*------------------------------------------------------------ */
			
			/*---------- Get Next level of tile and add to Queue -------------- */
			if((currentNode->tileCoords->imgABRX - currentNode->tileCoords->imgATLX) 
			   < (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else if((currentNode->tileCoords->imgABRY - currentNode->tileCoords->imgATLY) 
					< (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else
			{
				imageOverlap->findtiles(currentNode->tileCoords, tiles, transform);
				for(int i = 0; i < 9; i++)
				{
					stddevref = mathUtils.tileRangePercentage(&tiles[i], ref, true, refBand, -1);
					stddevfloat = mathUtils.tileRangePercentage(&tiles[i], floating, false, floatBand, -1);
					queue->add(imageTree->addNode(&tiles[i], stddevref, stddevfloat));
				}
			}
			
			
			/*************** Print transformation ***************/
			std::cout << "Transform of x: "
				<< transform.shiftX 
				<< " and y: " 
				<< transform.shiftY 
				<< std::endl;
			/***************************************************************/
			
			/*----------------------------------------------------------------- */
		}
		/////////////////////////////////////////////////////////////////
		/*************************************************************/
		
		/********** Print NonusImageTree *************************/
		imageTree->printTree();
		/*********************************************************/
		
		/********* Output Control Points for ENVI ***************/
		imageTree->write2EnviGcpsFile(ctrlptsOutputFile, -1);
		/*******************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( tiles != NULL )
		{
			delete [] tiles;
		}
		if( queue != NULL )
		{
			delete queue;
		}
		if(imageTree != NULL )
		{
			delete imageTree; // NOT YET IMPLEMENTED :-s
		}
		throw e;
	}
	
	/************** Free Memory ************************/
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( tiles != NULL )
	{
		delete [] tiles;
	}
	if( queue != NULL )
	{
		delete queue;
	}
	if(imageTree != NULL )
	{
		delete imageTree; // NOT YET IMPLEMENTED :-s
	}
	/**************************************************/
}

NonusImageTree* RegisterImages::constructNonusImageTreeSubPixel(GDALDataset *ref, 
																GDALDataset *floating,
																int pixelBuffer, 
																int bins, 
																int refBand, 
																int floatBand,
																int minTileSize,
																int measure,
																int search,
																int numWalks,
																int tmax,
																int tdecrease,
																int successful,
																int unsuccessful,
																bool errorCorrection,
																float measureThreshold)
throw(ImageRegistrationException)
{
	MathUtils mathUtils;
	NonusImageTree *imageTree = NULL;
	ImageOverlap *imageOverlap = NULL;
	TileCoords *tiles = NULL;
	Queue *queue = NULL;
	double stddevref = 0;
	double stddevfloat = 0;
	double imageARange = 0;
	double imageBRange = 0;
	try
	{
		srand((unsigned)time(NULL));
		
		imageARange = mathUtils.imageRange(ref, refBand);
		imageBRange = mathUtils.imageRange(floating, floatBand);
		
		/***************** Init the NonusImageTree *****************/
		imageTree = new NonusImageTree;
		/***********************************************************/
		
		/************** Find Overlapping areas **********************/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithShift(ref, floating, 0, 0);
		int *refImagePixels;
		int *floatImagePixels;
		double *geoCorners;
		refImagePixels = imageOverlap->getImageAPixelCoords();
		floatImagePixels = imageOverlap->getImageBPixelCoords();
		geoCorners = imageOverlap->getOverlapGeoCoords();
		
		TileCoords imageCoords;
		imageCoords.imgATLX = refImagePixels[0];
		imageCoords.imgATLY = refImagePixels[1];
		imageCoords.imgABRX = refImagePixels[2];
		imageCoords.imgABRY = refImagePixels[3];
		imageCoords.imgBTLX = floatImagePixels[0];
		imageCoords.imgBTLY = floatImagePixels[1];
		imageCoords.imgBBRX = floatImagePixels[2];
		imageCoords.imgBBRY = floatImagePixels[3];
		imageCoords.eastingTL = geoCorners[0];
		imageCoords.northingTL = geoCorners[1];
		imageCoords.eastingBR = geoCorners[2];
		imageCoords.northingBR = geoCorners[3];
		/*************************************************************/
		
		int numOfLevels = imageTree->estimateNumberLevels((imageCoords.imgABRX-imageCoords.imgATLX),
														  (imageCoords.imgABRY-imageCoords.imgATLY),
														  minTileSize);
		
		TreeLevel *treeLevels;
		treeLevels = new TreeLevel[numOfLevels];
		
		imageTree->estimateRequiredNodes((imageCoords.imgABRX-imageCoords.imgATLX),
										 (imageCoords.imgABRY-imageCoords.imgATLY),
										 minTileSize,
										 treeLevels,
										 numOfLevels);
		
		int numTreeNodes = treeLevels[numOfLevels-1].totalNodes;

		std::cout << "Level" << " \t " << "Nodes At Level"
			<< " \t " << "Total Nodes" << " \t " << "X Distance"
			<< " \t " << "Y Distance" << " \t " << "Angular Distance" << std::endl;
		for(int i = 0; i < numOfLevels; i++)
		{
			std::cout << treeLevels[i].level << " \t " << treeLevels[i].nodesAtLevel
					  << " \t " << treeLevels[i].totalNodes << " \t " << treeLevels[i].xDistance
			<< " \t " << treeLevels[i].yDistance << " \t " << treeLevels[i].angularDistance << std::endl;
		}

		numTreeNodes--;
		std::cout << "Number of required tree nodes = " << numTreeNodes << std::endl;
			
		/****** Perform Linear Subpixel Registration on the Images *********/
		Transform transform = findTileTransformation(ref, 
													 floating, 
													 pixelBuffer,
													 refBand, 
													 floatBand, 
													 &imageCoords,
													 measure,
													 bins,
													 search,
													 numWalks,
													 tmax,
													 tdecrease,
													 successful,
													 unsuccessful,
													 measureThreshold,
													 0,
													 0,
													 true);
		
		/*******************************************************************/
		
		/*************** Print transformation ***************/
		std::cout << "ROOT - Transform of x: "
			<< transform.shiftX 
			<< " and y: " 
			<< transform.shiftY 
			<< " Measure = "
			<< transform.measureValue
			<< std::endl;
		/***************************************************************/
		
		/****************** Create Nonus Image Tree Root **************/
		TileCoords *tileCoords = imageTree->setRoot(transform, imageCoords, 1, 1);
		/************************************************************/
		
		/****************** Calculate 9 tiles ************************/
		tiles = new TileCoords[9]; 
		imageOverlap->findtiles(tileCoords, tiles, transform);
		/*************************************************************/
		
		/****************** Create NonusImageTree *********************/
		
		//////// Create and Initialize Queue with Image tiles ////////////
		queue = new Queue;
		double tmpPercentageRangeA = 0;
		double tmpPercentageRangeB = 0;
		for(int i = 0; i < 9; i++)
		{
			//std::cout << "Calculate Tile range (Reference Image):\n";
			tmpPercentageRangeA = mathUtils.tileRangePercentage(&tiles[i], 
																ref, 
																true, 
																refBand, 
																imageARange);
			//std::cout << "Calculate Tile range (Floating Image):\n";
			tmpPercentageRangeB = mathUtils.tileRangePercentage(&tiles[i], 
																floating, 
																false, 
																floatBand, 
																imageBRange);
			queue->add(imageTree->addNode(&tiles[i], 
										  tmpPercentageRangeA, 
										  tmpPercentageRangeB));
		}
		/////////////////////////////////////////////////////////////////
		
		////////////// Initialize ////////////////////////////
		NonusTreeNode *currentNode;
		NonusTreeNode *tmpNode;
		NonusTreeNode **parentNodes = NULL;
		*parentNodes = new NonusTreeNode[treeLevels[0].nodesAtLevel];
		parentNodes[0] = imageTree->getRoot();
		int counter = 0;
		bool finished = false;
		//////////////////////////////////////////////////////
		
		std::cout << "\nLEVEL 0 - COMPLETE\n\n";
		
		/***************** Find transformations ************************/
		for( int i = 1; i < numOfLevels; i++)
		{
			counter = 0;
			////////////////// Fill Next Level of Nonus Tree //////////////////
			while(queue->getSize() > 0)
			{
				
				currentNode = queue->getNext();
				if(/*currentNode->stddevtilefloat < 0.2 |*/ currentNode->stddevtileref < 0.2)
				{
					transform.shiftX = 0;
					transform.shiftY = 0;
					transform.measureValue = -1;
				}
				else
				{
					/*------------------- Find transformation ----------------- */
					transform = findTileTransformation(ref, 
													   floating, 
													   pixelBuffer,
													   refBand, 
													   floatBand, 
													   currentNode->tileCoords,
													   measure,
													   bins,
													   search,
													   numWalks,
													   tmax,
													   tdecrease,
													   successful,
													   unsuccessful,
													   measureThreshold,
													   0,
													   0,
													   true);
					/*------------------------------------------------------------ */
				}
				
				/*------------------- set transformation ----------------- */
				currentNode->TileTransformation->shiftX = transform.shiftX;
				currentNode->TileTransformation->shiftY = transform.shiftY;
				currentNode->TileTransformation->measureValue = transform.measureValue;
				/*------------------------------------------------------------ */
				/*************** Print transformation ***************/
				std::cout << "Transform of x: "
					<< transform.shiftX 
					<< " and y: " 
					<< transform.shiftY 
					<< " measure = "
					<< transform.measureValue
					<< std::endl;
				/***************************************************************/
				
			}
	
			imageTree->getNodesAtLevel(treeLevels[i-1].level, parentNodes, treeLevels[i-1].nodesAtLevel);
			
			/////////// Correct Errors at level and find next level of tiles //////////
			for(int j = 0; j < treeLevels[i-1].nodesAtLevel; j++)
			{

				if( errorCorrection )
				{
					//int errorThreshold = pixelBuffer/i;
					int errorThreshold = 2;
					this->correctErrors(parentNodes[j],
										ref, 
										floating,
										pixelBuffer, 
										bins, 
										refBand, 
										floatBand,
										measure,
										errorThreshold);
				}
				else
				{
					// No error correction!!
				}
				
				
				if(numTreeNodes < imageTree->getNumNodes())
				{
					//std::cout << "Required number of tree nodes identified\n";
					finished = true;
				}
				else
				{
					for(int k = 0; k < 9; k++)
					{
						currentNode = parentNodes[j]->children[k];
						
						/////////////// Find the nodes for the next level ////////////////
						imageOverlap->findtiles(currentNode->tileCoords, tiles, transform);
						for(int n = 0; n < 9; n++)
						{
							stddevref = mathUtils.tileRangePercentage(&tiles[n], 
																	  ref, 
																	  true, 
																	  refBand, 
																	  imageARange);
							stddevfloat = mathUtils.tileRangePercentage(&tiles[n], 
																		floating, 
																		false, 
																		floatBand, 
																		imageBRange);
							tmpNode = imageTree->addNode(&tiles[n], 
														 stddevref, 
														 stddevfloat);
							if(tmpNode == NULL)
							{
								std::cout << "Something has gone VERY wrong and the returned node is NULL!!\n";
							}
							queue->add(tmpNode);
						}
					}
				}
			}
			/////////////////////////////////////////////////////////////////
			
			std::cout << "\nLEVEL " << i << " - COMPLETE\n\n";
		}
	}
	catch(ImageRegistrationException e)
	{
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( tiles != NULL )
		{
			delete [] tiles;
		}
		if( queue != NULL )
		{
			delete queue;
		}
		if(imageTree != NULL )
		{
			delete imageTree; // NOT YET IMPLEMENTED :-s
		}
		throw e;
	}
	
	/************** Free Memory ************************/
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( tiles != NULL )
	{
		delete [] tiles;
	}
	if( queue != NULL )
	{
		delete queue;
	}
	/**************************************************/
	return imageTree;
}

void RegisterImages::constructDiffResolutionPixel_EstimateSubPixelNonusImageTree(GDALDataset *ref, 
																				  GDALDataset *floating,
																				  const char *ctrlptsOutputFile,
																				  int pixelBuffer, 
																				  int bins, 
																				  int refBand, 
																				  int floatBand,
																				  int minTileSize,
																				  int measure)
throw(ImageRegistrationException)	
{
	MathUtils mathUtils;
	NonusImageTree *imageTree = NULL;
	ImageOverlap *imageOverlap = NULL;
	TileCoords *tiles = NULL;
	Queue *queue = NULL;
	double stddevref = 0;
	double stddevfloat = 0;
	double imageARange = 0;
	double imageBRange = 0;
	try
	{
		imageARange = mathUtils.imageRange(ref, refBand);
		imageBRange = mathUtils.imageRange(floating, floatBand);
		//std::cout << "Image A Range = " << imageARange << std::endl;
		//std::cout << "Image B Range = " << imageBRange << std::endl;
		/***************** Init the NonusImageTree *****************/
		imageTree = new NonusImageTree;
		/***********************************************************/
		
		/************** Find Overlapping areas **********************/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithDiffResolutions(ref, floating);
		int *refImagePixels;
		int *floatImagePixels;
		double *geoCorners;
		refImagePixels = imageOverlap->getImageAPixelCoords();
		floatImagePixels = imageOverlap->getImageBPixelCoords();
		geoCorners = imageOverlap->getOverlapGeoCoords();
		
		TileCoords imageCoords;
		imageCoords.imgATLX = refImagePixels[0];
		imageCoords.imgATLY = refImagePixels[1];
		imageCoords.imgABRX = refImagePixels[2];
		imageCoords.imgABRY = refImagePixels[3];
		imageCoords.imgBTLX = floatImagePixels[0];
		imageCoords.imgBTLY = floatImagePixels[1];
		imageCoords.imgBBRX = floatImagePixels[2];
		imageCoords.imgBBRY = floatImagePixels[3];
		imageCoords.eastingTL = geoCorners[0];
		imageCoords.northingTL = geoCorners[1];
		imageCoords.eastingBR = geoCorners[2];
		imageCoords.northingBR = geoCorners[3];
		/*************************************************************/
		
		/***************** TEST: Print overlapping coords *****************/
		
		std::cout << "[" << imageCoords.imgATLX << ", " << imageCoords.imgATLY << "]" <<
					"[" << imageCoords.imgABRX << ", " << imageCoords.imgABRY << "]\n";
		std::cout << "[" << imageCoords.imgBTLX << ", " << imageCoords.imgBTLY << "]" <<
					"[" << imageCoords.imgBBRX << ", " << imageCoords.imgBBRY << "]\n";
		std::cout << "[" << imageCoords.eastingTL << ", " << imageCoords.northingTL << "]" <<
					"[" << imageCoords.eastingBR << ", " << imageCoords.northingBR << "]\n";
		/*******************************************************************/
		
		/****** Perform Linear Subpixel Registration on the Images *********/
		Transform transform = registerTileDiffResolutionPixel_EstimateSubPixelSearchBuffer(ref, 
																							floating, 
																							pixelBuffer, 
																							bins, 
																							refBand, 
																							floatBand, 
																							&imageCoords,
																							1,
																							measure);
		/*******************************************************************/
		
		/*************** Print transformation ***************/
		std::cout << "ROOT - Transform of x: "
			<< transform.shiftX 
			<< " and y: " 
			<< transform.shiftY 
			<< std::endl;
		/***************************************************************/
		
		/****************** Create Nonus Image Tree Root **************/
		TileCoords *tileCoords = imageTree->setRoot(transform, imageCoords, 1, 1);
		/************************************************************/
		
		/****************** Calculate 9 tiles ************************/
		tiles = new TileCoords[9]; 
		imageOverlap->findtilesDiffResolution(tileCoords, tiles, transform);
		/*************************************************************/
		
		/****************** Create NonusImageTree *********************/
		
		//////// Create and Initialize Queue with Image tiles ////////////
		queue = new Queue;
		double tmpPercentageRangeA = 0;
		double tmpPercentageRangeB = 0;
		for(int i = 0; i < 9; i++)
		{
			tmpPercentageRangeA = mathUtils.tileRangePercentage(&tiles[i], 
																ref, 
																true, 
																refBand, 
																imageARange);
			tmpPercentageRangeB = mathUtils.tileRangePercentage(&tiles[i], 
																floating, 
																false, 
																floatBand, 
																imageBRange);
			queue->add(imageTree->addNode(&tiles[i], 
										  tmpPercentageRangeA, 
										  tmpPercentageRangeB));
		}
		/////////////////////////////////////////////////////////////////
		
		////////////// Initialize ////////////////////////////
		NonusTreeNode *currentNode;
		//////////////////////////////////////////////////////
		
		////////////////// Fill Nonus Tree //////////////////
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			
			if(currentNode->stddevtilefloat < 0.2 | currentNode->stddevtileref < 0.2)
			{
				transform.shiftX = 0;
				transform.shiftY = 0;
			}
			else
			{
				/*------------------- Find transformation ----------------- */
				transform = registerTileDiffResolutionPixel_EstimateSubPixelSearchBuffer(ref, 
																						  floating, 
																						  pixelBuffer, 
																						  bins, 
																						  refBand, 
																						  floatBand, 
																						  currentNode->tileCoords,
																						  1,
																						  measure);
				/*------------------------------------------------------------ */
			}
			
			
			
			/*------------------- set transformation ----------------- */
			currentNode->TileTransformation->shiftX = transform.shiftX;
			currentNode->TileTransformation->shiftY = transform.shiftY;
			/*------------------------------------------------------------ */
			//std::cout << "added transformation to tree\n";
			
			/*---------- Get Next level of tile and add to Queue -------------- */
			if((currentNode->tileCoords->imgABRX - currentNode->tileCoords->imgATLX) 
			   < (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else if((currentNode->tileCoords->imgABRY - currentNode->tileCoords->imgATLY) 
					< (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else
			{
				imageOverlap->findtilesDiffResolution(currentNode->tileCoords, tiles, transform);
				//std::cout << "identified new tiles.\n";
				for(int i = 0; i < 9; i++)
				{
					//std::cout << "Adding tiles to tree and calculating percentage range i = " << i << "\n";
					stddevref = mathUtils.tileRangePercentage(&tiles[i], 
															  ref, 
															  true, 
															  refBand, 
															  imageARange);
					//std::cout << "calculated ref\n";
					stddevfloat = mathUtils.tileRangePercentage(&tiles[i], 
																floating, 
																false, 
																floatBand, 
																imageBRange);
					//std::cout << "calculated floating\n";
					queue->add(imageTree->addNode(&tiles[i], 
												  stddevref, 
												  stddevfloat));
				}
			}
			
			
			/*************** Print transformation ***************/
			std::cout << "Transform of x: "
				<< transform.shiftX 
				<< " and y: " 
				<< transform.shiftY 
				<< std::endl;
			/***************************************************************/
			
			/*----------------------------------------------------------------- */
		}
		/////////////////////////////////////////////////////////////////
		/*************************************************************/
		
		/********** Print NonusImageTree *************************/
		imageTree->printTree();
		/*********************************************************/
		
		/********* Output Control Points for ENVI ***************/
		imageTree->writeMap2Image2EnviGcpsFile(ctrlptsOutputFile, -1);
		/*******************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( tiles != NULL )
		{
			delete [] tiles;
		}
		if( queue != NULL )
		{
			delete queue;
		}
		if(imageTree != NULL )
		{
			delete imageTree; // NOT YET IMPLEMENTED :-s
		}
		throw e;
	}
	
	/************** Free Memory ************************/
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( tiles != NULL )
	{
		delete [] tiles;
	}
	if( queue != NULL )
	{
		delete queue;
	}
	if(imageTree != NULL )
	{
		delete imageTree; // NOT YET IMPLEMENTED :-s
	}
	/**************************************************/
}

void RegisterImages::constructPixel_SubPixelNonusImageTree(GDALDataset *ref, 
														   GDALDataset *floating,
														   const char *ctrlptsOutputFile,
														   int pixelBuffer, 
														   int bins, 
														   int refBand, 
														   int floatBand,
														   int minTileSize,
														   double tileMovement,
														   int measure)
throw(ImageRegistrationException)	
{
	NonusImageTree *imageTree = NULL;
	ImageOverlap *imageOverlap = NULL;
	TileCoords *tiles = NULL;
	Queue *queue = NULL;
	//std::cout << "Starting to construt subPixel nonus image tree" << std::endl;
	try
	{
		/***************** Init the NonusImageTree *****************/
		imageTree = new NonusImageTree;
		/***********************************************************/
		
		/************** Find Overlapping areas **********************/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithShift(ref, floating, 0, 0);
		int *refImagePixels;
		int *floatImagePixels;
		double *geoCorners;
		refImagePixels = imageOverlap->getImageAPixelCoords();
		floatImagePixels = imageOverlap->getImageBPixelCoords();
		geoCorners = imageOverlap->getOverlapGeoCoords();
		
		TileCoords imageCoords;
		imageCoords.imgATLX = refImagePixels[0];
		imageCoords.imgATLY = refImagePixels[1];
		imageCoords.imgABRX = refImagePixels[2];
		imageCoords.imgABRY = refImagePixels[3];
		imageCoords.imgBTLX = floatImagePixels[0];
		imageCoords.imgBTLY = floatImagePixels[1];
		imageCoords.imgBBRX = floatImagePixels[2];
		imageCoords.imgBBRY = floatImagePixels[3];
		imageCoords.eastingTL = geoCorners[0];
		imageCoords.northingTL = geoCorners[1];
		imageCoords.eastingBR = geoCorners[2];
		imageCoords.northingBR = geoCorners[3];
		/*************************************************************/
		
		/****** Perform Linear Subpixel Registration on the Images *********/
		Transform transform = registerTilePixel_SubPixelSearchBuffer(ref, 
															   floating, 
															   pixelBuffer, 
															   bins, 
															   refBand, 
															   floatBand, 
															   &imageCoords,
															   tileMovement,
															   measure);
		/*******************************************************************/
		
		/****************** Create Nonus Image Tree Root **************/
		TileCoords *tileCoords = imageTree->setRoot(transform, imageCoords, 0, 0);
		/************************************************************/
		
		
		
		/****************** Calculate 9 tiles ************************/
		tiles = new TileCoords[9]; 
		imageOverlap->findtiles(tileCoords, tiles);
		/*************************************************************/
		
		/****************** Create NonusImageTree *********************/
		
		//////// Create and Initialize Queue with Image tiles ////////////
		queue = new Queue;
		for(int i = 0; i < 9; i++)
		{
			queue->add(imageTree->addNode(&tiles[i], 0, 0));
		}
		/////////////////////////////////////////////////////////////////
		
		////////////// Initialize ////////////////////////////
		NonusTreeNode *currentNode;
		//////////////////////////////////////////////////////
		
		////////////////// Fill Nonus Tree //////////////////
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			/*------------------- Find transformation ----------------- */
			transform = registerTilePixel_SubPixelSearchBuffer(ref, 
														 floating, 
														 pixelBuffer, 
														 bins, 
														 refBand, 
														 floatBand, 
														 currentNode->tileCoords,
														 tileMovement,
														 measure);
			/*------------------------------------------------------------ */
			
			/*------------------- set transformation ----------------- */
			currentNode->TileTransformation->shiftX = transform.shiftX;
			currentNode->TileTransformation->shiftY = transform.shiftY;
			/*------------------------------------------------------------ */
			
			/*---------- Get Next level of tile and add to Queue -------------- */
			if((currentNode->tileCoords->imgABRX - currentNode->tileCoords->imgATLX) 
			   < (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else if((currentNode->tileCoords->imgABRY - currentNode->tileCoords->imgATLY) 
					< (minTileSize*3))
			{
				// Don't get more tiles they will be too small!!
			}
			else
			{
				imageOverlap->findtiles(currentNode->tileCoords, tiles);
				for(int i = 0; i < 9; i++)
				{
					queue->add(imageTree->addNode(&tiles[i], 0, 0));
				}
			}
			/*----------------------------------------------------------------- */
		}
		/////////////////////////////////////////////////////////////////
		/*************************************************************/
		
		/********** Print NonusImageTree *************************/
		imageTree->printTree();
		/*********************************************************/
		
		/********* Output Control Points for ENVI ***************/
		imageTree->write2EnviGcpsFile(ctrlptsOutputFile, -1);
		/*******************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( tiles != NULL )
		{
			delete [] tiles;
		}
		if( queue != NULL )
		{
			delete queue;
		}
		if(imageTree != NULL )
		{
			delete imageTree; // NOT YET IMPLEMENTED :-s
		}
		throw e;
	}
	
	/************** Free Memory ************************/
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( tiles != NULL )
	{
		delete [] tiles;
	}
	if( queue != NULL )
	{
		delete queue;
	}
	if(imageTree != NULL )
	{
		delete imageTree; // NOT YET IMPLEMENTED :-s
	}
	/**************************************************/
}

Transform RegisterImages::registerTileSubPixelSearchBuffer(GDALDataset *ref, 
														   GDALDataset *floating, 
														   int pixelBuffer, 
														   int bins, 
														   int refBand, 
														   int floatBand,
														   TileCoords *tile,
														   double tileMovement,
														   int measure)
throw(ImageRegistrationException)
{
	
	double xShiftMax = 0;
	double yShiftMax = 0;
	double xShiftMin = 0;
	double yShiftMin = 0;
	
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	
	VectorImageMeasures *vecImageMeasures;
	vecImageMeasures = new VectorImageMeasures;
	
	bool findMax = true;
	
	if(measure == image_measures::mi)
	{
		findMax = true;
	}
	else if(measure == image_measures::clusterReward)
	{
		findMax = true;
	}
	else if(measure == image_measures::distance2Independence)
	{
		findMax = true;
	}
	else if(measure == image_measures::euclidean)
	{
		findMax = false;
	}
	else if(measure == image_measures::manhattan)
	{
		findMax = false;
	}
	else if(measure == image_measures::correlationCoefficient)
	{
		findMax = true;
	}
	else
	{
		findMax = true;
	}
	int bufferSize = (mathUtils->roundUp(pixelBuffer/tileMovement)*2) + 1;
	double **buffervalues = new double*[bufferSize];
	//std::cout << "Entered Buffer search subpixel pixelBuffer: " << pixelBuffer << std::endl;
	try
	{
		/********************* Calculate MI values for the Buffer ************************/
		
		std::cout << "bufferSize = " << bufferSize << std::endl;
		
		double xShiftInput = (pixelBuffer * (-1));
		double yShiftInput = pixelBuffer;
		
		double max = 0;
		double min = 0;
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			buffervalues[i] = new double[bufferSize];
			xShiftInput = (pixelBuffer * (-1));
			
			for(int j = 0; j<bufferSize; j++)
			{
				//std::cout << "\n\nxShiftInput: " << xShiftInput 
				//<< " yShiftInput: " << yShiftInput << std::endl;
				//std::cout << std::endl;
				buffervalues[i][j] = this->calcMeasureImagesTilePixelSubShift(ref, 
																		   floating, 
																		   xShiftInput, 
																		   yShiftInput, 
																		   bins, 
																		   refBand, 
																		   floatBand, 
																		   tile,
																		   measure);
				
				if(i == (bufferSize-1) & j == 0)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
				}
				else if( buffervalues[i][j] > max)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
				}
				else
				{
					// DO NOTHING
				}
				
				if(i == (bufferSize-1) & j == 0)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
				}
				else if( buffervalues[i][j] < min)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
				}
				else
				{
					// DO NOTHING
				}
				
				xShiftInput += tileMovement;
				if(xShiftInput > -0.000001 & xShiftInput < 0.000001)
				{
					xShiftInput = 0;
				}
			}
			yShiftInput -= tileMovement;
			if(yShiftInput > -0.000001 & yShiftInput < 0.000001)
			{
				yShiftInput = 0;
			}
		}
		/**********************************************************************************/
		
		/*********** TEST: Print out MI Buffer *************************/
		for(int i = (bufferSize-1); i >= 0; i--)
		{
				for(int j=0; j < bufferSize; j++)
				{
					std::cout << buffervalues[i][j] << ", ";
				}
				std::cout << std::endl;
		}
		/***************************************************************/
		
		/*************** Print value and transformation ***************/
		if(findMax)
		{
			std::cout << "Max = " 
			<< max 
			<< " Meaning a shift in pixels of x: "
			<< xShiftMax 
			<< " and y: " 
			<< yShiftMax 
			<< std::endl;
		}
		else
		{
			std::cout << "Min = " 
			<< min 
			<< " Meaning a shift in pixels of x: "
			<< xShiftMin 
			<< " and y: " 
			<< yShiftMin 
			<< std::endl;
		}
		/****************************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( vecImageMeasures != NULL )
		{
			delete vecImageMeasures;
		}
		if(buffervalues != NULL)
		{
			for(int i = 0; i < bufferSize; i++)
			{
				delete [] buffervalues[i];
			}
			delete [] buffervalues;
		}
		throw e;
	}
	
	if( vecImageMeasures != NULL )
	{
		delete vecImageMeasures;
	}
	if(buffervalues != NULL)
	{
		for(int i = 0; i < bufferSize; i++)
		{
			delete [] buffervalues[i];
		}
		delete [] buffervalues;
	}
	//std::exit(0);
	/************** Create Transform Struct and return *************/
	Transform transform;
	if(findMax)
	{
		transform.shiftX = xShiftMax;
		transform.shiftY = yShiftMax;
	}
	else
	{
		transform.shiftX = xShiftMin;
		transform.shiftY = yShiftMin;
	}
	
	return transform;
	/****************************************************************/
}

Transform RegisterImages::registerTilePixel_EstimateSubPixelSearchBuffer(GDALDataset *ref, 
																		 GDALDataset *floating, 
																		 int pixelBuffer, 
																		 int bins, 
																		 int refBand, 
																		 int floatBand,
																		 TileCoords *tile,
																		 int tileMovement,
																		 int measure)
throw(ImageRegistrationException)
{
	//std::cout << "Find new position for point\n";
	
	double xShiftMax = 0;
	double yShiftMax = 0;
	double xShiftMin = 0;
	double yShiftMin = 0;
	
	Transform transform;
	
	VectorImageMeasures *vecImageMeasures;
	vecImageMeasures = new VectorImageMeasures;
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	Interpolation *interpolation;
	interpolation = new Interpolation;
	
	bool findMax = true;
	
	if(measure == image_measures::mi)
	{
		findMax = true;
	}
	else if(measure == image_measures::euclidean)
	{
		findMax = false;
	}
	else if(measure == image_measures::manhattan)
	{
		findMax = false;
	}
	else if(measure == image_measures::correlationCoefficient)
	{
		findMax = true;
	}
	else if(measure == image_measures::clusterReward)
	{
		findMax = true;
	}
	else if(measure == image_measures::distance2Independence)
	{
		findMax = true;
	}
	else if(measure == image_measures::kolmogorovDistance)
	{
		findMax = true;
	}
	else if(measure == image_measures::kullbachDivergence)
	{
		findMax = true;
	}
	else if(measure == image_measures::hellingerDistance)
	{
		findMax = true;
	}
	else if(measure == image_measures::toussaintsDistance)
	{
		findMax = true;
	}
	else if(measure == image_measures::linKDivergence)
	{
		findMax = true;
	}
	else if(measure == image_measures::norm_mi_ecc)
	{
		findMax = true;
	}
	else if(measure == image_measures::norm_mi_y)
	{
		findMax = true;
	}
	int bufferSize = (pixelBuffer*2) + 1;
	//std::cout << "Entered Buffer search pixelBuffer: " << pixelBuffer << std::endl;
	
	double **buffervalues = new double*[bufferSize];
	
	try
	{
		/********************* Calculate measure values for the Buffer ************************/
		//*buffervalues = new double[bufferSize];
		
		double xShiftInput = (pixelBuffer * (-1));
		double yShiftInput = pixelBuffer;
		
		double max = 0;
		double min = 0;
		int xPixelMin = 0; //Used below to aid subpixel calc.
		int yPixelMin = 0; //Used below to aid subpixel calc.
		int xPixelMax = 0; //Used below to aid subpixel calc.
		int yPixelMax = 0; //Used below to aid subpixel calc.
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			buffervalues[i] = new double[bufferSize];
			xShiftInput = (pixelBuffer * (-1));
			
			for(int j = 0; j<bufferSize; j++)
			{
				buffervalues[i][j] = this->calcMeasureImagesTilePixelShift(ref, 
																		   floating, 
																		   xShiftInput, 
																		   yShiftInput, 
																		   bins, 
																		   refBand, 
																		   floatBand, 
																		   tile,
																		   measure);
				
				if(i == (bufferSize-1) & j == 0)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
					xPixelMax = j;
					yPixelMax = i;
					
				}
				else if( buffervalues[i][j] > max)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
					xPixelMax = j;
					yPixelMax = i;
				}
				else
				{
					// DO NOTHING
				}
				
				if(i == (bufferSize-1) & j == 0)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
					xPixelMin = j;
					yPixelMin = i;
				}
				else if( buffervalues[i][j] < min)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
					xPixelMin = j;
					yPixelMin = i;
				}
				else
				{
					// DO NOTHING
				}
				xShiftInput += tileMovement;
			}
			yShiftInput -= tileMovement;
		}
		/**********************************************************************************/
		
		/*********** TEST: Print out MI Buffer *************************
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			for(int j=0; j < bufferSize; j++)
			{
				std::cout << buffervalues[i][j] << ", ";
			}
			std::cout << std::endl;
		}
		/***************************************************************/
	
		/*************** Print value and transformation ***************/
		int xPixel = 0; //Used below to aid subpixel calc.
		int yPixel = 0; //Used below to aid subpixel calc.
		if(findMax)
		{
			//std::cout << "Max = " 
			//<< max 
			//<< " Meaning a shift in pixels of x: "
			//<< xShiftMax 
			//<< " and y: " 
			//<< yShiftMax 
			//<< std::endl;
			xPixel = xPixelMax;
			yPixel = yPixelMax;
		}
		else
		{
			//std::cout << "Min = " 
			//<< min 
			//<< " Meaning a shift in pixels of x: "
			//<< xShiftMin 
			//<< " and y: " 
			//<< yShiftMin 
			//<< std::endl;
			xPixel = xPixelMin;
			yPixel = yPixelMin;
		}
		/****************************************************************/
		
		/****************** Create Transform ***********************/
		if(findMax)
		{
			transform.shiftX = xShiftMax;
			transform.shiftY = yShiftMax;
			transform.measureValue = max;
		}
		else
		{
			transform.shiftX = xShiftMin;
			transform.shiftY = yShiftMin;
			transform.measureValue = min;
		}
		/****************************************************************/
		
		if( measure == 3 & max < 0.2 )
		{
			transform.shiftX = 0;
			transform.shiftY = 0;
		}
		else
		{
			/****************** SubPixel calculation ***********************/
			
			////////// Get Square of data around the point of interest ////////
			double points[9];
			int onEdge[9];
			
			//std::cout << "yPixel: " << yPixel << std::endl;
			//std::cout << "xPixel: " << xPixel << std::endl;
			
			points[4] = buffervalues[yPixel][xPixel];
			onEdge[4] = 0;
			if(xPixel == 0)
			{
				if(yPixel == 0)
				{
					//points[0 & 1 & 6] not available
					onEdge[0] = -1;
					onEdge[1] = -1;
					onEdge[6] = -1;
				}
				else if(yPixel == (bufferSize-1))
				{
					points[1] = buffervalues[yPixel-1][xPixel];
					onEdge[1] = 0;
					
					//points[0 & 6] not available
					onEdge[0] = -1;
					onEdge[6] = -1;
				}
				else
				{
					points[1] = buffervalues[yPixel-1][xPixel];
					onEdge[1] = 0;
					
					//points[0 & 6] not available
					onEdge[0] = -1;
					onEdge[6] = -1;
					
				}
				//points[3] not available
				onEdge[3] = -1;
			}
			else
			{
				if(yPixel == 0)
				{
					points[6] = buffervalues[yPixel+1][xPixel-1];
					onEdge[6] = 0;
					
					//points[0 & 1] not available
					onEdge[0] = -1;
					onEdge[1] = -1;
				}
				else if(yPixel == (bufferSize-1))
				{
					points[0] = buffervalues[yPixel-1][xPixel-1];
					points[1] = buffervalues[yPixel-1][xPixel];
					
					onEdge[0] = 0;
					onEdge[1] = 0;
					
					//points[6] not available
					onEdge[6] = -1;
				}
				else
				{
					points[0] = buffervalues[yPixel-1][xPixel-1];
					points[1] = buffervalues[yPixel-1][xPixel];
					points[6] = buffervalues[yPixel+1][xPixel-1];
					
					onEdge[0] = 0;
					onEdge[1] = 0;
					onEdge[6] = 0;
					
				}
				points[3] = buffervalues[yPixel][xPixel-1];
				onEdge[3] = 0;
			}
			
			if(xPixel == (bufferSize-1))
			{
				if(yPixel == (bufferSize-1))
				{
					//points[2 & 7 & 8] not available
					onEdge[2] = -1;
					onEdge[7] = -1;
					onEdge[8] = -1;
				}
				else if(yPixel == 0)
				{
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[7] = 0;
					
					//points[2 & 8] not availble
					onEdge[2] = -1;
					onEdge[8] = -1;
				}
				else
				{
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[7] = 0;
					
					//points[2 & 8] not availble
					onEdge[2] = -1;
					onEdge[8] = -1;
				}
				
				//points[5] not available
				onEdge[5] = -1;
			}
			else
			{
				if(yPixel == (bufferSize-1))
				{
					points[2] = buffervalues[yPixel-1][xPixel+1];
					onEdge[2] = 0;
					
					//points[8 & 7] not available
					onEdge[7] = -1;
					onEdge[8] = -1;
				}
				else if(yPixel == 0)
				{
					points[8] = buffervalues[yPixel+1][xPixel+1];
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[8] = 0;
					onEdge[7] = 0;
					
					//points[2] not available
					onEdge[2] = -1;
				}
				else
				{
					points[2] = buffervalues[yPixel-1][xPixel+1];
					points[8] = buffervalues[yPixel+1][xPixel+1];
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[2] = 0;
					onEdge[8] = 0;
					onEdge[7] = 0;
				}
				points[5] = buffervalues[yPixel][xPixel+1];
				onEdge[5] = 0;
			}
			////////////////////////////////////////////////////////////////
			
			Transform subPixelTransform = 
				interpolation->calcateSubPixelTranformationXYCurve(&points[0], 
																   &onEdge[0], 
																   0.1, 
																   findMax);
			
			transform.shiftX += subPixelTransform.shiftX;
			transform.shiftY += subPixelTransform.shiftY;
			
			/**************************************************************/
		}
	}
	catch(ImageRegistrationException e)
	{
		if( vecImageMeasures != NULL )
		{
			delete vecImageMeasures;
		}
		if( mathUtils != NULL)
		{
			delete mathUtils;
		}
		if(interpolation != NULL)
		{
			delete interpolation;
		}
		if(buffervalues != NULL)
		{
			for(int i = 0; i < bufferSize; i++)
			{
				delete [] buffervalues[i];
			}
			delete [] buffervalues;
		}
		throw e;
	}
	
	if( vecImageMeasures != NULL )
	{
		delete vecImageMeasures;
	}
	if( mathUtils != NULL)
	{
		delete mathUtils;
	}
	if(interpolation != NULL)
	{
		delete interpolation;
	}
	if(buffervalues != NULL)
	{
		for(int i = 0; i < bufferSize; i++)
		{
			delete [] buffervalues[i];
		}
		delete [] buffervalues;
	}
	
	/************** Create Transform Struct and return *************/
	return transform;
	/****************************************************************/
}

Transform RegisterImages::registerTileDiffResolutionPixel_EstimateSubPixelSearchBuffer(GDALDataset *ref, 
																						GDALDataset *floating, 
																						int pixelBuffer, 
																						int bins, 
																						int refBand, 
																						int floatBand,
																						TileCoords *tile,
																						int tileMovement,
																						int measure)
throw(ImageRegistrationException)
{
	
	double xShiftMax = 0;
	double yShiftMax = 0;
	double xShiftMin = 0;
	double yShiftMin = 0;
	
	Transform transform;
	
	VectorImageMeasures *vecImageMeasures;
	vecImageMeasures = new VectorImageMeasures;
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	Interpolation *interpolation;
	interpolation = new Interpolation;
	
	bool findMax = true;
	
	if(measure == image_measures::mi)
	{
		findMax = true;
	}
	else if(measure == image_measures::euclidean)
	{
		findMax = false;
	}
	else if(measure == image_measures::manhattan)
	{
		findMax = false;
	}
	if(measure == image_measures::correlationCoefficient)
	{
		findMax = true;
	}	
	//std::cout << "Entered Buffer search subpixel pixelBuffer: " << pixelBuffer << std::endl;
	int bufferSize = (pixelBuffer*2) + 1;
	double **buffervalues = NULL;
	try
	{
		/********************* Calculate measure values for the Buffer ************************/
		*buffervalues = new double[bufferSize];
		
		double xShiftInput = (pixelBuffer * (-1));
		double yShiftInput = pixelBuffer;
		
		double max = 0;
		double min = 0;
		int xPixelMin = 0; //Used below to aid subpixel calc.
		int yPixelMin = 0; //Used below to aid subpixel calc.
		int xPixelMax = 0; //Used below to aid subpixel calc.
		int yPixelMax = 0; //Used below to aid subpixel calc.
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			buffervalues[i] = new double[bufferSize];
			xShiftInput = (pixelBuffer * (-1));
			
			for(int j = 0; j<bufferSize; j++)
			{
				//std::cout << "i = " << i << " j = " << j << std::endl;
				//std::cout << "xShiftInput = " << xShiftInput << " yShiftInput = " << yShiftInput << std::endl;
				buffervalues[i][j] = this->calcMeasureDiffResolutionImagesTilePixelShift(ref, 
																						  floating, 
																						  xShiftInput, 
																						  yShiftInput, 
																						  bins, 
																						  refBand, 
																						  floatBand, 
																						  tile,
																						  measure,
																						  vecImageMeasures);
				
				//std::cout << "inserted distance measure\n";
				
				if(i == (bufferSize-1) & j == 0)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
					xPixelMax = j;
					yPixelMax = i;
					
				}
				else if( buffervalues[i][j] > max)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
					xPixelMax = j;
					yPixelMax = i;
				}
				else
				{
					// DO NOTHING
				}
				
				if(i == (bufferSize-1) & j == 0)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
					xPixelMin = j;
					yPixelMin = i;
				}
				else if( buffervalues[i][j] < min)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
					xPixelMin = j;
					yPixelMin = i;
				}
				else
				{
					// DO NOTHING
				}
				xShiftInput += tileMovement;
			}
			yShiftInput -= tileMovement;
		}
		/**********************************************************************************/
		
		/*********** TEST: Print out MI Buffer *************************
			for(int i = (bufferSize-1); i >= 0; i--)
		{
				for(int j=0; j < bufferSize; j++)
				{
					std::cout << buffervalues[i][j] << ", ";
				}
				std::cout << std::endl;
		}
		/***************************************************************/
		
		/*************** Print value and transformation ***************/
		int xPixel = 0; //Used below to aid subpixel calc.
		int yPixel = 0; //Used below to aid subpixel calc.
		if(findMax)
		{
			//std::cout << "Max = " 
			//<< max 
			//<< " Meaning a shift in pixels of x: "
			//<< xShiftMax 
			//<< " and y: " 
			//<< yShiftMax 
			//<< std::endl;
			xPixel = xPixelMax;
			yPixel = yPixelMax;
		}
		else
		{
			//std::cout << "Min = " 
			//<< min 
			//<< " Meaning a shift in pixels of x: "
			//<< xShiftMin 
			//<< " and y: " 
			//<< yShiftMin 
			//<< std::endl;
			xPixel = xPixelMin;
			yPixel = yPixelMin;
		}
		/****************************************************************/
		
		/****************** Create Transform ***********************/
		if(findMax)
		{
			transform.shiftX = xShiftMax;
			transform.shiftY = yShiftMax;
		}
		else
		{
			transform.shiftX = xShiftMin;
			transform.shiftY = yShiftMin;
		}
		/****************************************************************/
		
		//std::cout << "Calculate subpixel part of transformation\n";
		
		if( measure == 3 & max < 0.2 )
		{
			transform.shiftX = 0;
			transform.shiftY = 0;
		}
		else
		{
			/****************** SubPixel calculation ***********************/
			
			////////// Get Square of data around the point of interest ////////
			double points[9];
			int onEdge[9];
			
			//std::cout << "yPixel: " << yPixel << std::endl;
			//std::cout << "xPixel: " << xPixel << std::endl;
			
			points[4] = buffervalues[yPixel][xPixel];
			onEdge[4] = 0;
			if(xPixel == 0)
			{
				if(yPixel == 0)
				{
					//points[0 & 1 & 6] not available
					onEdge[0] = -1;
					onEdge[1] = -1;
					onEdge[6] = -1;
				}
				else if(yPixel == (bufferSize-1))
				{
					points[1] = buffervalues[yPixel-1][xPixel];
					onEdge[1] = 0;
					
					//points[0 & 6] not available
					onEdge[0] = -1;
					onEdge[6] = -1;
				}
				else
				{
					points[1] = buffervalues[yPixel-1][xPixel];
					onEdge[1] = 0;
					
					//points[0 & 6] not available
					onEdge[0] = -1;
					onEdge[6] = -1;
					
				}
				//points[3] not available
				onEdge[3] = -1;
			}
			else
			{
				if(yPixel == 0)
				{
					points[6] = buffervalues[yPixel+1][xPixel-1];
					onEdge[6] = 0;
					
					//points[0 & 1] not available
					onEdge[0] = -1;
					onEdge[1] = -1;
				}
				else if(yPixel == (bufferSize-1))
				{
					points[0] = buffervalues[yPixel-1][xPixel-1];
					points[1] = buffervalues[yPixel-1][xPixel];
					
					onEdge[0] = 0;
					onEdge[1] = 0;
					
					//points[6] not available
					onEdge[6] = -1;
				}
				else
				{
					points[0] = buffervalues[yPixel-1][xPixel-1];
					points[1] = buffervalues[yPixel-1][xPixel];
					points[6] = buffervalues[yPixel+1][xPixel-1];
					
					onEdge[0] = 0;
					onEdge[1] = 0;
					onEdge[6] = 0;
					
				}
				points[3] = buffervalues[yPixel][xPixel-1];
				onEdge[3] = 0;
			}
			
			if(xPixel == (bufferSize-1))
			{
				if(yPixel == (bufferSize-1))
				{
					//points[2 & 7 & 8] not available
					onEdge[2] = -1;
					onEdge[7] = -1;
					onEdge[8] = -1;
				}
				else if(yPixel == 0)
				{
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[7] = 0;
					
					//points[2 & 8] not availble
					onEdge[2] = -1;
					onEdge[8] = -1;
				}
				else
				{
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[7] = 0;
					
					//points[2 & 8] not availble
					onEdge[2] = -1;
					onEdge[8] = -1;
				}
				
				//points[5] not available
				onEdge[5] = -1;
			}
			else
			{
				if(yPixel == (bufferSize-1))
				{
					points[2] = buffervalues[yPixel-1][xPixel+1];
					onEdge[2] = 0;
					
					//points[8 & 7] not available
					onEdge[7] = -1;
					onEdge[8] = -1;
				}
				else if(yPixel == 0)
				{
					points[8] = buffervalues[yPixel+1][xPixel+1];
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[8] = 0;
					onEdge[7] = 0;
					
					//points[2] not available
					onEdge[2] = -1;
				}
				else
				{
					points[2] = buffervalues[yPixel-1][xPixel+1];
					points[8] = buffervalues[yPixel+1][xPixel+1];
					points[7] = buffervalues[yPixel+1][xPixel];
					onEdge[2] = 0;
					onEdge[8] = 0;
					onEdge[7] = 0;
				}
				points[5] = buffervalues[yPixel][xPixel+1];
				onEdge[5] = 0;
			}
			////////////////////////////////////////////////////////////////
			
			Transform subPixelTransform = 
				interpolation->calcateSubPixelTranformationXYCurve(&points[0], 
																   &onEdge[0], 
																   0.1, 
																   findMax);
			
			transform.shiftX += subPixelTransform.shiftX;
			transform.shiftY += subPixelTransform.shiftY;
			
			/**************************************************************/
		}
	}
	catch(ImageRegistrationException e)
	{
		if( vecImageMeasures != NULL )
		{
			delete vecImageMeasures;
		}
		if( mathUtils != NULL)
		{
			delete mathUtils;
		}
		if(interpolation != NULL)
		{
			delete interpolation;
		}
		if(buffervalues != NULL)
		{
			for(int i = 0; i < bufferSize; i++)
			{
				delete [] buffervalues[i];
			}
			delete [] buffervalues;
		}
		throw e;
	}
	
	if( vecImageMeasures != NULL )
	{
		delete vecImageMeasures;
	}
	if( mathUtils != NULL)
	{
		delete mathUtils;
	}
	if(interpolation != NULL)
	{
		delete interpolation;
	}
	if(buffervalues != NULL)
	{
		for(int i = 0; i < bufferSize; i++)
		{
			delete [] buffervalues[i];
		}
		delete [] buffervalues;
	}
	
	/************** Create Transform Struct and return *************/
	return transform;
	/****************************************************************/
}

Transform RegisterImages::registerTilePixel_SubPixelSearchBuffer(GDALDataset *ref, 
																 GDALDataset *floating, 
																 int pixelBuffer, 
																 int bins, 
																 int refBand, 
																 int floatBand,
																 TileCoords *tile,
																 double tileMovement,
																 int measure)
throw(ImageRegistrationException)
{
	
	double xShiftMax = 0;
	double yShiftMax = 0;
	double xShiftMin = 0;
	double yShiftMin = 0;
	
	Transform transform;
	
	VectorImageMeasures *vecImageMeasures;
	vecImageMeasures = new VectorImageMeasures;
	MathUtils *mathUtils;
	mathUtils = new MathUtils;
	
	bool findMax = true;
	
	if(measure == image_measures::mi)
	{
		findMax = true;
	}
	else if(measure == image_measures::euclidean)
	{
		findMax = false;
	}
	else if(measure == image_measures::manhattan)
	{
		findMax = false;
	}
	
	int bufferSize = (pixelBuffer*2) + 1;
	double **buffervalues = NULL;
	
	//std::cout << "Entered Buffer search subpixel pixelBuffer: " << pixelBuffer << std::endl;
	try
	{
		/********************* Calculate measure values for the Buffer ************************/
		*buffervalues = new double[bufferSize];
		
		double xShiftInput = 0;
		double yShiftInput = pixelBuffer;
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			buffervalues[i] = new double[bufferSize];
			xShiftInput = (pixelBuffer * (-1));
			
			for(int j = 0; j<bufferSize; j++)
			{
				//std::cout << "\n\nxShiftInput: " << xShiftInput 
				//<< " yShiftInput: " << yShiftInput << std::endl;
				//std::cout << std::endl;
				buffervalues[i][j] = this->calcMeasureImagesTilePixelShift(ref, 
																		   floating, 
																		   xShiftInput, 
																		   yShiftInput, 
																		   bins, 
																		   refBand, 
																		   floatBand, 
																		   tile,
																		   measure);
				
				//std::cout << " bufferValue = " << buffervalues[i][j] << std::endl;
				xShiftInput += 1;
				if(xShiftInput > -0.000001 & xShiftInput < 0.000001)
				{
					xShiftInput = 0;
				}
			}
			yShiftInput -= 1;
			if(yShiftInput > -0.000001 & yShiftInput < 0.000001)
			{
				yShiftInput = 0;
			}
		}
		/**********************************************************************************/
		
		/*********** TEST: Print out MI Buffer *************************/
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			for(int j=0; j < bufferSize; j++)
			{
				std::cout << buffervalues[i][j] << ", ";
			}
			std::cout << std::endl;
		}
		/***************************************************************/
		
		/******************** Find MAX and MIN in Buffer ************************/
		double max = 0;
		double min = 0;
		
		xShiftInput = 0;
		yShiftInput = pixelBuffer;
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			xShiftInput = (pixelBuffer * (-1));
			for(int j = 0; j<bufferSize; j++)
			{
				if(i == (bufferSize-1) & j == 0)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
				}
				else if( buffervalues[i][j] > max)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
				}
				else
				{
					// DO NOTHING
				}
				
				if(i == (bufferSize-1) & j == 0)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
				}
				else if( buffervalues[i][j] < min)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
				}
				else
				{
					// DO NOTHING
				}
				xShiftInput += 1;
				if(xShiftInput > -0.000001 & xShiftInput < 0.000001)
				{
					xShiftInput = 0;
				}
			}
			yShiftInput -= 1;
			if(yShiftInput > -0.000001 & yShiftInput < 0.000001)
			{
				yShiftInput = 0;
			}
		}
		/****************************************************************/
		
		/*************** Print value and transformation ***************/
		if(findMax)
		{
			std::cout << "Max = " 
			<< max 
			<< " Meaning a shift in pixels of x: "
			<< xShiftMax 
			<< " and y: " 
			<< yShiftMax 
			<< std::endl;
		}
		else
		{
			std::cout << "Min = " 
			<< min 
			<< " Meaning a shift in pixels of x: "
			<< xShiftMin 
			<< " and y: " 
			<< yShiftMin 
			<< std::endl;
		}
		/****************************************************************/
		
		/****************** Create Transform ***********************/
		if(findMax)
		{
			transform.shiftX = xShiftMax;
			transform.shiftY = yShiftMax;
		}
		else
		{
			transform.shiftX = xShiftMin;
			transform.shiftY = yShiftMin;
		}
		/****************************************************************/
		
		/****************** SubPixel calculation ***********************/
		
		/********************* Calculate measure values for the Buffer ************************/
		bufferSize = (mathUtils->roundUp(1/tileMovement)*2) + 1;
		
		xShiftInput = 0;
		yShiftInput = transform.shiftY + 1;
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			xShiftInput = transform.shiftX - 1;
			
			for(int j = 0; j < bufferSize; j++)
			{
				//std::cout << "\nxShiftInput: " << xShiftInput 
				//<< " yShiftInput: " << yShiftInput << std::endl;
				//std::cout << std::endl;
				buffervalues[i][j] = this->calcMeasureImagesTilePixelShift(ref, 
																		   floating, 
																		   xShiftInput, 
																		   yShiftInput, 
																		   bins, 
																		   refBand, 
																		   floatBand, 
																		   tile,
																		   measure);
				
				//std::cout << " bufferValue = " << buffervalues[i][j] << std::endl;
				xShiftInput += tileMovement;
				if(xShiftInput > -0.000001 & xShiftInput < 0.000001)
				{
					xShiftInput = 0;
				}
			}
			yShiftInput -= tileMovement;
			if(yShiftInput > -0.000001 & yShiftInput < 0.000001)
			{
				yShiftInput = 0;
			}
		}
		/**********************************************************************************/
		
		
		/*********** TEST: Print out MI Buffer *************************/
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			for(int j=0; j < bufferSize; j++)
			{
				std::cout << buffervalues[i][j] << ", ";
			}
			std::cout << std::endl;
		}
		/***************************************************************/
		
		/******************** Find MAX and MIN in Buffer ************************/
		max = 0;
		min = 0;
		
		xShiftInput = 0;
		yShiftInput = transform.shiftY + 1;
		
		for(int i = (bufferSize-1); i >= 0; i--)
		{
			xShiftInput = transform.shiftX - 1;
			for(int j = 0; j<bufferSize; j++)
			{
				if(i == (bufferSize-1) & j == 0)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
				}
				else if( buffervalues[i][j] > max)
				{
					max = buffervalues[i][j];
					xShiftMax = xShiftInput;
					yShiftMax = yShiftInput;
				}
				else
				{
					// DO NOTHING
				}
				
				if(i == (bufferSize-1) & j == 0)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
				}
				else if( buffervalues[i][j] < min)
				{
					min = buffervalues[i][j];
					xShiftMin = xShiftInput;
					yShiftMin = yShiftInput;
				}
				else
				{
					// DO NOTHING
				}
				xShiftInput += tileMovement;
				if(xShiftInput > -0.000001 & xShiftInput < 0.000001)
				{
					xShiftInput = 0;
				}
			}
			yShiftInput -= tileMovement;
			if(yShiftInput > -0.000001 & yShiftInput < 0.000001)
			{
				yShiftInput = 0;
			}
		}
		/****************************************************************/
		
		/*************** Print value and transformation ***************/
		std::cout << "Subpixel shift:" << std::endl;
		if(findMax)
		{
			std::cout << "Max = " 
			<< max 
			<< " Meaning a shift in pixels of x: "
			<< xShiftMax 
			<< " and y: " 
			<< yShiftMax 
			<< std::endl;
		}
		else
		{
			std::cout << "Min = " 
			<< min 
			<< " Meaning a shift in pixels of x: "
			<< xShiftMin 
			<< " and y: " 
			<< yShiftMin 
			<< std::endl;
		}
		/****************************************************************/
		
		/****************** Create Transform ***********************/
		if(findMax)
		{
			transform.shiftX = xShiftMax;
			transform.shiftY = yShiftMax;
		}
		else
		{
			transform.shiftX = xShiftMin;
			transform.shiftY = yShiftMin;
		}
		/****************************************************************/		
		
		/***************************************************************/
		
	}
	catch(ImageRegistrationException e)
	{
		if( vecImageMeasures != NULL )
		{
			delete vecImageMeasures;
		}
		if(buffervalues != NULL)
		{
			for(int i = 0; i < bufferSize; i++)
			{
				delete [] buffervalues[i];
			}
			delete [] buffervalues;
		}
		throw e;
	}
	
	if( vecImageMeasures != NULL )
	{
		delete vecImageMeasures;
	}
	if(buffervalues != NULL)
	{
		for(int i = 0; i < bufferSize; i++)
		{
			delete [] buffervalues[i];
		}
		delete [] buffervalues;
	}
	//std::exit(0);
	/************** Create Transform Struct and return *************/
	
	return transform;
	/****************************************************************/
}


Transform RegisterImages::registerTileSubPixelSurfaceWalking(GDALDataset *ref, 
															 GDALDataset *floating, 
															 int bins, 
															 int refBand, 
															 int floatBand,
															 TileCoords *tile,
															 double tileMovement,
															 int measure)
throw(ImageRegistrationException)
{
	SurfacePosition *currentMeasure = NULL;
	currentMeasure = new SurfacePosition;
	
	SurfacePosition *prevMeasure = NULL;
	prevMeasure = new SurfacePosition;
	
	VectorImageMeasures *vecImageMeasures;
	vecImageMeasures = new VectorImageMeasures;
	
	SurfacePosition *surroundingMeasures = NULL;
	surroundingMeasures = new SurfacePosition[9];
	
	bool findMax = true;
	
	if(measure == image_measures::mi)
	{
		findMax = true;
	}
	else if(measure == image_measures::euclidean)
	{
		findMax = false;
	}
	else if(measure == image_measures::manhattan)
	{
		findMax = false;
	}
	
	//std::cout << "Entered Buffer search subpixel pixelBuffer: " << pixelBuffer << std::endl;
	try
	{
		
		/************************* Search Surface **************************/
		// Starting Point (in the middle)
		currentMeasure->measure = this->calcMeasureImagesTilePixelShift(ref, 
																		floating, 
																		currentMeasure->xShift, 
																		currentMeasure->yShift, 
																		bins, 
																		refBand, 
																		floatBand, 
																		tile,
																		measure);
		
		double measureValue = 0;
		bool continueLoop = true;
		while(continueLoop)
		{
			prevMeasure->xShift = currentMeasure->xShift;
			prevMeasure->yShift = currentMeasure->yShift;
			prevMeasure->measure = currentMeasure->measure;
		
			// Calculate measures for the surrounding pixels
			surroundingMeasures[0].xShift = currentMeasure->xShift - tileMovement;
			surroundingMeasures[0].yShift = currentMeasure->yShift - tileMovement;
			surroundingMeasures[1].xShift = currentMeasure->xShift;
			surroundingMeasures[1].yShift = currentMeasure->yShift - tileMovement;
			surroundingMeasures[2].xShift = currentMeasure->xShift + tileMovement;
			surroundingMeasures[2].yShift = currentMeasure->yShift - tileMovement;
		
			surroundingMeasures[3].xShift = currentMeasure->xShift - tileMovement;
			surroundingMeasures[3].yShift = currentMeasure->yShift;
			// There is no centre position as this has already been calculated.
			surroundingMeasures[4].xShift = currentMeasure->xShift + tileMovement;
			surroundingMeasures[4].yShift = currentMeasure->yShift;
		
			surroundingMeasures[5].xShift = currentMeasure->xShift - tileMovement;
			surroundingMeasures[5].yShift = currentMeasure->yShift + tileMovement;
			surroundingMeasures[6].xShift = currentMeasure->xShift;
			surroundingMeasures[6].yShift = currentMeasure->yShift + tileMovement;
			surroundingMeasures[7].xShift = currentMeasure->xShift + tileMovement;
			surroundingMeasures[7].yShift = currentMeasure->yShift + tileMovement;
		
		
		
			for(int i = 0; i < 8; i++)
			{
				measureValue = this->calcMeasureImagesTilePixelShift(ref, 
																floating, 
																surroundingMeasures[i].xShift, 
																surroundingMeasures[i].yShift, 
																bins, 
																refBand, 
																floatBand, 
																tile,
																measure);
				
				surroundingMeasures[i].measure = measureValue;
				
				if(findMax)
				{
					if(measureValue > currentMeasure->measure)
					{
						currentMeasure->measure = measureValue;
						currentMeasure->xShift = surroundingMeasures[i].xShift;
						currentMeasure->yShift = surroundingMeasures[i].yShift;
					}
				}
				else
				{
					if(measureValue < currentMeasure->measure)
					{
						currentMeasure->measure = measureValue;
						currentMeasure->xShift = surroundingMeasures[i].xShift;
						currentMeasure->yShift = surroundingMeasures[i].yShift;
					}
				}
			}
			if(currentMeasure->measure == prevMeasure->measure &
			   currentMeasure->xShift == prevMeasure->xShift &
			   currentMeasure->yShift == prevMeasure->yShift)
			{
				continueLoop = false;
			}
		}
		/****************************************************************/
		if(currentMeasure->xShift < 0.00000001 & currentMeasure->xShift > -0.00000001)
		{
			currentMeasure->xShift = 0;
		}
		if(currentMeasure->yShift < 0.00000001 & currentMeasure->yShift > -0.00000001)
		{
			currentMeasure->yShift = 0;
		}
		/*************** Print value and transformation ***************/
			std::cout << "Measure = " 
			<< currentMeasure->measure 
			<< " Meaning a shift in pixels of x: "
			<< currentMeasure->xShift 
			<< " and y: " 
			<< currentMeasure->yShift 
			<< std::endl;
		/****************************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( vecImageMeasures != NULL )
		{
			delete vecImageMeasures;
		}
		throw e;
	}
	
	/************** Create Transform Struct and return *************/
	Transform transform;
	transform.shiftX = currentMeasure->xShift;
	transform.shiftY = currentMeasure->yShift;
	/****************************************************************/
	
	if( vecImageMeasures != NULL )
	{
		delete vecImageMeasures;
	}
	if( currentMeasure != NULL )
	{
		delete currentMeasure;
	}
	if( prevMeasure != NULL )
	{
		delete prevMeasure;
	}
	if( surroundingMeasures != NULL )
	{
		delete surroundingMeasures;
	}

	return transform;
	
}

double RegisterImages::calcMeasureImagesTilePixelShift(GDALDataset *ref, 
													   GDALDataset *floating, 
													   double xShift, 
													   double yShift, 
													   int bins, 
													   int refBand, 
													   int floatBand,
													   TileCoords *tile,
													   int measure)
throw(ImageRegistrationException)
{
	double returnValue = 0;
	
	//std::cout << "Calculating Image Measures: \n";
	
	if(measure == image_measures::mi)
	{
		//std::cout << "Measure = MI\n";
		
		ImageOverlap *imageOverlap = NULL;
		JointHistogram *jointHistogram = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, floating, xShift, yShift, tile);
		/***************************************************************************/
		//std::cout << "Generating Joint Histogram! \n";
		/******************* Generate Joint Histogram ***************************/
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		/************************************************************************/
		
		/************************** Calculate MI *******************************/
		if(successJH)
		{
			//std::cout << "Created Histogram now calculating MI\n";
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcMutualInformation(*jointHistogram);
			//std::cout << "Calculated MI\n";
		}
		else
		{
			returnValue = -999;
		}
		/************************************************************************/
		
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		if( jhIM != NULL )
		{
			delete jhIM;
		}
	}
	else if(measure == image_measures::euclidean)
	{
		ImageOverlap *imageOverlap = NULL;
		VectorImageMeasures *vecImageMeasures = new VectorImageMeasures;
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		returnValue = vecImageMeasures->calcEuclideanDistance(ref, 
															  floating, 
															  refBand, 
															  floatBand, 
															  imageOverlap,
															  xShift,
															  yShift);
		if( vecImageMeasures != NULL)
		{
			delete vecImageMeasures;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
	}
    else if(measure == image_measures::manhattan)
    {
		ImageOverlap *imageOverlap = NULL;
		VectorImageMeasures *vecImageMeasures = new VectorImageMeasures;
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		returnValue = vecImageMeasures->calcManhattanDistance(ref, 
															  floating, 
															  refBand, 
															  floatBand, 
															  imageOverlap,
															  xShift,
															  yShift);
		if( vecImageMeasures != NULL)
		{
			delete vecImageMeasures;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
	}
	else if(measure == image_measures::correlationCoefficient)
    {
		ImageOverlap *imageOverlap = NULL;
		CorrelationMeasures *correlationMeasures = new CorrelationMeasures;
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		//imageOverlap->printOverlappingArea(true);
		returnValue = correlationMeasures->calcCorrelationCoefficient(ref, 
																	  floating, 
																	  refBand, 
																	  floatBand, 
																	  imageOverlap);
		
		//std::cout << "Correlation = " << returnValue << " xShift = " << xShift << " yShift = " << yShift << std::endl;
		if( correlationMeasures != NULL)
		{
			delete correlationMeasures;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
	}
	else if(measure == image_measures::clusterReward)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcClusterRewardImageMeasure(*jointHistogram,imageOverlap->getNumPixels());
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::distance2Independence)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcDistance2Independence(*jointHistogram);		
		}
		else
		{
			returnValue = -999;
		}
		
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::kolmogorovDistance)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcKolmogorovDistance(*jointHistogram);	
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::kullbachDivergence)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcKullbachDivergence(*jointHistogram);	
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::hellingerDistance)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcHellingerDistance(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::toussaintsDistance)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcToussaintsDistance(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::linKDivergence)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcLinKDivergence(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	if(measure == image_measures::norm_mi_ecc)
	{
		ImageOverlap *imageOverlap = NULL;
		JointHistogram *jointHistogram = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, floating, xShift, yShift, tile);
		/***************************************************************************/
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcMutualInformationECC(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		if( jhIM != NULL )
		{
			delete jhIM;
		}
	}
	if(measure == image_measures::norm_mi_y)
	{
		ImageOverlap *imageOverlap = NULL;
		JointHistogram *jointHistogram = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, floating, xShift, yShift, tile);
		/***************************************************************************/
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateJointHistogram(ref, floating, refBand, floatBand, imageOverlap);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcMutualInformationY(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		if( jhIM != NULL )
		{
			delete jhIM;
		}
	}
	
	return returnValue;
}


double RegisterImages::calcMeasureImagesTilePixelSubShift(GDALDataset *ref, 
													   GDALDataset *floating, 
													   double xShift, 
													   double yShift, 
													   int bins, 
													   int refBand, 
													   int floatBand,
													   TileCoords *tile,
														  int measure)
throw(ImageRegistrationException)
{
	double returnValue = 0;
	
	if(measure == image_measures::mi)
	{
		ImageOverlap *imageOverlap = NULL;
		JointHistogram *jointHistogram = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, floating, xShift, yShift, tile);
		/***************************************************************************/
		
		/******************* Generate Joint Histogram ***************************/
		jointHistogram = new JointHistogram(bins);
		
		bool successJH = jointHistogram->generateSubPixelJointHistogramWithInterp(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		//bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		/************************************************************************/
		
		/************************** Calculate MI *******************************/
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcMutualInformation(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		/************************************************************************/
		
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		if( jhIM != NULL )
		{
			delete jhIM;
		}
	}
	else if(measure == image_measures::euclidean)
	{
		ImageOverlap *imageOverlap = NULL;
		VectorImageMeasures *vecImageMeasures = new VectorImageMeasures;
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		returnValue = vecImageMeasures->calcEuclideanDistanceCubicInterpolation(ref, 
															  floating, 
															  refBand, 
															  floatBand, 
															  imageOverlap,
															  xShift,
															  yShift);
		if( vecImageMeasures != NULL)
		{
			delete vecImageMeasures;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
	}
    else if(measure == image_measures::manhattan)
    {
		ImageOverlap *imageOverlap = NULL;
		VectorImageMeasures *vecImageMeasures = new VectorImageMeasures;
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		returnValue = vecImageMeasures->calcManhattanDistance(ref, 
															  floating, 
															  refBand, 
															  floatBand, 
															  imageOverlap,
															  xShift,
															  yShift);
		if( vecImageMeasures != NULL)
		{
			delete vecImageMeasures;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
	}
	else if(measure == image_measures::correlationCoefficient)
    {
		ImageOverlap *imageOverlap = NULL;
		CorrelationMeasures *correlationMeasures = new CorrelationMeasures;
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		returnValue = correlationMeasures->calcCorrelationCoefficient(ref, 
																	  floating, 
																	  refBand, 
																	  floatBand, 
																	  imageOverlap,
																	  xShift, 
																	  yShift);
		
		//std::cout << "Correlation = " << returnValue << " xShift = " << xShift << " yShift = " << yShift << std::endl;
		if( correlationMeasures != NULL)
		{
			delete correlationMeasures;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
	}
	else if(measure == image_measures::clusterReward)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);

		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcClusterRewardImageMeasure(*jointHistogram,imageOverlap->getNumPixels());
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::distance2Independence)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcDistance2Independence(*jointHistogram);		
		}
		else
		{
			returnValue = -999;
		}
		
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::kolmogorovDistance)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcKolmogorovDistance(*jointHistogram);	
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::kullbachDivergence)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcKullbachDivergence(*jointHistogram);	
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::hellingerDistance)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcHellingerDistance(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::toussaintsDistance)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcToussaintsDistance(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	else if(measure == image_measures::linKDivergence)
    {
		ImageOverlap *imageOverlap = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		JointHistogram *jointHistogram = NULL;
		
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcLinKDivergence(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( jhIM != NULL)
		{
			delete jhIM;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
	}
	if(measure == image_measures::norm_mi_ecc)
	{
		ImageOverlap *imageOverlap = NULL;
		JointHistogram *jointHistogram = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, floating, xShift, yShift, tile);
		/***************************************************************************/
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcMutualInformationECC(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
		
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		if( jhIM != NULL )
		{
			delete jhIM;
		}
	}
	if(measure == image_measures::norm_mi_y)
	{
		ImageOverlap *imageOverlap = NULL;
		JointHistogram *jointHistogram = NULL;
		JointHistogramImageMeasures *jhIM = NULL;
		
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, floating, xShift, yShift, tile);
		/***************************************************************************/
		
		jointHistogram = new JointHistogram(bins);
		bool successJH = jointHistogram->generateSubPixelJointHistogram(ref, floating, refBand, floatBand, imageOverlap,xShift, yShift);
		
		if(successJH)
		{
			jhIM = new JointHistogramImageMeasures;
			returnValue = jhIM->calcMutualInformationY(*jointHistogram);
		}
		else
		{
			returnValue = -999;
		}
			
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		if( jhIM != NULL )
		{
			delete jhIM;
		}
	}
	
	return returnValue;
}

double RegisterImages::calcMIImagesTileSubPixelShift(GDALDataset *ref, 
													 GDALDataset *floating, 
													 double xShift, 
													 double yShift, 
													 int bins, 
													 int refBand, 
													 int floatBand,
													 TileCoords *tile)
throw(ImageRegistrationException)
{
	double mi_value = 0;
	ImageOverlap *imageOverlap = NULL;
	JointHistogram *jointHistogram = NULL;
	//JointHistogram *jointHistogram2 = NULL;
	MutualInformation *mi = NULL;
	
	try
	{
		/*************** TEST: Print out tile details **********************
		std::cout << "xShift: " << xShift << " yShift: " << yShift << " \n";
		std::cout << " Image A: ";
		std::cout << "[" << tile->imgATLX << ", " << tile->imgATLY << "] [" 
		<< tile->imgABRX << ", " << tile->imgABRY << "]\n";
		std::cout << " Image B: ";
		std::cout << "[" << tile->imgBTLX << ", " << tile->imgBTLY << "] [" 
		<< tile->imgBBRX << ", " << tile->imgBBRY << "]\n";
		std::cout << " Geo Coords: ";
		std::cout << "[" << tile->eastingTL << ", " << tile->northingTL << "] [" 
		<< tile->eastingBR << ", " << tile->northingBR << "]\n";
		/***************************************************************************/
		
		/**** Find Overlapping area (xShift might take tile outside image area) *****/
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithinTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		/***************************************************************************/
		
		/******************* Generate Joint Histogram ***************************/
		jointHistogram = new JointHistogram(bins);
				
		jointHistogram->generateSubPixelJointHistogram(ref, 
													   floating, 
													   refBand, 
													   floatBand, 
													   imageOverlap,
													   xShift,
													   yShift);
		
		//jointHistogram2 = new JointHistogram(bins);
		//jointHistogram2->generateSubPixelJointHistogramWithInterp(ref, 
		//											   floating, 
		//											   refBand, 
		//											   floatBand, 
		//											   imageOverlap,
		//											   xShift,
		//											   yShift);
		/************************************************************************/
		
		/************************** Calculate MI *******************************/
		mi = new MutualInformation;
		double mi_value_bilinear = mi->calcMutualInformation(*jointHistogram);
		//double mi_value_pvi = mi->calcMutualInformation(*jointHistogram2);
		
		//mi_value = mi_value_pvi + (mi_value_bilinear - mi_value_pvi)/2;
		mi_value = mi_value_bilinear;
		/************************************************************************/
	}
	catch(ImageRegistrationException e)
	{
		if( mi != NULL)
		{
			delete mi;
		}
		if( imageOverlap != NULL )
		{
			delete imageOverlap;
		}
		if( jointHistogram != NULL )
		{
			delete jointHistogram;
		}
		throw e;
	}
	
	/*********************** Free Memory ************************************/
	if( mi != NULL)
	{
		delete mi;
	}
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	if( jointHistogram != NULL )
	{
		delete jointHistogram;
	}
	/************************************************************************/
	return mi_value;
}

double RegisterImages::calcMeasureDiffResolutionImagesTilePixelShift(GDALDataset *ref, 
																	  GDALDataset *floating, 
																	  double xShift, 
																	  double yShift, 
																	  int bins, 
																	  int refBand, 
																	  int floatBand,
																	  TileCoords *tile,
																	  int measure,
																	  VectorImageMeasures *vecImageMeasures)
throw(ImageRegistrationException)
{
	double returnValue = 0;
	ImageOverlap *imageOverlap = NULL;
	if(measure == image_measures::mi)
	{
		returnValue = calcMIImagesTileSubPixelShift(ref, 
													floating, 
													xShift, 
													yShift, 
													bins, 
													refBand, 
													floatBand, 
													tile);
	}
	else if(measure == image_measures::euclidean)
	{
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithDiffResolutionsTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		
		returnValue = vecImageMeasures->calcEuclideanDistance(ref, 
															  floating, 
															  refBand, 
															  floatBand, 
															  imageOverlap,
															  xShift,
															  yShift);
	}
    else if(measure == image_measures::manhattan)
    {
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithDiffResolutionsTileWithFloatShift(ref, 
																  floating, 
																  xShift, 
																  yShift, 
																  tile);
		returnValue = vecImageMeasures->calcManhattanDistance(ref, 
															  floating, 
															  refBand, 
															  floatBand, 
															  imageOverlap,
															  xShift,
															  yShift);
	}
	else if(measure == image_measures::correlationCoefficient)
    {
		CorrelationMeasures correlationMeasures;
		imageOverlap = new ImageOverlap;
		imageOverlap->calcOverlappingAreaWithDiffResolutionsTileWithFloatShift(ref, 
																			   floating, 
																			   xShift, 
																			   yShift, 
																			   tile);
		returnValue = correlationMeasures.calcDiffResolutionCorrelationCoefficient(ref, 
																					floating, 
																					refBand, 
																					floatBand, 
																					imageOverlap);
	}
	
	if( imageOverlap != NULL )
	{
		delete imageOverlap;
	}
	
	return returnValue;
}

Transform RegisterImages::findExtremaInSurfaceSimulatedAnnealing(GDALDataset *ref, 
																 GDALDataset *floating, 
																 int pixelBuffer,
																 int refBand, 
																 int floatBand,
																 TileCoords *tile,
																 int measure,
																 int startX,
																 int startY,
																 int bins, 
																 bool max,
																 int tmax,
																 int tdecrease,
																 int successful,
																 int unsuccessful)
throw(ImageRegistrationException)
{	
	MathUtils mathUtils;
	TransformsTable *table = new TransformsTable(300);
	const int tMAX = tmax;
	int t = tMAX;
	int successfulMoves = 0;
	int unsuccessfulMoves = 0;
	
	Transform current;
	//Transform previous;
	Transform next;
	current.shiftX = startX;
	current.shiftY = startY;
	current.measureValue = this->calcMeasureImagesTilePixelShift(ref, 
																 floating, 
																 startX, 
																 startY, 
																 bins, 
																 refBand, 
																 floatBand, 
																 tile,
																 measure);
	table->insert(&current,false);
	double p = 0;
	int numMoves = 0;
	int rangeUpper = 0;
	int rangeLower = 0;
	bool findNextMove = true;
	while(t >= 0)
	{
		successfulMoves = 0;
		unsuccessfulMoves = 0;
		while(successfulMoves < successful & unsuccessfulMoves < unsuccessful)
		{
			// Find next move randomly
			findNextMove = true;
			numMoves = 0;
			while(findNextMove)
			{
				rangeLower = mathUtils.round(current.shiftX-1);
				rangeUpper = mathUtils.round(current.shiftX+1);
				
				next.shiftX = mathUtils.randomWithinRange(rangeLower,rangeUpper);
				rangeLower = mathUtils.round(current.shiftY-1);
				rangeUpper = mathUtils.round(current.shiftY+1);
				
				next.shiftY = mathUtils.randomWithinRange(rangeLower,rangeUpper);
				numMoves++;
				if(!table->search(&next))
				{
					findNextMove = false;
				}
				else
				{
					findNextMove = true;
				}
				if(current.shiftX >= pixelBuffer |
				   current.shiftX <= (pixelBuffer*-1) |
				   current.shiftY >= pixelBuffer |
				   current.shiftY <= (pixelBuffer * -1))
				{
					findNextMove = true;
				}
		
				if(numMoves == 8)
				{
					while(findNextMove)
					{
						rangeLower = mathUtils.round(pixelBuffer*(-1));
						rangeUpper = mathUtils.round(pixelBuffer);
						next.shiftX = mathUtils.randomWithinRange(rangeLower,rangeUpper);
						next.shiftY = mathUtils.randomWithinRange(rangeLower,rangeUpper);

						if(!table->search(&next))
						{
							findNextMove = false;
						}
						else
						{
							//Next contained within the table
						}
					}
				}
			}
			// Find image measure value for next location
			next.measureValue = this->calcMeasureImagesTilePixelShift(ref, 
																	  floating, 
																	  next.shiftX, 
																	  next.shiftY, 
																	  bins, 
																	  refBand, 
																	  floatBand, 
																	  tile,
																	  measure);
			
			// If next image measure > current image measure
			if(next.measureValue > current.measureValue)
			{
				current.shiftX = next.shiftX;
				current.shiftY = next.shiftY;
				current.measureValue = next.measureValue;
				table->insert(&current,false);
				successfulMoves++;
			}
			else
			{
				p = (((1/((next.measureValue - current.measureValue)*(-1))) * t)/tMAX);
				
				if(p > 5)
				{
					current.shiftX = next.shiftX;
					current.shiftY = next.shiftY;
					current.measureValue = next.measureValue;
					table->insert(&current,false);
					successfulMoves++;
				}
				else
				{
					table->insert(&next, false);
					unsuccessfulMoves++;
				}
			}
		}
		
		t = t - tdecrease;
	}
	
	current = table->findMaxMinMeasure(true);
	
	// Identify subpixel component.
	int onEdge[9];
	double measures[9];
	int counter = 0;
	int x = mathUtils.round(current.shiftX);
	int y = mathUtils.round(current.shiftY);
	int xMove = -1;
	int yMove = -1;
	for(int i = 0; i < 3; i++)
	{
		for(int j = 0; j < 3; j++)
		{
			measures[counter] = this->calcMeasureImagesTilePixelShift(ref, 
																 floating, 
																 (x+xMove), 
																 (y+yMove), 
																 bins, 
																 refBand, 
																 floatBand, 
																 tile,
																 measure);
			onEdge[counter] = 0;
			xMove++;
			counter++;
		}
		xMove = -1;
		yMove++;
	}
	
	Interpolation interpolation;
	Transform subPixelTransform = 
		interpolation.calcateSubPixelTranformationXYCurve(&measures[0], 
														  &onEdge[0], 
														  0.1, 
														  max);
	
	current.shiftX = current.shiftX + subPixelTransform.shiftX;
	current.shiftY = current.shiftY + subPixelTransform.shiftY;
	
	if( table != NULL)
	{
		delete table;
	}
	return current;
}

Transform RegisterImages::findExtremaInSurface(GDALDataset *ref, 
											   GDALDataset *floating, 
											   int pixelBuffer,
											   int refBand, 
											   int floatBand,
											   TileCoords *tile,
											   int measure,
											   int startX,
											   int startY,
											   int bins, 
											   bool max)
throw(ImageRegistrationException)
{
	Transform current;
	double currentValue = 0;
	double pixels[3][3];
	double previous_pixels[3][3];
	double x = 0;
	double y = 0;
	current.shiftX = startX;
	current.shiftY = startY;
	int xMove = -1;
	int yMove = -1;
	
	do
	{
		x = current.shiftX;
		y = current.shiftY;
		xMove = -1;
		yMove = -1;
		for(int i = 0; i < 3; i++)
		{
			for(int j = 0; j < 3; j++)
			{
				//std::cout << "xMove = " << xMove << " x+xMove " << x+xMove << std::endl;
				//std::cout << "yMove = " << yMove << " y+yMove " << y+yMove << std::endl;
				pixels[i][j] = this->calcMeasureImagesTilePixelShift(ref, 
																	 floating, 
																	 (x+xMove), 
																	 (y+yMove), 
																	 bins, 
																	 refBand, 
																	 floatBand, 
																	 tile,
																	 measure);
				xMove++;
			}
			xMove = -1;
			yMove++;
		}
		
		xMove = -1;
		yMove = -1;
		for(int i = 0; i < 3; i++)
		{
			for(int j = 0; j < 3; j++)
			{
				if(i == 0 & j == 0)
				{
					currentValue = pixels[i][j];
					current.shiftX = x+xMove;
					current.shiftY = y+yMove;
					current.measureValue = pixels[i][j];
				}
				
				if(max)
				{
					if(pixels[i][j] > currentValue)
					{
						currentValue = pixels[i][j];
						current.shiftX = x+xMove;
						current.shiftY = y+yMove;
						current.measureValue = pixels[i][j];
					}
				}
				else
				{
					if(pixels[i][j] < currentValue)
					{
						currentValue = pixels[i][j];
						current.shiftX = x+xMove;
						current.shiftY = y+yMove;
						current.measureValue = pixels[i][j];
					}
				}
			/*	std::cout << "currentValue = " << currentValue 
				<< " Shift = [" <<current.shiftX << ", " << current.shiftY << "]\n";
				std::cout << "pixels[i][j] = " << pixels[i][j] << " Shift = [" << x+xMove
				<< ", " << y+yMove << "]\n";*/
				xMove++;
			}
			xMove = -1;
			yMove++;
		} 
		if(current.shiftX >= pixelBuffer |
		   current.shiftX <= (pixelBuffer*-1) |
		   current.shiftY >= pixelBuffer |
		   current.shiftY <= (pixelBuffer * -1))
		{
			//std::cout << "breaking out of loop as reached the buffer!\n";
			break;
		}
		//std::cout << "current shift = [" << current.shiftX << ", " << 
		//	current.shiftY << "]\n";
		//std::cout << "x and y = [" << x << ", " << y << "]\n";
		for(int i = 0; i < 3; i++)
		{
			for(int j = 0; j < 3; j++)
			{
				previous_pixels[i][j] = pixels[i][j];
			}
		}
		
	}while(x != current.shiftX & y != current.shiftY);
	
	// Identify subpixel component.
	int onEdge[9];
	double measures[9];
	int counter = 0;
	for(int i = 0; i < 3; i++)
	{
		for(int j=0; j<3;j++)
		{
			measures[counter]  = pixels[i][j];
			onEdge[counter] = 0;
			counter++;
		}
	}
	
	//std::cout << measures[0] << ", " << measures[1] << ", " << measures[2] << "\n";  
	//std::cout << measures[3] << ", " << measures[4] << ", " << measures[5] << "\n";  
	//std::cout << measures[6] << ", " << measures[7] << ", " << measures[8] << "\n";  
	
	Interpolation interpolation;
	Transform subPixelTransform = 
		interpolation.calcateSubPixelTranformationXYCurve(&measures[0], 
														  &onEdge[0], 
														  0.1, 
														  max);
	current.shiftX = current.shiftX + subPixelTransform.shiftX;
	current.shiftY = current.shiftY + subPixelTransform.shiftY;

	return current;
}

Transform RegisterImages::findTileTransformation(GDALDataset *ref, 
												 GDALDataset *floating, 
												 int pixelBuffer,
												 int refBand, 
												 int floatBand,
												 TileCoords *tile,
												 int measure,
												 int bins,
												 int search,
												 int numWalks,
												 int tmax,
												 int tdecrease,
												 int successful,
												 int unsuccessful,
												 float measureThreshold,
												 int possStartX,
												 int possStartY,
												 bool randomStart)
throw(ImageRegistrationException)
{	
	MathUtils mathUtils;
	Transform result;
	result.shiftX = 0;
	result.shiftY = 0;
	result.measureValue = 0;
	int numberIterations = numWalks;
	Transform *transformations = new Transform[numberIterations];
	bool max = true;
	if(measure == image_measures::mi)
	{
		max = true;
	}
	else if(measure == image_measures::euclidean)
	{
		max = false;
	}
	else if(measure == image_measures::manhattan)
	{
		max = false;
	}
	else if(measure == image_measures::correlationCoefficient)
	{
		max = true;
	}
	else if(measure == image_measures::clusterReward)
	{
		max = true;
	}
	else if(measure == image_measures::distance2Independence)
	{
		max = true;
	}
	else if(measure == image_measures::kolmogorovDistance)
	{
		max = true;
	}
	else if(measure == image_measures::kullbachDivergence)
	{
		max = true;
	}
	else if(measure == image_measures::hellingerDistance)
	{
		max = true;
	}
	else if(measure == image_measures::toussaintsDistance)
	{
		max = true;
	}
	else if(measure == image_measures::linKDivergence)
	{
		max = true;
	}
	else if(measure == image_measures::norm_mi_ecc)
	{
		max = true;
	}
	else if(measure == image_measures::norm_mi_y)
	{
		max = true;
	}
	int startX = 0;
	int startY = 0;
	
	if(search == image_search::simulated_annealing)
	{
		if(randomStart)
		{
			startX = (mathUtils.randomWithinRange(0, (pixelBuffer*2))) - pixelBuffer;
			startY = (mathUtils.randomWithinRange(0, (pixelBuffer*2))) - pixelBuffer;
		}
		else
		{
			startX = possStartX;
			startY = possStartY;
		}
		
	//	std::cout << "Start Point [" << startX << ", " << startY << "]\n";
		result = this->findExtremaInSurfaceSimulatedAnnealing(ref,
															  floating,
															  pixelBuffer,
															  refBand,
															  floatBand,
															  tile,
															  measure,
															  startX,
															  startY,
															  bins,
															  max,
															  tmax,
															  tdecrease,
															  successful,
															  unsuccessful);
	}
	else if( search == image_search::hill_climbing)
	{
		for(int i = 0; i < numberIterations; i++)
		{
			if(randomStart)
			{
				startX = (mathUtils.randomWithinRange(0, (pixelBuffer*2))) - pixelBuffer;
				startY = (mathUtils.randomWithinRange(0, (pixelBuffer*2))) - pixelBuffer;
			}
			else
			{
				startX = possStartX;
				startY = possStartY;
			}
			
		//	std::cout << "Start Point [" << startX << ", " << startY << "]\n";
			transformations[i] = this->findExtremaInSurface(ref,
															floating,
															pixelBuffer,
															refBand,
															floatBand,
															tile,
															measure,
															startX,
															startY,
															bins,
															max);
		}
		
		// Select one with the highest/lowest measure.
		result.shiftX = transformations[0].shiftX;
		result.shiftY = transformations[0].shiftY;
		result.measureValue = transformations[0].measureValue;
		for(int i = 0; i < numberIterations; i++)
		{
			if(max)
			{
				if(result.measureValue < transformations[i].measureValue)
				{
					result.shiftX = transformations[i].shiftX;
					result.shiftY = transformations[i].shiftY;
					result.measureValue = transformations[i].measureValue;
				}
			}
			else
			{
				if(result.measureValue > transformations[i].measureValue)
				{
					result.shiftX = transformations[i].shiftX;
					result.shiftY = transformations[i].shiftY;
					result.measureValue = transformations[i].measureValue;
				}
			}
		}
	}
	else if(search == image_search::exhaustive)
	{
		result = registerTilePixel_EstimateSubPixelSearchBuffer(ref, 
																floating, 
																pixelBuffer, 
																bins, 
																refBand, 
																floatBand, 
																tile,
																1,
																measure);
	}
	
	//std::cout << "RESULT [" << result.shiftX << "," << result.shiftY << "] " << result.measureValue << std::endl;
	//exit(-1);
	if(transformations != NULL)
	{
		delete [] transformations;
	}
	
	return result;
}

void RegisterImages::correctErrors(NonusTreeNode *parent,
								   GDALDataset *ref, 
								   GDALDataset *floating,
								   int pixelBuffer, 
								   int bins, 
								   int refBand, 
								   int floatBand,
								   int measure,
								   int errorThreshold)
throw(ImageRegistrationException)
{
	MathUtils mathUtils;
	/********* TEST: Print parent and children for processing ***********/
	std::cout << "\n\t\t[" << parent->TileTransformation->shiftX 
		<< "," << parent->TileTransformation->shiftY << "]\n";
	for(int i = 0; i < 9; i++)
	{
		std::cout << "[" << parent->children[i]->TileTransformation->shiftX << "," 
		<< parent->children[i]->TileTransformation->shiftY << "]";
		if(i == 2 | i == 5)
		{
			std::cout << std::endl;
		}
	}
	std::cout << std::endl;	
	/*********************************************************************/
	
	/**************** Calculate Average Shift ************************/
	double xAverage = 0;
	double yAverage = 0;
	int counter = 0;
	for(int i = 0; i < 9; i++)
	{
		if(parent->children[i]->TileTransformation->measureValue > 0)
		{
			xAverage += parent->children[i]->TileTransformation->shiftX;
			yAverage += parent->children[i]->TileTransformation->shiftY;
			counter++;
		}
	}
	
	xAverage = xAverage/counter;
	yAverage = yAverage/counter;
	
	std::cout << "xAverage = " << xAverage << std::endl;
	std::cout << "yAverage = " << yAverage << std::endl;
	/********************************************************************/
	
	/*************** Assign new transformation to the tile ***************/
	bool max = true;
	if(measure == image_measures::mi)
	{
		max = true;
	}
	else if(measure == image_measures::euclidean)
	{
		max = false;
	}
	else if(measure == image_measures::manhattan)
	{
		max = false;
	}
	if(measure == image_measures::correlationCoefficient)
	{
		max = true;
	}
	double xShift = 0;
	double yShift = 0;
	for(int i = 0; i < 9; i++)
	{
		xShift = parent->children[i]->TileTransformation->shiftX;
		yShift = parent->children[i]->TileTransformation->shiftY;
		Transform transform;
		if((mathUtils.absoluteValue(xShift - xAverage) > errorThreshold) | 
		   (mathUtils.absoluteValue(yShift - yAverage) > errorThreshold))
		{
			std::cout << "Changed [" << xShift << "," << xShift << "]";
			//Recalculate Shift!!!!
			transform = this->findExtremaInSurface(ref,
												   floating,
												   pixelBuffer/4,
												   refBand,
												   floatBand,
												   parent->children[i]->tileCoords,
												   measure,
												   mathUtils.round(xAverage),
												   mathUtils.round(yAverage),
												   bins,
												   max);
			parent->children[i]->TileTransformation->shiftX = transform.shiftX;
			parent->children[i]->TileTransformation->shiftY = transform.shiftY;
			parent->children[i]->TileTransformation->measureValue = transform.measureValue;
			std::cout << " to [" << transform.shiftX << "," << transform.shiftY << "]\n";

		}
		else
		{
			// Shift OK!
		}
	}
	/*********************************************************************/
}


double RegisterImages::findWindowMeasureWithOrigin(GDALDataset *ref,
												   GDALDataset *floating,
												   int *origin, 
												   int refband,
												   int floatband,
												   int windowSize, 
												   int measure, 
												   int bins,
												   double xShift,
												   double yShift,
												   ImageOverlap *imgOverlap)
throw(ImageRegistrationException)
{
	MathUtils mathUtils;
	double returnValue = 0;
	TileCoords *tile = new TileCoords;
	
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
	
	// Retrieve overlapping areas
	int *refImagePixels = imgOverlap->getImageAPixelCoords();
	int *floatImagePixels = imgOverlap->getImageBPixelCoords();
	double *geoCoords = imgOverlap->getOverlapGeoCoords();
	double resolution = imgOverlap->getPixelXRes();
	
	// Identify reference image tile
	tile->imgATLX = origin[0] - windowSize;
	tile->imgATLY = origin[1] - windowSize;
	tile->imgABRX = origin[0] + windowSize;
	tile->imgABRY = origin[1] + windowSize;
	
	int diffX = floatImagePixels[0] - refImagePixels[0];
	int diffY = floatImagePixels[1] - refImagePixels[1]; 
	
	//Find position of origin in Floating image
	/*std::cout << "\nResolution: " << resolution << std::endl;
	std::cout << "Reference Origin: [" << origin[0] << "," << origin[1] << "]\n";
	std::cout << "Reference: [" << refImagePixels[0] << "," << refImagePixels[1] << "][" 
		<< refImagePixels[2] << "," << refImagePixels[3] << "]\n";
	std::cout << "Floating: [" << floatImagePixels[0] << "," << floatImagePixels[1] << "][" 
		<< floatImagePixels[2] << "," << floatImagePixels[3] << "]\n";
	std::cout << "diff: [" << diffX << "," << diffY << "]\n";*/
	
	int bX = origin[0] + diffX;
	int bY = origin[1] + diffY;
	
	// Identify floating image tile
	tile->imgBTLX = bX - windowSize;
	tile->imgBTLY = bY - windowSize;
	tile->imgBBRX = bX + windowSize;
	tile->imgBBRY = bY + windowSize;
	
	/*std::cout << "Reference Tile (Before Trim)[" << tile->imgATLX << "," << tile->imgATLY << "][" 
		<< tile->imgABRX << "," << tile->imgABRY << "]\n";
	std::cout << "Floating Tile (Before Trim)[" << tile->imgBTLX << "," << tile->imgBTLY << "][" 
		<< tile->imgBBRX << "," << tile->imgBBRY << "]\n";*/
	
	// check and updating the tile falls within the overlapping image
	int tmpdifferenceA = 0;
	int tmpdifferenceB = 0;
	int windowDimensions[4] = {0};
	
	if(tile->imgATLX < refImagePixels[0] | tile->imgBTLX < floatImagePixels[0])
	{
		//TLX
		tmpdifferenceA = refImagePixels[0] - tile->imgATLX; 
		tmpdifferenceB = floatImagePixels[0] - tile->imgBTLX; 
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[0] = windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[0] = windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[0] = windowSize;
	}
	
	if(tile->imgATLY < refImagePixels[1] | tile->imgBTLY < floatImagePixels[1])
	{
		//TLY
		tmpdifferenceA = refImagePixels[1] - tile->imgATLY;
		tmpdifferenceB = floatImagePixels[1] - tile->imgBTLY;
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[1] = windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[1] = windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[1] = windowSize;
	}
	
	if(tile->imgABRX > refImagePixels[2] | tile->imgBBRX > floatImagePixels[2])
	{
		//BRX
		tmpdifferenceA = tile->imgABRX - refImagePixels[2];
		tmpdifferenceB = tile->imgBBRX - floatImagePixels[2];
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[2] = windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[2] = windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[2] = windowSize;
	}
	
	if(tile->imgABRY > refImagePixels[3] | tile->imgBBRY > floatImagePixels[3])
	{
		//BRY
		tmpdifferenceA = tile->imgABRY - refImagePixels[3]; 
		tmpdifferenceB = tile->imgBBRY - floatImagePixels[3]; 
		
		if(tmpdifferenceA > tmpdifferenceB)
		{
			windowDimensions[3] = windowSize - tmpdifferenceA;
		}
		else
		{
			windowDimensions[3] = windowSize - tmpdifferenceB;
		}
	}
	else
	{
		windowDimensions[3] = windowSize;
	}
	
	//Produce Final Tile
	tile->imgATLX = origin[0] - windowDimensions[0];
	tile->imgATLY = origin[1] - windowDimensions[1];
	tile->imgABRX = origin[0] + windowDimensions[2];
	tile->imgABRY = origin[1] + windowDimensions[3];
	
	tile->imgBTLX = bX - windowDimensions[0];
	tile->imgBTLY = bY - windowDimensions[1];
	tile->imgBBRX = bX + windowDimensions[2];
	tile->imgBBRY = bY + windowDimensions[3];
	
	
	// Get Geographic Coordinates for Tile.
	tile->eastingTL = geoCoords[0] + ((tile->imgATLX - refImagePixels[0])*resolution);
	tile->northingTL = geoCoords[1] + ((tile->imgATLY - refImagePixels[1])*resolution);
	tile->eastingBR = tile->eastingTL + ((tile->imgABRX - tile->imgATLX)*resolution);
	tile->northingBR = tile->northingTL +  ((tile->imgABRY - tile->imgATLY)*resolution);
	
	/*std::cout << "Reference Tile [" << tile->imgATLX << "," << tile->imgATLY << "][" 
		<< tile->imgABRX << "," << tile->imgABRY << "]\n";
	std::cout << "Floating Tile [" << tile->imgBTLX << "," << tile->imgBTLY << "][" 
		<< tile->imgBBRX << "," << tile->imgBBRY << "]\n";
	std::cout << "Geographic Tile [" << tile->eastingTL << "," << tile->northingTL << "][" 
		<< tile->eastingBR << "," << tile->northingBR << "]\n";*/
	
	returnValue = this->calcMeasureImagesTilePixelShift(ref,
														floating,
														xShift,
														yShift,
														bins,
														refband,
														floatband,
														tile,
														measure);
	if(tile != NULL)
	{
		delete tile;
	}
	return returnValue;
}

RegisterImages::~RegisterImages()
{
	
}
