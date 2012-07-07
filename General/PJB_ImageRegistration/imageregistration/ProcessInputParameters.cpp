/*
 *  ProcessInputParameters.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 23/08/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "ProcessInputParameters.h"

ProcessInputParameters::ProcessInputParameters()
{
	
}

bool ProcessInputParameters::importParameters(const char *inputfilePath)
{
	/************* File Parameters ******************/
	const std::string batch = "batch";
	bool batch_bool = false;
	const std::string ref_image = "ref_image";
	bool ref_image_bool = false;
	const std::string float_image = "float_image";
	bool float_image_bool = false;
	const std::string tmp_path = "tmp_path";
	bool tmp_path_bool = false;
	const std::string pts_path = "pts_path";
	bool pts_path_bool = false;
	const std::string ref_band = "ref_band";
	bool ref_band_bool = false;
	const std::string float_band = "float_band";
	bool float_band_bool = false;
	const std::string distance_measure = "distance_measure";
	bool distance_measure_bool = false;
	const std::string search_algor = "search_algor";
	bool search_algor_bool = false;
	const std::string search_area = "search_area";
	bool search_area_bool = false;
	const std::string jhbins = "jhbins";
	bool jhbins_bool = false;
	const std::string numwalks = "numwalks";
	bool numwalks_bool = false;
	const std::string tmax = "tmax";
	bool tmax_bool = false;
	const std::string tdecrease = "tdecrease";
	bool tdecrease_bool = false;
	const std::string successful = "successful";
	bool successful_bool = false;
	const std::string unsuccessful = "unsuccessful";
	bool unsuccessful_bool = false;
	const std::string threshold_measure = "threshold_measure";
	bool threshold_measure_bool = false;
	const std::string pyramid_levels = "pyramid_levels";
	bool pyramid_levels_bool = false;
	const std::string pixel_gaps = "pixel_gaps";
	bool pixel_gaps_bool = false;
	const std::string max_iterations = "max_iterations";
	bool max_iterations_bool = false;
	const std::string network_update_threshold = "network_update_threshold";
	bool network_update_threshold_bool = false;
	const std::string network_update_weights = "network_update_weights";
	bool network_update_weights_bool = false;
	const std::string correction_stddev = "correction_stddev";
	bool correction_stddev_bool = false;
	const std::string tilePercentageRangeThreshold = "tilePercentageRangeThreshold";
	bool tilePercentageRangeThreshold_bool = false;
	const std::string ctrl_pts = "ctrl_pts";
	bool ctrl_pts_bool = false;
	const std::string openBracket = "{";
	const std::string closeBracket = "}";
	/************************************************/
	
	std::ifstream inputFile;
	inputFile.open(inputfilePath);
	std::string currentStr;
	bool first = true;
	string text;
	int regParam = 0;
	
	if(inputFile)
	{
		std::cout << "File is being read..\n";
		while (! inputFile.eof() )
		{
			if(first)
			{
				std::getline(inputFile,currentStr);
				vector<string> tokens;
				this->Tokenize(currentStr, tokens, "= ");
				for(vector<string>::iterator it = tokens.begin();
					it != tokens.end(); it++)
				{
					if(batch.compare(*it) == 0)
					{
						std::cout << "batch command found!\n";
						batch_bool  = true;
					}
					else if(batch_bool)
					{
						numberOfProcesses = atoi(it->c_str());
					}
				}
				first = false;
				params = new RegistrationParams[numberOfProcesses];
			}
			else
			{
				std::getline(inputFile,currentStr);
				vector<string> tokens;
				this->Tokenize(currentStr, tokens, "=");
				for(vector<string>::iterator it = tokens.begin();
					it != tokens.end(); it++)
				{
					text.erase(0, text.length());
					text = *it;
					this->removeWhiteSpace(&text);
					
					if(openBracket.compare(text) == 0)
					{
						ref_image_bool = false;
						float_image_bool = false;
						tmp_path_bool = false;
						pts_path_bool = false;
						ref_band_bool = false;
						float_band_bool = false;
						distance_measure_bool = false;
						search_algor_bool = false;
						search_area_bool = false;
						jhbins_bool = false;
						numwalks_bool = false;
						tmax_bool = false;
						tdecrease_bool = false;
						successful_bool = false;
						unsuccessful_bool = false;
						threshold_measure_bool = false;
						pyramid_levels_bool = false;
						pixel_gaps_bool = false;
						max_iterations_bool = false;
						network_update_threshold_bool = false;
						network_update_weights_bool = false;
						correction_stddev_bool = false;
						tilePercentageRangeThreshold_bool = false;
						ctrl_pts_bool = false;
					}
					else if(closeBracket.compare(text) == 0)
					{
						regParam++;
					}
					else if(ref_image.compare(text) == 0)
					{
						ref_image_bool = true;
					}
					else if(float_image.compare(text) == 0)
					{
						float_image_bool = true;
					}
					else if(tmp_path.compare(text) == 0)
					{
						tmp_path_bool = true;
					}
					else if(pts_path.compare(text) == 0)
					{
						pts_path_bool = true;
					}
					else if(ref_band.compare(text) == 0)
					{
						ref_band_bool = true;
					}
					else if(float_band.compare(text) == 0)
					{
						float_band_bool = true;
					}
					else if(distance_measure.compare(text) == 0)
					{
						distance_measure_bool = true;
					}
					else if(search_algor.compare(text) == 0)
					{
						search_algor_bool = true;
					}
					else if(search_area.compare(text) == 0)
					{
						search_area_bool = true;
					}
					else if(jhbins.compare(text) == 0)
					{
						jhbins_bool = true;
					}
					else if(numwalks.compare(text) == 0)
					{
						numwalks_bool = true;
					}
					else if(tmax.compare(text) == 0)
					{
						tmax_bool = true;
					}
					else if(tdecrease.compare(text) == 0)
					{
						tdecrease_bool = true;
					}
					else if(successful.compare(text) == 0)
					{
						successful_bool = true;
					}
					else if(unsuccessful.compare(text) == 0)
					{
						unsuccessful_bool = true;
					}
					else if(threshold_measure.compare(text) == 0)
					{
						threshold_measure_bool = true;
					}
					else if(pyramid_levels.compare(text) == 0)
					{
						pyramid_levels_bool = true;
					}
					else if(pixel_gaps.compare(text) == 0)
					{
						pixel_gaps_bool = true;
					}
					else if(max_iterations.compare(text) == 0)
					{
						max_iterations_bool = true;
					}
					else if(network_update_threshold.compare(text) == 0)
					{
						network_update_threshold_bool = true;
					}
					else if(network_update_weights.compare(text) == 0)
					{
						network_update_weights_bool = true;
					}
					else if(correction_stddev.compare(text) == 0)
					{
						correction_stddev_bool = true;
					}
					else if(tilePercentageRangeThreshold.compare(text) == 0)
					{
						tilePercentageRangeThreshold_bool = true;
					}
					else if(ctrl_pts.compare(text) == 0)
					{
						ctrl_pts_bool = true;
					}
					else if(ref_image_bool)
					{
						std::cout << "\nreference Image. Text (Before) = " << text << std::endl;
						params[regParam].refImage = new char[text.length()];
						strcpy(params[regParam].refImage, text.c_str());
						std::cout << "reference Image. Text (After) = " << params[regParam].refImage << std::endl;
		
						ref_image_bool = false;
					}
					else if(float_image_bool)
					{
						std::cout << "\nfloating Image. Text (Before) = " << text << std::endl;
						std::cout << "reference Image.  (before) = " << params[regParam].refImage << std::endl;
						params[regParam].floatImage = new char[text.length()];
						strcpy(params[regParam].floatImage, text.c_str());
						std::cout << "reference Image. Text (After) = " << params[regParam].refImage << std::endl;
						std::cout << "floating Image. Text (after) = " << params[regParam].floatImage << std::endl;

						float_image_bool = false;
					}
					else if(tmp_path_bool)
					{
						std::cout << "\ntmp path. Text (Before) = " << text << std::endl;
						std::cout << "reference Image. Text (before) = " << params[regParam].refImage << std::endl;
						std::cout << "floating Image. Text (before) = " << params[regParam].floatImage << std::endl;
						params[regParam].tmpPath = new char[text.length()];
						strcpy(params[regParam].tmpPath, text.c_str());
						std::cout << "reference Image. Text (After) = " << params[regParam].refImage << std::endl;
						std::cout << "floating Image. Text (after) = " << params[regParam].floatImage << std::endl;
						std::cout << "tmp path. Text (after) = " << params[regParam].tmpPath << std::endl;
						tmp_path_bool = false;
					}
					else if(pts_path_bool)
					{
						std::cout << "\noutput control pts. Text (Before) = " << text << std::endl;
						std::cout << "reference Image. Text (before) = " << params[regParam].refImage << std::endl;
						std::cout << "floating Image. Text (before) = " << params[regParam].floatImage << std::endl;
						std::cout << "tmp path. Text (before) = " << params[regParam].tmpPath << std::endl;
						params[regParam].outCtrlPts = new char[text.length()];
						strcpy(params[regParam].outCtrlPts, text.c_str());
						std::cout << "reference Image. Text (After) = " << params[regParam].refImage << std::endl;
						std::cout << "floating Image. Text (after) = " << params[regParam].floatImage << std::endl;
						std::cout << "tmp path. Text (after) = " << params[regParam].tmpPath << std::endl;
						std::cout << "output control pts. Text (after) = " << params[regParam].outCtrlPts << std::endl;
						pts_path_bool = false;
					}
					else if(ref_band_bool)
					{
						params[regParam].refBand = atoi(text.c_str());
						ref_band_bool = false;
					}
					else if(float_band_bool)
					{
						params[regParam].floatBand = atoi(text.c_str());
						float_band_bool = false;
					}
					else if(distance_measure_bool)
					{
						params[regParam].distanceMeasure = atoi(text.c_str());
						distance_measure_bool = false;
					}
					else if(search_algor_bool)
					{
						params[regParam].searchAlgor = atoi(text.c_str());
						search_algor_bool = false;
					}
					else if(search_area_bool)
					{
						params[regParam].searchArea = atoi(text.c_str());
						search_area_bool = false;
					}
					else if(jhbins_bool)
					{
						params[regParam].jhBins = atoi(text.c_str());
						jhbins_bool = false;
					}
					else if(numwalks_bool)
					{
						params[regParam].numWalks = atoi(text.c_str());
						numwalks_bool = false;
					}
					else if(tmax_bool)
					{
						params[regParam].tmax = atoi(text.c_str());
						tmax_bool = false;
					}
					else if(tdecrease_bool)
					{
						params[regParam].tdecrease = atoi(text.c_str());
						tdecrease_bool = false;
					}
					else if(successful_bool)
					{
						params[regParam].successful = atoi(text.c_str());
						successful_bool = false;
					}
					else if(unsuccessful_bool)
					{
						params[regParam].unsuccessful = atoi(text.c_str());
						unsuccessful_bool = false;
					}
					else if(threshold_measure_bool)
					{
						params[regParam].thresholdMeasure = atof(text.c_str());
						threshold_measure_bool = false;
					}
					else if(pyramid_levels_bool)
					{
						vector<string> moreTokens;
						this->Tokenize(text, moreTokens, ":");
						
						if(moreTokens.size() != 2)
						{
							std::cout << "Problem parsing pyramid levels\n";
							return false;
						}
						params[regParam].pyramidLevels = atoi(moreTokens.front().c_str());

						params[regParam].pyramidScales = new float[params[regParam].pyramidLevels];
						params[regParam].levelWindows = new int[params[regParam].pyramidLevels];
												
						vector<string> scalesTokens;
						this->Tokenize(moreTokens.back(), scalesTokens, ")(");
						if(scalesTokens.size() != params[regParam].pyramidLevels)
						{
							std::cout << "Problem parsing pyramid levels - diff number of details as levels\n";
							return false;
						}
						string currentText;
						int counter = 0;
						for(vector<string>::iterator iterTokens = scalesTokens.begin();
							iterTokens != scalesTokens.end(); iterTokens++)
						{
							currentText = *iterTokens;
							vector<string> evenMoreTokens;
							this->Tokenize(currentText, evenMoreTokens, ",");
							params[regParam].pyramidScales[counter] = atof(evenMoreTokens.front().c_str());
							params[regParam].levelWindows[counter] = atoi(evenMoreTokens.back().c_str());
							counter++;
						}
						pyramid_levels_bool = false;
					}
					else if(pixel_gaps_bool)
					{
						vector<string> moreTokens;
						this->Tokenize(text, moreTokens, ":");
						
						if(moreTokens.size() != 2)
						{
							std::cout << "Problem parsing pixel gaps\n";
							return false;
						}
						params[regParam].xPixelGap = atoi(moreTokens.front().c_str());
						params[regParam].yPixelGap = atoi(moreTokens.back().c_str());
						pixel_gaps_bool = false;
					}
					else if(max_iterations_bool)
					{
						params[regParam].maxIterations = atoi(text.c_str());
						max_iterations_bool = false;
					}
					else if(network_update_threshold_bool)
					{
						params[regParam].networkUpdateThreshold = atoi(text.c_str());
						network_update_threshold_bool = false;
					}
					else if(network_update_weights_bool)
					{
						vector<string> moreTokens;
						this->Tokenize(text, moreTokens, ":");
						
						if(moreTokens.size() != 2)
						{
							std::cout << "Problem parsing network update weights\n";
							return false;
						}
						params[regParam].networkUpdates = atoi(moreTokens.front().c_str());
						
						params[regParam].networkUpdateDistances = new int[params[regParam].pyramidLevels];
						params[regParam].networkUpdateWeights = new double[params[regParam].pyramidLevels];
						
						vector<string> scalesTokens;
						this->Tokenize(moreTokens.back(), scalesTokens, ")(");
						if(scalesTokens.size() != params[regParam].pyramidLevels)
						{
							std::cout << "Problem parsing network update weights - diff number of details as levels\n";
							return false;
						}
						string currentText;
						int counter = 0;
						for(vector<string>::iterator iterTokens = scalesTokens.begin();
							iterTokens != scalesTokens.end(); iterTokens++)
						{
							currentText = *iterTokens;
							vector<string> evenMoreTokens;
							this->Tokenize(currentText, evenMoreTokens, ",");
							params[regParam].networkUpdateDistances[counter] = atoi(evenMoreTokens.front().c_str());
							params[regParam].networkUpdateWeights[counter] = atof(evenMoreTokens.back().c_str());
							counter++;
						}
						network_update_weights_bool = false;
					}
					else if(correction_stddev_bool)
					{
						params[regParam].correctionStdDevs = atoi(text.c_str());
						correction_stddev_bool = false;
					}
					else if(tilePercentageRangeThreshold_bool)
					{
						params[regParam].tilePercentageRangeThreshold = atof(text.c_str());
						tilePercentageRangeThreshold_bool = false;
					}
					else if(ctrl_pts_bool)
					{
						ctrl_pts_bool = false;
						vector<string> moreTokens;
						this->Tokenize(text, moreTokens, ",");
						
						if(moreTokens.size() != 4)
						{
							std::cout << "Problem parsing control points\n";
							return false;
						}
						int counter = 0;
						int currentValue;
						
						for(vector<string>::iterator iterTokens = moreTokens.begin();
							iterTokens != moreTokens.end(); iterTokens++)
						{
							currentValue = atoi(iterTokens->c_str());
							// image2image
							if(counter == 0 & currentValue == 1)
							{
								params[regParam].image2image = true;
							}
							else if(counter == 0 & currentValue != 1)
							{
								params[regParam].image2image = false;
							}
							// image2imageScaled
							else if(counter == 1 & currentValue == 1)
							{
								params[regParam].image2imageScaled = true;
							}
							else if(counter == 1 & currentValue != 1)
							{
								params[regParam].image2imageScaled = false;
							}
							// image2map
							else if(counter == 2 & currentValue == 1)
							{
								params[regParam].image2map = true;
							}
							else if(counter == 2 & currentValue != 1)
							{
								params[regParam].image2map = false;
							}
							//image2mapScaled
							else if(counter == 3 & currentValue == 1)
							{
								params[regParam].image2mapScaled = true;
							}
							else if(counter == 3 & currentValue != 1)
							{
								params[regParam].image2mapScaled = false;
							}

							counter++;
						}
					}
					
				}
			}
			
		}
		inputFile.close();
	}
	else
	{
		std::cout << "Cannot read file " << inputfilePath << "\n";
		return false;
	}
	return true;
}

