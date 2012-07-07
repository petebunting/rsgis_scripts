/*
 *  ImageNetwork.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 06/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "ImageNetwork.h"

ImageNetwork::ImageNetwork()
{
	
}

void ImageNetwork::updateNode(ImageNetworkNode *node, 
							  int level, 
							  Transform* transform,
							  double distanceThreshold,
							  float *levelScales,
							  double* networkUpdateWeights,
							  int* distanceSteps,
							  int numberOfSteps)
{
	std::cout << "Updating network from movement [" << transform->shiftX 
	<< "," << transform->shiftY << "] of node " << node->nodeID << " with measure of "
	<< transform->measureValue << " on level " << node->level << " with window size " 
	<< node->windowSize << std::endl;
	
	SortedNodeDistance* sortedNodes = NULL;
	
	for(int i = level; i >= 0; i--)
	{
		sortedNodes = new SortedNodeDistance(node, distanceThreshold);

		// Find the Nodes to update.
		this->findNodes4Update(node,
							   i,
							   transform,
							   distanceThreshold,
							   levelScales,
							   sortedNodes);
		//std::cout << "\n\n ******* Found Nodes for level " << i << " *******\n\n";
 		// Update the required Nodes.
		this->updateImageNetworkNodes(sortedNodes, 
									  transform, 
									  networkUpdateWeights,
									  distanceSteps,
									  numberOfSteps,
									  node->pixelRes);
		
		//std::cout << "\n\n ******* Updated Nodes for level " << i << " *******\n\n";
		//std::cout << "Finished level " << i << std::endl;
		if(sortedNodes != NULL)
		{
			//std::cout << " Deleting Sorted Nodes with Size = " << sortedNodes->getSize() << std::endl;
			delete sortedNodes;
			//sortedNodes = NULL;
		}
	}
	node->transform->measureValue = transform->measureValue;
	//std::cout << "Finished Network Update...\n";
}

void ImageNetwork::updateImageNetworkNodes(SortedNodeDistance* sortedNodes, 
										   Transform* transform, 
										   double* networkUpdateWeights,
										   int* distanceSteps,
										   int numberOfSteps, 
										   double inputResolution)
{
	double currentNodeDistance = 0;
	ImageNetworkNode* currentNode = NULL;
	double currentNodeXShift = 0;
	double currentNodeYShift = 0;
	double weighting = 0;
	double scaling = 0;
	sortedNodes->startIterator();
	while(sortedNodes->hasNext())
	{
		currentNode = sortedNodes->next(&currentNodeDistance);
		
		if(currentNodeDistance <= distanceSteps[0])
		{
			weighting = 1/pow((currentNodeDistance+1), networkUpdateWeights[0]);
		}
		else if(currentNodeDistance > distanceSteps[numberOfSteps-1])
		{
			weighting = 1/pow((currentNodeDistance+1), networkUpdateWeights[numberOfSteps-1]);
		}
		else
		{
			for(int i = 1; i < numberOfSteps; i++)
			{
				if(currentNodeDistance > distanceSteps[i-1] &
				   currentNodeDistance <= distanceSteps[i])
				{
					weighting = 1/pow((currentNodeDistance+1), networkUpdateWeights[i]);
				}
			}
		}
		
		scaling = inputResolution/currentNode->pixelRes;
		/*
		std::cout << "\nWeighting = " << weighting << " at Distance " << currentNodeDistance << std::endl;
		
		std::cout << "Input Pixel Resolution: " << inputResolution << " currentNode resolution: " 
					<< currentNode->pixelRes << " on Level " << currentNode->level 
					<< " so scaling of " << scaling << std::endl;*/
		
		/*currentNodeXShift = currentNode->transform->shiftX - (transform->shiftX * scaling);
		currentNodeYShift = currentNode->transform->shiftY - (transform->shiftY * scaling);*/
		
	/*	std::cout << "currentNode Shift: [" << currentNode->transform->shiftX << "," << 
				currentNode->transform->shiftY << "] Input Transformation: [" << 
				transform->shiftX << "," << transform->shiftY << "] Different with scaling: ["
				<< currentNodeXShift << "," << currentNodeYShift << "]\n";*/
		
		/*currentNode->transform->shiftX = currentNode->transform->shiftX - (currentNodeXShift * weighting);
		currentNode->transform->shiftY = currentNode->transform->shiftY - (currentNodeYShift * weighting); */
		
		/*std::cout << "Output currentNode shift: ["<< currentNode->transform->shiftX << "," << 
			currentNode->transform->shiftY << "]\n";*/
		
		currentNodeXShift = transform->shiftX * weighting;
		currentNodeYShift = transform->shiftY * weighting;
		
		currentNode->transform->shiftX += (currentNodeXShift * scaling);
		currentNode->transform->shiftY += (currentNodeYShift * scaling);
	}
}

void ImageNetwork::findNodes4Update(ImageNetworkNode *node, 
									int level, 
									Transform* transform,
									double distanceThreshold,
									float *levelScales,
									SortedNodeDistance* sortedNodes)
{
	NodeQueue* queue = new NodeQueue;
	NetworkNodesLookUp* lookup = new NetworkNodesLookUp;
	ImageNetworkNode* currentNode = NULL;
	int addReturn = 0;
	bool first = true;
	
	// Find start node.	
	if(node->level == level)
	{
		queue->addNode(node);
	}
	else
	{
		double distance = 0;
		double tmpDistance = 0;
		ImageNetworkNode* tmpNode = NULL;
		first = true;
		for(int i = 0; i < this->networkLevels[level].numNodes; i++)
		{
			if(first)
			{
				distance = sortedNodes->calcDistance(networkLevels[level].nodes[i], levelScales);
				tmpNode = networkLevels[level].nodes[i];
				first = false;
			}
			else
			{
				tmpDistance = sortedNodes->calcDistance(networkLevels[level].nodes[i], levelScales);
				if(tmpDistance < distance)
				{
					tmpNode = networkLevels[level].nodes[i];
					distance = tmpDistance;
				}
			}
		}
		queue->addNode(tmpNode);
	}
	
	while(queue->getSize() != 0)
	{
		currentNode = queue->getHead();
		addReturn = sortedNodes->addNode(currentNode, levelScales, false);
		
		if(addReturn == addNodeOutput::OK)
		{
			//std::cout << "Finding Nodes to be added to Queue\n";
			for(int j = 0; j < networkLevels[level].numNodes; j++)
			{
				if(networkLevels[level].edges[currentNode->nodeID][j] == 1)
				{
					if(!lookup->search(networkLevels[level].nodes[j]))
					{
						//std::cout << "Add node to queue\n";
						queue->addNode(networkLevels[level].nodes[j]);
						//std::cout << "Added node to queue\n";
						//std::cout << "Add node to lookup\n";
						lookup->insert(networkLevels[level].nodes[j],false);
						//std::cout << "Added node to lookup\n";
					}
				}
			}
			//std::cout << "Finished adding nodes to Queue.\n";
		}
		//else
		//{
		//	std::cout << "node already in queue so not adding anything to queue.\n";
		//}
	}

	if(queue != NULL)
	{
		delete queue;
	}
	if(lookup != NULL)
	{
		delete lookup;
	}	
}
	
