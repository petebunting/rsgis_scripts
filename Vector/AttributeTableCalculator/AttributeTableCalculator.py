#!/usr/bin/env python
###############################################################################
# $Id: get_soundg.py 18195 2009-12-06 20:24:39Z rouault $
#
# Project:  OGR Python samples
# Purpose:  Extract SOUNDGings from an S-57 dataset, and write them to
#           Shapefile format, creating one feature for each sounding, and
#           adding the elevation as an attribute for easier use. 
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2003, Frank Warmerdam <warmerdam@pobox.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################
# Adapted by Dan Clewley (daniel.clewley@gmail.com) to perform Attribute Table
# Calculations.
# 10/06/2012
###############################################################################

try:
    from osgeo import osr
    from osgeo import ogr
except ImportError:
    import osr
    import ogr

import string, sys, os

class AttributeTableCalculator(object):

    def getLayerNameFromPath(self, inFile):
        ''' Takes full file path and returns name, withough path or extension'''
        baseFileName = os.path.basename(inFile)
        layerName = os.path.splitext(baseFileName)
        return layerName[0]
    
    def calculateField(self, inFieldValues):
        # Field calculation to be used.
        field1 = inFieldValues[0]
        field1 = field1.replace('-','')
        pcount = field1.count('.')
        outFieldInt = 0
        if pcount == 2:
            elements = field1.split('.', pcount)
            outField = elements[0] + elements[1] + elements[2]
            outFieldInt = int(outField)
        return outFieldInt
    
    def processFeature(self, inSHPFile, outSHPFile, outFieldName, inFieldNames):
        # Open input shapefile
        inSHP = ogr.Open(inSHPFile)
        inSHPLayerName = self.getLayerNameFromPath(inSHPFile)
        inSHPLayer = inSHP.GetLayerByName(inSHPLayerName)
        outSRS = inSHPLayer.GetSpatialRef()
        
        # Create the output shapefile. 
        shp_driver = ogr.GetDriverByName('ESRI Shapefile')
        shp_driver.DeleteDataSource(outSHPFile)
        outSHP = shp_driver.CreateDataSource(outSHPFile)
        outSHPLayerName = self.getLayerNameFromPath(outSHPFile)
        outSHPLayer = outSHP.CreateLayer(outSHPLayerName, outSRS, ogr.wkbPolygon)
        
        # Create copy of origional shapefile and add field for output.
        
        inSHPLayerDef = inSHPLayer.GetLayerDefn()
        inFieldCount = inSHPLayerDef.GetFieldCount()
        
        out_mapping = []
        for fld_index in range(inFieldCount):
            inField = inSHPLayerDef.GetFieldDefn(fld_index)
            
            fd = ogr.FieldDefn(inField.GetName(), inField.GetType())
            fd.SetWidth(inField.GetWidth())
            fd.SetPrecision(inField.GetPrecision())
            if outSHPLayer.CreateField(fd) != 0:
                out_mapping.append(-1)
            else:
                out_mapping.append(outSHPLayer.GetLayerDefn().GetFieldCount() - 1)
        
        fd = ogr.FieldDefn(outFieldName, ogr.OFTReal) # Set name and type for output field
        fd.SetWidth(12)
        fd.SetPrecision(4)
        outSHPLayer.CreateField(fd)
            
        # Loop though features
        
        feature = inSHPLayer.GetNextFeature()
        while feature is not None:
        
            # Copy input features
            multi_geom = feature.GetGeometryRef()
            
            outFeature = ogr.Feature(feature_def=outSHPLayer.GetLayerDefn())
            for fld_index in range(inFieldCount):
                outFeature.SetField(out_mapping[fld_index], feature.GetField(fld_index))
        
            # Perform field calculation
            inFieldValues = []
            for name in inFieldNames:
                inFieldValues.append(feature.GetField(feature.GetFieldIndex(name)))
            
            outFieldValue = self.calculateField(inFieldValues)
            
            outFeature.SetField(outFieldName, outFieldValue)
            
            outFeature.SetGeometry(multi_geom)
            outSHPLayer.CreateFeature(outFeature)
            
            outFeature.Destroy()
            feature.Destroy()
        
            feature = inSHPLayer.GetNextFeature()
        
        outSHP.Destroy()
        inSHP.Destroy()

    def help(self):
        print 'python AttributeTableCalculator.py inSHP outSHP outFieldName inFieldName[s]'
        
        
if __name__ == '__main__':
    atc = AttributeTableCalculator()
    if len(sys.argv) < 5:
        atc.help()
    else:
        inFieldNames = []
        inSHPFile = sys.argv[1].strip()
        outSHPFile = sys.argv[2].strip()
        outFieldName = sys.argv[3].strip()
        i = 4
        while i < len(sys.argv):
            inFieldNames.append(str(sys.argv[i]).strip())
            i+=1
        atc.processFeature(inSHPFile, outSHPFile, outFieldName, inFieldNames)
    

    
