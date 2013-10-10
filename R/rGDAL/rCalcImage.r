# rCalcImage.r
# Provides similar functionality to RSGISLib CalcImage class / RIOS applier 
# in R.
# Executes function, operating on R data frames for all pixels in image.
#
# Dan Clewley (clewley@usc.edu)
# 26/09/2013
#
# This script is made available under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The functions are based on RSGISCalcImage.cpp from RSGISLib
# created by Pete Bunting and Copyright 2013 RSGISLib.
#

library(rgdal)

calcImageNoOut <- function(inputFile, calcImageDFFunction, otherArgs=NULL)
{
    # A function to itterativly loop through a GDAL dataset. Reads in width*blockSize at a time
    # A user supplied function, operating on a dataframe is run for chunks of data

    # Open file
    inputDS <- new("GDALReadOnlyDataset",inputFile)
    
    # Get dimensions
    inDimensions <- dim(inputDS)
    height <- inDimensions[1]
    width <- inDimensions[2]
    numInBands <- seq(1,inDimensions[3]) # Setting up as a sequence so for loops are similar to those in RSGISLib
    
    # Get block size
    band1 = getRasterBand(inputDS,band=1)
    blockSize <- getRasterBlockSize(band1)
    
    yBlockSize <- blockSize[1]
    xBlockSize <- blockSize[2]
    
    nYBlocks <- floor(height / yBlockSize)
    remainRows <- height - (nYBlocks * yBlockSize)
    rowOffset <- 0
    
    # Set up names for data frame
    inDFNames <- c()
    for(n in numInBands)
    {
        bName <- paste("band",n,sep="")
        inDFNames <- c(inDFNames, bName)
    }
    
    cat("Started")
    # Loop images to process data
    i <- 0
    while (i < nYBlocks) 
    {
        # Read in data to data frame
        for(n in numInBands)
    	{
            rowOffset = (yBlockSize * i)
    
            inputRasterBandData <- getRasterData(inputDS, n, offset=c(rowOffset, 0),region.dim=c(yBlockSize,width))
    
            if(n == 1)
            {
                inDF <- as.data.frame(c(inputRasterBandData))
            }
            else
            {
                inDF <- cbind(inDF,c(inputRasterBandData))
            }
    
    	}
    
        # Set names
        names(inDF) <- inDFNames
    
        # Run function
        calcImageDFFunction(inDF, otherArgs)
                        
        percentComplete <- floor(100*rowOffset / height)

        cat("\r",percentComplete," %       ")
                        
        i <- i+1
    }
                
    if(remainRows > 0)
    {
        for(n in numInBands)
    	{
            rowOffset <- yBlockSize * nYBlocks
    
            inputRasterBandData <- getRasterData(inputDS, n, offset=c(rowOffset, 0),region.dim=c(remainRows,width))
    
            if(n == 1)
            {
                inDF <- as.data.frame(c(inputRasterBandData))
            }
            else
            {
                inDF <- cbind(inDF,c(inputRasterBandData))
            }
    	}

        # Set names
        names(inDF) <- inDFNames
    
        # Run function
        calcImageDFFunction(inDF, otherArgs)
    }
    
    cat("\rComplete\n")
    # Close dataset
    closeDataset(inputDS)
    # Tidy up
    rm(inDF)
    rm(inputRasterBandData)
}

calcImage <- function(inputFile, outputFile, calcImageDFFunction, otherArgs=NULL, nOutBands=1, outFormat="KEA", outDataType="Float32")
{
    # A function to itterativly loop through a GDAL dataset. Reads in width*blockSize at a time
    # A user supplied function, operating on a dataframe is run for chunks of data

    # Open file
    inputDS <- new("GDALReadOnlyDataset",inputFile)
    
    # Get dimensions
    inDimensions <- dim(inputDS)
    height <- inDimensions[1]
    width <- inDimensions[2]

    if(is.na(inDimensions[3]))
    {
        numInBands <- c(1)
    }
    else
    {
        numInBands <- seq(1,inDimensions[3])
    }
    numOutBands <- seq(1,nOutBands)
    
    # Get block size
    band1 = getRasterBand(inputDS,band=1)
    blockSize <- getRasterBlockSize(band1)
    
    yBlockSize <- blockSize[1]
    xBlockSize <- blockSize[2]
    
    nYBlocks <- floor(height / yBlockSize)
    remainRows <- height - (nYBlocks * yBlockSize)
    rowOffset <- 0
    
    # Set up names for data frame
    inDFNames <- c()
    for(n in numInBands)
    {
        bName <- paste("band",n,sep="")
        inDFNames <- c(inDFNames, bName)
    }

    # Create output dataset
    
    outputDS <- new("GDALTransientDataset", fname=outputFile, driver=new("GDALDriver",outFormat), bands=nOutBands, rows=height, cols=width, type=outDataType)

    cat("Started")
    # Loop images to process data
    i <- 0
    while (i < nYBlocks) 
    {
        # Read in data to data frame
        for(n in numInBands)
    	{
            rowOffset = (yBlockSize * i)
    
            inputRasterBandData <- getRasterData(inputDS, n, offset=c(rowOffset, 0),region.dim=c(yBlockSize,width))
    
            if(n == 1)
            {
                inDF <- as.data.frame(c(inputRasterBandData))
            }
            else
            {
                inDF <- cbind(inDF,c(inputRasterBandData))
            }
    
    	}
    
        # Set names
        names(inDF) <- inDFNames
    
        # Run function
        outDF <- calcImageDFFunction(inDF, otherArgs)

        # Save out data
        for(n in numOutBands)
    	{
            # Reshape
            outputRasterBandData <- array(as.matrix(outDF[1]),dim=c(width,yBlockSize))

            putRasterData(outputDS, outputRasterBandData, offset=c(rowOffset, 0))

    	}
         
        percentComplete <- floor(100*rowOffset / height)

        cat("\r",percentComplete," %       ")
                        
        i <- i+1
    }
                
    if(remainRows > 0)
    {
        for(n in numInBands)
    	{
            rowOffset <- yBlockSize * nYBlocks
    
            inputRasterBandData <- getRasterData(inputDS, n, offset=c(rowOffset, 0),region.dim=c(remainRows,width))
    
            if(n == 1)
            {
                inDF <- as.data.frame(c(inputRasterBandData))
            }
            else
            {
                inDF <- cbind(inDF,c(inputRasterBandData))
            }
    	}

        # Set names
        names(inDF) <- inDFNames
    
        # Run function
        outDF <- calcImageDFFunction(inDF, otherArgs)

        # Save out data
        for(n in numOutBands)
    	{
            # Reshape
            outputRasterBandData <- array(as.matrix(outDF[1]),dim=c(width,remainRows))

            putRasterData(outputDS, outputRasterBandData, offset=c(rowOffset, 0))
    	}

    }
    
    cat("\rComplete\n")
    # Close dataset
    GDAL.close(inputDS)
    saveDataset(outputDS,outputFile)
    GDAL.close(outputDS)
    # Tidy up
    rm(inDF)
    rm(outDF)
    rm(inputRasterBandData)
    rm(outputRasterBandData)
}

