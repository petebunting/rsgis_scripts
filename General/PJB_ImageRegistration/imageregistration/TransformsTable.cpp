/*
 *  TransformsTable.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 01/05/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "TransformsTable.h"

TransformsTable::TransformsTable()
{
	table = new Transform[100];
	tableIncrement = 100;
	size = 0;
	totalSize = 100;
}

TransformsTable::TransformsTable(int startSize)
{
	table = new Transform[startSize];
	tableIncrement = 100;
	size = 0;
	totalSize = startSize;
}

TransformsTable::TransformsTable(int startSize, int increment)
{
	table = new Transform[startSize];
	tableIncrement = increment;
	size = 0;
	totalSize = startSize;
}

void TransformsTable::insert(Transform *data, bool update)
	throw(TransformsTableException)
{
	bool dataContained;
	int location = 0;
	try
	{
		dataContained = this->binaryChopSearch(data, &location);
		
		if(update & dataContained)
		{
			table[location].measureValue = data->measureValue;
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
			table[location].shiftX = data->shiftX;
			table[location].shiftY = data->shiftY;
			table[location].measureValue = data->measureValue;
		}
	}
	catch(TransformsTableException e)
	{
		//Tidy any elements if error code == XXX then tidy Y.
		throw e;
	}
}

bool TransformsTable::search(Transform *data)
	throw(TransformsTableException)
{
	int location;
	return this->binaryChopSearch(data, &location);
}

bool TransformsTable::getTransform(double shiftX, double shiftY, Transform *transform)
throw(TransformsTableException)
{
	Transform tmp;
	bool available = false;
	tmp.shiftX = shiftX;
	tmp.shiftY = shiftY;
	int location;
	available = this->binaryChopSearch(&tmp, &location);
	if(available)
	{
		transform->shiftX = table[location].shiftX;
		transform->shiftY = table[location].shiftY;
		transform->measureValue = table[location].measureValue;
	}
	else
	{
		transform = NULL;
	}
	return available;
}

bool TransformsTable::remove(Transform *data)
	throw(TransformsTableException)
{
	bool dataContained;
	bool successful;
	int location = 0;
	try
	{
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
	}
	catch(TransformsTableException e)
	{
		//Tidy any elements if error code == XXX then tidy Y.
		throw e;
	}
	return successful;
}

int TransformsTable::getSize()
{
	return this->size;
}
void TransformsTable::printTable()
{
	if(size == 0)
	{
		std::cout << "Empty Table\n";
	}
	else
	{
		for(int i = 0; i < size; i++)
		{
			std::cout << "" << i << ": [" << table[i].shiftX << "," 
					<< table[i].shiftY << "] " << table[i].measureValue 
					<< std::endl;
		}
	}
}

TransformsTable::~TransformsTable()
{
	delete table;
}

bool TransformsTable::binaryChopSearch(Transform *data, int *location)
	throw(TransformsTableException)
{
	MathUtils mathUtils;
	int min = 0;
	int max = size-1;
	int midPoint = 0;
	bool found;
	bool continueLoop = true;
	if(size == 0)
	{
		*location = 0;
		found = false;
		continueLoop = false;
	}
	
	while(continueLoop)
	{
		if((max-min) < 2)
		{
			// If data in within table
			if(data->shiftX == table[min].shiftX & data->shiftY == table[min].shiftY)
			{
				*location = min;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->shiftX == table[max].shiftX & data->shiftY == table[max].shiftY)
			{
				*location = max;
				found = true;
				continueLoop = false;
				break;
			}
			
			if(data->shiftX == table[min].shiftX)
			{
				if(data->shiftY < table[min].shiftY)
				{
					*location = min;
					found = false;
					continueLoop = false;
					break;
				}
				else
				{
					*location = min+1;
					found = false;
					continueLoop = false;
					break;
				}
			}
			else if(data->shiftX == table[max].shiftX)
			{
				if(data->shiftY < table[max].shiftY)
				{
					*location = max;
					found = false;
					continueLoop = false;
					break;
				}
				else
				{
					*location = max+1;
					found = false;
					continueLoop = false;
					break;
				}
			}
			else
			{
				if(data->shiftX < table[min].shiftX)
				{
					*location = min;
					found = false;
					continueLoop = false;
					break;
				}
				else if(data->shiftX > table[min].shiftX &
						data->shiftX < table[max].shiftX)
				{
					*location = max;
					found = false;
					continueLoop = false;
					break;
				}
				else
				{
					*location = max+1;
					found = false;
					continueLoop = false;
					break;					
				}
			}
		}
		else
		{
			midPoint = min + mathUtils.round((max-min)/2);
			if(data->shiftX == table[midPoint].shiftX & data->shiftY == table[midPoint].shiftY)
			{
				*location = midPoint;
				found = true;
				continueLoop = false;
				break;
			}
			else if(data->shiftX == table[midPoint].shiftX)
			{
				// Sort using Y axis.
				if(data->shiftY < table[midPoint].shiftY)
				{
					max = midPoint;
				}
				else if(data->shiftY > table[midPoint].shiftY)
				{
					min = midPoint;
				}
				else
				{
					throw TransformsTableException("Error in search cannot find place for element! line 317",
												   error_codes::cannot_find_place4node);
				}
			}
			else
			{
				//Sort Using X axis
				if(data->shiftX < table[midPoint].shiftX)
				{
					max = midPoint;
				}
				else if(data->shiftX > table[midPoint].shiftX)
				{
					min = midPoint;
				}
				else
				{
					throw TransformsTableException("Error in search cannot find place for element! line 334",
												   error_codes::cannot_find_place4node);
				}
			}
		}
	}

	return found;
}

void TransformsTable::increaseTableSize(int increaseBy)
	throw(TransformsTableException)
{
		//std::cout << "size increasing\n";	
		
	// Create new table
	Transform *newTempTable = new Transform[totalSize + increaseBy];
	
	//Copy data from old to new table
	for(int i = 0; i < size; i++)
	{
		newTempTable[i] = table[i];
	}
	
	// delete old table;
	delete table;
	
	//Assign new table to old
	table = newTempTable;
	
	// Delete temp table
	delete newTempTable;
	
	// Alter totalSize	
	totalSize = totalSize + increaseBy;
}

void TransformsTable::bumpdown(int location)
	throw(TransformsTableException)
{
	int currentPointer = 0;
	if(size > 0)
	{
		currentPointer = size-1;
	}
		
	if(size+1 == totalSize)
	{
		this->increaseTableSize(this->tableIncrement);
	}
	
	while(currentPointer >= location)
	{
		table[currentPointer+1] = table[currentPointer];
		currentPointer--;
	}
	size++;
}

void TransformsTable::bumpup(int location)
{
	int currentPointer = location;
	
	while(currentPointer < size)
	{
		table[currentPointer] = table[currentPointer+1];
		currentPointer++;
	}
	size--;
}

Transform TransformsTable::findMaxMinMeasure(bool max)
{
	Transform transform = table[0];
	for(int i = 1; i < size; i++)
	{
		if(max)
		{
			if(table[i].measureValue > transform.measureValue)
			{
				transform = table[i];
			}
		}
		else
		{
			if(table[i].measureValue < transform.measureValue)
			{
				transform = table[i];
			}
		}
	}
	return transform;
}
