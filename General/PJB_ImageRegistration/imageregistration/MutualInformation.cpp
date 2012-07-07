/*
 *  MutualInformation.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 09/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "MutualInformation.h"

MutualInformation::MutualInformation()
{
	
}

double MutualInformation::calcMutualInformation(JointHistogram &jointHistogram)
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
	
	/************************* TEST: Local Joint Histogram *******************
	for(int i=0; i<jointHistLength; i++)
	{
		std::cout << jointHist[i] << ", ";
		if(i % jointHistSize == 0)
		{
			std::cout << std::endl;
		}
	}
	std::cout << std::endl;
	*************************************************************************/
	
	/*********************** Sum Joint Histogram ***************************/
	double sumJH = 0;
	
	// Sum the joint histogram
	for(int i=0; i < jointHistLength; i++)
	{
		sumJH += jointHist[i];
	}
	//TEST Print:
	//std::cout << "sumJH: " << sumJH << std::endl;
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
	
	/******************** TEST: Print JPMF *********************************
	for(int i=0; i<jointHistLength; i++)
	{
		std::cout << jpmf[i] << ", ";
		if(i % jointHistSize == 0)
		{
			std::cout << std::endl;
		}
	}
	std::cout << std::endl;
	***********************************************************************/
	
	/************* Marginal Probablity Mass Funcations **********************/
	double *r_mpmf = new double[jointHistSize];
	double *f_mpmf = new double[jointHistSize];
	double sumProbs = 0;
	
	// PF(f)
	for(int i = 0; i<jointHistSize; i++)
	{
		sumProbs = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			sumProbs += jpmf[(jointHistSize*j)+i];
		}
		f_mpmf[i] = sumProbs;
	}
	
	// PR(r)
	for(int i = 0; i<jointHistSize; i++)
	{
		sumProbs = 0;
		// Sum the column in the joint histogram.
		for(int j = 0; j<jointHistSize; j++)
		{
			sumProbs += jpmf[(jointHistSize * i) + j];
		}
		r_mpmf[i] = sumProbs;
	}
	/************************************************************************/

	/************ TEST: Print Marginal Probablity Mass Funcations *************
	std::cout << "Floating: \n";
	for(int i = 0; i<jointHistSize; i++)
	{
		std::cout << f_mpmf[i] << ", ";
	}
	std::cout << std::endl;
	
	std::cout << "Reference: \n";
	for(int i = 0; i<jointHistSize; i++)
	{
		std::cout << r_mpmf[i] << ", ";
	}
	std::cout << std::endl;
	**************************************************************************/
	
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
	
	/******************* TEST: Print entropy values **************************
	std::cout << "Joint Entropy: " << joint_entropy << std::endl;
	std::cout << "Floating Entropy: " << float_entropy << std::endl;
	std::cout << "Reference Entropy: " << ref_entropy << std::endl;
	*************************************************************************/
	
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
		delete r_mpmf;
	}
	if(f_mpmf != NULL)
	{
		delete f_mpmf;
	}
	if(jpmf != NULL)
	{
		delete jpmf;
	}
	return mi;
}

MutualInformation::~MutualInformation()
{
	
}
