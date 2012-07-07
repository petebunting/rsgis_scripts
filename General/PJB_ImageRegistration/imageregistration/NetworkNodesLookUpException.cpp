/*
 *  NetworkNodesLookUpException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 18/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "NetworkNodesLookUpException.h"

NetworkNodesLookUpException::NetworkNodesLookUpException(const char* message, const int error) : ImageRegistrationException(message, error)
{
	// do nothing
}

NetworkNodesLookUpException::~NetworkNodesLookUpException() throw()
{
	// do nothing
}