void ImageNetwork::constructNetwork(ImagePyramid *pyramid, 
									int numLevels,
									int xPixelStep,
									int yPixelStep,
									int *windowSizes,
									float *levelScales)
{
	std::cout << "Create Empty Data Structures.\n";
	/**************** Construct Empty Data Structures ********************/
	this->constructEmptyDatastructures(pyramid, 
									   numLevels,
									   xPixelStep,
									   yPixelStep);
	/********************************************************************/
	std::cout << "Created Empty Data Structures.\n";
	
	std::cout << "Fill Data Structures with Nodes and Edges.\n";
	/********************** Create local variables *********************/
	this->createNodesAndInLevelEdges(pyramid,
									 numLevels,
									 xPixelStep,
									 yPixelStep,
									 windowSizes);
	/****************************************************************/
	std::cout << "Filled Data Structures with Nodes and Edges.\n";
	/*double distance = 0;
	double xDistance = 0;
	double yDistance = 0;
	for(int i = numLevels-1; i >= 0; i--)
	{
		std::cout << "On Level " << i << " xNodes = " << networkLevels[i].xNodes 
		<< " yNodes = " << networkLevels[i].yNodes << std::endl; 
		for(int j = 0; j < networkLevels[i].numNodes; j++)
		{
			std::cout << "\nNode " << j << " on level " << i << " neighbours:\n";
			for(int k = 0; k < networkLevels[i].numNodes; k++)
			{
				if(networkLevels[i].edges[j][k] == 1)
				{
					xDistance = networkLevels[i].nodes[j]->imageA->x - networkLevels[i].nodes[k]->imageA->x;
					if(xDistance < 0)
					{
						xDistance = xDistance*(-1);
					}
					yDistance = networkLevels[i].nodes[j]->imageA->y - networkLevels[i].nodes[k]->imageA->y;
					if(yDistance < 0)
					{
						yDistance = yDistance*(-1);
					}
					distance = sqrt((xDistance*xDistance)+(yDistance*yDistance));
					std::cout << "Node " << k << " distance = " << distance << std::endl;
				}
			}
		}
	}*/
	
	//std::cout << "Create Edges between levels.\n";
	/**************** Construct Empty Data Structures ********************
	this->createInterLevelEdges(pyramid,
								numLevels,
								xPixelStep,
								yPixelStep,
								levelScales);
	********************************************************************/
	//std::cout << "Created Edges between levels.\n";
}

void ImageNetwork::constructEmptyDatastructures(ImagePyramid *pyramid, 
												int numLevels,
												int xPixelStep,
												int yPixelStep)
{
	MathUtils mathUtils;
	PyramidLevel *pyramidLevel = NULL;
	int *refImagePixels;
	int xNodes = 0;
	int yNodes = 0;
	int totalNodes = 0;
	double tmpXNodes = 0;
	double tmpYNodes = 0;
	int pixelXSize = 0;
	int pixelYSize = 0;
	this->numberOfLevels = numLevels;
	
	// Create Image Resolution Levels
	this->networkLevels = new ImageResolutionLevel[numLevels];
		
	for(int i = 0; i < numLevels; i++)
	{
		// Get Level
		pyramidLevel = pyramid->getLevel(i);
		refImagePixels = pyramidLevel->imgOverlap->getImageAPixelCoords();
		
		// Identify Image Size;
		pixelXSize = refImagePixels[2] - refImagePixels[0];
		pixelYSize = refImagePixels[3] - refImagePixels[1];
		
		//std::cout << "Pixel X Size = " << pixelXSize << "(" << refImagePixels[2] << " - " << refImagePixels[0] << ")\n";
		//std::cout << "Pixel Y Size = " << pixelYSize << "(" << refImagePixels[3] << " - " << refImagePixels[1] << ")\n";
		
		// Calculate Number of Nodes
		tmpXNodes = (double(pixelXSize)/(xPixelStep+1));
		xNodes = mathUtils.roundDown(tmpXNodes);
		tmpYNodes = (double(pixelYSize)/(yPixelStep+1));
		yNodes = mathUtils.roundDown(tmpYNodes);
		totalNodes = xNodes * yNodes;
		
		//std::cout << "xNodes = " << xNodes << " (" << tmpXNodes <<") yNodes = " << yNodes 
		//	<< " (" << tmpYNodes << ") total Nodes = " << totalNodes << std::endl;
		
		// Create and enter data into structure.
		networkLevels[i].nodes = new ImageNetworkNode* [totalNodes];
		
		networkLevels[i].edges = new float* [totalNodes];
		for(int k = 0; k < totalNodes; k++)
		{
			networkLevels[i].edges[k] = new float[totalNodes];
			for(int n = 0; n < totalNodes; n++)
			{
				networkLevels[i].edges[k][n] = 0;
			}
		}
		networkLevels[i].numNodes = totalNodes;
		networkLevels[i].xNodeGap = xPixelStep;
		networkLevels[i].yNodeGap = yPixelStep;
		networkLevels[i].xNodes = xNodes;
		networkLevels[i].yNodes = yNodes;
		networkLevels[i].totalMeasures = 0;
		networkLevels[i].numMeasures = 0;
		networkLevels[i].meanMeasure = 0;
	}
	
}

