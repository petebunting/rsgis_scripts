/*
 *  NonusImageTree.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 15/11/2005.
 *  Copyright 2005  Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#include "NonusImageTree.h"

NonusImageTree::NonusImageTree()
{
	rootset = FALSE;
}

TileCoords* NonusImageTree::setRoot(Transform imageTransformation, TileCoords imageCoords, double stddevref, double stddevfloat)
throw(NonusImageTreeException)
{
	/**************** Check the root node has been set. *****************/
	if(rootset == FALSE)
	{
		root = new NonusTreeNode;
		//root->children = new NonusTreeNode[9];
		root->tileCoords = new TileCoords;
		root->tileCoords->imgATLX = imageCoords.imgATLX;
		root->tileCoords->imgATLY = imageCoords.imgATLY;
		root->tileCoords->imgABRX = imageCoords.imgABRX;
		root->tileCoords->imgABRY = imageCoords.imgABRY;
		root->tileCoords->imgBTLX = imageCoords.imgBTLX;
		root->tileCoords->imgBTLY = imageCoords.imgBTLY;
		root->tileCoords->imgBBRX = imageCoords.imgBBRX;
		root->tileCoords->imgBBRY = imageCoords.imgBBRY;
		root->tileCoords->eastingTL = imageCoords.eastingTL;
		root->tileCoords->northingTL = imageCoords.northingTL;
		root->tileCoords->eastingBR = imageCoords.eastingBR;
		root->tileCoords->northingBR = imageCoords.northingBR;
		root->TileTransformation = new Transform;
		root->TileTransformation->shiftX = imageTransformation.shiftX;
		root->TileTransformation->shiftY = imageTransformation.shiftY;
		root->stddevtileref = stddevref;
		root->stddevtilefloat = stddevfloat;
		root->nodeID = 0;
		for( int i = 0; i < 9; i++ )
		{
			root->children[i] = 0;
		}
		//std::cout << "Root Node set\n";
		rootset = TRUE;
		treeSize = 1;
	}
	else
	{
		throw NonusImageTreeException("The root Node has already been set.", error_codes::root_already_set);
	}
	/**********************************************************************/
	return root->tileCoords;
}

