/*
 *  NodeQueue.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 16/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "NodeQueue.h"

NodeQueue::NodeQueue()
{
	size = 0;
}

void NodeQueue::addNode(ImageNetworkNode* node)
{
	NodeQueueElement *element = new NodeQueueElement;
	element->node = node;
	element->next = 0;
	if(size == 0)
	{
		end = element;
		head = element;
	}
	else
	{
		end->next = element;
		end = element;
	}
	size++;
}

ImageNetworkNode* NodeQueue::getHead()
throw(QueueException)
{
	ImageNetworkNode *tmpImageNetworkNode = NULL;
	if(size == 0)
	{
		throw QueueException("Queue is empty you cannot retrieve anything from here.", error_codes::empty_queue);
	}
	else 
	{
		tmpImageNetworkNode = head->node;
		NodeQueueElement *tmpNode = head;
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
	return tmpImageNetworkNode;
}

int NodeQueue::getSize()
{
	return size;
}

void NodeQueue::printQueue()
{
	std::cout << "\n******** Node Queue (" << size << ") ********\n";
	if(size == 0)
	{
		std::cout << "Queue is empty!\n";
	}
	else
	{
		NodeQueueElement* element = head;
		if(head->next == NULL)
		{
			std::cout << "head->next is NULL!\n";
		}
		for(int i = 0; i < size; i++)
		{
			std::cout << i << ") ";
			if(element == NULL)
			{
				std::cout << "NULL\n";
				break;
			}
			else
			{
				std::cout << "Node ID " << element->node->nodeID << " on level " 
						  << element->node->level << std::endl;
			}
			element = element->next;
		}
	}
	std::cout << std::endl;
}

NodeQueue::~NodeQueue()
{
	try
	{
		if(head != NULL)
		{
			while( size > 0)
			{
				this->getHead();
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