void ImageNetwork::createNodesAndInLevelEdges(ImagePyramid *pyramid, 
											  int numLevels,
											  int xPixelStep,
											  int yPixelStep,
											  int *windowSizes)
{
	MathUtils mathUtils;
	PyramidLevel *pyramidLevel = NULL;
	int *refImagePixels;
	int *floatImagePixels;
	double *geoCorners;
	int pixelXStep = 0;
	int pixelYStep = 0;
	double geoXStep = 0;
	double geoYStep = 0;
	int xStartA = 0;
	int yStartA = 0;
	int xStartB = 0;
	int yStartB = 0;
	double xGeoStart = 0;
	double yGeoStart = 0;
	int xIncrement = 0;
	int yIncrement = 0;
	double imageRange = 0;
	TileCoords tile;
	
	/******************************* Create Nodes ****************************/
	// Loop through levels.
	for(int i = 0; i < numLevels; i++)
	{
		// Get Level
		pyramidLevel = pyramid->getLevel(i);
		refImagePixels = pyramidLevel->imgOverlap->getImageAPixelCoords();
		floatImagePixels = pyramidLevel->imgOverlap->getImageBPixelCoords();
		geoCorners = pyramidLevel->imgOverlap->getOverlapGeoCoords();
		
		// Idenfity Steps between Nodes.
		pixelXStep = networkLevels[i].xNodeGap;
		pixelYStep = networkLevels[i].yNodeGap;
		geoXStep = pixelXStep/pyramidLevel->imageRes;
		geoYStep = pixelYStep/pyramidLevel->imageRes;
		
		// Identify Start Points
		xStartA = refImagePixels[0] + pixelXStep;
		yStartA = refImagePixels[1] + pixelYStep;
		xStartB = floatImagePixels[0] + pixelXStep;
		yStartB = floatImagePixels[1] + pixelYStep;
		xGeoStart = geoCorners[0] + geoXStep;
		yGeoStart = geoCorners[1] - geoYStep;
		
		// Setup Variables
		xIncrement = 0;
		yIncrement = 0;
		
		// Find Image Range
		imageRange = mathUtils.imageRange(pyramidLevel->imageA, 1);
		
		//Construct Level
		for(int j = 0; j < networkLevels[i].numNodes; j++)
		{
			if(xIncrement == networkLevels[i].xNodes)
			{
				xIncrement = 0;
				yIncrement++;
			}
			
			// Create Node
			networkLevels[i].nodes[j] = new ImageNetworkNode;
			networkLevels[i].nodes[j]->nodeID = j;
			networkLevels[i].nodes[j]->windowSize = windowSizes[i];
			networkLevels[i].nodes[j]->imageA = new PointPxlCoords;
			networkLevels[i].nodes[j]->imageA->x = xStartA + xIncrement + (pixelXStep * xIncrement);
			networkLevels[i].nodes[j]->imageA->y = yStartA + yIncrement + (pixelYStep * yIncrement);
			networkLevels[i].nodes[j]->imageB = new PointPxlCoords;
			networkLevels[i].nodes[j]->imageB->x = xStartB + xIncrement + (pixelXStep * xIncrement);
			networkLevels[i].nodes[j]->imageB->y = yStartB + yIncrement + (pixelYStep * yIncrement);
			networkLevels[i].nodes[j]->geoPosition = new PointGeoCoords;
			networkLevels[i].nodes[j]->geoPosition->eastings = xGeoStart + pyramidLevel->imageRes + (geoXStep * xIncrement);
			networkLevels[i].nodes[j]->geoPosition->northings = yGeoStart - (pyramidLevel->imageRes + (geoYStep * yIncrement));
			networkLevels[i].nodes[j]->transform = new Transform;
			networkLevels[i].nodes[j]->transform->shiftX = 0;
			networkLevels[i].nodes[j]->transform->shiftY = 0;
			networkLevels[i].nodes[j]->transform->measureValue = 0;
			networkLevels[i].nodes[j]->level = i;
			networkLevels[i].nodes[j]->pixelRes = pyramidLevel->imageRes;
			pyramid->getTileCoords4PointWindow(networkLevels[i].nodes[j], i, &tile);
			networkLevels[i].nodes[j]->percentageRange = mathUtils.tileRangePercentage(&tile,
																					   pyramidLevel->imageA,
																					   true,
																					   1,
																					   imageRange);
			 
			/* Key for numbered edges away from the centre (current node).
			 *   0 1 2
			 * 4 3 X 
			 *   5 6 7
			 */
			
			// Create the Edges with Weights
			if(yIncrement == 0)
			{
				// TOP LINE only insert horizontal edges.
				if(xIncrement == 0)
				{
					// Left edge of the structure.
					// DO nothing this is the first node and therefore has nothing to link to.
				}	
				else
				{
					// Otherwise just connection the horizontal edges 3 and 4.
					networkLevels[i].edges[j][j-1] = 1;
					networkLevels[i].edges[j-1][j] = 1;
				}
			}
			else
			{
				if(xIncrement == 0)
				{
					// Left edge of the structure. - Only connect vertically.
					// Connect vertical edge 1.
					networkLevels[i].edges[j][j-networkLevels[i].xNodes] = 1;
					networkLevels[i].edges[j-networkLevels[i].xNodes][j] = 1;
					// Connect vertical edge 2.
					networkLevels[i].edges[j][(j-networkLevels[i].xNodes)+1] = 1;
					networkLevels[i].edges[(j-networkLevels[i].xNodes)+1][j] = 1;
				}
				else if(xIncrement == networkLevels[i].xNodes-1)
				{
					// Right Edge of the structure.
					// Connect vertical edge 0.
					networkLevels[i].edges[j][(j-networkLevels[i].xNodes)-1] = 1;
					networkLevels[i].edges[(j-networkLevels[i].xNodes)-1][j] = 1;
					// Connect vertical edge 1.
					networkLevels[i].edges[j][j-networkLevels[i].xNodes] = 1;
					networkLevels[i].edges[j-networkLevels[i].xNodes][j] = 1;
					// Connect vertical edges 3 and 4
					networkLevels[i].edges[j][j-1] = 1;
					networkLevels[i].edges[j-1][j] = 1;
				}
				else
				{
					// Otherwise Connect All.
					// Connect vertical edge 0.
					networkLevels[i].edges[j][(j-networkLevels[i].xNodes)-1] = 1;
					networkLevels[i].edges[(j-networkLevels[i].xNodes)-1][j] = 1;
					// Connect vertical edge 1.
					networkLevels[i].edges[j][j-networkLevels[i].xNodes] = 1;
					networkLevels[i].edges[j-networkLevels[i].xNodes][j] = 1;
					// Connect vertical edge 2.
					networkLevels[i].edges[j][(j-networkLevels[i].xNodes)+1] = 1;
					networkLevels[i].edges[(j-networkLevels[i].xNodes)+1][j] = 1;
					// Connect vertical edges 3 and 4
					networkLevels[i].edges[j][j-1] = 1;
					networkLevels[i].edges[j-1][j] = 1;
				}
			}
			xIncrement++;
		}
	}
}

