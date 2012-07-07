#include <iostream>
#include "gdal_priv.h"
#include "ImageHistogram.h"
#include "JointHistogram.h"
#include "ImageUtil.h"
#include "ImagesUtil.h"
#include "MutualInformation.h"
#include <string>
#include "ImageNotAvailableException.h"
#include "TestImageRegistration.h"
#include "ImageMeasures.h"
#include "VectorExport.h"
#include "Interpolation.h"
#include "TransformsTableTests.h"
#include "ProcessInputParameters.h"

class Control
{
public:
	void runImageRegistrationTests();
	void runImageInterpolationTests();
	
	void generateImageHistogram(const char *file, int bins);
	
	void generateJointHistogram(const char *ref, 
								const char *floating, 
								const char *outfilename, 
								int bins, 
								int refBand, 
								int floatBand);
	
	void registerImagesBufferSearch(const char *ref, 
									const char *floating, 
									const char *outfilename, 
									int buffer, 
									int bins, 
									int refBand, 
									int floatBand);
	
	void imagesOverlap(const char *ref, const char *floating);
	
	void calcMI(const char *ref, 
				const char *floating, 
				int bins, 
				int refBand, 
				int floatBand);
	
	void registerImagesNonLinearTransformation(const char *ref, 
											   const char *floating, 
											   int buffer, 
											   int bins, 
											   int refBand, 
											   int floatBand,
											   int minTileSize);
	
	void registerImagesNonLinearTransformationSubPixel(const char *ref, 
													   const char *floating, 
													   const char *outfilename, 
													   int buffer, 
													   int bins, 
													   int refBand, 
													   int floatBand,
													   int minTileSize,
													   float tileMovement,
													   int measure);
	
	void registerImagesNonLinearTransformationEstimateSubPixel(const char *ref,
															   const char *floating,
															   const char *ptsOutputFile,
															   int searchBuffer,
															   int jhBins,
															   int refBand,
															   int floatBand,
															   int minTileSize,
															   int distanceMeasure);
	void registerMultiResolutionImagesNonLinearTransformationEstimateSubPixel(const char *ref,
																			  const char *floating,
																			  const char *ptsOutputFile,
																			  int searchBuffer,
																			  int jhBins,
																			  int refBand,
																			  int floatBand,
																			  int minTileSize,
																			  int distanceMeasure);
	void registerAllImageUsingSubPixelDiffResolutions(const char *ref,
													  const char *floating,
													  const char *ptsOutputFile,
													  int searchBuffer,
													  int jhBins,
													  int refBand,
													  int floatBand,
													  int minTileSize,
													  int distanceMeasure,
													  bool errorCorrection,
													  int search,
													  float measureThreshold);
	
	void runImageInterpolationTests(const char *imageFilepath, double shift, int pixelMovement, int imageBand);
	void vectorOutput();
	void testImageInterpolation(const char *data, 
								double outputXResolution,
								double outputYResolution,
								const char *filename, 
								const char *format, 
								int band);
	
	void findControlPoints(const char *reference,
						   const char *floating,
						   const char *ptsOutputPath,
						   const char *tmpPath,
						   int searchBuffer,
						   int jhBins,
						   int refBand,
						   int floatBand,
						   int minTileSize,
						   int measure,
						   int search,
						   int numWalks,
						   int tmax,
						   int tdecrease,
						   int successful,
						   int unsuccessful,
						   bool image2image,
						   bool image2imageScaled,
						   bool map2image,
						   bool map2imageScaled,
						   bool errorCorrection,
						   float measureThreshold);
	void findControlPointsNetwork(const char *reference,
								  const char *floating,
								  const char *tmpPath,
								  const char *ptsOutput,
								  int refBand,
								  int floatBand,
								  int distanceMeasure,
								  int searchAlgor,
								  int searchArea,
								  int jhBins,
								  int numWalks,
								  int tmax,
								  int tdecrease,
								  int successful,
								  int unsuccessful,
								  float thresholdMeasure,
								  int numLevels,
								  int xPixelStep,
								  int yPixelStep,
								  float *levelScales,
								  int *windowLevel,
								  int numberIterations,
								  int networkDistanceThreshold,
								  double* networkUpdateWeights,
								  int* distanceSteps,
								  int numberOfSteps,
								  int correctionStdDev,
								  double tilePercentageRangeThreshold,
								  bool image2image,
								  bool image2imageScaled,
								  bool map2image,
								  bool map2imageScaled,
								  bool printFilepaths,
								  bool printOverlap,
								  bool performReg);
	
