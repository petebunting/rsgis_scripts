/*
 *  ProcessInputParameters.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 23/08/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef ProcessInputParams_H
#define ProcessInputParams_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "ImagesUtil.h"
#include "ImageRegistrationException.h"
using namespace std;

struct RegistrationParams
{
	char* refImage;
	char* floatImage;
	char* tmpPath;
	char* outCtrlPts;
	int refBand;
	int floatBand;
	int distanceMeasure;
	int searchAlgor;
	int searchArea;
	int jhBins;
	int numWalks;
	int tmax;
	int tdecrease;
	int successful;
	int unsuccessful;
	float thresholdMeasure;
	int pyramidLevels;
	float* pyramidScales;
	int* levelWindows;
	int xPixelGap;
	int yPixelGap;
	int maxIterations;
	int networkUpdateThreshold;
	int networkUpdates;
	int* networkUpdateDistances;
	double* networkUpdateWeights;
	int correctionStdDevs;
	double tilePercentageRangeThreshold;
	bool image2image;
	bool image2imageScaled;
	bool image2map;
	bool image2mapScaled;
};

class ProcessInputParameters
{
public:
	ProcessInputParameters();
	bool importParameters(const char *inputfilePath);
	void runRegistration(const char *inputfilePath);
	void printSummary();
	void Tokenize(const string& str,
				  vector<string>& tokens,
				  const string& delimiters);
	void removeWhiteSpace(string* str);
	~ProcessInputParameters();
protected:
	RegistrationParams* params;
	int numberOfProcesses;
};

#endif
