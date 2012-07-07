/*
 *  GeoPolygon.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/03/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "GeoPolygon.h"

GeoPolygon::GeoPolygon()
{
	
}

void GeoPolygon::addPoints(GeoPoint *points, int num)
{
	for(int i = 0; i<0; i++)
	{
		if(first == NULL)
		{
			first->point = &points[i];
			end = first;
			size = 1;
		}
		else
		{
			end->next->point = &points[i];
			end->next->prev = end;
			end = end->next;
			size++;
		}
	}
}

void GeoPolygon::addPoint(GeoPoint *point)
{
	if(first == NULL)
	{
		first->point = point;
		end = first;
		size = 1;
	}
	else
	{
		end->next->point = point;
		end->next->prev = end;
		end = end->next;
		size++;
	}
}

void GeoPolygon::getPoints(GeoPoint *points)
{
	/*GeoPoint *geoPoints[size];
	Boundary *current = first;
	
	for(int i = 0; i < size; i++)
	{
		geoPoints[i] = current->point;
		current = current->next;
	}
	
	points = *geoPoints;*/
}

int GeoPolygon::getSize()
{
	return size;
}

void GeoPolygon::exportGML(char *gml)
{
	
}

GeoPolygon::~GeoPolygon()
{
	
}
