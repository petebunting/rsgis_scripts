/*
 *  ImageNetworkException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 08/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "ImageNetworkException.h"

ImageNetworkException::ImageNetworkException(const char* message, const int error) : ImageRegistrationException(message, error)
{
	// do nothing
}

ImageNetworkException::~ImageNetworkException() throw()
{
	// do nothing
}

