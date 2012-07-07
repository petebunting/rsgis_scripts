/*
 *  ArrayUtils.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 14/01/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */


#ifndef ArrayUtils_H
#define ArrayUtils_H

class ArrayUtils
{
public:
	ArrayUtils();
	void setArray2Zeros(double *array, int length);
	void setArray2Zeros(int *array, int length);
	int findIndexOfMax(double *arr, int size);
	int findIndexOfMin(double *arr, int size);
};

#endif


