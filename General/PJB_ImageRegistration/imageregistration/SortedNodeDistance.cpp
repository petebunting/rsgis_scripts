/*
 *  SortedNodeDistance.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 16/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "SortedNodeDistance.h"

SortedNodeDistance::SortedNodeDistance(ImageNetworkNode* startNode, double notifyThreshold)
{
	this->startNode = startNode;
	totalSize = 500;
	tableIncrement = 500;
	size = 0;
	list = new ListElement* [totalSize];
	this->notifyThreshold = notifyThreshold;
}

SortedNodeDistance::SortedNodeDistance(ImageNetworkNode* startNode, double notifyThreshold, int startSize)
{
	this->startNode = startNode;
	totalSize = startSize;
	tableIncrement = 500;
	size = 0;
	list = new ListElement* [totalSize];
	this->notifyThreshold = notifyThreshold;
}

SortedNodeDistance::SortedNodeDistance(ImageNetworkNode* startNode, double notifyThreshold, int startSize, int increment)
{
	this->startNode = startNode;
	totalSize = startSize;
	tableIncrement = increment;
	size = 0;
	list = new ListElement* [totalSize];
	this->notifyThreshold = notifyThreshold;
}

double SortedNodeDistance::calcDistance(ImageNetworkNode* node, float *levelScales)
{	
	double scaledImageAX = 0;
	double scaledImageAY = 0;
	
	scaledImageAX = node->imageA->x;
	scaledImageAY = node->imageA->y;
	
	for(int i = startNode->level; i > node->level; i--)
	{
		scaledImageAX = scaledImageAX / levelScales[i];
		scaledImageAY = scaledImageAY / levelScales[i];
	}
	
	double distance = sqrt(((startNode->imageA->x - scaledImageAX)*
							(startNode->imageA->x - scaledImageAX))+
						   ((startNode->imageA->y - scaledImageAY)*
							(startNode->imageA->y - scaledImageAY)));
	return distance;
}

int SortedNodeDistance::addNode(ImageNetworkNode* node, float *levelScales, bool update)
{
	int output = addNodeOutput::OK;
	ListElement* newElement = new ListElement;
	newElement->node = node;
	newElement->distance = this->calcDistance(node, levelScales);
	
	//std::cout << "Node being inputted: " << newElement->node->nodeID 
	//	<< " on level " << newElement->node->level << " with distance " << newElement->distance << std::endl;
	//this->print();
	int location = 0;
	bool dataContained = this->binaryChopSearch(newElement, &location);
	if(update & dataContained)
	{
		list[location] = newElement;
	}
	else if(!update & dataContained)
	{
		// Nothing to do.
	}
	else
	{
		// Need to bump down 
		this->bumpdown(location);
		
		// Insert
		list[location] = newElement;
	}		
	//this->print();
	//std::cout << " * Node Added * \n";
	return output;
}

ImageNetworkNode* SortedNodeDistance::getTopNode(double* distance)
{
	*distance = list[0]->distance;
	ImageNetworkNode* tmp = list[0]->node;
	this->bumpup(0);
	return tmp;
}

void SortedNodeDistance::peek(ImageNetworkNode* node)
{
	node = list[0]->node;
}

int SortedNodeDistance::getSize()
{
	return size;
}

void SortedNodeDistance::print()
{
	std::cout << " ************ Sorted Nodes (" << size << ")************* \n";
	if(size == 0)
	{
		std::cout << "List is empty!\n";
	}
	else if(list == NULL)
	{
		std::cout << "LIST IS NULL!\n";
	}
	else
	{
		for(int i = 0; i < size; i++)
		{
			std::cout << i << ") ";
			if(list[i] == NULL)
			{
				std::cout << "NULL\n";
			}
			else if(list[i]->node == NULL)
			{
				std::cout << "Node is NULL\n";
			}
			else
			{
				std::cout << "Node " << list[i]->node->nodeID << " on level " 
				<< list[i]->node->level << " with distance " << list[i]->distance << std::endl;
			}
		}
	}
}

void SortedNodeDistance::startIterator()
{
	iteratorIndex = 0;
}

bool SortedNodeDistance::hasNext()
{
	bool returnValue = false;
	if(iteratorIndex+1 < size)
	{
		returnValue = true;
	}
	
	return returnValue;
}

ImageNetworkNode* SortedNodeDistance::next(double* distance)
{
	*distance = list[iteratorIndex]->distance;
	return list[iteratorIndex++]->node; 
}

void SortedNodeDistance::printReverse()
{
	std::cout << " ************ Reversed Sorted Nodes (" << size << ")************* \n";
	if(size == 0)
	{
		std::cout << "List is empty!\n";
	}
	else
	{
		for(int i = size-1; i >= 0; i--)
		{
			std::cout << i << ") ";
			if(list[i] == NULL)
			{
				std::cout << "NULL\n";
			}
			else
			{
				std::cout << "Node " << list[i]->node->nodeID << " on level " 
				<< list[i]->node->level << " with distance " << list[i]->distance << std::endl;
			}
		}
	}
}

void SortedNodeDistance::startIteratorReverse()
{
	iteratorIndex = size-1;
}

bool SortedNodeDistance::hasNextReverse()
{
	bool returnValue = false;
	if(iteratorIndex-1 >= 0)
	{
		returnValue = true;
	}
	
	return returnValue;
}

ImageNetworkNode* SortedNodeDistance::nextReverse(double* distance)
{
	*distance = list[iteratorIndex]->distance;
	return list[iteratorIndex--]->node; 
}


bool SortedNodeDistance::binaryChopSearch(ListElement *data, int *location)
{	
	//this->print();
	MathUtils mathUtils;
	int min = 0;
	int max = size-1;
	int midPoint = 0;
	bool found = false;
	bool continueLoop = true;
	
	if(size == 0)
	{
		*location = 0;
		found = false;
		continueLoop = false;
	}
	//std::cout << "Start loop\n";
	while(continueLoop)
	{
		//std::cout << "Min = " << min << " Max = " << max << std::endl;
		if((max-min) < 2)
		{
			// If data in within table
			if(data->distance == list[min]->distance)
			{
				*location = min;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->distance == list[max]->distance )
			{
				*location = max;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->distance < list[min]->distance)
			{
				*location = min;
				found = false;
				continueLoop = false;
				break;
			}
			else if(data->distance > list[min]->distance &
					data->distance < list[max]->distance)
			{
				*location = min+1;
				found  = false;
				continueLoop = false;
				break;
			}
			else if(data->distance > list[max]->distance)
			{
				*location = max+1;
				found = false;
				continueLoop = false;
				break;
			}
			
		}
		else
		{
			midPoint = min + mathUtils.round((max-min)/2);
			//std::cout << "MidPoint = " << midPoint << " distance = " 
			//		  << list[midPoint]->distance << std::endl;
			if(data->distance == list[midPoint]->distance)
			{
				*location = midPoint;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->distance < list[midPoint]->distance)
			{
				max = midPoint;
			}
			else
			{
				min = midPoint;
			}
		}
	}
	/*if(*location > 0 & *location < size)
	{
		if(*location-1 >= 0)
		{
			std::cout << "Returned Location -1 = " << *location-1 << " distance = " 
			<< list[*location-1]->distance << std::endl;
		}
		
		std::cout << "Returned Location = " << *location << " distance = " 
				  << list[*location]->distance << std::endl;
		if(*location+1 < size)
		{
			std::cout << "Returned Location + 1 = " << *location+1 << " distance = " 
			<< list[*location+1]->distance << std::endl;
		}
	}
	else
	{
		std::cout << "location = " << *location << std::endl;
	}*/
	
	return found;
}