/*void ImageNetwork::createInterLevelEdges(ImagePyramid *pyramid, 
										 int numLevels,
										 int xPixelStep,
										 int yPixelStep,
										 float *levelScales)
{	
	levelEdges = new float** [numLevels-1];
	int finalParentNode = 0;
	for(int i = 0; i < (numLevels-1); i++)
	{
		levelEdges[i] = new float* [networkLevels[i].numNodes];
		for(int j = 0; j < networkLevels[i].numNodes; j++)
		{
			levelEdges[i][j] = new float[networkLevels[i+1].numNodes];
			for(int k = 0; k < networkLevels[i+1].numNodes; k++)
			{
				levelEdges[i][j][k] = 0;
			}
			
			finalParentNode = this->findClosestParent(pyramid, 
													  networkLevels[i].nodes[j], 
													  levelScales, 
													  xPixelStep, 
													  yPixelStep);
			levelEdges[i][j][finalParentNode] = 1;
		}
	}
}*/

int ImageNetwork::findClosestParent(ImagePyramid *pyramid,
									ImageNetworkNode *node, 
									float* levelScales, 
									int xPixelStep, 
									int yPixelStep)
{
	int childLevel = node->level;
	int parentLevel = node->level +1;
	
	//int* imageACorners = pyramid->getLevel(parentLevel)->imgOverlap->getImageAPixelCoords();

	double imageAPxlScaled2Parentx = node->imageA->x / levelScales[childLevel];
	double imageAPxlScaled2Parenty = node->imageA->y / levelScales[childLevel];
	
	/*************** Find nearest node to this pixel location *****************/
	bool first = true;
	double minDistance = 0;
	double tmpDistance = 0;
	int minNode = 0;
	for(int i = 0; i < networkLevels[parentLevel].numNodes; i++)
	{
		if(first)
		{
			minDistance = sqrt(((networkLevels[parentLevel].nodes[i]->imageA->x - imageAPxlScaled2Parentx)*
								(networkLevels[parentLevel].nodes[i]->imageA->x - imageAPxlScaled2Parentx)) +
							   ((networkLevels[parentLevel].nodes[i]->imageA->y - imageAPxlScaled2Parenty)*
								(networkLevels[parentLevel].nodes[i]->imageA->y - imageAPxlScaled2Parenty)));
			minNode = i;
			first = false;
		}
		else
		{
			tmpDistance = sqrt(((networkLevels[parentLevel].nodes[i]->imageA->x - imageAPxlScaled2Parentx)*
								(networkLevels[parentLevel].nodes[i]->imageA->x - imageAPxlScaled2Parentx)) +
							   ((networkLevels[parentLevel].nodes[i]->imageA->y - imageAPxlScaled2Parenty)*
								(networkLevels[parentLevel].nodes[i]->imageA->y - imageAPxlScaled2Parenty)));
			
			if(tmpDistance < minDistance)
			{
				minDistance = tmpDistance;
				minNode = i;
			}
		}
	}
	/***************************************************************************/
	return minNode;
}

void ImageNetwork::checkNodeMovementsAtLevel(int level, 
											 int stdDevsFromMean,
											 double distanceThreshold,
											 float *levelScales,
											 double* networkUpdateWeights,
											 int* distanceSteps,
											 int numberOfSteps)
{
	double meanXShift = 0;
	double meanYShift = 0;
	double sqMeanXShift = 0;
	double sqMeanYShift = 0;
	int numNodes = 0;
	for(int i = 0; i < networkLevels[level].numNodes; i++)
	{
		if(networkLevels[level].nodes[i]->transform->measureValue > 0)
		{
			meanXShift += networkLevels[level].nodes[i]->transform->shiftX;
			meanYShift += networkLevels[level].nodes[i]->transform->shiftY;
			sqMeanXShift += networkLevels[level].nodes[i]->transform->shiftX*networkLevels[level].nodes[i]->transform->shiftX;
			sqMeanYShift += networkLevels[level].nodes[i]->transform->shiftY*networkLevels[level].nodes[i]->transform->shiftY;
			numNodes++;
		}
	}
	
	meanXShift = meanXShift/numNodes;
	meanYShift = meanYShift/numNodes;
	sqMeanXShift = sqMeanXShift/numNodes;
	sqMeanYShift = sqMeanYShift/numNodes;
	
	double stddevShiftX = sqrt( sqMeanXShift - (meanXShift*meanXShift));
	double stddevShiftY = sqrt( sqMeanYShift - (meanYShift*meanYShift));
	
	std::cout << std::endl;
	//std::cout << "Mean shift at level " << level << " is [" << meanXShift << ", " << meanYShift << "]\n";
	//std::cout << "stddev of shift at level " << level << " is [" << stddevShiftX << ", " << stddevShiftY << "]\n";
	
	double currentXShift = 0;
	double currentYShift = 0;
	
	double lowerXThreshold = meanXShift - (stddevShiftX * stdDevsFromMean);
	double upperXThreshold = meanXShift + (stddevShiftX * stdDevsFromMean);
	double lowerYThreshold = meanYShift - (stddevShiftY * stdDevsFromMean);
	double upperYThreshold = meanYShift + (stddevShiftY * stdDevsFromMean);
	
	bool update = false;
	Transform transform;
	transform.shiftX = 0;
	transform.shiftY = 0;
	transform.measureValue = 0;
	
	for(int i = 0; i < networkLevels[level].numNodes; i++)
	{
		//std::cout << "Node " << i << std::endl;
		currentXShift = networkLevels[level].nodes[i]->transform->shiftX;
		currentYShift = networkLevels[level].nodes[i]->transform->shiftY;
		
		if(currentXShift < lowerXThreshold | currentXShift > upperXThreshold)
		{
			transform.shiftX = meanXShift - currentXShift;
			//std::cout << "Node " << i << " X Shift changed currentXShift =  " << currentXShift 
			//<< " meanXShift = " << meanXShift << " transform.shiftX = " << transform.shiftX <<  std::endl; 
			update = true;
		}
		else
		{
			transform.shiftX = 0;
		}
		if(currentYShift < lowerYThreshold | currentYShift > upperYThreshold)
		{
			transform.shiftY = meanYShift - currentYShift;
			//std::cout << "Node " << i << " Y Shift changed currentYShift =  " << currentYShift 
			//<< " meanYShift = " << meanYShift << " transform.shiftY = " << transform.shiftY <<  std::endl; 
			update = true;
		}
		else
		{
			transform.shiftY = 0;
		}
		
		if(update)
		{
			transform.measureValue = 0;
			this->updateNode(networkLevels[level].nodes[i], 
							 networkLevels[level].nodes[i]->level, 
							 &transform, 
							 distanceThreshold, 
							 levelScales, 
							 networkUpdateWeights,
							 distanceSteps,
							 numberOfSteps);
			update = false;
		}
	}
	std::cout << std::endl;
}

