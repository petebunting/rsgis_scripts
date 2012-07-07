#include <iostream>
#include "gdal_priv.h"
#include "ImageUtils.h"

class Control
{
public:
	void runRasterize(const char *inputImageFile,
			  const char *inputCSV,
			  const char *outputImageFile,
			  int numAttribute,
			  int ignoreLines);
};

void Control::runRasterize(const char *inputImageFile, 
			   const char *inputCSV, 
			   const char *outputImageFile, 
			   int numAttributes, 
			   int ignoreLines)
{
	GDALAllRegister();
	GDALDataset *inputImage = (GDALDataset *) GDALOpen(inputImageFile, GA_ReadOnly);
	// Check read in correctly.
	if(inputImage == NULL)
	{
		std::cout << "Bugger could not open Image " << std::endl;
	}
	else
	{
		std::cout << "Data from has been read in OK!\n";
	}
	
	ImageUtils *utils = new ImageUtils();
	utils->rasterizeDefiniens(inputImage, outputImageFile, inputCSV, numAttributes, ignoreLines);
	delete utils;
	GDALClose(inputImage);
}

int main(int argc, char **argv)
{
	std::cout << "Number Arguments: " << argc-1 << std::endl;
	if(argc != 6)
	{
	    std::cout << "Requires 5 inputs\n";
	    std::cout << "./rasterize <input_image> <input_CSV> <output_image> <num attributes> <ignore_lines>\n";
	    std::exit(1);
	}
	const char *inputImageFile = "";
	const char *inputCSV = "";
	const char *outputImageFile = "";
	int numAttributes = 0;
	int ignoreLines = 0;
	
	for(int i = 0; i < argc; i++)
	{
	    std::cout << i << ": " << argv[i] << std::endl;
	    if(i == 1)
	    {
	   	inputImageFile = argv[i];
	    }
	    else if(i == 2)
	    {
		inputCSV = argv[i];
	    }
	    else if(i == 3)
	    {
		outputImageFile = argv[i];
	    }
	    else if(i == 4)
	    {
		numAttributes = atoi(argv[i]);
	    }
	    else if(i == 5)
	    {
		ignoreLines = atoi(argv[i]);
	    }
	}


	Control *ctrl = new Control();
	ctrl->runRasterize(inputImageFile, inputCSV, outputImageFile, numAttributes, ignoreLines);
	delete ctrl;
	return (0);
}