void ProcessInputParameters::runRegistration(const char *inputfilePath)
{
	if(importParameters(inputfilePath))
	{
		this->printSummary();
		
		ImagesUtil *imgsUtil;
		
		for(int i = 0; i < numberOfProcesses; i++)
		{
			try
			{
				imgsUtil = new ImagesUtil(params[i].refImage,  params[i].floatImage, true);
				imgsUtil->findControlPointsNetwork( params[i].tmpPath,
													params[i].outCtrlPts,
													params[i].refBand,
													params[i].floatBand,
													params[i].distanceMeasure,
													params[i].searchAlgor,
													params[i].searchArea,
													params[i].jhBins,
													params[i].numWalks,
													params[i].tmax,
													params[i].tdecrease,
													params[i].successful,
													params[i].unsuccessful,
													params[i].thresholdMeasure,
													params[i].pyramidLevels,
													params[i].xPixelGap,
													params[i].yPixelGap,
													params[i].pyramidScales,
													params[i].levelWindows,
													params[i].maxIterations,
													params[i].networkUpdateThreshold,
													params[i].networkUpdateWeights,
													params[i].networkUpdateDistances,
													params[i].networkUpdates,
													params[i].correctionStdDevs,
													params[i].tilePercentageRangeThreshold,
													params[i].image2image,
													params[i].image2imageScaled,
													params[i].image2map,
													params[i].image2mapScaled);
			}
			catch( ImageRegistrationException e )
			{
				std::cout << "An Exception has occured: " << e.what() << std::endl;
				std::cout << "Error Code: " << e.getErrorCode() << std::endl;
				return;
			}
			
			if( imgsUtil != NULL )
			{
				delete imgsUtil;
			}
			
		}
	}
	else
	{
		std::cout << "Have failed to access parameters please check you input.\n";
	}
}

