/*
 *  ImageProcessingException.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "ImageProcessingException.h"

ImageProcessingException::ImageProcessingException(const char* message, const int error, const int image) : ImageRegistrationException(message, error)
{
	errorImage = image;
}

const int ImageProcessingException::getImageCode()
{
	return errorImage;
}

ImageProcessingException::~ImageProcessingException() throw()
{
	// do nothing
}
