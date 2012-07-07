/*
 *  NetworkNodesLookUp.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 18/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef NetworkNodesLookUp_H
#define NetworkNodesLookUp_H

#include "ImageNetworkStructures.h"
#include <iostream>
#include "MathUtils.h"

class NetworkNodesLookUp
{
public:
	NetworkNodesLookUp();
	NetworkNodesLookUp(int startSize);
	NetworkNodesLookUp(int startSize, int increment);
	void insert(ImageNetworkNode *data, bool update);
	bool search(ImageNetworkNode *data);
	bool remove(ImageNetworkNode *data);
	int getSize();
	void printTable();
	void check4NULLs(const char* comment);
	~NetworkNodesLookUp();
private:
		bool binaryChopSearch(ImageNetworkNode *data, int *location);
	void increaseTableSize(int increaseBy);
	void bumpdown(int location);
	void bumpup(int location);
	ImageNetworkNode** list;
	int size;
	int totalSize;
	int tableIncrement;
};

#endif
