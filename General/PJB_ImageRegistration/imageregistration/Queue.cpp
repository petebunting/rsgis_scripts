/*
 *  Queue.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 15/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "Queue.h"

Queue::Queue()
{
	size = 0;
}

NonusTreeNode* Queue::getNext()
{
	NonusTreeNode *tmpTreeNode = NULL;
	if(size == 0)
	{
		throw QueueException("Queue is empty you cannot retrieve anything from here.", error_codes::empty_queue);
	}
	else 
	{
		tmpTreeNode = head->data;
		QueueNode *tmpNode = head;
		if(head->next == NULL )
		{
			size = 0;
			end = 0;
			head = 0;
		}
		else
		{
			head = head->next;
			size--;
		}
		if( tmpNode != NULL )
		{
			delete tmpNode;
		}
	}
	return tmpTreeNode;
}

void Queue::add(NonusTreeNode *data)
{
	QueueNode *node = new QueueNode;
	node->data = data;
	node->next = 0;
	if(size == 0)
	{
		end = node;
		head = node;
	}
	else
	{
		end->next = node;
		end = node;
	}
	size++;
	if(end->data == NULL)
	{
		std::cout << "Data at the end node is NULL!!\n";
	}
}

int Queue::getSize()
{
	return size;
}

Queue::~Queue()
{
	try
	{
		if(head != NULL)
		{
			while( size > 0)
			{
				this->getNext();
			}
		}
	}
	catch(QueueException e)
	{
		if(e.getErrorCode() == error_codes::empty_queue)
		{
			// do nothing.
		}
	}
	if(end != NULL)
	{
		delete end;
	}
}
