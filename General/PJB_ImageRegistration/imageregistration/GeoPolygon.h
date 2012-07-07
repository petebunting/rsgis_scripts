/*
 *  AberPolygon.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/03/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef GeoPolygon_H
#define GeoPolygon_H

#include "GeoPoint.h"
#include <iostream>

struct Boundary{
	GeoPoint *point;
	Boundary *next;
	Boundary *prev;
};

class GeoPolygon
{
public:
	GeoPolygon();
	void addPoints(GeoPoint *points, int num);
	void addPoint(GeoPoint *point);
	void getPoints(GeoPoint *points);
	int getSize();
	void exportGML(char *gml);
	~GeoPolygon();
protected:
	Boundary *first;
	Boundary *end;
	int size;
};

#endif