NonusTreeNode* NonusImageTree::addNode(TileCoords *tileCoords, double stddevref, double stddevfloat)
	throw(NonusImageTreeException)
{
	//MathUtils mathUtils;
	//std::cout << "\nEntered addNode\n";
	
	/******************** TEST: Print out tile info. **************************
	
	std::cout << "Tile passed In to addNode.\n";
	std::cout << "[" << tileCoords->imgATLX << ", " << tileCoords->imgATLY << "][" << tileCoords->imgABRX << ", " << tileCoords->imgABRY << "]\n";
	std::cout << "[" << tileCoords->imgBTLX << ", " << tileCoords->imgBTLY << "][" << tileCoords->imgBBRX << ", " << tileCoords->imgBBRY << "]\n";
	std::cout << "[" << tileCoords->eastingTL << ", " << tileCoords->northingTL << "][" << tileCoords->eastingBR << ", " << tileCoords->northingBR << "]\n";
	
	std::cout << "ROOT:\n";
	std::cout << "[" << root->tileCoords->imgATLX << ", " << root->tileCoords->imgATLY << "][" << root->tileCoords->imgABRX << ", " << root->tileCoords->imgABRY << "]\n";
	std::cout << "[" << root->tileCoords->imgBTLX << ", " << root->tileCoords->imgBTLY << "][" << root->tileCoords->imgBBRX << ", " << root->tileCoords->imgBBRY << "]\n";
	std::cout << "[" << root->tileCoords->eastingTL << ", " << root->tileCoords->northingTL << "][" << root->tileCoords->eastingBR << ", " << root->tileCoords->northingBR << "]\n";
	std::cout << "transformation in ROOT. Transformation: [" << root->TileTransformation->shiftX << ", " << root->TileTransformation->shiftY << "]\n";
	/************************************************************************/
	
	
	/**************** Check the root node has been set. *****************/
	if(rootset == false)
	{
		throw NonusImageTreeException("The root Node has not been set.", error_codes::root_not_set);
	}
	else
	{
		//do nothing.
	}
	/**********************************************************************/
	
	/****************** Find location for new node **********************/
	int differenceX = 0;
	int differenceY = 0;
	int tileWidth = 0;
	int tileHeight = 0;
	
	//Find Centre Point 
	int xTileCentre = tileCoords->imgATLX + ((tileCoords->imgABRX - tileCoords->imgATLX)/2);
	int yTileCentre = tileCoords->imgATLY + ((tileCoords->imgABRY - tileCoords->imgATLY)/2);
	
	//std::cout << "xTileCentre = " << xTileCentre << " yTileCentre = " << yTileCentre << std::endl;
	
	NonusTreeNode *previousNode = NULL;
	int currentNodeIndex;
	NonusTreeNode *currentNode = root;
	do
	{
		//std::cout << "Looping..\n";
		//Setup Variables;
		differenceX = currentNode->tileCoords->imgABRX - currentNode->tileCoords->imgATLX;
		differenceY = currentNode->tileCoords->imgABRY - currentNode->tileCoords->imgATLY;
		
		//std::cout << "Difference X" << differenceX << std::endl;
		//std::cout << "Difference Y" << differenceY << std::endl;
		
		tileWidth = differenceX/3;
		tileHeight = differenceY/3;
		
		//std::cout << "BEFORE\nTile Width: " << tileWidth << std::endl;
		//std::cout << "Tile Height: " << tileHeight << std::endl;
		
		if( tileWidth*3 < differenceX)
		{
			tileWidth++;
		}
		if( tileHeight*3 < differenceY)
		{
			tileHeight++;
		}
		//std::cout << "Tile Width: " << tileWidth << std::endl;
		//std::cout << "Tile Height: " << tileHeight << std::endl;
		
		
		//////////////////////////// Top Row ///////////////////////////////
		// Tile 0
		if( xTileCentre > currentNode->tileCoords->imgATLX &
			yTileCentre > currentNode->tileCoords->imgATLY &
			xTileCentre < (currentNode->tileCoords->imgATLX + tileWidth) &
			yTileCentre < (currentNode->tileCoords->imgATLY + tileHeight) )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[0];
			currentNodeIndex = 0;
			//std::cout << "Tile 0\n";
		}
		
		// Tile 1
		else if( xTileCentre > (currentNode->tileCoords->imgATLX + tileWidth) &
			     yTileCentre > currentNode->tileCoords->imgATLY &
				 xTileCentre < (currentNode->tileCoords->imgATLX + (tileWidth*2)) &
			     yTileCentre < (currentNode->tileCoords->imgATLY + tileHeight) )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[1];
			currentNodeIndex = 1;
			//std::cout << "Tile 1\n";
		}
		
		// Tile 2
		else if( xTileCentre > (currentNode->tileCoords->imgATLX + (tileWidth*2)) &
			     yTileCentre > currentNode->tileCoords->imgATLY &
				 xTileCentre < currentNode->tileCoords->imgABRX &
			     yTileCentre < (currentNode->tileCoords->imgATLY + tileHeight) )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[2];
			currentNodeIndex = 2;
			//std::cout << "Tile 2\n";
		}
		///////////////////////////////////////////////////////////////////////////
		
		//////////////////////////// Middle Row ///////////////////////////////
		// Tile 3
		else if( xTileCentre > currentNode->tileCoords->imgATLX &
			yTileCentre > (currentNode->tileCoords->imgATLY + tileHeight) &
			xTileCentre < (currentNode->tileCoords->imgATLX + tileWidth) &
			yTileCentre < (currentNode->tileCoords->imgATLY + (tileHeight*2)) )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[3];
			currentNodeIndex = 3;
			//std::cout << "Tile 3\n";
		}
		
		// Tile 4
		else if( xTileCentre > (currentNode->tileCoords->imgATLX + tileWidth) &
			     yTileCentre > (currentNode->tileCoords->imgATLY + tileHeight) &
				 xTileCentre < (currentNode->tileCoords->imgATLX + (tileWidth*2)) &
			     yTileCentre < (currentNode->tileCoords->imgATLY + (tileHeight*2)) )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[4];
			currentNodeIndex = 4;
			//std::cout << "Tile 4\n";
		}
		
		// Tile 5
		else if( xTileCentre > (currentNode->tileCoords->imgATLX + (tileWidth*2)) &
			     yTileCentre > (currentNode->tileCoords->imgATLY + tileHeight) &
				 xTileCentre < currentNode->tileCoords->imgABRX &
			     yTileCentre < (currentNode->tileCoords->imgATLY + (tileHeight*2)) )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[5];
			currentNodeIndex = 5;
			//std::cout << "Tile 5\n";
		}
		///////////////////////////////////////////////////////////////////////////
		
		//////////////////////////// Bottom Row ///////////////////////////////
		// Tile 6
		else if( xTileCentre > currentNode->tileCoords->imgATLX &
			yTileCentre > (currentNode->tileCoords->imgATLY + (tileHeight*2)) &
			xTileCentre < (currentNode->tileCoords->imgATLX + tileWidth) &
			yTileCentre < currentNode->tileCoords->imgABRY )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[6];
			currentNodeIndex = 6;
			//std::cout << "Tile 6\n";
		}
		
		// Tile 7
		else if( xTileCentre > (currentNode->tileCoords->imgATLX + tileWidth) &
			     yTileCentre > (currentNode->tileCoords->imgATLY + (tileHeight*2)) &
				 xTileCentre < (currentNode->tileCoords->imgATLX + (tileWidth*2)) &
			     yTileCentre < currentNode->tileCoords->imgABRY )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[7];
			currentNodeIndex = 7;
			//std::cout << "Tile 7\n";
		}
		
		// Tile 8
		else if( xTileCentre > (currentNode->tileCoords->imgATLX + (tileWidth*2)) &
			     yTileCentre > (currentNode->tileCoords->imgATLY + (tileHeight*2)) &
				 xTileCentre < currentNode->tileCoords->imgABRX &
			     yTileCentre < currentNode->tileCoords->imgABRY )
		{
			previousNode = currentNode;
			currentNode = currentNode->children[8];
			currentNodeIndex = 8;
			//std::cout << "Tile 8\n";
		}
		///////////////////////////////////////////////////////////////////////////
		
		//////////////////////////// ELSE - ERROR /////////////////////////////////
		else
		{
			/********************* Error print something useful *******************************/
			std::cout << "Tile passed In to addNode.\n";
			std::cout << "[" << tileCoords->imgATLX << ", " << tileCoords->imgATLY << "][" << tileCoords->imgABRX << ", " << tileCoords->imgABRY << "]\n";
			std::cout << "[" << tileCoords->imgBTLX << ", " << tileCoords->imgBTLY << "][" << tileCoords->imgBBRX << ", " << tileCoords->imgBBRY << "]\n";
			std::cout << "[" << tileCoords->eastingTL << ", " << tileCoords->northingTL << "][" << tileCoords->eastingBR << ", " << tileCoords->northingBR << "]\n";
			
			std::cout << "ROOT:\n";
			std::cout << "[" << root->tileCoords->imgATLX << ", " << root->tileCoords->imgATLY << "][" << root->tileCoords->imgABRX << ", " << root->tileCoords->imgABRY << "]\n";
			std::cout << "[" << root->tileCoords->imgBTLX << ", " << root->tileCoords->imgBTLY << "][" << root->tileCoords->imgBBRX << ", " << root->tileCoords->imgBBRY << "]\n";
			std::cout << "[" << root->tileCoords->eastingTL << ", " << root->tileCoords->northingTL << "][" << root->tileCoords->eastingBR << ", " << root->tileCoords->northingBR << "]\n";
			std::cout << "transformation in ROOT. Transformation: [" << root->TileTransformation->shiftX << ", " << root->TileTransformation->shiftY << "]\n";
			std::cout << "xTileCentre = " << xTileCentre << " yTileCentre = " << yTileCentre << std::endl;
			//this->printTreeInFull();
			/************************************************************************/
			
			
			throw NonusImageTreeException("Tile does not fit into this NonusImageTree", error_codes::outside_of_area);
		}
		///////////////////////////////////////////////////////////////////////////
	}while(currentNode != NULL);
	/*********************************************************************/
	
	/*********************** Insert Node *************************/
	previousNode->children[currentNodeIndex] = new NonusTreeNode;
	for( int i = 0; i < 9; i++ )
	{
		previousNode->children[currentNodeIndex]->children[i] = 0;
	}
	
	previousNode->children[currentNodeIndex]->tileCoords = new TileCoords;
	previousNode->children[currentNodeIndex]->tileCoords->imgATLX = tileCoords->imgATLX;
	previousNode->children[currentNodeIndex]->tileCoords->imgATLY = tileCoords->imgATLY;
	previousNode->children[currentNodeIndex]->tileCoords->imgABRX = tileCoords->imgABRX;
	previousNode->children[currentNodeIndex]->tileCoords->imgABRY = tileCoords->imgABRY;
	
	previousNode->children[currentNodeIndex]->tileCoords->imgBTLX = tileCoords->imgBTLX;
	previousNode->children[currentNodeIndex]->tileCoords->imgBTLY = tileCoords->imgBTLY;
	previousNode->children[currentNodeIndex]->tileCoords->imgBBRX = tileCoords->imgBBRX;
	previousNode->children[currentNodeIndex]->tileCoords->imgBBRY = tileCoords->imgBBRY;
	
	previousNode->children[currentNodeIndex]->tileCoords->eastingTL = tileCoords->eastingTL;
	previousNode->children[currentNodeIndex]->tileCoords->northingTL = tileCoords->northingTL;
	previousNode->children[currentNodeIndex]->tileCoords->eastingBR = tileCoords->eastingBR;
	previousNode->children[currentNodeIndex]->tileCoords->northingBR = tileCoords->northingBR;
	
	previousNode->children[currentNodeIndex]->TileTransformation = new Transform;
	previousNode->children[currentNodeIndex]->TileTransformation->shiftX = 0;
	previousNode->children[currentNodeIndex]->TileTransformation->shiftY = 0;
	previousNode->children[currentNodeIndex]->stddevtileref = stddevref;
	previousNode->children[currentNodeIndex]->stddevtilefloat = stddevfloat;
	previousNode->children[currentNodeIndex]->nodeID = treeSize;
	treeSize++;
	//std::cout << "Node added to Tree. Index:" << currentNodeIndex << "\n";
	/*************************************************************/
	
	return previousNode->children[currentNodeIndex];
}

