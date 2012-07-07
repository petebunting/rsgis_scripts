/*
 *  ImageNetwork.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 06/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef ImageNetwork_H
#define ImageNetwork_H

#include "ImageNetworkException.h"
#include "FileOutputException.h"
#include "ErrorCodes.h"
#include "MathUtils.h"
#include "ImageNetworkStructures.h"
#include "ImagePyramid.h"
#include "SortedNodeDistance.h"
#include "NodeQueue.h"
#include <iostream>
#include "NetworkNodesLookUp.h"

class ImageNetwork{
public: 
	ImageNetwork();
	void updateNode(ImageNetworkNode *node, 
					int level, 
					Transform* transform,
					double distanceThreshold,
					float *levelScales,
					double* networkUpdateWeights,
					int* distanceSteps,
					int numberOfSteps);
	
	void updateImageNetworkNodes(SortedNodeDistance* sortedNodes, 
								 Transform* transform, 
								 double* networkUpdateWeights,
								 int* distanceSteps,
								 int numberOfSteps, 
								 double inputResolution);
	
	void findNodes4Update(ImageNetworkNode *node, 
						  int level, 
						  Transform* transform,
						  double distanceThreshold,
						  float *levelScales,
						  SortedNodeDistance* sortedNodes);
	
	void checkLevelEdgeLengths(SortedNodeDistance* sortedNodes, 
							   int xStep, 
							   int yStep, 
							   double diffThreshold,
							   double distanceThreshold,
							   float *levelScales,
							   double* networkUpdateWeights,
							   int* distanceSteps,
							   int numberOfSteps);
	
	void checkNodeNeighboringMovements(int level);
	
	void checkNodeMovementsAtLevel(int level, 
								   int stdDevsFromMean,
								   double distanceThreshold,
								   float *levelScales,
								   double* networkUpdateWeights,
								   int* distanceSteps,
								   int numberOfSteps);
	
	void constructNetwork(ImagePyramid *pyramid, 
						  int numLevels,
						  int xPixelStep,
						  int yPixelStep,
						  int *windowSizes,
						  float *levelScales);
	
	void constructEmptyDatastructures(ImagePyramid *pyramid, 
									  int numLevels,
									  int xPixelStep,
									  int yPixelStep);
	
	void createNodesAndInLevelEdges(ImagePyramid *pyramid, 
									int numLevels,
									int xPixelStep,
									int yPixelStep,
									int *windowSizes);
	
	/*void createInterLevelEdges(ImagePyramid *pyramid, 
							   int numLevels,
							   int xPixelStep,
							   int yPixelStep,
							   float *levelScales);*/
	int findClosestParent(ImagePyramid *pyramid,
						  ImageNetworkNode *node, 
						  float* levelScales, 
						  int xPixelStep, 
						  int yPixelStep);
	
	int getNumberOfLevels();
	
	ImageResolutionLevel* getNetworkLevel(int level);
						  
	void exportENVIControlPointsImage2Image(int level, const char *outputFilePath)
		throw(FileOutputException);
	void exportENVIControlPointsImage2ImageScaled(int level, 
												  const char *outputFilePath,
												  double xScale,
												  double yScale)
		throw(FileOutputException);
	void exportENVIControlPointsMap2Image(int level, 
										  const char *outputFilePath)
		throw(FileOutputException);
	void exportENVIControlPointsMap2ImageScaled(int level, 
												const char *outputFilePath,
												double xScale,
												double yScale)
		throw(FileOutputException);
	void exporttxtNetwork(int level, const char *outputFilePath)
		throw(FileOutputException);
	void exportLevelEdges(int level, const char *outputFilePath)
		throw(FileOutputException);
	void exportNetworkAsText(int level, const char *outputFilePath)
		throw(FileOutputException);
	void exportNodeTransformationsAtlevel(int level, const char *outputFilePath)
		throw(FileOutputException);
	~ImageNetwork();
private:
	ImageResolutionLevel *networkLevels;
	//float ***levelEdges;
	int numberOfLevels;
};

#endif