	void runTableTests();
	void useExternalFile(const char* file);
	void findMeasuresStrip(const char *refImage,
						   const char *floatImage,
						   int *origin, 
						   int refBand,
						   int floatBand,
							int axis, 
							int length, 
							int windowSize, 
							int measure, 
						    int bins,
						   const char *outputFile);
};

void Control::generateImageHistogram(const char *file, int bins)
{
	ImageHistogram *imgHis = new ImageHistogram(bins);
	ImageUtil *imgUtil = new ImageUtil(file);
	imgUtil->generateHistogram(*imgHis);
	imgHis->printTextHistogram();
}

void Control::generateJointHistogram(const char *ref, 
									 const char *floating, 
									 const char *outfilename, 
									 int bins, 
									 int refBand, 
									 int floatBand)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->generateJointHistogram(refBand, floatBand, outfilename, bins);
	}
	catch(ImageNotAvailableException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	catch(ImageRegistrationException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::registerImagesBufferSearch(const char *ref, 
										 const char *floating, 
										 const char *outfilename, 
										 int buffer, 
										 int bins, 
										 int refBand, 
										 int floatBand)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->registerImages(buffer, outfilename, bins, refBand, floatBand);
	}
	catch(ImageNotAvailableException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::calcMI(const char *ref, 
					 const char *floating,  
					 int bins, 
					 int refBand, 
					 int floatBand)
{		
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		double mi = imgsUtil->calcMI(bins, refBand, floatBand);
		std::cout << "MI = " << mi << std::endl;
	}
	catch(ImageNotAvailableException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	catch(ImageRegistrationException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::registerImagesNonLinearTransformation(const char *ref, 
													const char *floating, 
													int buffer, 
													int bins, 
													int refBand, 
													int floatBand,
													int minTileSize)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->registerImagesNonLinearTransformation(buffer, bins, refBand, floatBand, minTileSize);
	}
	catch(ImageNotAvailableException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::imagesOverlap(const char *ref, const char *floating)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->printOverlap(false);
	}
	catch(ImageNotAvailableException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::registerImagesNonLinearTransformationSubPixel(const char *ref, 
															const char *floating, 
															const char *outfilename, 
															int buffer, 
															int bins, 
															int refBand, 
															int floatBand,
															int minTileSize,
															float tileMovement,
															int measure)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->registerImagesNonLinearTransformationSubPixel(outfilename, 
																buffer, 
																bins, 
																refBand, 
																floatBand, 
																minTileSize, 
																tileMovement,
																measure);
	}
	catch( ImageRegistrationException e )
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::registerImagesNonLinearTransformationEstimateSubPixel(const char *ref,
																	const char *floating,
																	const char *ptsOutputFile,
																	int searchBuffer,
																	int jhBins,
																	int refBand,
																	int floatBand,
																	int minTileSize,
																	int distanceMeasure)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->registerImagesNonLinearTransformationEstimateSubPixel(ptsOutputFile, 
																		searchBuffer, 
																		jhBins, 
																		refBand, 
																		floatBand, 
																		minTileSize, 
																		distanceMeasure);
	}
	catch( ImageRegistrationException e )
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::registerAllImageUsingSubPixelDiffResolutions(const char *ref,
														   const char *floating,
														   const char *ptsOutputFile,
														   int searchBuffer,
														   int jhBins,
														   int refBand,
														   int floatBand,
														   int minTileSize,
														   int distanceMeasure,
														   bool errorCorrection,
														   int search,
														   float measureThreshold)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->registerAllImagesSubPixelDiffResolutions(ptsOutputFile, 
														   "/home/pjb/rsgis/tmp_image_file.tif",
														   searchBuffer, 
														   jhBins, 
														   refBand, 
														   floatBand, 
														   minTileSize, 
														   distanceMeasure,
														   search,
														   10,
														   100,
														   10,
														   10,
														   20,
														   true,
														   false,
														   false,
														   false,
														   errorCorrection,
														   measureThreshold);
	}
	catch( ImageRegistrationException e )
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}