void NonusImageTree::printTreeInFull()
{
	std::cout << "Nonus Image Tree:\n";
	std::cout << "Transformation of Root: (" << root->stddevtileref << ", " << root->stddevtilefloat << "): [" 
			  << root->TileTransformation->shiftX 
			  << ", " 
			  << root->TileTransformation->shiftY 
			  << "]\n";
	std::cout << "[" << root->tileCoords->imgATLX << ", " << root->tileCoords->imgATLY << "][" << root->tileCoords->imgABRX << ", " << root->tileCoords->imgABRY << "]\n";
	std::cout << "[" << root->tileCoords->imgBTLX << ", " << root->tileCoords->imgBTLY << "][" << root->tileCoords->imgBBRX << ", " << root->tileCoords->imgBBRY << "]\n";
	std::cout << "[" << root->tileCoords->eastingTL << ", " << root->tileCoords->northingTL << "][" << root->tileCoords->eastingBR << ", " << root->tileCoords->northingBR << "]\n";
	
	Queue *queue = new Queue;
	NonusTreeNode *currentNode = root;

	do
	{
		// Print out current Node
		// Add current Node's children to the Queue.
		for(int i = 0; i < 9; i++)
		{
			std::cout << " (" << currentNode->children[i]->stddevtileref << ", " 
			<< currentNode->children[i]->stddevtilefloat << ") : [" 
			<< currentNode->children[i]->TileTransformation->shiftX << ", " 
			<< currentNode->children[i]->TileTransformation->shiftY << "]";
			std::cout << "[" << currentNode->children[i]->tileCoords->imgATLX << ", " << currentNode->children[i]->tileCoords->imgATLY << "][" << currentNode->children[i]->tileCoords->imgABRX << ", " << currentNode->children[i]->tileCoords->imgABRY << "]";
			//std::cout << "[" << currentNode->children[i]->tileCoords->imgBTLX << ", " << currentNode->children[i]->tileCoords->imgBTLY << "][" << currentNode->children[i]->tileCoords->imgBBRX << ", " << currentNode->children[i]->tileCoords->imgBBRY << "]";
			//std::cout << "[" << currentNode->children[i]->tileCoords->eastingTL << ", " << currentNode->children[i]->tileCoords->northingTL << "][" << currentNode->children[i]->tileCoords->eastingBR << ", " << currentNode->children[i]->tileCoords->northingBR << "]";
			
			queue->add(currentNode->children[i]);
			if(i == 2 | i == 5)
			{
				std::cout << std::endl;
			}
		}
		std::cout << std::endl << std::endl;		
		currentNode = queue->getNext();
	}while( currentNode->children[1] != NULL );
	if( queue != NULL )
	{
		delete queue;
	}
}

