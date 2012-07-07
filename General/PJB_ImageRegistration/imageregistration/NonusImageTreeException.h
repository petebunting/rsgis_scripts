/*
 *  NonusImageTreeException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef NonusImageTreeException_H
#define NonusImageTreeException_H

#include "ImageRegistrationException.h"

class NonusImageTreeException : public ImageRegistrationException
{
public:
	NonusImageTreeException(const char* message, const int error);
	virtual ~NonusImageTreeException() throw();
};

#endif
