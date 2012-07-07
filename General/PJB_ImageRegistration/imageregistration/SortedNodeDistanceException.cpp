/*
 *  SortedNodeDistanceException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 16/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "SortedNodeDistanceException.h"

SortedNodeDistanceException::SortedNodeDistanceException(const char* message, const int error) : ImageRegistrationException(message, error)
{
	// do nothing
}

SortedNodeDistanceException::~SortedNodeDistanceException() throw()
{
	// do nothing
}