void NonusImageTree::printTree()
{
	std::cout << "Nonus Image Tree:\n";
	std::cout << "Transformation of Root: (" << root->stddevtileref 
			  << ", " << root->stddevtilefloat << "): [" 
			  << root->TileTransformation->shiftX 
			  << ", " 
			  << root->TileTransformation->shiftY 
			  << "]\n";
	Queue *queue = new Queue;
	NonusTreeNode *currentNode = root;
	
	int numNodes = 1;
	
	do
	{
		// Print out current Node
		// Add current Node's children to the Queue.
		for(int i = 0; i < 9; i++)
		{
			std::cout /*<< " (" << currentNode->children[i]->stddevtileref << ", " 
			<< currentNode->children[i]->stddevtilefloat << ") : [" */ << "["
			<< currentNode->children[i]->TileTransformation->shiftX << ", " 
			<< currentNode->children[i]->TileTransformation->shiftY << "]";
			queue->add(currentNode->children[i]);
			if(i == 2 | i == 5)
			{
				std::cout << std::endl;
			}
			numNodes++;
		}
		std::cout << std::endl << std::endl;		
		currentNode = queue->getNext();
		
	}while( currentNode->children[1] != NULL );
	
	std::cout << "Number of Nodes: " << numNodes << std::endl;
	
	if( queue != NULL )
	{
		delete queue;
	}
}


void NonusImageTree::write2EnviGcpsFile(const char *outputFilePath, int treeDepth)
	throw(FileOutputException, NonusImageTreeException)
{
	/*
	 * Tree Depth - Ranges from 0 - Max Depth.
	 * -1 = Max Depth.
	 */
	
	// Find the tree depth.	
	int maxLevel = 0;
	int currentLevelSize = 1;
	int levelIncrement = 1;
	bool continueLoop = true;
	
	while(continueLoop)
	{
		if(currentLevelSize < treeSize)
		{
			maxLevel++;
		}
		else
		{
			continueLoop = false;
		}
		levelIncrement = levelIncrement * 9;
		currentLevelSize = currentLevelSize + levelIncrement;
	}
	
	//std::cout << "Number of Levels = " << maxLevel << std::endl;
	
	// Check inputted depth is within the depth of the tree 
	// and if -1 was inputted the max depth is used.
	if( treeDepth > maxLevel )
	{
		throw NonusImageTreeException("There is insuffient levels in the tree.", 
									  error_codes::insufficient_levels);
	}
	else
	{
		if( treeDepth == -1 )
		{
			treeDepth = maxLevel;
		}
	}
	
	//std::cout << "Tree Depth = " << treeDepth << std::endl;
	
	// Find the size and finish to the level.
	currentLevelSize = 1;
	levelIncrement = 1;
	int startPoint = 0;
	int finishPoint = 0;
	for(int i = 0; i <= treeDepth; i++)
	{
		if(i == treeDepth)
		{
			finishPoint = currentLevelSize;
		}
		else
		{
			startPoint = currentLevelSize;
			levelIncrement = levelIncrement * 9;
			currentLevelSize = currentLevelSize + levelIncrement;
		}
	}
	
	//std::cout << "treeDepth = " << treeDepth << " startPoint = " << startPoint 
	//	      << " finishPoint = " << finishPoint << std::endl;
	
	// Prepare Queue with items to be written out.
	Queue *queue = NULL;
	queue = new Queue;
	NonusTreeNode *currentNode = root;
	NonusTreeNode *tmpNode;
	int count = 1;
	continueLoop = true;
	do
	{
		// Print out current Node
		// Add current Node's children to the Queue.
		for(int i = 0; i < 9; i++)
		{
			tmpNode = currentNode->children[i];
			if(tmpNode == NULL)
			{
				std::cout << "tmpNode is NULL tree element is NULL! i = " << i << std::endl;
			}
			else
			{
				//std::cout << "tmpNode is not NULL!! nodeID = " << tmpNode->nodeID << std::endl;
			}
			queue->add(tmpNode);
		}
		if( count < startPoint)
		{
			currentNode = queue->getNext();
			count++;
			//std::cout << "Remove Node from Queue\n";
		}
		else
		{
			continueLoop = false;
		}
		
	}while( currentNode != NULL & continueLoop );
	
	double tmpTileXCentre = 0;
	double tmpTileYCentre = 0;
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment in file heading.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Base Image (x,y), Warp Image (x,y)\n";
		
		//int count2 = 0;
		//int null_count = 0;
		//int normal_count = 0;
		int ctrlpointCounter = 0;
		// Write Data.
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			if(currentNode != NULL)
			{
				ctrlpointCounter++;
			/*	std::cout << "\nControl Point: " << ctrlpointCounter << std::endl;
				std::cout << "Image A: [" << currentNode->tileCoords->imgATLX << ", "
				<< currentNode->tileCoords->imgATLY << "]["
				<< currentNode->tileCoords->imgABRX << ", "
				<< currentNode->tileCoords->imgABRY << "]\n";
				std::cout << "Image B: [" << currentNode->tileCoords->imgBTLX << ", "
				<< currentNode->tileCoords->imgBTLY << "]["
				<< currentNode->tileCoords->imgBBRX << ", "
				<< currentNode->tileCoords->imgBBRY << "]\n";
			*/
				tmpTileXCentre = double(currentNode->tileCoords->imgATLX + 
										(double(currentNode->tileCoords->imgABRX - 
												currentNode->tileCoords->imgATLX)/2));
				tmpTileYCentre = double(currentNode->tileCoords->imgATLY + 
										(double(currentNode->tileCoords->imgABRY - 
												currentNode->tileCoords->imgATLY)/2));
				outputFile << "\t" << tmpTileXCentre << "\t" << tmpTileYCentre;
				//std::cout << "Image A Tile Centre: [" << tmpTileXCentre << ", " << tmpTileYCentre << "]"<< std::endl;
				
				tmpTileXCentre = double(currentNode->tileCoords->imgBTLX + 
								 (double(currentNode->tileCoords->imgBBRX - 
								  currentNode->tileCoords->imgBTLX)/2))
								  + currentNode->TileTransformation->shiftX 
								  + 0.25;

				tmpTileYCentre = double(currentNode->tileCoords->imgBTLY + 
								 (double(currentNode->tileCoords->imgBBRY - 
								   currentNode->tileCoords->imgBTLY)/2)
								  + currentNode->TileTransformation->shiftY)
								  + 0.25;
				outputFile << "\t" << tmpTileXCentre << "\t" << tmpTileYCentre << std::endl;
				//std::cout << "Image B Tile Centre: [" << tmpTileXCentre << ", " << tmpTileYCentre << "]"<< std::endl;

				//count2++;
				//normal_count++;
			}
			else
			{
				//std::cout << "Node " << count2 << " is NULL!!\n";
				//count2++;
				//null_count++;
			}
		}
		
		//std::cout << "Number of NULL nodes: " << null_count << std::endl;
		//std::cout << "Number of normal nodes: " << normal_count << std::endl;
		
		// Close File.
		outputFile.close();
		//std::cout << "File Closed\n";
	}
	else
	{
		if(queue != NULL)
		{
			delete queue;
		}
		if(currentNode != NULL)
		{
			//delete currentNode;
		}
		if(tmpNode != NULL)
		{
			//delete tmpNode;
		}
		// Throw exception if the file didn't open.
		throw FileOutputException("The output file can not be created", error_codes::cannot_create_output_file);
	}
	
	if(queue != NULL)
	{
		delete queue;
	}
	//std::cout << "Released Queue Memory!\n";
	if(currentNode != NULL)
	{
		//delete currentNode;
	}
	//std::cout << "Released CurrentNode Memory!\n";
	if(tmpNode != NULL)
	{
		//delete tmpNode;
	}
	//std::cout << "Released tmpNode Memory!\n";
}

