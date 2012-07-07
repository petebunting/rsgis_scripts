/*
 *  Point.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/03/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "GeoPoint.h"

GeoPoint::GeoPoint()
{
	
}

GeoPoint::GeoPoint(double x, double y, double east, double north)
{
	xPixel = x;
	yPixel = y;
	eastings = east;
	northings = north;
}

void GeoPoint::setXPixel(double x)
{
	xPixel = x;
}

void GeoPoint::setYPixel(double y)
{
	yPixel = y;
}
void GeoPoint::setEastings(double east)
{
	eastings = east;
}

void GeoPoint::setNorthings(double north)
{
	northings = north;
}

double GeoPoint::getXPixel()
{
	return xPixel;
}

double GeoPoint::getYPixel()
{
	return yPixel;
}

double GeoPoint::getEastings()
{
	return eastings;
}

double GeoPoint::getNorthings()
{
	return northings;
}

void GeoPoint::clone(GeoPoint *point)
{
	point->setXPixel(xPixel);
	point->setYPixel(yPixel); 
	point->setEastings(eastings); 
	point->setNorthings(northings);

}

GeoPoint::~GeoPoint()
{
	
}
