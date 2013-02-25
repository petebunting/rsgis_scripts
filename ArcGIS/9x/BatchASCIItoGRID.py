#####################################################
## NAME: BatchASCIItoGRID
## Source Name: BatchASCIItoGRID.py
## Version: ArcGIS 9.1
## Author: Joe Wheaton
## Usage: BatchASCIItoGRID <input_data>, <output_format>, {data_type}
## Required Arguments: A set of input ASCII files to be converted, The output
##   raster dataset to be created. When not saving to a geodatabase, specify
##   .tif for a TIFF file format, .img for an ERDAS IMAGINE file format, or no
##  extension for a GRID file format.

##                     
## Optional Arguments: Data Type (Integer or Float).

## Description:  
## Date: 19 April 2007
## Updated: 19 April 2007
#####################################################

import sys, os, win32com.client, string
#ConversionUtils win32api,, win32com.client
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

msgNonExist="Output location does not exist: "
msgSuccess="Successfully converted: "
msgFail="Failed to convert: "

gp.AddMessage("STARTED")

try:


# Argument 1 is the list of Rasters to be converted
    inRasters = gp.GetParameterAsText(0)
    gp.AddMessage("inRasters: " + inRasters)   
    # The list is split by semicolons ";"
    inRasters_list = string.split(inRasters,";")
    #gp.AddMessage("inRasters_list: " + inRasters_list)
    
    # The output workspace where the shapefiles are created
    outWorkspace = gp.GetParameterAsText(1)
    gp.AddMessage("outWorkspace: " + outWorkspace)  
    # Set the destination workspace parameter (which is the same value as the output workspace)
    # the purpose of this parameter is to allow connectivity in Model Builder.
    #gp.SetParameterAsText(2,outWorkspace)

    ext = gp.GetParameterAsText(2)
    gp.AddMessage("EXT: " + ext)  
    gp.AddMessage("Got Arguments")
    # Get proper extension based on the format string
    if (ext == "IMAGINE Image"):
        ext = ".img"
    elif (ext == "TIFF"):
        ext = ".tif"
    elif (ext == "GRID"):
        ext = ""

    gp.AddMessage("EXT: " + ext)    
    
    # Error trapping, in case the output workspace doesn't exist
    if not gp.Exists(outWorkspace):
        raise Exception, msgNonExist + "%s" % (outWorkspace)

    # Loop through the list of input Rasters and convert/copy each to the output geodatabase or folder
    for inRaster in inRasters_list:

        raster_base_with_ext = os.path.split(inRaster)[1]
        raster_base = string.split(raster_base_with_ext,".")[0]
        raster_base = "\\" + raster_base
        
        try:
            ##raster = ConversionUtils.ValidateInputRaster(raster)
            #outRaster = ConversionUtils.GenerateRasterName(raster, outWorkspace, ext)
            outRaster = outWorkspace + raster_base + ext
            # Copy/Convert the inRaster to the outRaster
            ##ConversionUtils.CopyRasters(raster, outRaster, "")
            gp.ASCIIToRaster_conversion(inRaster, outRaster, "FLOAT")
            # If the Copy/Convert was successfull add a message stating this
            gp.AddMessage(msgSuccess + "%s To %s" % (inRaster, outRaster))
            

        except Exception, ErrorDesc:
            # Except block for the loop. If the tool fails to convert one of the Rasters, it will come into this block
            #  and add warnings to the messages, then proceed to attempt to convert the next input Raster.
            WarningMessage = (msgFail + "%s" % (raster_base))

            if gp.GetMessages(2) != "":
                WarningMessage = WarningMessage + ". " + (gp.GetMessages(2))
            elif ErrorDesc != "":
                WarningMessage = WarningMessage + (str(ErrorDesc))

            # Add the message as a warning.
            gp.AddWarning(WarningMessage)

except Exception, ErrorDesc:
    # Except block if the tool could not run at all.
    #  For example, not all parameters are provided, or if the output path doesn't exist.
    gp.AddError(str(ErrorDesc))
    