void NonusImageTree::writeMap2Image2EnviGcpsFile(const char *outputFilePath, int treeDepth)
throw(FileOutputException, NonusImageTreeException)
{
	/*
	 * Tree Depth - Ranges from 0 - Max Depth.
	 * -1 = Max Depth.
	 */
	
	// Find the tree depth.	
	int maxLevel = 0;
	int currentLevelSize = 1;
	int levelIncrement = 1;
	bool continueLoop = true;
	
	while(continueLoop)
	{
		if(currentLevelSize < treeSize)
		{
			maxLevel++;
		}
		else
		{
			continueLoop = false;
		}
		levelIncrement = levelIncrement * 9;
		currentLevelSize = currentLevelSize + levelIncrement;
	}
	// Check inputted depth is within the depth of the tree 
	// and if -1 was inputted the max depth is used.
	if( treeDepth > maxLevel )
	{
		throw NonusImageTreeException("There is insuffient levels in the tree.", error_codes::insufficient_levels);
	}
	else
	{
		if( treeDepth == -1 )
		{
			treeDepth = maxLevel;
		}
	}
	
	// Find the size and finish to the level.
	currentLevelSize = 1;
	levelIncrement = 1;
	int startPoint = 0;
	int finishPoint = 0;
	for(int i = 0; i <= treeDepth; i++)
	{
		if(i == treeDepth)
		{
			finishPoint = currentLevelSize;
		}
		else
		{
			startPoint = currentLevelSize;
			levelIncrement = levelIncrement * 9;
			currentLevelSize = currentLevelSize + levelIncrement;
		}
	}
	
	//std::cout << "treeDepth = " << treeDepth << " startPoint = " << startPoint 
	//	      << " finishPoint = " << finishPoint << std::endl;
	
	// Prepare Queue with items to be written out.
	Queue *queue = NULL;
	queue = new Queue;
	NonusTreeNode *currentNode = root;
	int count = 1;
	continueLoop = true;
	do
	{
		// Print out current Node
		// Add current Node's children to the Queue.
		for(int i = 0; i < 9; i++)
		{
			queue->add(currentNode->children[i]);
		}
		if( count < startPoint)
		{
			currentNode = queue->getNext();
			count++;
			//std::cout << "Remove Node from Queue\n";
		}
		else
		{
			continueLoop = false;
		}
		
	}while( currentNode != NULL & continueLoop );
	
	double tmpTileXCentre = 0;
	double tmpTileYCentre = 0;
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment in file heading.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Map (eastings,northings), Warp Image (x,y)\n";
		
		double tmp1 = 0;
		double tmp2 = 0;
		// Write Data.
		while(queue->getSize() > 0)
		{
			
			currentNode = queue->getNext();
			
			tmp1 = double(currentNode->tileCoords->eastingBR - 
						  currentNode->tileCoords->eastingTL);
			tmp2 = tmp1/2;
			tmpTileXCentre = double(currentNode->tileCoords->eastingTL + tmp2)-1;
			
			tmp1 = double(currentNode->tileCoords->northingTL - 
						  currentNode->tileCoords->northingBR);
			tmp2 = tmp1/2;
			tmpTileYCentre = double(currentNode->tileCoords->northingBR + tmp2);
			
			outputFile << "\t" << tmpTileXCentre << "\t" << tmpTileYCentre;
			
			tmpTileXCentre = double(currentNode->tileCoords->imgBTLX + 
								(double(currentNode->tileCoords->imgBBRX - 
								currentNode->tileCoords->imgBTLX)/2))
								+ currentNode->TileTransformation->shiftX 
								+ 0.25;
			
			tmpTileYCentre = double(currentNode->tileCoords->imgBTLY + 
								(double(currentNode->tileCoords->imgBBRY - 
								currentNode->tileCoords->imgBTLY)/2)
								+ currentNode->TileTransformation->shiftY)
								+ 0.25;
			outputFile << "\t" << tmpTileXCentre << "\t" << tmpTileYCentre << std::endl;
			
		}
		
		// Close File.
		outputFile.close();
	}
	else
	{
		// Throw exception if the file didn't open.
		throw FileOutputException("The output file can not be created", error_codes::cannot_create_output_file);
	}
	
	if(queue != NULL)
	{
		delete queue;
	}
}

