/*
 *  TransformsTableTests.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 01/05/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "TransformsTableTests.h"

TransformsTableTests::TransformsTableTests()
{
	
}

void TransformsTableTests::runTests()
{
	srand((unsigned)time(NULL)); // Seed random generator
	try
	{
		MathUtils mathUtils;
		Transform *transform = new Transform;
		
		TransformsTable *table = new TransformsTable(10);
		table->printTable();
		
		for(int i = 0; i < 10; i++)
		{
			//std::cout << "" << i << " : \n";
			transform->shiftX = mathUtils.randomWithinRange(-10,10);
			transform->shiftY = mathUtils.randomWithinRange(-10,10);
			transform->measureValue = rand();
			table->insert(transform, false);
			//table->printTable();
			//std::cout << "\n"; 
		}
		
		transform->shiftX = 9;
		transform->shiftY = 1;
		transform->measureValue = 0.5;
		table->insert(transform, true);
		table->printTable();
		
		if(table->search(transform))
		{
			std::cout << "Found element!!\n";
		}
		else
		{
			std::cout << "Search ERROR! element [9,1] has not been found.\n";
		}
		
		if(table->remove(transform))
		{
			std::cout << "Element found and removed!!\n";
		}
		else
		{
			std::cout << "Remove ERROR! element [9,1] has not been removed.\n";
		}	
		
		transform->shiftX = 8;
		transform->shiftY = 1;
		transform->measureValue = 0.81;
		table->insert(transform, true);
		table->printTable();
		
		for(int i = 0; i < 10; i++)
		{
			//std::cout << "" << i << " : \n";
			transform->shiftX = mathUtils.randomWithinRange(0,10);
			transform->shiftY = mathUtils.randomWithinRange(0,10);
			transform->measureValue = rand();
			table->insert(transform, false);
			//table->printTable();
			//std::cout << "\n"; 
		}
		
		transform->shiftX = 0;
		transform->shiftY = 1;
		transform->measureValue = 0.81;
		table->insert(transform, true);
		std::cout << "\n";
		table->printTable();
		
		if(table->remove(transform))
		{
			std::cout << "Element found and removed!!\n";
		}
		else
		{
			std::cout << "Remove ERROR! element [8,1] has not been removed.\n";
		}	
		
		for(int i = 0; i < 10; i++)
		{
			//std::cout << "" << i << " : \n";
			transform->shiftX = mathUtils.randomWithinRange(-5,10);
			transform->shiftY = mathUtils.randomWithinRange(-5,10);
			transform->measureValue = rand();
			table->insert(transform, false);
			//table->printTable();
			// 
		}
		std::cout << "\n";
		table->printTable();
	}
	catch(TransformsTableException e)
	{
		std::cout << "TransformsTableException Thrown:\n" << e.what() <<
				"\n With error code: " << e.getErrorCode();
	}
}

TransformsTableTests::~TransformsTableTests()
{
	
}
