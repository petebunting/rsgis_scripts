/*
 *  NonusTreeNode.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 15/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef NonusTreeNode_H
#define NonusTreeNode_H


#include "ImageTiling.h"

struct NonusTreeNode{
	NonusTreeNode *children[9];
	Transform *TileTransformation;
	TileCoords *tileCoords;
	double stddevtileref;
	double stddevtilefloat;
	int nodeID;
};

#endif

