/*
 *  TransformsTableException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 01/05/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef TransformsTableException_H
#define TransformsTableException_H

#include "ImageRegistrationException.h"

class TransformsTableException : public ImageRegistrationException
{
public:
	TransformsTableException(const char* message, const int error);
	virtual ~TransformsTableException() throw();
};

#endif
