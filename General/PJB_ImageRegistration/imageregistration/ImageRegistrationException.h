/*
 *  ImageRegistrationException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef ImageRegistrationException_H
#define ImageRegistrationException_H

#include <exception>
#include <string>

class ImageRegistrationException : public std::exception
{
public:
	ImageRegistrationException(const char* message, const int error);
	virtual ~ImageRegistrationException() throw();
	virtual const char* what();
	const int getErrorCode();
private:
	const char* msgs;
	int errorCode;
};

#endif
