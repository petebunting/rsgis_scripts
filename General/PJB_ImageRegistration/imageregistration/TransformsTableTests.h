/*
 *  TransformsTableTests.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 01/05/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef TransformsTable_TEST_H
#define TransformsTable_TEST_H

#include "TransformsTableException.h"
#include "TransformsTable.h"
#include "ErrorCodes.h"
#include "ImageTiling.h"
#include <iostream>
#include <cstdlib>
#include <ctime>
#include "MathUtils.h"

class TransformsTableTests{
public: 
	TransformsTableTests();
	void runTests();
	~TransformsTableTests();
private:
		
};

#endif
