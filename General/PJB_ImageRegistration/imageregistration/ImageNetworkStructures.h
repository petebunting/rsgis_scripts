/*
 *  ImageNetworkStructures.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 08/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef ImageNetworkStructures_H
#define ImageNetworkStructures_H

#include "ImageTiling.h"

struct PointPxlCoords{
	int x;
	int y;
};

struct PointGeoCoords{
	float eastings;
	float northings;
};

struct ImageNetworkNode{
	int nodeID;
	PointPxlCoords *imageA;
	PointPxlCoords *imageB;
	PointGeoCoords *geoPosition;
	int windowSize;
	Transform *transform;
	int level;
	double pixelRes;
	double percentageRange;
};

struct ImageResolutionLevel{
	ImageNetworkNode** nodes;
	float** edges;
	int xNodeGap;
	int yNodeGap;
	int xNodes;
	int yNodes;
	int numNodes;
	double totalMeasures;
	int numMeasures;
	double meanMeasure;
};

#endif

