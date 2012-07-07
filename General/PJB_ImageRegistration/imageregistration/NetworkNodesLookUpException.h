/*
 *  NetworkNodesLookUpException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 18/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef NetworkNodesLookUpException_H
#define NetworkNodesLookUpException_H

#include "ImageRegistrationException.h"

class NetworkNodesLookUpException : public ImageRegistrationException
{
public:
	NetworkNodesLookUpException(const char* message, const int error);
	virtual ~NetworkNodesLookUpException() throw();
};

#endif
