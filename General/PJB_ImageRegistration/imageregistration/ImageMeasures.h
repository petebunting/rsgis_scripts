/*
 *  ImageMeasures.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 23/01/2006.
 *  Copyright 2006 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef Image_Measures_H
#define Image_Measures_H

namespace image_measures
{
	enum
	{
		mi = 0,
		euclidean = 1,
		manhattan = 2,
		correlationCoefficient = 3,
		clusterReward = 4,
		distance2Independence = 5,
		kolmogorovDistance = 6,
		kullbachDivergence = 7,
		hellingerDistance = 8,
		toussaintsDistance = 9,
		linKDivergence = 10,
		norm_mi_ecc = 11,
		norm_mi_y = 12
	};
}

namespace image_search
{
	enum
	{
		exhaustive = 0,
		hill_climbing = 1,
		simulated_annealing = 2
	};
}

#endif
