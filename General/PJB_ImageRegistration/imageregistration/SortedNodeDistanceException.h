/*
 *  SortedNodeDistanceException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 16/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef SortedNodeDistanceException_H
#define SortedNodeDistanceException_H

#include "ImageRegistrationException.h"

class SortedNodeDistanceException : public ImageRegistrationException
{
public:
	SortedNodeDistanceException(const char* message, const int error);
	virtual ~SortedNodeDistanceException() throw();
};

#endif
