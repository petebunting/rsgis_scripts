/*
 *  AberPoint.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/03/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef GeoPoint_H
#define GeoPoint_H

//#include <iostream>

class GeoPoint
{
public:
	GeoPoint();
	GeoPoint(double x, double y, double east, double north);
	void setXPixel(double x);
	void setYPixel(double y);
	void setEastings(double east);
	void setNorthings(double north);
	double getXPixel();
	double getYPixel();
	double getEastings();
	double getNorthings();
	void clone(GeoPoint *point);
	~GeoPoint();
protected:
	double xPixel;
	double yPixel;
	double eastings;
	double northings;
};

#endif