void Control::registerMultiResolutionImagesNonLinearTransformationEstimateSubPixel(const char *ref,
																				   const char *floating,
																				   const char *ptsOutputFile,
																				   int searchBuffer,
																				   int jhBins,
																				   int refBand,
																				   int floatBand,
																				   int minTileSize,
																				   int distanceMeasure)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(ref, floating, true);
		imgsUtil->registerImagesMultiResolutionNonLinearTransformationEstimateSubPixel(ptsOutputFile, 
																					   searchBuffer, 
																					   jhBins, 
																					   refBand, 
																					   floatBand, 
																					   minTileSize, 
																					   distanceMeasure);
	}
	catch( ImageRegistrationException e )
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::runImageRegistrationTests()
{
	std::cout << "Running tests..." << std::endl;
	const char *referenceImage = "/home/pjb/rsgis/registration_test_images/casi/p142_casi_ref.tif";
	const char *floatingImage = "/home/pjb/rsgis/registration_test_images/casi/p142_casi_ref.tif";
	TestImageRegistration *test = new TestImageRegistration;
	for(int i = 0; i < 22; i++)
	{
		test->testImageOverlap(i, referenceImage, floatingImage);
	}
	
	test->testMIValues(referenceImage, floatingImage);
}

void Control::runImageInterpolationTests()
{
	TestImageRegistration *test = new TestImageRegistration;
	test->testImageInterpolation();
	//test->testTriangularImageInterpolation();
}

void Control::runImageInterpolationTests(const char *imageFilepath, double shift, int pixelMovement, int imageBand)
{
	TestImageRegistration *test = new TestImageRegistration;
	test->testEuclideanDistanceUsingSmallImages(imageFilepath, shift, pixelMovement, imageBand);
}

void Control::vectorOutput()
{
	VectorExport vecExport;
	vecExport.outputVector();
}

void Control::testImageInterpolation(const char *data,  
									 double outputXResolution,
									 double outputYResolution,
									 const char *filename, 
									 const char *format, 
									 int band)
{
	GDALAllRegister();
	try
	{
		Interpolation interpolation;
		GDALDataset *newImage;
		GDALDataset *imageData;
		imageData = (GDALDataset *) GDALOpen(data, GA_ReadOnly);
		if(imageData == NULL)
		{
			std::cout << "Bugger could not open Image " << data << std::endl;
			throw ImageNotAvailableException("Could not Open Image.", error_codes::reference_image);
		}
		newImage = interpolation.createNewImage(imageData, outputXResolution, outputYResolution, filename, format, band);
		GDALClose(newImage);
		GDALClose(imageData);
	}
	catch(FileOutputException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	catch(ImageOutputException e)
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
}

void Control::runTableTests()
{
	TransformsTableTests *tests = new TransformsTableTests;
	tests->runTests();
	delete tests;
}


void Control::findControlPoints(const char *reference,
								const char *floating,
								const char *ptsOutputPath,
								const char *tmpPath,
								int searchBuffer,
								int jhBins,
								int refBand,
								int floatBand,
								int minTileSize,
								int measure,
								int search,
								int numWalks,
								int tmax,
								int tdecrease,
								int successful,
								int unsuccessful,
								bool image2image,
								bool image2imageScaled,
								bool map2image,
								bool map2imageScaled,
								bool errorCorrection,
								float measureThreshold)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(reference, floating, true);
		imgsUtil->registerAllImagesSubPixelDiffResolutions(ptsOutputPath, 
														   tmpPath,
														   searchBuffer, 
														   jhBins, 
														   refBand, 
														   floatBand, 
														   minTileSize, 
														   measure,
														   search,
														   numWalks,
														   tmax,
														   tdecrease,
														   successful,
														   unsuccessful,
														   image2image,
														   image2imageScaled,
														   map2image,
														   map2imageScaled,
														   errorCorrection,
														   measureThreshold);
	}
	catch( ImageRegistrationException e )
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
}