void NonusImageTree::writeMap2Image2EnviGcpsFile(const char *outputFilePath, int treeDepth, double xScale, double yScale)
throw(FileOutputException, NonusImageTreeException)
{
	/*
	 * Tree Depth - Ranges from 0 - Max Depth.
	 * -1 = Max Depth.
	 */
	
	// Find the tree depth.	
	int maxLevel = 0;
	int currentLevelSize = 1;
	int levelIncrement = 1;
	bool continueLoop = true;
	
	while(continueLoop)
	{
		if(currentLevelSize < treeSize)
		{
			maxLevel++;
		}
		else
		{
			continueLoop = false;
		}
		levelIncrement = levelIncrement * 9;
		currentLevelSize = currentLevelSize + levelIncrement;
	}
	// Check inputted depth is within the depth of the tree 
	// and if -1 was inputted the max depth is used.
	if( treeDepth > maxLevel )
	{
		throw NonusImageTreeException("There is insuffient levels in the tree.", error_codes::insufficient_levels);
	}
	else
	{
		if( treeDepth == -1 )
		{
			treeDepth = maxLevel;
		}
	}
	
	// Find the size and finish to the level.
	currentLevelSize = 1;
	levelIncrement = 1;
	int startPoint = 0;
	int finishPoint = 0;
	for(int i = 0; i <= treeDepth; i++)
	{
		if(i == treeDepth)
		{
			finishPoint = currentLevelSize;
		}
		else
		{
			startPoint = currentLevelSize;
			levelIncrement = levelIncrement * 9;
			currentLevelSize = currentLevelSize + levelIncrement;
		}
	}
	
	//std::cout << "treeDepth = " << treeDepth << " startPoint = " << startPoint 
	//	      << " finishPoint = " << finishPoint << std::endl;
	
	// Prepare Queue with items to be written out.
	Queue *queue = NULL;
	queue = new Queue;
	NonusTreeNode *currentNode = root;
	int count = 1;
	continueLoop = true;
	do
	{
		// Print out current Node
		// Add current Node's children to the Queue.
		for(int i = 0; i < 9; i++)
		{
			queue->add(currentNode->children[i]);
		}
		if( count < startPoint)
		{
			currentNode = queue->getNext();
			count++;
			//std::cout << "Remove Node from Queue\n";
		}
		else
		{
			continueLoop = false;
		}
		
	}while( currentNode != NULL & continueLoop );
	
	double tmpTileXCentre = 0;
	double tmpTileYCentre = 0;
	double tmp1 = 0;
	double tmp2 = 0;
	double tmpTileXCentreScaled = 0;
	double tmpTileYCentreScaled = 0;
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		// Write Comment in file heading.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Map (eastings,northings), Warp Image (x,y)\n";
		
		// Write Data.
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			
			tmp1 = double(currentNode->tileCoords->eastingBR - 
						  currentNode->tileCoords->eastingTL);
			tmp2 = tmp1/2;
			tmpTileXCentre = double(currentNode->tileCoords->eastingTL + tmp2)-2;
			
			tmp1 = double(currentNode->tileCoords->northingTL - 
						  currentNode->tileCoords->northingBR);
			tmp2 = tmp1/2;
			tmpTileYCentre = double(currentNode->tileCoords->northingBR + tmp2);
			
			outputFile << "\t" << tmpTileXCentre << "\t" << tmpTileYCentre;			
			
			tmpTileXCentre = double(currentNode->tileCoords->imgBTLX + 
									(double(currentNode->tileCoords->imgBBRX - 
											currentNode->tileCoords->imgBTLX)/2))
				+ currentNode->TileTransformation->shiftX;
			tmpTileYCentre = double(currentNode->tileCoords->imgBTLY + 
									(double(currentNode->tileCoords->imgBBRY - 
											currentNode->tileCoords->imgBTLY)/2)
									+ currentNode->TileTransformation->shiftY);
			if( xScale == 0)
			{
				tmpTileXCentreScaled = tmpTileXCentre + 0.25;
			}
			else
			{
				tmpTileXCentreScaled = (tmpTileXCentre*xScale) + (1/xScale)/4;
			}
			
			if( yScale == 0)
			{
				tmpTileYCentreScaled = tmpTileYCentre + 0.25;
			}
			else
			{
				tmpTileYCentreScaled = (tmpTileYCentre*yScale) + (1/yScale)/4;
			}
			
			outputFile << "\t" << tmpTileXCentreScaled << "\t" << tmpTileYCentreScaled << std::endl;
		}
		
		// Close File.
		outputFile.close();
	}
	else
	{
		// Throw exception if the file didn't open.
		throw FileOutputException("The output file can not be created", error_codes::cannot_create_output_file);
	}
	
	if(queue != NULL)
	{
		delete queue;
	}
}

