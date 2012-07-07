/*
 *  TransformsTableException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 01/05/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "TransformsTableException.h"

TransformsTableException::TransformsTableException(const char* message, const int error) : ImageRegistrationException(message, error)
{
	// do nothing
}

TransformsTableException::~TransformsTableException() throw()
{
	// do nothing
}
