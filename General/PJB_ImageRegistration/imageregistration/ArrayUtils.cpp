/*
 *  ArrayUtils.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 14/01/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "ArrayUtils.h"


ArrayUtils::ArrayUtils()
{
	
}

void ArrayUtils::setArray2Zeros(double *array, int length)
{
	for(int i = 0; i < length; i++)
	{
		array[i] = 0;
	}
}

void ArrayUtils::setArray2Zeros(int *array, int length)
{
	for(int i = 0; i < length; i++)
	{
		array[i] = 0;
	}
}

int ArrayUtils::findIndexOfMax(double *arr, int size)
{
	double maxValue = arr[0];
	int maxIndex = 0;
	
	for(int i = 0; i < size; i++)
	{
		if(maxValue < arr[i])
		{
			maxIndex = i;
			maxValue = arr[i];
		}
	}
	return maxIndex;
}

int ArrayUtils::findIndexOfMin(double *arr, int size)
{
	double minValue = arr[0];
	int minIndex = 0;
	
	for(int i = 0; i < size; i++)
	{
		if(minValue > arr[i])
		{
			minIndex = i;
			minValue = arr[i];
		}
	}
	return minIndex;
}