void ImageNetwork::checkLevelEdgeLengths(SortedNodeDistance* sortedNodes, 
										 int xStep, 
										 int yStep, 
										 double diffThreshold,
										 double distanceThreshold,
										 float *levelScales,
										 double* networkUpdateWeights,
										 int* distanceSteps,
										 int numberOfSteps)
{	
	// Calculate Original Node distances.
	double xPosTmp = 0;
	double yPosTmp = 0;
	double xPosCurrent = 0;
	double yPosCurrent = 0;
	
	xStep++;
	yStep++;
	
	double xDistThresholdUpper = xStep + (diffThreshold*xStep);
	double xDistThresholdLower = xStep - (diffThreshold*xStep);
	double yDistThresholdUpper = yStep + (diffThreshold*yStep);
	double yDistThresholdLower = yStep - (diffThreshold*yStep);

	double tmpXDistance = 0;
	double tmpYDistance = 0;
	Transform transform;
	transform.shiftX = 0;
	transform.shiftY = 0;
	transform.measureValue = 0;
	bool update = false;
	
	/*std::cout << "Distances [" << xStep << ", " << yStep << ", " << angularDistance << "]\n";
	std::cout << "Difference Threshold = " << diffThreshold << " Differences [" << (diffThreshold*xStep)
			  << ", " << (diffThreshold*yStep) << ", " << (diffThreshold*angularDistance) << "]\n";
	std::cout << "Upper Thresholds [" << xDistThresholdUpper << ", "
		<< yDistThresholdUpper << ", " << angDistThresholdUpper << "] Lower Thresholds ["
		<< xDistThresholdLower << ", " << yDistThresholdLower << ", " << angDistThresholdLower << "]\n";*/
	
	// Loop through nodes.
	sortedNodes->startIteratorReverse();
	ImageNetworkNode* currentNode = NULL;
	ImageNetworkNode* tmpNode = NULL;
	double distance = 0;
	while(sortedNodes->hasNextReverse())
	{
		// Get Node.
		currentNode = sortedNodes->nextReverse(&distance);
		xPosCurrent = currentNode->imageB->x + currentNode->transform->shiftX;
		yPosCurrent = currentNode->imageB->y + currentNode->transform->shiftY;
		//std::cout << "\nCurrent Node " << currentNode->nodeID << " [" << xPosCurrent << ", " << yPosCurrent << "]\n";

		// Loop through node edges.
		for(int i = 0; i < networkLevels[currentNode->level].numNodes; i++)
		{
			if(networkLevels[currentNode->level].edges[currentNode->nodeID][i] == 1)
			{
				tmpNode = networkLevels[currentNode->level].nodes[i];
				xPosTmp = tmpNode->imageB->x + tmpNode->transform->shiftX;
				yPosTmp = tmpNode->imageB->y + tmpNode->transform->shiftY;

				update = false;
				// Decide whether horizontal vertical or diagonal.
				if( tmpNode->nodeID == currentNode->nodeID-1)
				{
					// Left
					tmpXDistance = xPosCurrent - xPosTmp;
					/*std::cout << "tmpXDistance (LEFT) = " << tmpXDistance << " xDistThresholdUpper = " 
					<< xDistThresholdUpper << " xDistThresholdLower = " << xDistThresholdLower << std::endl;*/
					
					// X Axis
					if(tmpXDistance > xDistThresholdUpper)
					{
						update = true;
						transform.shiftX = tmpXDistance - xDistThresholdUpper;
					}
					else if(tmpXDistance < xDistThresholdLower)
					{
						update = true;
						transform.shiftX = xDistThresholdLower - tmpXDistance;
					}
					else
					{
						transform.shiftX = 0;
					}
					
					// Y Axis
					if( yPosTmp > yPosCurrent)
					{
						tmpYDistance = yPosCurrent - yPosTmp;
						if(tmpYDistance > (diffThreshold*yStep))
						{
							update = true;
							transform.shiftY = (tmpYDistance - (diffThreshold*yStep))*(-1);
						}
						else
						{
							transform.shiftY = 0;
						}
					}
					else if(yPosTmp < yPosCurrent)
					{
						tmpYDistance = yPosCurrent - yPosTmp;
						if(tmpYDistance > (diffThreshold*yStep))
						{
							update = true;
							transform.shiftY = tmpYDistance - (diffThreshold*yStep);
						}
						else
						{
							transform.shiftY = 0;
						}
					}
					else
					{
						// Do nothing
						transform.shiftY = 0;
					}
				}
				else if(tmpNode->nodeID == currentNode->nodeID+1)
				{
					// Right
					tmpXDistance = xPosTmp - xPosCurrent;
					/*std::cout << "tmpXDistance (RIGHT) = " << tmpXDistance << " xDistThresholdUpper = " 
					<< xDistThresholdUpper << " xDistThresholdLower = " << xDistThresholdLower << std::endl;*/
					
					// X Axis
					if(tmpXDistance > xDistThresholdUpper)
					{
						update = true;
						transform.shiftX = tmpXDistance - xDistThresholdUpper;
					}
					else if(tmpXDistance < xDistThresholdLower)
					{
						update = true;
						transform.shiftX = xDistThresholdLower - tmpXDistance;
					}
					else
					{
						transform.shiftX = 0;
					}
					
					// Y Axis
					if( yPosTmp > yPosCurrent)
					{
						tmpYDistance = yPosTmp - yPosCurrent;
						if(tmpYDistance > (diffThreshold*yStep))
						{
							update = true;
							transform.shiftY = (tmpYDistance - (diffThreshold*yStep))*(-1);
						}
						else
						{
							transform.shiftY = 0;
						}
					}
					else if(yPosTmp < yPosCurrent)
					{
						tmpYDistance = yPosCurrent - yPosTmp;
						if(tmpYDistance > (diffThreshold*yStep))
						{
							update = true;
							transform.shiftY = tmpYDistance - (diffThreshold*yStep);
						}
						else
						{
							transform.shiftY = 0;
						}
					}
					else
					{
						// Do nothing
						transform.shiftY = 0;
					}
				}
				else if(tmpNode->nodeID == (currentNode->nodeID - networkLevels[currentNode->level].xNodes))
				{
					// Top
					tmpYDistance = yPosCurrent - yPosTmp;
				/*	std::cout << "tmpYDistance (TOP) = " << tmpYDistance << " yDistThresholdUpper = " 
						      << yDistThresholdUpper << " yDistThresholdLower = " << yDistThresholdLower << std::endl;*/
				
					// Y Axis
					if(tmpYDistance > yDistThresholdUpper)
					{
						update = true;
						transform.shiftY = tmpYDistance - yDistThresholdUpper;
					}
					else if(tmpYDistance < yDistThresholdLower)
					{
						update = true;
						transform.shiftY = yDistThresholdLower - tmpYDistance;
					}
					else 
					{
						transform.shiftY = 0;
					}
					
					// X Axis
					if(xPosTmp > xPosCurrent)
					{
						tmpXDistance = xPosTmp - xPosCurrent;
						if(tmpXDistance > (diffThreshold*xStep))
						{
							update = true;
							transform.shiftX = (tmpXDistance - (diffThreshold*xStep))*(-1);
						}
						else
						{
							transform.shiftX = 0;
						}
					}
					else if(xPosTmp < xPosCurrent)
					{
						tmpXDistance = xPosTmp - xPosCurrent;
						if(tmpXDistance > (diffThreshold*xStep))
						{
							update = true;
							transform.shiftX = tmpXDistance - (diffThreshold*xStep);
						}
						else
						{
							transform.shiftX = 0;
						}
					}
					else
					{
						transform.shiftX = 0;
					}
				}
				else if(tmpNode->nodeID == (currentNode->nodeID + networkLevels[currentNode->level].xNodes))
				{
					// Bottom
					tmpYDistance = yPosTmp - yPosCurrent;
				/*	std::cout << "tmpYDistance (Bottom) = " << tmpYDistance << " yDistThresholdUpper = " 
					<< yDistThresholdUpper << " yDistThresholdLower = " << yDistThresholdLower << std::endl;*/
					
					// Y Axis
					if(tmpYDistance > yDistThresholdUpper)
					{
						update = true;
						transform.shiftY = tmpYDistance - yDistThresholdUpper;
					}
					else if(tmpYDistance < yDistThresholdLower)
					{
						update = true;
						transform.shiftY = yDistThresholdLower - tmpYDistance;
					}
					else 
					{
						transform.shiftY = 0;
					}
					
					// X Axis
					if(xPosTmp > xPosCurrent)
					{
						tmpXDistance = xPosTmp - xPosCurrent;
						if(tmpXDistance > (diffThreshold*xStep))
						{
							update = true;
							transform.shiftX = (tmpXDistance - (diffThreshold*xStep))*(-1);
						}
						else
						{
							transform.shiftX = 0;
						}
					}
					else if(xPosTmp < xPosCurrent)
					{
						tmpXDistance = xPosTmp - xPosCurrent;
						if(tmpXDistance > (diffThreshold*xStep))
						{
							update = true;
							transform.shiftX = tmpXDistance - (diffThreshold*xStep);
						}
						else
						{
							transform.shiftX = 0;
						}
					}
					else
					{
						transform.shiftX = 0;
					}
				}
				else if(tmpNode->nodeID == (currentNode->nodeID - networkLevels[currentNode->level].xNodes)-1)
				{
					// Top Left
					tmpYDistance =  yPosCurrent - yPosTmp;  // TOP
					tmpXDistance = xPosCurrent - xPosTmp;  // LEFT
					
				/*	std::cout << "tmpYDistance (TOP LEFT) = " << tmpYDistance << " yDistThresholdUpper = " 
						<< yDistThresholdUpper << " yDistThresholdLower = " << yDistThresholdLower 
						<< " tmpXDistance = " << tmpXDistance << " xDistThresholdUpper = " << xDistThresholdUpper
						<< " xDistThresholdLower = " << xDistThresholdLower << std::endl; */
					
					// Y Axis
					if(tmpYDistance > yDistThresholdUpper)
					{
						update = true;
						transform.shiftY = tmpYDistance - yDistThresholdUpper;
					}
					else if(tmpYDistance < yDistThresholdLower)
					{
						update = true;
						transform.shiftY = yDistThresholdLower - tmpYDistance;
					}
					else 
					{
						transform.shiftY = 0;
					}
					
					// X Axis
					if(tmpXDistance > xDistThresholdUpper)
					{
						update = true;
						transform.shiftX = tmpXDistance - xDistThresholdUpper;
					}
					else if(tmpXDistance < xDistThresholdLower)
					{
						update = true;
						transform.shiftX = xDistThresholdLower - tmpXDistance;
					}
					else
					{
						transform.shiftX = 0;
					}
				}
				else if(tmpNode->nodeID == (currentNode->nodeID - networkLevels[currentNode->level].xNodes)+1)
				{
					// Top Right
					tmpYDistance = yPosCurrent - yPosTmp;  // TOP
					tmpXDistance = xPosTmp - xPosCurrent;  // RIGHT
				/*	std::cout << "tmpYDistance (TOP RIGHT) = " << tmpYDistance << " yDistThresholdUpper = " 
						<< yDistThresholdUpper << " yDistThresholdLower = " << yDistThresholdLower 
						<< " tmpXDistance = " << tmpXDistance << " xDistThresholdUpper = " << xDistThresholdUpper
						<< " xDistThresholdLower = " << xDistThresholdLower << std::endl; */
					
					// Y Axis
					if(tmpYDistance > yDistThresholdUpper)
					{
						update = true;
						transform.shiftY = tmpYDistance - yDistThresholdUpper;
					}
					else if(tmpYDistance < yDistThresholdLower)
					{
						update = true;
						transform.shiftY = yDistThresholdLower - tmpYDistance;
					}
					else 
					{
						transform.shiftY = 0;
					}
					
					// X Axis
					if(tmpXDistance > xDistThresholdUpper)
					{
						update = true;
						transform.shiftX = tmpXDistance - xDistThresholdUpper;
					}
					else if(tmpXDistance < xDistThresholdLower)
					{
						update = true;
						transform.shiftX = xDistThresholdLower - tmpXDistance;
					}
					else
					{
						transform.shiftX = 0;
					}
				}
				else if(tmpNode->nodeID == (currentNode->nodeID + networkLevels[currentNode->level].xNodes)-1)
				{
					// Bottom Left
					tmpYDistance = yPosTmp - yPosCurrent;  // BOTTOM
					tmpXDistance = xPosCurrent - xPosTmp;  // LEFT
					
					/*std::cout << "tmpYDistance (BOTTOM LEFT) = " << tmpYDistance << " yDistThresholdUpper = " 
						<< yDistThresholdUpper << " yDistThresholdLower = " << yDistThresholdLower 
						<< " tmpXDistance = " << tmpXDistance << " xDistThresholdUpper = " << xDistThresholdUpper
						<< " xDistThresholdLower = " << xDistThresholdLower << std::endl; */
					
					// Y Axis
					if(tmpYDistance > yDistThresholdUpper)
					{
						update = true;
						transform.shiftY = tmpYDistance - yDistThresholdUpper;
					}
					else if(tmpYDistance < yDistThresholdLower)
					{
						update = true;
						transform.shiftY = yDistThresholdLower - tmpYDistance;
					}
					else 
					{
						transform.shiftY = 0;
					}
					
					// X Axis
					if(tmpXDistance > xDistThresholdUpper)
					{
						update = true;
						transform.shiftX = tmpXDistance - xDistThresholdUpper;
					}
					else if(tmpXDistance < xDistThresholdLower)
					{
						update = true;
						transform.shiftX = xDistThresholdLower - tmpXDistance;
					}
					else
					{
						transform.shiftX = 0;
					}
				}
				else if(tmpNode->nodeID == (currentNode->nodeID + networkLevels[currentNode->level].xNodes)+1)
				{
					// Bottom Right
					tmpYDistance = yPosTmp - yPosCurrent;  // BOTTOM
					tmpXDistance = xPosTmp - xPosCurrent;  // RIGHT
					
					/*std::cout << "tmpYDistance (BOTTOM RIGHT) = " << tmpYDistance << " yDistThresholdUpper = " 
						<< yDistThresholdUpper << " yDistThresholdLower = " << yDistThresholdLower 
						<< " tmpXDistance = " << tmpXDistance << " xDistThresholdUpper = " << xDistThresholdUpper
						<< " xDistThresholdLower = " << xDistThresholdLower << std::endl; */
					
					// Y Axis
					if(tmpYDistance > yDistThresholdUpper)
					{
						update = true;
						transform.shiftY = tmpYDistance - yDistThresholdUpper;
					}
					else if(tmpYDistance < yDistThresholdLower)
					{
						update = true;
						transform.shiftY = yDistThresholdLower - tmpYDistance;
					}
					else 
					{
						transform.shiftY = 0;
					}
					
					// X Axis
					if(tmpXDistance > xDistThresholdUpper)
					{
						update = true;
						transform.shiftX = tmpXDistance - xDistThresholdUpper;
					}
					else if(tmpXDistance < xDistThresholdLower)
					{
						update = true;
						transform.shiftX = xDistThresholdLower - tmpXDistance;
					}
					else
					{
						transform.shiftX = 0;
					}
				}
				
				if(update)
				{
					std::cout << "Transform [" << transform.shiftX << ", " 
							  << transform.shiftY << "] is to be applied to Node " << tmpNode->nodeID << "\n";
					//tmpNode->transform->shiftX += transform.shiftX;
					//tmpNode->transform->shiftY += transform.shiftY;
					if(tmpNode->transform->shiftX > 80 | tmpNode->transform->shiftY > 80)
					{
						std::cout << "tmpNode " << tmpNode->nodeID << " has transformation [" 
								  << tmpNode->transform->shiftX << ", " << tmpNode->transform->shiftY 
								  << "]\n";
						exit(-1);
						
					}
				}
			}
		}
	}
}