void Control::findControlPointsNetwork(const char *reference,
									   const char *floating,
									   const char *tmpPath,
									   const char *ptsOutput,
									   int refBand,
									   int floatBand,
									   int distanceMeasure,
									   int searchAlgor,
									   int searchArea,
									   int jhBins,
									   int numWalks,
									   int tmax,
									   int tdecrease,
									   int successful,
									   int unsuccessful,
									   float thresholdMeasure,
									   int numLevels,
									   int xPixelStep,
									   int yPixelStep,
									   float *levelScales,
									   int *windowLevel,
									   int numberIterations,
									   int networkDistanceThreshold,
									   double* networkUpdateWeights,
									   int* distanceSteps,
									   int numberOfSteps,
									   int correctionStdDev,
									   double tilePercentageRangeThreshold,
									   bool image2image,
									   bool image2imageScaled,
									   bool map2image,
									   bool map2imageScaled,
									   bool printFilepaths,
									   bool printOverlap,
									   bool performReg)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(reference, floating, printFilepaths);
		
		if(printOverlap)
		{
			imgsUtil->printOverlap(true);
		}
		
		if(performReg)
		{
			imgsUtil->findControlPointsNetwork( tmpPath,
												ptsOutput,
												refBand,
												floatBand,
												distanceMeasure,
												searchAlgor,
												searchArea,
												jhBins,
												numWalks,
												tmax,
												tdecrease,
												successful,
												unsuccessful,
												thresholdMeasure,
												numLevels,
												xPixelStep,
												yPixelStep,
												levelScales,
												windowLevel,
												numberIterations,
												networkDistanceThreshold,
												networkUpdateWeights,
												distanceSteps,
												numberOfSteps,
												correctionStdDev,
												tilePercentageRangeThreshold,
												image2image,
												image2imageScaled,
												map2image,
												map2imageScaled);
		}
		
	}
	catch( ImageRegistrationException e )
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}
	
}

void Control::useExternalFile(const char* file)
{
	ProcessInputParameters processInput;
	processInput.runRegistration(file);
}

void Control::findMeasuresStrip(const char *refImage,
								const char *floatImage,
								int *origin, 
								int refBand,
								int floatBand,
								int axis, 
								int length, 
								int windowSize, 
								int measure, 
								int bins,
								const char *outputFile)
{
	ImagesUtil *imgsUtil;
	try
	{
		imgsUtil = new ImagesUtil(refImage, floatImage, true);
		imgsUtil->findSimilarityStrip(origin,
									  refBand,
									  floatBand,
									  axis, 
									  length,
									  windowSize, 
									  measure, 
									  bins,
									  outputFile);
	}
	catch( ImageRegistrationException e )
	{
		std::cout << "An Exception has occured: " << e.what() << std::endl;
		std::cout << "Error Code: " << e.getErrorCode() << std::endl;
		std::exit(-1);
	}
	
	if( imgsUtil != NULL )
	{
		delete imgsUtil;
	}	
}


