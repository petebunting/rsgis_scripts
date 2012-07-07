/*
 *  TransformsTable.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 01/05/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef TransformsTable_H
#define TransformsTable_H

#include "TransformsTableException.h"
#include "ErrorCodes.h"
#include "ImageTiling.h"
#include <iostream>
#include "MathUtils.h"

class TransformsTable{
public: 
	TransformsTable();
	TransformsTable(int startSize);
	TransformsTable(int startSize, int increment);
	void insert(Transform *data, bool update)
		throw(TransformsTableException);
	bool search(Transform *data)
		throw(TransformsTableException);
	bool remove(Transform *data)
		throw(TransformsTableException);
	Transform findMaxMinMeasure(bool max);
	bool getTransform(double shiftX, double shiftY, Transform *transform)
		throw(TransformsTableException);
	int getSize();
	void printTable();
	~TransformsTable();
private:
	bool binaryChopSearch(Transform *data, int *location)
		throw(TransformsTableException);
	void increaseTableSize(int increaseBy)
		throw(TransformsTableException);
	void bumpdown(int location)
		throw(TransformsTableException);
	void bumpup(int location);
	Transform *table;
	int size;
	int totalSize;
	int tableIncrement;
};

#endif
