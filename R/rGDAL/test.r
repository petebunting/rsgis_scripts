source('rCalcImage.r')

inputFile <- 'test_in.kea'
outputFile <- 'test_out.kea'

# Test 1 - No output
testFunction <- function(inputDF, otherargs)
{
    # Take only data with ground truth pixels
    trainData <- subset(inputDF, inputDF$band12 > 0)

    # If first run setup data frame, else append
    if(otherargs$i == 0)
    {
        otherargs$outdataframe <- trainData
    }
    else
    {
        otherargs$outdataframe <- rbind(otherargs$outdataframe, trainData)
    }
    otherargs$i = otherargs$i + 1
    rm(trainData)
}

# Set up class to hold output parameters (need to be able to pass by reference)
setupArgs <- setRefClass('otherargs',fields=c('outdataframe','i'))

otherArgs <- setupArgs()

otherArgs$i = 0

# Run function over image
calcImageNoOut(inputFile, testFunction, otherArgs)


# Test 2 - Output
testFunction2 <- function(inputDF, otherargs)
{
    return(as.data.frame(inputDF$band1))
}

calcImage(inputFile, outputFile, testFunction2)