void ImageNetwork::checkNodeNeighboringMovements(int level)
{
	bool update = false;
	Transform transforms[9] = {0};
	int transformsAvailable[9] = {-1};
	Transform correctedTransform;
	double sumXTransforms = 0;
	double sumYTransforms = 0;
	int counter = 0;
	
	// Loop through nodes.
	ImageNetworkNode* currentNode = NULL;
	ImageNetworkNode* tmpNode = NULL;
	for(int n = 0; n < networkLevels[level].numNodes; n++)
	{
		//std::cout << "Currently on Node " << n << std::endl;
		// Get Node.
		for(int i = 0; i < 9; i++)
		{
			transformsAvailable[i] = -1;
		}

		currentNode = networkLevels[level].nodes[n];
		transforms[4] = *currentNode->transform;
		transformsAvailable[4] = 1;
		update = false;
		// Loop through node edges.
		for(int i = 0; i < networkLevels[currentNode->level].numNodes; i++)
		{
			if(networkLevels[currentNode->level].edges[currentNode->nodeID][i] == 1)
			{
				tmpNode = networkLevels[currentNode->level].nodes[i];
				
				// Decide whether horizontal vertical or diagonal.
				if( tmpNode->nodeID == currentNode->nodeID-1)
				{
					// Left
					transforms[3] = *tmpNode->transform;
					transformsAvailable[3] = 1;
				}
				else if(tmpNode->nodeID == currentNode->nodeID+1)
				{
					// Right
					transforms[5] = *tmpNode->transform;
					transformsAvailable[5] = 1;
				}
				else if(tmpNode->nodeID == (currentNode->nodeID - networkLevels[currentNode->level].xNodes))
				{
					// Top
					transforms[1] = *tmpNode->transform;
					transformsAvailable[1] = 1;
				}
				else if(tmpNode->nodeID == (currentNode->nodeID + networkLevels[currentNode->level].xNodes))
				{
					// Bottom
					transforms[7] = *tmpNode->transform;
					transformsAvailable[7] = 1;
				}
				else if(tmpNode->nodeID == (currentNode->nodeID - networkLevels[currentNode->level].xNodes)-1)
				{
					// Top Left
					transforms[0] = *tmpNode->transform;
					transformsAvailable[0] = 1;
				}
				else if(tmpNode->nodeID == (currentNode->nodeID - networkLevels[currentNode->level].xNodes)+1)
				{
					// Top Right
					transforms[2] = *tmpNode->transform;
					transformsAvailable[2] = 1;
				}
				else if(tmpNode->nodeID == (currentNode->nodeID + networkLevels[currentNode->level].xNodes)-1)
				{
					// Bottom Left
					transforms[6] = *tmpNode->transform;
					transformsAvailable[6] = 1;
				}
				else if(tmpNode->nodeID == (currentNode->nodeID + networkLevels[currentNode->level].xNodes)+1)
				{
					// Bottom Right
					transforms[8] = *tmpNode->transform;
					transformsAvailable[8] = 1;
				}
			}
		}	
		sumXTransforms = 0;
		sumYTransforms = 0;
		counter = 0;
		for(int i = 0; i < 9; i++)
		{
			if(transformsAvailable[i] == 1)
			{
				sumXTransforms += transforms[i].shiftX;
				sumYTransforms += transforms[i].shiftY;
				counter++;
			}
		}
		
		correctedTransform.shiftX = sumXTransforms/counter;
		correctedTransform.shiftY = sumYTransforms/counter;
		update = true;
		// Update if needed.
		if(update)
		{
			//std::cout << "Changes Node " << currentNode->nodeID << " from [" << currentNode->transform->shiftX
			//		  << ", " << currentNode->transform->shiftY << "] to [" << correctedTransform.shiftX
			//		  << ", " << correctedTransform.shiftY << "]\n";
			currentNode->transform->shiftX = correctedTransform.shiftX;
			currentNode->transform->shiftY = correctedTransform.shiftY;
		}
		
	}
	
}

