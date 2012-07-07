/*
 *  QueueException.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef QueueException_H
#define QueueException_H

#include "ImageRegistrationException.h"

class QueueException : public ImageRegistrationException
{
public:
	QueueException(const char* message, const int error);
	virtual ~QueueException() throw();
};

#endif
