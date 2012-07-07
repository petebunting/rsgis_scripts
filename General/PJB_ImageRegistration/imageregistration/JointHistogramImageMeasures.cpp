/*
 *  JointHistogramImageMeasures.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 02/08/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "JointHistogramImageMeasures.h"

JointHistogramImageMeasures::JointHistogramImageMeasures()
{
	
}

double JointHistogramImageMeasures::calcClusterRewardImageMeasure(JointHistogram &jointHistogram, int numberPixels)
{
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJHsq = 0;
	// Sum the squared joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJHsq += (jointHist[i]*jointHist[i]);
	}
	/************************************************************************/
	
	/******************* Create Marginal Histograms ***********************/
	double *marginalHistogramI = new double[jointHistSize];
	double *marginalHistogramJ = new double[jointHistSize];
	for( int i = 0; i < jointHistSize; i++)
	{
		marginalHistogramI[i] = 0;
		marginalHistogramJ[i] = 0;
		for(int j = 0; j < jointHistSize; j++)
		{
			marginalHistogramI[i] += jointHist[j + (i * jointHistSize)];
			marginalHistogramJ[i] += jointHist[(j * jointHistSize) + i];
		}
	}
	/************************************************************************/
	
	/*********************** Sum Marginal Histograms ***************************/
	double sumMHI = 0;
	double sumMHJ = 0;
	// Sum the Marginal Histograms
	for(int i=0; i < jointHistSize; i++)
	{
		sumMHI += (marginalHistogramI[i]*marginalHistogramI[i]);
		sumMHJ += (marginalHistogramJ[i]*marginalHistogramJ[i]);
	}
	/************************************************************************/
	
	/******************* Calculate value of F *******************************/
	double f = 0;
	f = sqrt(sumMHI*sumMHJ);
	/************************************************************************/
	
	/***************** Calculate Cluster Reward Image Measure **************/
	double cra = 0;
	cra = ((sumJHsq/f) - (f / (numberPixels*numberPixels))) / (1 - (f/(numberPixels*numberPixels)));
	/***********************************************************************/
	
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(marginalHistogramI != NULL)
	{
		delete [] marginalHistogramI;
	}
	if(marginalHistogramJ != NULL)
	{
		delete [] marginalHistogramJ;
	}
	return cra;
}

