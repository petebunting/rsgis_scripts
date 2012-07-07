/*
 *  Queue.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 15/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef Queue_H
#define Queue_H

#include "NonusTreeNode.h"
#include "QueueException.h"
#include "ErrorCodes.h"
#include <iostream>

struct QueueNode{
	NonusTreeNode *data;
	QueueNode *next;
};

class Queue{
public: 
	Queue();
	NonusTreeNode* getNext();
	void add(NonusTreeNode *data);
	int getSize();
	~Queue();
private:
	QueueNode *head;
	QueueNode *end;
	int size;
};

#endif
