/*
 *  NodeQueue.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 16/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef NodeQueue_H
#define NodeQueue_H

#include "ImageNetworkStructures.h"
#include "QueueException.h"
#include "ErrorCodes.h"
#include <iostream>

struct NodeQueueElement{
	NodeQueueElement* next;
	ImageNetworkNode* node;
};

class NodeQueue
{
public:
	NodeQueue();
	void addNode(ImageNetworkNode* node);
	ImageNetworkNode* getHead()throw(QueueException);
	int getSize();
	void printQueue();
	~NodeQueue();
private:
	NodeQueueElement* head;
	NodeQueueElement* end;
	int size;
};

#endif