double JointHistogramImageMeasures::calcMutualInformation(JointHistogram &jointHistogram)
{
	
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0)
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/****** Calculate the Entropy of each Image and their join Entropy *******/
	
	double joint_entropy;
	double float_entropy;
	double ref_entropy;
	
	// Calc Joint Entropy
	joint_entropy = 0;
	for(int i = 0; i < jointHistLength; i++)
	{
		if(jpmf[i] != 0)
		{
			joint_entropy += jpmf[i] * log(jpmf[i]);
		}
	}
	joint_entropy = joint_entropy * (-1);
	
	// Calc Ref Entropy
	ref_entropy = 0;
	for(int i = 0; i < jointHistSize; i++)
	{
		if(r_mpmf[i] != 0)
		{
			ref_entropy += r_mpmf[i] * log(r_mpmf[i]);
		}
	}
	ref_entropy = ref_entropy * (-1);
	
	// Calc float Entropy
	float_entropy = 0;
	for(int i = 0; i < jointHistSize; i++)
	{
		if(f_mpmf[i] != 0)
		{
			float_entropy += f_mpmf[i] * log(f_mpmf[i]);
		}
	}
	float_entropy = float_entropy * (-1);
	
	/**************************************************************************/
	
	/******************** Calculate MI **************************************/
	double mi = 0;
	mi = (ref_entropy + float_entropy) - joint_entropy;
	/*************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return mi;
}

double JointHistogramImageMeasures::calcMutualInformationECC(JointHistogram &jointHistogram)
{
	
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0)
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/****** Calculate the Entropy of each Image and their join Entropy *******/
	
	double joint_entropy;
	double float_entropy;
	double ref_entropy;
	
	// Calc Joint Entropy
	joint_entropy = 0;
	for(int i = 0; i < jointHistLength; i++)
	{
		if(jpmf[i] != 0)
		{
			joint_entropy += jpmf[i] * log(jpmf[i]);
		}
	}
	joint_entropy = joint_entropy * (-1);
	
	// Calc Ref Entropy
	ref_entropy = 0;
	for(int i = 0; i < jointHistSize; i++)
	{
		if(r_mpmf[i] != 0)
		{
			ref_entropy += r_mpmf[i] * log(r_mpmf[i]);
		}
	}
	ref_entropy = ref_entropy * (-1);
	
	// Calc float Entropy
	float_entropy = 0;
	for(int i = 0; i < jointHistSize; i++)
	{
		if(f_mpmf[i] != 0)
		{
			float_entropy += f_mpmf[i] * log(f_mpmf[i]);
		}
	}
	float_entropy = float_entropy * (-1);
	
	/**************************************************************************/
	
	/******************** Calculate MI **************************************/
	double mi = 0;
	double norm_mi = 0;
	mi = (ref_entropy + float_entropy) - joint_entropy;
	norm_mi = (2 * mi) / (ref_entropy + float_entropy);
	/*************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return norm_mi;
}

double JointHistogramImageMeasures::calcMutualInformationY(JointHistogram &jointHistogram)
{
	
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0)
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/****** Calculate the Entropy of each Image and their join Entropy *******/
	
	double joint_entropy;
	double float_entropy;
	double ref_entropy;
	
	// Calc Joint Entropy
	joint_entropy = 0;
	for(int i = 0; i < jointHistLength; i++)
	{
		if(jpmf[i] != 0)
		{
			joint_entropy += jpmf[i] * log(jpmf[i]);
		}
	}
	joint_entropy = joint_entropy * (-1);
	
	// Calc Ref Entropy
	ref_entropy = 0;
	for(int i = 0; i < jointHistSize; i++)
	{
		if(r_mpmf[i] != 0)
		{
			ref_entropy += r_mpmf[i] * log(r_mpmf[i]);
		}
	}
	ref_entropy = ref_entropy * (-1);
	
	// Calc float Entropy
	float_entropy = 0;
	for(int i = 0; i < jointHistSize; i++)
	{
		if(f_mpmf[i] != 0)
		{
			float_entropy += f_mpmf[i] * log(f_mpmf[i]);
		}
	}
	float_entropy = float_entropy * (-1);
	
	/**************************************************************************/
	
	/******************** Calculate MI **************************************/
	double mi = 0;
	mi = (ref_entropy + float_entropy) / joint_entropy;
	/*************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return mi;
}

double JointHistogramImageMeasures::calcDistance2Independence(JointHistogram &jointHistogram)
{
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0 | isnan(jointHist[i]))
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/***************** Calculate Distance to Independence ******************/
	double d2i = 0;
	
	for(int i = 0; i < jointHistSize; i++)
	{
		for(int j = 0; j < jointHistSize; j++)
		{
			if(jpmf[j+(i*jointHistSize)] != 0)
			{
				d2i += ((jpmf[j+(i*jointHistSize)] - (r_mpmf[i]*f_mpmf[j]))*(jpmf[j+(i*jointHistSize)] 
																		 - (r_mpmf[i]*f_mpmf[j])))/(r_mpmf[i]*f_mpmf[j]);
			}
		}
	}
	
	/************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return d2i;
}

double JointHistogramImageMeasures::calcKolmogorovDistance(JointHistogram &jointHistogram)
{
	MathUtils mathUtils;
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0)
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/***************** Calculate Distance to Independence ******************/
	double kolmDis = 0;
	
	for(int i = 0; i < jointHistSize; i++)
	{
		for(int j = 0; j < jointHistSize; j++)
		{
			kolmDis += mathUtils.absoluteValue(jpmf[j+(i*jointHistSize)] - (r_mpmf[i]*f_mpmf[j]));
		}
	}
	kolmDis = kolmDis/2;
	/************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return kolmDis;
}

double JointHistogramImageMeasures::calcKullbachDivergence(JointHistogram &jointHistogram)
{
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0 | isnan(jointHist[i]))
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/***************** Calculate Distance to Independence ******************/
	double kullDiverg = 0;
	
	for(int i = 0; i < jointHistSize; i++)
	{
		for(int j = 0; j < jointHistSize; j++)
		{
			if(jpmf[j+(i*jointHistSize)] != 0)
			{
				kullDiverg += ((r_mpmf[i]*f_mpmf[j]) - jpmf[j+(i*jointHistSize)]) *
				(log(r_mpmf[i]*f_mpmf[j]) - log(jpmf[j+(i*jointHistSize)]));
			}
		}
	}
	/************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return kullDiverg;
}

double JointHistogramImageMeasures::calcHellingerDistance(JointHistogram &jointHistogram)
{
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0)
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/***************** Calculate Distance to Independence ******************/
	double hellDist = 0;
	
	for(int i = 0; i < jointHistSize; i++)
	{
		for(int j = 0; j < jointHistSize; j++)
		{
			hellDist += (sqrt(jpmf[j+(i*jointHistSize)]) - sqrt(r_mpmf[i]*f_mpmf[j])) *
						(sqrt(jpmf[j+(i*jointHistSize)]) - sqrt(r_mpmf[i]*f_mpmf[j]));
		}
	}
	hellDist = hellDist/2;
	/************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return hellDist;
}

double JointHistogramImageMeasures::calcToussaintsDistance(JointHistogram &jointHistogram)
{
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0 | isnan(jointHist[i]))
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
		
	}
	/************************************************************************/
	
	/***************** Calculate Distance to Independence ******************/
	double tousDist = 0;
	
	for(int i = 0; i < jointHistSize; i++)
	{
		for(int j = 0; j < jointHistSize; j++)
		{
			if(jpmf[j+(i*jointHistSize)] != 0)
			{
				tousDist += jpmf[j+(i*jointHistSize)] - ((2 * jpmf[j+(i*jointHistSize)] * (r_mpmf[i]*f_mpmf[j])) /
							(jpmf[j+(i*jointHistSize)] + (r_mpmf[i]*f_mpmf[j])));
			}
		}
	}
	/************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	
	return tousDist;
}

double JointHistogramImageMeasures::calcLinKDivergence(JointHistogram &jointHistogram)
{
	/************************* Get JointHistogram ****************************/
	double *jointHist;
	int jointHistSize;
	int jointHistLength;
	jointHistSize = jointHistogram.getNumberBins();
	jointHistLength = jointHistSize*jointHistSize;
	jointHist = new double[jointHistLength];
	jointHistogram.getJointHistogramImage(jointHist);
	/************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	/************************************************************************/
	
	//std::cout << "sumJH : " << sumJH << std::endl;
	
	/************* Joint Probability Mass Funcation **************************/
	double *jpmf = new double[jointHistLength];
	
	for(int i=0; i < jointHistLength; i++)
	{
		if(jointHist[i] == 0 | isnan(jointHist[i]))
		{
			jpmf[i] = 0;
		}
		else
		{
			jpmf[i] = jointHist[i]/sumJH;
		}
	}
	/************************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	
	// PF
	for(int i = 0; i<jointHistSize; i++)
	{
		f_mpmf[i] = 0;
		r_mpmf[i] = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			f_mpmf[i] += jpmf[(jointHistSize*j)+i];
			r_mpmf[i] += jpmf[(jointHistSize * i) + j];
		}
	}
	/************************************************************************/
	
	/***************** Calculate Distance to Independence ******************/
	double linKDiverg = 0;
	
	for(int i = 0; i < jointHistSize; i++)
	{
		for(int j = 0; j < jointHistSize; j++)
		{
			if(jpmf[j+(i*jointHistSize)] != 0)
			{
				linKDiverg += jpmf[j+(i*jointHistSize)] *
				log((2*jpmf[j+(i*jointHistSize)])/(jpmf[j+(i*jointHistSize)] + (r_mpmf[i]*f_mpmf[j])));
			}
		}
	}
	/************************************************************************/
	
	//Free Memory
	if(jointHist != NULL)
	{
		delete [] jointHist;
	}
	if(r_mpmf != NULL)
	{
		delete [] r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete [] f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete [] jpmf;
	}
	return linKDiverg;
}

JointHistogramImageMeasures::~JointHistogramImageMeasures()
{
	
}
