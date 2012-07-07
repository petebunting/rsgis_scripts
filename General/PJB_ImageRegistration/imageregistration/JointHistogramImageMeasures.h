/*
 *  JointHistogramImageMeasures.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/08/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef JointHistogramImageMeasures_H
#define JointHistogramImageMeasures_H

#include "JointHistogram.h"
#include <iostream>
#include "math.h"
#include "ImageRegistrationException.h"
#include "ErrorCodes.h"
#include "MathUtils.h"

class JointHistogramImageMeasures
{
public:
	JointHistogramImageMeasures();
	double calcClusterRewardImageMeasure(JointHistogram &jointHistogram, int numPixels);
	double calcMutualInformationECC(JointHistogram &jointHistogram);
	double calcMutualInformationY(JointHistogram &jointHistogram);
	double calcMutualInformation(JointHistogram &jointHistogram);
	double calcDistance2Independence(JointHistogram &jointHistogram);
	double calcKolmogorovDistance(JointHistogram &jointHistogram);
	double calcKullbachDivergence(JointHistogram &jointHistogram);
	double calcHellingerDistance(JointHistogram &jointHistogram);
	double calcToussaintsDistance(JointHistogram &jointHistogram);
	double calcLinKDivergence(JointHistogram &jointHistogram);
	~JointHistogramImageMeasures();
};
#endif


