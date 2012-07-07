##########################################
# Makefile for ImageRegistration Package #
#                                        #
# Author: Peter Bunting                  #
# Contact: pjb00@aber.ac.uk              #
# Date: 22/08/2006                       #
# Version: 1.00                          #
##########################################

CC = gcc
CXXFLAGS = -Os  -lgdal -dynamic
EXECUTABLE = ImageRegistration

ImgReg_Input = ArrayUtils.h \
	      	   ArrayUtils.cpp \
	      	   ImageTiling.h \
	           ImageRegistrationException.h \
	           ImageRegistrationException.cpp \
	           ImageNotAvailableException.h \
	           ImageNotAvailableException.cpp \
		   ErrorCodes.h \
	           FileOutputException.h \
	      	   FileOutputException.cpp \
	           ImageOutputException.h \
	           ImageOutputException.cpp \
	           ImageProcessingException.h \
	           ImageProcessingException.cpp \
		   NonusImageTreeException.h \
		   NonusImageTreeException.cpp \
	           MathUtils.h \
	           MathUtils.cpp \
	           ImageOverlap.h \
	           ImageOverlap.cpp \
	           Interpolation.h \
	           Interpolation.cpp \
	           ImageNetworkStructures.h \
	           QueueException.h \
	           QueueException.cpp \
	           NonusTreeNode.h \
	           NetworkNodesLookUpException.h \
	           NetworkNodesLookUpException.cpp \
	           SortedNodeDistanceException.h \
	           SortedNodeDistanceException.cpp \
	           NetworkNodesLookUp.h \
	           NetworkNodesLookUp.cpp \
	           NodeQueue.h \
	           NodeQueue.cpp \
	           SortedNodeDistance.h \
	           SortedNodeDistance.cpp \
	           ImagePyramid.h \
	           ImagePyramid.cpp \
	           ImageNetworkException.h \
	           ImageNetworkException.cpp \
	           TransformsTableException.h \
	           TransformsTableException.cpp \
	           Queue.h \
	           Queue.cpp \
	           JointHistogram.h \
	           JointHistogram.cpp \
	           ImageNetwork.h \
	           ImageNetwork.cpp \
	           TransformsTable.h \
	           TransformsTable.cpp \
	           CorrelationMeasures.h \
	           CorrelationMeasures.cpp \
	           ImageMeasures.h \
	           VectorImageMeasures.h \
	           VectorImageMeasures.cpp \
	           MutualInformation.h \
	           MutualInformation.cpp \
	           JointHistogramImageMeasures.h \
	           JointHistogramImageMeasures.cpp \
	           NonusImageTree.h \
	           NonusImageTree.cpp \
	           RegisterImages.h \
	           RegisterImages.cpp \
	           ImageHistogram.h \
	           ImageHistogram.cpp \
	           ImageUtil.h \
	           ImageUtil.cpp \
	           ImagesUtil.h \
	           ImagesUtil.cpp \
	           VectorExport.h \
	           VectorExport.cpp \
	           TransformsTableTests.h \
	           TransformsTableTests.cpp \
	           TestImageRegistration.h \
	           TestImageRegistration.cpp \
	           ProcessInputParameters.h \
	           ProcessInputParameters.cpp \
	           main.cpp
	         
ImgReg_Input_cpp = ArrayUtils.cpp \
	           ImageRegistrationException.cpp \
	      	   FileOutputException.cpp \
	           ImageOutputException.cpp \
	           ImageNotAvailableException.cpp \
	           ImageProcessingException.cpp \
		   NonusImageTreeException.cpp \
	           MathUtils.cpp \
	           ImageOverlap.cpp \
	           Interpolation.cpp \
	           QueueException.cpp \
	           NetworkNodesLookUpException.cpp \
	           SortedNodeDistanceException.cpp \
	           NetworkNodesLookUp.cpp \
	           NodeQueue.cpp \
	           SortedNodeDistance.cpp \
	           ImagePyramid.cpp \
	           ImageNetworkException.cpp \
	           TransformsTableException.cpp \
	           Queue.cpp \
	           JointHistogram.cpp \
	           ImageNetwork.cpp \
	           TransformsTable.cpp \
	           CorrelationMeasures.cpp \
	           VectorImageMeasures.cpp \
	           MutualInformation.cpp \
	           JointHistogramImageMeasures.cpp \
	           NonusImageTree.cpp \
	           RegisterImages.cpp \
	           ImageHistogram.cpp \
	           ImageUtil.cpp \
	           ImagesUtil.cpp \
	           VectorExport.cpp \
	           TransformsTableTests.cpp \
	           TestImageRegistration.cpp \
	           ProcessInputParameters.cpp \
	           main.cpp
	           
ImageRegistration : $(ImgReg_Input)
	$(CC) $(CXXFLAGS)  $(ImgReg_Input_cpp)  -o $(EXECUTABLE)

Clean: 
	rm -rf  $(EXECUTABLE)

