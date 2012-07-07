/*
 *  ImageOutputException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef ImageOutputException_H
#define ImageOutputException_H

#include "ImageRegistrationException.h"

class ImageOutputException : public ImageRegistrationException
{
public:
	ImageOutputException(const char* message, const int error);
	virtual ~ImageOutputException() throw();
};

#endif
