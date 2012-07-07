/*
 *  SortedNodeDistance.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 16/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef SortedNodeDistance_H
#define SortedNodeDistance_H

#include "ImageNetworkStructures.h"
#include "MathUtils.h"

struct ListElement{
	ImageNetworkNode* node;
	double distance;
};

namespace addNodeOutput
{
	enum 
	{
		exists = -1,
		OK = 0,
		overThreshold = 1
	};
}

class SortedNodeDistance
{
public: 
	SortedNodeDistance(ImageNetworkNode* startNode, double notifyThreshold);
	SortedNodeDistance(ImageNetworkNode* startNode, double notifyThreshold, int startSize);
	SortedNodeDistance(ImageNetworkNode* startNode, double notifyThreshold, int startSize, int increment);
	double calcDistance(ImageNetworkNode* node, float *levelScales);
	int addNode(ImageNetworkNode* node, float *levelScales, bool update);
	ImageNetworkNode* getTopNode(double* distance);
	void peek(ImageNetworkNode* node);
	int getSize();
	void print();
	void startIterator();
	bool hasNext();
	ImageNetworkNode* next(double* distance);
	void printReverse();
	void startIteratorReverse();
	bool hasNextReverse();
	ImageNetworkNode* nextReverse(double* distance);
	~SortedNodeDistance();
	
private:
	bool binaryChopSearch(ListElement *data, int *location);
	void increaseTableSize(int increaseBy);
	void bumpdown(int location);
	void bumpup(int location);	
	ImageNetworkNode* startNode;
	ListElement** list;
	int size;
	double notifyThreshold;
	int totalSize;
	int tableIncrement;
	int iteratorIndex;
};

#endif