int ImageNetwork::getNumberOfLevels()
{
	return numberOfLevels;
}

ImageResolutionLevel* ImageNetwork::getNetworkLevel(int level)
{
	return &networkLevels[level];
}

void ImageNetwork::exportENVIControlPointsImage2Image(int level, 
													  const char *outputFilePath)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment at top of file.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Base Image (x,y), Warp Image (x,y)\n";
		
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{
			outputFile << "\t" << networkLevels[level].nodes[i]->imageA->x
					   << "\t" << networkLevels[level].nodes[i]->imageA->y
					   << "\t" << (networkLevels[level].nodes[i]->imageB->x 
								   + networkLevels[level].nodes[i]->transform->shiftX)
					   << "\t" << (networkLevels[level].nodes[i]->imageB->y
								   + networkLevels[level].nodes[i]->transform->shiftY)
					   << std::endl;
			
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
}

void ImageNetwork::exportNetworkAsText(int level, 
									   const char *outputFilePath)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment at top of file.
		outputFile << "; Output network as a next file of level " << level << std::endl;
		outputFile << ";ImageA_X\tImageA_Y\tImageB_X\tImageB_Y\tWindow Size\tPixel Resolution\tPercentage Range\tmeasure Value" << std::endl;
		
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{
			outputFile << "\t" << networkLevels[level].nodes[i]->imageA->x
			<< "\t" << networkLevels[level].nodes[i]->imageA->y
			<< "\t" << (networkLevels[level].nodes[i]->imageB->x 
						+ networkLevels[level].nodes[i]->transform->shiftX)
			<< "\t" << (networkLevels[level].nodes[i]->imageB->y
						+ networkLevels[level].nodes[i]->transform->shiftY)
			<< "\t" << networkLevels[level].nodes[i]->windowSize
			<< "\t" << networkLevels[level].nodes[i]->pixelRes
			<< "\t" << networkLevels[level].nodes[i]->percentageRange
			<< "\t" << networkLevels[level].nodes[i]->transform->measureValue
			<< std::endl;
			
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
}

