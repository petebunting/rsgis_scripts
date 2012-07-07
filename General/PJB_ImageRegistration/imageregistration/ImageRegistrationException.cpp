/*
 *  ImageRegistrationException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "ImageRegistrationException.h"

ImageRegistrationException::ImageRegistrationException(const char* message, int error) : exception()
{
	msgs = message;
	errorCode = error;
}

const char* ImageRegistrationException::what()
{
	return msgs;
}

const int ImageRegistrationException::getErrorCode()
{
	return errorCode;
}

ImageRegistrationException::~ImageRegistrationException() throw()
{
	// do nothing
}
