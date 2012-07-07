/*
 *  ImageNotAvailableException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef ImageNotAvailableException_H
#define ImageNotAvailableException_H

#include "ImageRegistrationException.h"

class ImageNotAvailableException : public ImageRegistrationException
{
public:
	ImageNotAvailableException(const char* message, const int error);
	virtual ~ImageNotAvailableException() throw();
};

#endif
