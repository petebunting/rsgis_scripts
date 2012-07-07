/*
 *  ImageNetworkException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 08/06/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef ImageNetworkException_H
#define ImageNetworkException_H

#include "ImageRegistrationException.h"

class ImageNetworkException : public ImageRegistrationException
{
public:
	ImageNetworkException(const char* message, const int error);
	virtual ~ImageNetworkException() throw();
};

#endif