void NonusImageTree::write2EnviGcpsFile(const char *outputFilePath, int treeDepth, double xScale, double yScale)
throw(FileOutputException, NonusImageTreeException)
{
	//std::cout << "X Scale: " << xScale << " Y Scale: " << yScale << std::endl;
	/*
	 * Tree Depth - Ranges from 0 - Max Depth.
	 * -1 = Max Depth.
	 */
	
	// Find the tree depth.	
	int maxLevel = 0;
	int currentLevelSize = 1;
	int levelIncrement = 1;
	bool continueLoop = true;
	
	while(continueLoop)
	{
		if(currentLevelSize < treeSize)
		{
			maxLevel++;
		}
		else
		{
			continueLoop = false;
		}
		levelIncrement = levelIncrement * 9;
		currentLevelSize = currentLevelSize + levelIncrement;
	}
	
	//std::cout << "Number of Levels = " << maxLevel << std::endl;
	
	// Check inputted depth is within the depth of the tree 
	// and if -1 was inputted the max depth is used.
	if( treeDepth > maxLevel )
	{
		throw NonusImageTreeException("There is insuffient levels in the tree.", 
									  error_codes::insufficient_levels);
	}
	else
	{
		if( treeDepth == -1 )
		{
			treeDepth = maxLevel;
		}
	}
	
	//std::cout << "Tree Depth = " << treeDepth << std::endl;
	
	// Find the size and finish to the level.
	currentLevelSize = 1;
	levelIncrement = 1;
	int startPoint = 0;
	int finishPoint = 0;
	for(int i = 0; i <= treeDepth; i++)
	{
		if(i == treeDepth)
		{
			finishPoint = currentLevelSize;
		}
		else
		{
			startPoint = currentLevelSize;
			levelIncrement = levelIncrement * 9;
			currentLevelSize = currentLevelSize + levelIncrement;
		}
	}
	
	//std::cout << "treeDepth = " << treeDepth << " startPoint = " << startPoint 
	//	      << " finishPoint = " << finishPoint << std::endl;
	
	// Prepare Queue with items to be written out.
	Queue *queue = NULL;
	queue = new Queue;
	NonusTreeNode *currentNode = root;
	NonusTreeNode *tmpNode;
	int count = 1;
	continueLoop = true;
	do
	{
		// Print out current Node
		// Add current Node's children to the Queue.
		for(int i = 0; i < 9; i++)
		{
			tmpNode = currentNode->children[i];
			if(tmpNode == NULL)
			{
				std::cout << "tmpNode is NULL tree element is NULL! i = " << i << std::endl;
			}
			else
			{
				//std::cout << "tmpNode is not NULL!! nodeID = " << tmpNode->nodeID << std::endl;
			}
			queue->add(tmpNode);
		}
		if( count < startPoint)
		{
			currentNode = queue->getNext();
			count++;
			//std::cout << "Remove Node from Queue\n";
		}
		else
		{
			continueLoop = false;
		}
		
	}while( currentNode != NULL & continueLoop );
	
	double tmpTileXCentre = 0;
	double tmpTileYCentre = 0;
	double tmpTileXCentreScaled = 0;
	double tmpTileYCentreScaled = 0;
	// Open the file.
	std::ofstream outputFile(outputFilePath);
	if(outputFile.is_open())
	{
		
		// Write Comment in file heading.
		outputFile << "; Ground Control Points for ENVI created from Image Registration\n";
		outputFile << "; software created at the University of Wales, Aberystwyth. For\n";
		outputFile << "; more infomation please contact pjb00@aber.ac.uk\n";
		outputFile << "; Base Image (x,y), Warp Image (x,y)\n";
		
		// Write Data.
		while(queue->getSize() > 0)
		{
			currentNode = queue->getNext();
			tmpTileXCentre = double(currentNode->tileCoords->imgATLX + 
							  (double(currentNode->tileCoords->imgABRX - 
								currentNode->tileCoords->imgATLX)/2));
			tmpTileYCentre = double(currentNode->tileCoords->imgATLY + 
				(double(currentNode->tileCoords->imgABRY - 
				  currentNode->tileCoords->imgATLY)/2));

			outputFile << "\t" << tmpTileXCentre << "\t" << tmpTileYCentre;
			
			tmpTileXCentre = double(currentNode->tileCoords->imgBTLX + 
							  (double(currentNode->tileCoords->imgBBRX - 
								currentNode->tileCoords->imgBTLX)/2))
								+ currentNode->TileTransformation->shiftX;
			tmpTileYCentre = double(currentNode->tileCoords->imgBTLY + 
							(double(currentNode->tileCoords->imgBBRY - 
							  currentNode->tileCoords->imgBTLY)/2)
							  + currentNode->TileTransformation->shiftY);
			if( xScale == 0)
			{
				tmpTileXCentreScaled = tmpTileXCentre + 0.25;
			}
			else
			{
				tmpTileXCentreScaled = (tmpTileXCentre*xScale) + (1/xScale)/4;
			}
			
			if( yScale == 0)
			{
				tmpTileYCentreScaled = tmpTileYCentre + 0.25;
			}
			else
			{
				tmpTileYCentreScaled = (tmpTileYCentre*yScale) + (1/yScale)/4;
			}
			
			outputFile << "\t" << tmpTileXCentreScaled << "\t" << tmpTileYCentreScaled << std::endl;
		}
		
		// Close File.
		outputFile.close();
	}
	else
	{
		// Throw exception if the file didn't open.
		throw FileOutputException("The output file can not be created", error_codes::cannot_create_output_file);
	}
	
	if(queue != NULL)
	{
		delete queue;
	}
}

