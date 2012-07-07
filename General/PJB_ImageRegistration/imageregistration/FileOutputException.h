/*
 *  FileOutputException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 15/01/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef FileOutputException_H
#define FileOutputException_H

#include "ImageRegistrationException.h"

class FileOutputException : public ImageRegistrationException
{
public:
	FileOutputException(const char* message, const int error);
	virtual ~FileOutputException() throw();
};

#endif