void ImageNetwork::exportENVIControlPointsMap2Image(int level, 
													const char *outputFilePath)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment at top of file.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Base Coordinates (x,y), Warp Image (x,y)\n";
		
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{
			outputFile << "\t" << networkLevels[level].nodes[i]->geoPosition->eastings
			<< "\t" << networkLevels[level].nodes[i]->geoPosition->northings
			<< "\t" << (networkLevels[level].nodes[i]->imageB->x 
						+ networkLevels[level].nodes[i]->transform->shiftX)
			<< "\t" << (networkLevels[level].nodes[i]->imageB->y
						+ networkLevels[level].nodes[i]->transform->shiftY)
			<< std::endl;
			
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
}

void ImageNetwork::exportENVIControlPointsImage2ImageScaled(int level, 
															const char *outputFilePath,
															double xScale,
															double yScale)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment at top of file.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Base Image (x,y), Warp Image (x,y)\n";
		
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{
			outputFile << "\t" << networkLevels[level].nodes[i]->imageA->x
			<< "\t" << networkLevels[level].nodes[i]->imageA->y
			<< "\t" << (((networkLevels[level].nodes[i]->imageB->x 
						+ networkLevels[level].nodes[i]->transform->shiftX)*xScale) + 0.5)
			<< "\t" << (((networkLevels[level].nodes[i]->imageB->y
						+ networkLevels[level].nodes[i]->transform->shiftY)*yScale) + 0.5)
			<< std::endl;
			
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
}

void ImageNetwork::exportENVIControlPointsMap2ImageScaled(int level, 
														  const char *outputFilePath,
														  double xScale,
														  double yScale)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment at top of file.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Base Coordinate (x,y), Warp Image (x,y)\n";
		
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{
			outputFile << "\t" << networkLevels[level].nodes[i]->geoPosition->eastings
			<< "\t" << networkLevels[level].nodes[i]->geoPosition->northings
			<< "\t" << (((networkLevels[level].nodes[i]->imageB->x 
						 + networkLevels[level].nodes[i]->transform->shiftX)*xScale) + 0.5)
			<< "\t" << (((networkLevels[level].nodes[i]->imageB->y
						 + networkLevels[level].nodes[i]->transform->shiftY)*yScale) + 0.5)
			<< std::endl;
			
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
}

void ImageNetwork::exportLevelEdges(int level, const char *outputFilePath)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{
			for(int j = 0; j < networkLevels[level].numNodes; j++)
			{
				outputFile << "\t" << networkLevels[level].edges[i][j];
			}
			outputFile << std::endl;
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
	
}

void ImageNetwork::exporttxtNetwork(int level, 
									const char *outputFilePath)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment at top of file.
		outputFile << "; This file contains the nodes which make up the network\n";
		outputFile << ";  and were extracted from software created at the University\n";
		outputFile << "; of Wales, Aberystwyth. For more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Base Image (x,y), Warp Image (x,y), Geo (x,y) nodeID\n";
		
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{
			outputFile << "\t" << networkLevels[level].nodes[i]->imageA->x
			<< "\t" << networkLevels[level].nodes[i]->imageA->y
			<< "\t" << (networkLevels[level].nodes[i]->imageB->x)
			<< "\t" << (networkLevels[level].nodes[i]->imageB->y)
			<< "\t" << networkLevels[level].nodes[i]->geoPosition->eastings
			<< "\t" << (networkLevels[level].nodes[i]->geoPosition->northings - 7140000)
			<< "\t" << networkLevels[level].nodes[i]->nodeID
			<< std::endl;
			
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
}

void ImageNetwork::exportNodeTransformationsAtlevel(int level, 
													const char *outputFilePath)
throw(FileOutputException)
{
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		for(int i = 0; i < networkLevels[level].numNodes; i++)
		{

				outputFile << networkLevels[level].nodes[i]->nodeID << ", "
						   << networkLevels[level].nodes[i]->imageA->x << ", " 
						   << networkLevels[level].nodes[i]->imageA->y << ", " 
						   << networkLevels[level].nodes[i]->transform->shiftX << ", " 
						   << networkLevels[level].nodes[i]->transform->shiftY << ", "
						   << (networkLevels[level].nodes[i]->imageA->x + networkLevels[level].nodes[i]->transform->shiftX) << ", " 
						   << (networkLevels[level].nodes[i]->imageA->y + networkLevels[level].nodes[i]->transform->shiftY) << ", " 
						   << networkLevels[level].nodes[i]->transform->measureValue << ", "
						   << networkLevels[level].nodes[i]->windowSize << "\n";
		}
	}
	else
	{
		throw new FileOutputException("Could not open file to output control points.", 
									  error_codes::cannot_create_output_file);
	}
}

ImageNetwork::~ImageNetwork()
{
	
}
