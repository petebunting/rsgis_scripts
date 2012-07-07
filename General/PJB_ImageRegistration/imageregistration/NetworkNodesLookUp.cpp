/*
 *  NetworkNodesLookUp.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 18/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "NetworkNodesLookUp.h"

NetworkNodesLookUp::NetworkNodesLookUp()
{
	totalSize = 500;
	tableIncrement = 500;
	size = 0;
	list = new ImageNetworkNode* [totalSize];
}

NetworkNodesLookUp::NetworkNodesLookUp(int startSize)
{
	totalSize = startSize;
	tableIncrement = 500;
	size = 0;
	list = new ImageNetworkNode* [totalSize];
}

NetworkNodesLookUp::NetworkNodesLookUp(int startSize, int increment)
{
	totalSize = startSize;
	tableIncrement = increment;
	size = 0;
	list = new ImageNetworkNode* [totalSize];
}

void NetworkNodesLookUp::insert(ImageNetworkNode *data, bool update)
{
	bool dataContained;
	int location = 0;
	dataContained = this->binaryChopSearch(data, &location);
	if(update & dataContained)
	{
		list[location] = data;
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
		list[location] = data;
	}
}

bool NetworkNodesLookUp::search(ImageNetworkNode *data)
{
	int location;
	return this->binaryChopSearch(data, &location);
}

bool NetworkNodesLookUp::remove(ImageNetworkNode *data)
{
	bool dataContained;
	bool successful;
	int location = 0;
	
	dataContained = this->binaryChopSearch(data, &location);
	if(dataContained)
	{
		// Bump up writing over element to be removed
		this->bumpup(location);
		successful = true;
	}
	else
	{
		successful = false;
	}

	return successful;
}

int NetworkNodesLookUp::getSize()
{
	return size;
}

void NetworkNodesLookUp::printTable()
{
	std::cout << "\n************ Nodes Lookup Table *************\n";
	if(size == 0)
	{
		std::cout << "Lookup table is empty\n";
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
			else
			{
				std::cout << "Node " << list[i]->nodeID << " on level " << list[i]->level << std::endl;
			}
		}
	}
	std::cout << std::endl;
}

void NetworkNodesLookUp::check4NULLs(const char* comment)
{
	if(size == 0)
	{
		std::cout << "Lookup table is empty\n";
	}
	else
	{
		for(int i = 0; i < size; i++)
		{
			if(list[i] == NULL)
			{
				std::cout << i << ") " << "NULL -- " << comment << " -- \n";
			}
		}
	}
}


bool NetworkNodesLookUp::binaryChopSearch(ImageNetworkNode *data, int *location)
{	
	//std::cout << "Performing BinaryChop NetworkNodesLookUp\n";
	//std::cout << "Size = " << size << std::endl;
	/*for(int i = 0; i < size; i++)
	{
		std::cout << i;
		if( list[i] == NULL)
		{
			std::cout << " is NULL\n";
		}
		else
		{
			std::cout << " is Node " << list[i]->nodeID << std::endl;
		}
	}*/
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
			if(data->nodeID == list[min]->nodeID)
			{
				*location = min;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->nodeID == list[max]->nodeID )
			{
				*location = max;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->nodeID < list[min]->nodeID)
			{
				*location = min;
				found = false;
				continueLoop = false;
				break;
			}
			else if(data->nodeID > list[min]->nodeID &
					data->nodeID < list[max]->nodeID)
			{
				*location = min+1;
				found  = false;
				continueLoop = false;
				break;
			}
			else if(data->nodeID > list[max]->nodeID)
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

			if(data->nodeID == list[midPoint]->nodeID)
			{
				*location = midPoint;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->nodeID < list[midPoint]->nodeID)
			{
				max = midPoint;
			}
			else
			{
				min = midPoint;
			}
		}
	}
	//std::cout << "Finished BinaryChop NetworkNodesLookUp\n";
	return found;
}

void NetworkNodesLookUp::increaseTableSize(int increaseBy)
{
	//std::cout << "Increasing size of lookup!\n";
	// Create new table
	ImageNetworkNode** newTempTable = new ImageNetworkNode* [totalSize + increaseBy];
	
	//Copy data from old to new table
	for(int i = 0; i < size; i++)
	{
		newTempTable[i] = list[i];
		//list[i] = NULL;
	}
		
	delete list;
	
	//Assign new table to old
	list = newTempTable;
	
	//delete newTempTable;
	
	// Alter totalSize	
	totalSize = totalSize + increaseBy;
}

void NetworkNodesLookUp::bumpdown(int location)
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

void NetworkNodesLookUp::bumpup(int location)
{
	int currentPointer = location;
	
	while(currentPointer < size)
	{
		list[currentPointer] = list[currentPointer+1];
		currentPointer++;
	}
	size--;
}

NetworkNodesLookUp::~NetworkNodesLookUp()
{
	delete list;
}