void SortedNodeDistance::increaseTableSize(int increaseBy)
{
	//std::cout << "Increaing list size (SortedNodes)\n";
	// Create new table
	ListElement** newTempTable = new ListElement* [totalSize + increaseBy];
	
	//Copy data from old to new table
	for(int i = 0; i < size; i++)
	{
		newTempTable[i] = list[i];
		list[i] = NULL;
	}
	
	delete list;
	
	//Assign new table to old
	list = newTempTable;
	
	// Alter totalSize	
	totalSize = totalSize + increaseBy;
	//this->print();
}

void SortedNodeDistance::bumpdown(int location)
{
	//std::cout << "bumping down in NetworkNodesLookUp. Location = " << location << " size = " 
	//		  << size << " total Size = " << totalSize << std::endl;
	int currentPointer = 0;
	if(size > 0)
	{
		currentPointer = size-1;
	}
	
	if(size+1 == totalSize)
	{
		//std::cout << "Increasing table size!\n";
		this->increaseTableSize(this->tableIncrement);
		//std::cout << "Now size = " << size << " and total size = " << totalSize << std::endl;
		//this->printTable();
	}
	
	while(currentPointer >= location)
	{
		//std::cout << "currentPointer = " << currentPointer << std::endl;
		list[currentPointer+1] = list[currentPointer];
		currentPointer--;
	}
	list[location] = NULL;
	size++;
}

void SortedNodeDistance::bumpup(int location)
{
	int currentPointer = location;
	
	while(currentPointer < size)
	{
		list[currentPointer] = list[currentPointer+1];
		currentPointer++;
	}
	size--;
}




SortedNodeDistance::~SortedNodeDistance()
{
	for(int i = 0; i < size; i++)
	{
		list[i]->node = NULL;
		delete list[i];
	}
	delete list;
}
