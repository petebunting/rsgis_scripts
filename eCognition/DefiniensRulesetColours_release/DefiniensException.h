/*
 *  DefiniensException.h
 *  DefiniensRulesetColours
 *
 *  Created by Pete Bunting on 22/02/2008.
 *  Copyright 2008 Aberystwyth University. All rights reserved.
 *
 */

#ifndef DefiniensException_H
#define DefiniensException_H

#include <exception>

class DefiniensException : public std::exception
{
public:
	DefiniensException(const char* message);
	virtual ~DefiniensException() throw();
	virtual const char* what();
private:
	const char* msgs;
};

#endif
