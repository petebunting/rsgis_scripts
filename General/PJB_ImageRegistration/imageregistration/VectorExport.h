/*
 *  VectorExport.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/03/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef VectorExport_H
#define VectorExport_H

#include "ogrsf_frmts.h"
#include <iostream>
#include "ogr_spatialref.h"

class VectorExport
{
public:
	VectorExport();
	void outputVector();
	~VectorExport();
};

#endif
