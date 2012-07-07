/*
 *  NonusImageTree.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 15/11/2005.
 *  Copyright 2005  Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */
#ifndef NonusImageTree_H
#define NonusImageTree_H

#include "ImageOverlap.h"
#include "Queue.h"
#include <iostream>
#include <fstream>
#include "NonusTreeNode.h"
#include "NonusImageTreeException.h"
#include "ErrorCodes.h"
#include "FileOutputException.h"

struct TreeLevel {
	int level;
	int nodesAtLevel;
	int totalNodes;
	int xDistance;
	int yDistance;
	double angularDistance;
};

class NonusImageTree
{
public:
	NonusImageTree();
	TileCoords* setRoot(Transform imageTransformation, TileCoords tileCoords, double stddevref, double stddevfloat)
		throw(NonusImageTreeException);
	NonusTreeNode* addNode(TileCoords *tileCoords, double stddevref, double stddevfloat)
		throw(NonusImageTreeException);
	void printTree();
	void printTreeInFull();
	void writeMap2Image2EnviGcpsFile(const char *outputFilePath, int treeDepth)
		throw(FileOutputException, NonusImageTreeException);
	void write2EnviGcpsFile(const char *outputFilePath, int treeDepth)
		throw(FileOutputException, NonusImageTreeException);
	void writeMap2Image2EnviGcpsFile(const char *outputFilePath, int treeDepth, double xScale, double yScale)
		throw(FileOutputException, NonusImageTreeException);
	void write2EnviGcpsFile(const char *outputFilePath, int treeDepth, double xScale, double yScale)
		throw(FileOutputException, NonusImageTreeException);
	void estimateRequiredNodes(int xPixels, int yPixels, int minTileSize, TreeLevel *treeLevels, int numLevels);

	int estimateNumberLevels(int xPixels, int yPixels, int minTileSize);
	int getNumNodes();
	int getNodesAtLevel(int level, NonusTreeNode **nodes, int length)
		throw(NonusImageTreeException);
	NonusTreeNode* getRoot();
	~NonusImageTree();
protected:
	NonusTreeNode *root;
	bool rootset;
	int treeSize;
};

#endif
