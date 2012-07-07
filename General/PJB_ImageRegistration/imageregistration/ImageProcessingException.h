/*
 *  ImageProcessingException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef ImageProcessingException_H
#define ImageProcessingException_H

#include "ImageRegistrationException.h"

class ImageProcessingException : public ImageRegistrationException
{
public:
	ImageProcessingException(const char* message, const int error, const int image);
	virtual ~ImageProcessingException() throw();
	const int getImageCode();
private:
	int errorImage;
};

#endif
