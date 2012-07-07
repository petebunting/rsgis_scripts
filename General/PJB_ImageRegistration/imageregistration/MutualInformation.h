/*
 *  MutualInformation.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 09/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef MI_H
#define MI_H

#include "JointHistogram.h"
#include <iostream>
#include "math.h"
#include "ImageRegistrationException.h"
#include "ErrorCodes.h"

class MutualInformation
{
public:
	MutualInformation();
	double calcMutualInformation(JointHistogram &jointHistogram);
	~MutualInformation();
};
#endif