int main (int argc, char * const argv[]) 
{	
	Control *ctrl = new Control;
	/*int origin[2] = {250,250};
	
	ctrl->findMeasuresStrip("/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene1_landsatFPC_subset",
							"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene1_ALOS_Landsat_2X3Y_tif.tif",
							origin,
							1, //refband
							1, //floatband
							0, //axis
							100, //length
							25, // window size
							3, // Measure
							100, //bins
							"/Users/pete/Desktop/strips/test.txt");*/
	
	
	float scaleLevels[3] = {2, 2, 2};
	int levelWindows[3] = {25, 25, 25};
	double networkUpdateWeights[3] = {0.2, 0.2, 0.2};
	int distanceSteps[3] = {100, 300, 500};
	
	char* const referenceImages[48] = {
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p142_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/LiDAR_Base/LiDAR/p138_LiDAR",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p142_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p142_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p142_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p142_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p138_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p138_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p138_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/p138_HyMap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune2_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune2_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune2_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune2_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune8_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune8_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune8_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/HyMap_Base/HyMap/injune8_hymap_ratio",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene1_landsatFPC_subset",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene1_landsatFPC_subset",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene1_landsatFPC_subset",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene1_landsatFPC_subset",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene2_landsatFPC_subset",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene2_landsatFPC_subset",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene2_landsatFPC_subset",
		"/Users/pete/Desktop/Registration_Tests/BaseImages/Landsat_Base/Landsat/scene2_landsatFPC_subset",
	};
	
	char* const floatingImages[48] = {
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p142_CASI_LiDAR_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p142_CASI_LiDAR_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p142_CASI_LiDAR_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p142_CASI_LiDAR_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p138_CASI_LiDAR_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p138_CASI_LiDAR_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p138_CASI_LiDAR_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4Lidar/p138_CASI_LiDAR_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p142_HyMap_LiDAR_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p142_HyMap_LiDAR_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p142_HyMap_LiDAR_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p142_HyMap_LiDAR_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p138_HyMap_LiDAR_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p138_HyMap_LiDAR_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p138_HyMap_LiDAR_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/HyMap_4Lidar/p138_HyMap_LiDAR_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p142_AIRSAR_LiDAR_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p142_AIRSAR_LiDAR_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p142_AIRSAR_LiDAR_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p142_AIRSAR_LiDAR_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p138_AIRSAR_LiDAR_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p138_AIRSAR_LiDAR_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p138_AIRSAR_LiDAR_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4Lidar/p138_AIRSAR_LiDAR_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p142_CASI_HyMap_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p142_CASI_HyMap_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p142_CASI_HyMap_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p142_CASI_HyMap_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p138_CASI_HyMap_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p138_CASI_HyMap_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p138_CASI_HyMap_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/CASI_4HyMap/p138_CASI_HyMap_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune2_AIRSAR_HyMap_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune2_AIRSAR_HyMap_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune2_AIRSAR_HyMap_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune2_AIRSAR_HyMap_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune8_AIRSAR_HyMap_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune8_AIRSAR_HyMap_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune8_AIRSAR_HyMap_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/AIRSAR_4HyMap/Injune8_AIRSAR_HyMap_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene1_ALOS_Landsat_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene1_ALOS_Landsat_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene1_ALOS_Landsat_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene1_ALOS_Landsat_16X18Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene2_ALOS_Landsat_2X3Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene2_ALOS_Landsat_4X6Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene2_ALOS_Landsat_8X10Y_tif.tif",
		"/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ALOS_4Landsat/scene2_ALOS_Landsat_16X18Y_tif.tif"
	};
	
	char* const outputPaths[48] = {
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_16X18Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_2X3Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_4X6Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_8X10Y_cc_09",
		"/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_16X18Y_cc_09"
	};
	
	int refBands[48] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
	int floatBands[48] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,4,4,4,4,4,4,4,16,16,16,16,16,16,16,16,4,4,4,4,4,4,4,4,1,1,1,1,1,1,1,1};
	int xSteps[48] = {8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,50,50,50,50,50,50,50,50};
	int ySteps[48] = {8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,50,50,50,50,50,50,50,50};
	float imageMeasureThresholds[48] = {0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9};
	
	for(int i = 20; i < 24; i++)
	{
		ctrl->findControlPointsNetwork(referenceImages[i], // Ref Image
									   floatingImages[i], // Float Image
									   "/Users/pete/Desktop/Registration_Tests/cc/Image_Pyramid/", // Tmp output dir
									   outputPaths[i], // output control points
									   refBands[i], // ref band
									   floatBands[i], // float band
									   3, // distance measure (0 - MI | 1 - euclidean | 2 - Manhatten | 3 - Correlation)
									   0, // Search Algorthim (0 - Exhaustive | 1 - Hill Walking | 2 - Simulated Annealing)
									   20, // Search Restriction
									   100, // Joint histogram bins
									   10, // Number of Walks - Hill Walking
									   100, // tMax - Simulated Annealing
									   10, // tdecrease - Simulated Annealing
									   10, // number of successful - Simulated Annealing
									   20, // number of unsuccessful - Simulated Annealing
									   imageMeasureThresholds[i], //0.4 0.6 Image Measure Threshold - Correlation
									   3, // Number of Levels
									   xSteps[i], // X Pixel Steps
									   ySteps[i], // Y Pixel Steps
									   scaleLevels, // Array of scaling between levels
									   levelWindows, // Pixel sized windows around network nodes.
									   5, // Iterations at each level
									   500, // Distance threshold for network updates
									   networkUpdateWeights, // Alpha values to update network update weights.
									   distanceSteps, // Distance thresholds associated with weights
									   3, // Number of Steps for the updates
									   2, // Number of standard deviations from mean allowed before correction
									   0.2, // percentage of image range within a tile (Areas with no variation cannot be matched)
									   true, // image2image control points
									   false, // image2image Scaled control points
									   false, // image2map control points.
									   false, // image2map Scaled control points
									   true, // Print out successfull file opening
									   true, // Print image overlap
									   true); // Perform Registration
	}
	
	for(int i = 0; i < 8; i++)
	{
		ctrl->findControlPointsNetwork(referenceImages[i], // Ref Image
									   floatingImages[i], // Float Image
									   "/Users/pete/Desktop/Registration_Tests/cc/Image_Pyramid/", // Tmp output dir
									   outputPaths[i], // output control points
									   refBands[i], // ref band
									   floatBands[i], // float band
									   3, // distance measure (0 - MI | 1 - euclidean | 2 - Manhatten | 3 - Correlation)
									   0, // Search Algorthim (0 - Exhaustive | 1 - Hill Walking | 2 - Simulated Annealing)
									   20, // Search Restriction
									   100, // Joint histogram bins
									   10, // Number of Walks - Hill Walking
									   100, // tMax - Simulated Annealing
									   10, // tdecrease - Simulated Annealing
									   10, // number of successful - Simulated Annealing
									   20, // number of unsuccessful - Simulated Annealing
									   imageMeasureThresholds[i], //0.4 0.6 Image Measure Threshold - Correlation
									   3, // Number of Levels
									   xSteps[i], // X Pixel Steps
									   ySteps[i], // Y Pixel Steps
									   scaleLevels, // Array of scaling between levels
									   levelWindows, // Pixel sized windows around network nodes.
									   5, // Iterations at each level
									   500, // Distance threshold for network updates
									   networkUpdateWeights, // Alpha values to update network update weights.
									   distanceSteps, // Distance thresholds associated with weights
									   3, // Number of Steps for the updates
									   2, // Number of standard deviations from mean allowed before correction
									   0.2, // percentage of image range within a tile (Areas with no variation cannot be matched)
									   true, // image2image control points
									   false, // image2image Scaled control points
									   false, // image2map control points.
									   false, // image2map Scaled control points
									   true, // Print out successfull file opening
									   true, // Print image overlap
									   true); // Perform Registration
	}
	
	
	return 0;
}

