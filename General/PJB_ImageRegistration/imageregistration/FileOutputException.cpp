/*
 *  FileOutputException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 15/01/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "FileOutputException.h"

FileOutputException::FileOutputException(const char* message, const int error) : ImageRegistrationException(message, error)
{
	// do nothing
}

FileOutputException::~FileOutputException() throw()
{
	// do nothing
}