int NonusImageTree::getNodesAtLevel(int level, NonusTreeNode **nodes, int length)
throw(NonusImageTreeException)
{
	// Count number of levels in the tree.
	int maxLevel = 0;
	int currentLevelSize = 1;
	int levelIncrement = 1;
	bool continueLoop = true;
	
	while(continueLoop)
	{
		if(currentLevelSize < treeSize)
		{
			maxLevel++;
		}
		else
		{
			continueLoop = false;
		}
		levelIncrement = levelIncrement * 9;
		currentLevelSize = currentLevelSize + levelIncrement;
	}
	
	if( level > maxLevel )
	{
		throw NonusImageTreeException("There is insuffient levels in the tree.", 
									  error_codes::insufficient_levels);
	}
	
	//Calculate start and end points.
	int start = 1;
	int end = 0;
	if(level == 0 )
	{
		start = 0;
		end = 1;
	}
	else
	{
		levelIncrement = 1;
		for(int i = 0; i < level-1; i++)
		{
			levelIncrement = levelIncrement * 9;
			start = start + levelIncrement;
		}
		end = start + (levelIncrement * 9);
	}
	
	//std::cout << "Length " << length << " end-start = " << (end-start) << std::endl;
	//std::cout << "Level = " << level << " Max Level = " << maxLevel << " Start = " << start << " End = " << end << std::endl;
	
	if(length < (end-start))
	{
		throw NonusImageTreeException("The list passed in is of insuffient length for this output.", 
									  error_codes::insufficient_levels);
	}
	
	Queue *queue = NULL;
	queue = new Queue;
	NonusTreeNode *currentNode = root;
	NonusTreeNode *tmpNode;
	int count = 1;
	int listCount = 0;
	continueLoop = true;
	do
	{
		for(int i = 0; i < 9; i++)
		{
			tmpNode = currentNode->children[i];
			if(tmpNode == NULL)
			{
				std::cout << "tmpNode is NULL tree element is NULL! i = " << i << std::endl;
			}
			queue->add(tmpNode);
		}
		
		if( count < start)
		{
			currentNode = queue->getNext();
			count++;
		}
		else if(count >= start & count < end)
		{
			// add to output list.
			currentNode = queue->getNext();
			//std::cout << "Node " << listCount << " has ID " << currentNode->nodeID << std::endl;
			nodes[listCount++] = currentNode;
			count++;
		}
		else
		{
			count++;
			continueLoop = false;
		}
		
	}while( currentNode != NULL & continueLoop );
	return ++listCount;
}

void NonusImageTree::estimateRequiredNodes(int xPixels, 
										   int yPixels, 
										   int minTileSize, 
										   TreeLevel *treeLevels, 
										   int numLevels)
{
	MathUtils mathUtils;
	int numNodes = 1;
	int nodesAtLevel = 1;
	int xPixelsAtLevel = xPixels;
	int yPixelsAtLevel = yPixels;

	treeLevels[0].level = 0;
	treeLevels[0].nodesAtLevel = 1;
	treeLevels[0].totalNodes = 1;
	treeLevels[0].xDistance = xPixelsAtLevel;
	treeLevels[0].yDistance = yPixelsAtLevel;
	treeLevels[0].angularDistance = sqrt((xPixelsAtLevel*xPixelsAtLevel)+(yPixelsAtLevel*yPixelsAtLevel));
	
	for(int i = 1; i < numLevels; i++)
	{
		// Add Level to Structure
		treeLevels[i].level = i;
		
		// Calculate Nodes at Level
		nodesAtLevel = nodesAtLevel * 9;
		treeLevels[i].nodesAtLevel = nodesAtLevel;
		
		// Increment total number of nodes.
		numNodes = numNodes + nodesAtLevel;
		treeLevels[i].totalNodes = numNodes;
		
		// Create x Size of tiles at level
		xPixelsAtLevel = mathUtils.round(((double)xPixelsAtLevel)/3);
		treeLevels[i].xDistance = xPixelsAtLevel;
		
		// Create y Size of tiles at level
		yPixelsAtLevel = mathUtils.round(((double)yPixelsAtLevel)/3);
		treeLevels[i].yDistance = yPixelsAtLevel;
		
		// Calcuate Angular distance at level
		treeLevels[i].angularDistance = sqrt((xPixelsAtLevel*xPixelsAtLevel)+(yPixelsAtLevel*yPixelsAtLevel));	
	}	
}

int NonusImageTree::estimateNumberLevels(int xPixels, int yPixels, int minTileSize)
{
	MathUtils mathUtils;
	int numPixels = 0;
	int numLevels = -1;
	
	if(xPixels < yPixels)
	{
		numPixels = xPixels;
	}
	else
	{
		numPixels = yPixels;
	}
	
	while(numPixels > minTileSize)
	{
		numPixels = mathUtils.round(((double)numPixels)/3);
		numLevels++;
	}
	return ++numLevels;
}

int NonusImageTree::getNumNodes()
{
	return treeSize;
}

NonusTreeNode* NonusImageTree::getRoot()
{
	return root;
}

NonusImageTree::~NonusImageTree()
{
	// Needs to be implemented.
}
