/*
 *  QueueException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "QueueException.h"

QueueException::QueueException(const char* message, const int error) : ImageRegistrationException(message, error)
{
	// do nothing
}

QueueException::~QueueException() throw()
{
	// do nothing
}