void ProcessInputParameters::printSummary()
{
	std::cout << "numberOfProcesses = " << numberOfProcesses << std::endl;
	for(int i = 0; i < numberOfProcesses; i++)
	{
		std::cout << "Got parameters for process " << i << " will now run registration!!\n";
		std::cout << "Reference Image: " << params[i].refImage << std::endl;
		std::cout << "Floating Image: " << params[i].floatImage << std::endl;
		std::cout << "tmp path: " << params[i].tmpPath << std::endl;
		std::cout << "output control points: " << params[i].outCtrlPts << std::endl;
		
		std::cout << "Reference band: " << params[i].refBand << std::endl;
		std::cout << "floating band: " << params[i].floatBand << std::endl;
		std::cout << "distance measure: " << params[i].distanceMeasure << std::endl;
		std::cout << "Search Algorithm: " << params[i].searchAlgor << std::endl;
		std::cout << "Search Area: " << params[i].searchArea << std::endl;
		std::cout << "jhBins: " << params[i].jhBins << std::endl;
		std::cout << "numWalks: " << params[i].numWalks << std::endl;
		std::cout << "tmax: " << params[i].tmax << std::endl;
		std::cout << "tdecrease: " << params[i].tdecrease << std::endl;
		std::cout << "successful: " << params[i].successful << std::endl;
		std::cout << "unsuccessful: " << params[i].unsuccessful << std::endl;
		std::cout << "threshold measure: " << params[i].thresholdMeasure << std::endl;
		std::cout << "pyramid levels: " << params[i].pyramidLevels << std::endl;
		std::cout << "pyramid scaled: [";
		for(int j = 0; j< params[i].pyramidLevels; j++)
		{
			if(j == params[i].pyramidLevels-1)
			{
				std::cout << params[i].pyramidScales[j] << "]\n";
			}
			else
			{
				std::cout << params[i].pyramidScales[j] << ", ";
			}
		}
		std::cout << "Window sizes: [";
		for(int j = 0; j< params[i].pyramidLevels; j++)
		{
			if(j == params[i].pyramidLevels-1)
			{
				std::cout << params[i].levelWindows[j] << "]\n";
			}
			else
			{
				std::cout << params[i].levelWindows[j] << ", ";
			}
		}
		std::cout << "x Pixal Gap: " << params[i].xPixelGap << std::endl;
		std::cout << "Y Pixel Gap: " << params[i].yPixelGap << std::endl;
		std::cout << "Max Iterations: " << params[i].maxIterations << std::endl;
		std::cout << "network update threshold: " << params[i].networkUpdateThreshold << std::endl;
		std::cout << "Network Updates: " << params[i].networkUpdates << std::endl;
		std::cout << "networkUpdateDistances: [";
		for(int j = 0; j< params[i].networkUpdates; j++)
		{
			if(j == params[i].networkUpdates-1)
			{
				std::cout << params[i].networkUpdateDistances[j] << "]\n";
			}
			else
			{
				std::cout << params[i].networkUpdateDistances[j] << ", ";
			}
		}
		std::cout << "networkUpdateWeights: [";
		for(int j = 0; j< params[i].networkUpdates; j++)
		{
			if(j == params[i].networkUpdates-1)
			{
				std::cout << params[i].networkUpdateWeights[j] << "]\n";
			}
			else
			{
				std::cout << params[i].networkUpdateWeights[j] << ", ";
			}
		}
		
		std::cout << "Correct Stddev: " << params[i].correctionStdDevs << std::endl;
		if(params[i].image2image)
		{
			std::cout << "Image2Image = true\n";
		}
		else
		{
			std::cout << "Image2Image = false\n";
		}
		if(params[i].image2imageScaled)
		{
			std::cout << "Image2ImageScaled = true\n";
		}
		else
		{
			std::cout << "Image2ImageScaled = false\n";
		}
		if(params[i].image2map)
		{
			std::cout << "image2map = true\n";
		}
		else
		{
			std::cout << "image2map = false\n";
		}
		if(params[i].image2mapScaled)
		{
			std::cout << "image2mapScaled = true\n";
		}
		else
		{
			std::cout << "image2mapScaled = false\n";
		}
	}
}

void ProcessInputParameters::Tokenize(const string& str,
									  vector<string>& tokens,
									  const string& delimiters)
{
    // Skip delimiters at beginning.
    string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    string::size_type pos = str.find_first_of(delimiters, lastPos);
	
    while (string::npos != pos || string::npos != lastPos)
    {
        // Found a token, add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}

void ProcessInputParameters::removeWhiteSpace(string* str)
{
	// Find Spaces
	string space = " ";
	unsigned int pos = str->find(space);
	while(pos != string::npos)
	{
		str->erase(pos, 1);
		pos = str->find(space);
	}
	
	// Find Tabs
	string tab = "\t";
	pos = str->find(tab);
	while(pos != string::npos)
	{
		str->erase(pos, 1);
		pos = str->find(tab);
	}
}


ProcessInputParameters::~ProcessInputParameters()
{
	
}
