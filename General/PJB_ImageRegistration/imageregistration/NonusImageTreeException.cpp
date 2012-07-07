/*
 *  NonusImageTreeException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "NonusImageTreeException.h"

NonusImageTreeException::NonusImageTreeException(const char* message, const int error) : ImageRegistrationException(message, error)
{
	// do nothing
}

NonusImageTreeException::~NonusImageTreeException() throw()
{
	// do nothing
}
