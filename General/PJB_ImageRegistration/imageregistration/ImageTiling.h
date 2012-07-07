/*
 *  ImageTiling.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/03/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef ImageTiling_H
#define ImageTiling_H

struct TileCoords {
	int imgATLX;
	int imgATLY;
	int imgABRX;
	int imgABRY;
	int imgBTLX;
	int imgBTLY;
	int imgBBRX;
	int imgBBRY;
	double eastingTL;
	double northingTL;
	double eastingBR;
	double northingBR;
};


struct Transform {
	double shiftX;
	double shiftY;
	double measureValue;
};

#endif
