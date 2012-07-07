/*
 *  DefiniensException.cpp
 *  DefiniensRulesetColours
 *
 *  Created by Pete Bunting on 22/02/2008.
 *  Copyright 2008 Aberystwyth University. All rights reserved.
 *
 */

#include "DefiniensException.h"

DefiniensException::DefiniensException(const char* message) : exception()
{
	msgs = message;
}

const char* DefiniensException::what()
{
	return msgs;
}

DefiniensException::~DefiniensException() throw()
{
	// do nothing
}
