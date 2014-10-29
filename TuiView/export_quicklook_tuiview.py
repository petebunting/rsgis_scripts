#!/usr/bin/env python
#
# A script to export quicklooks  
# using TuiView,
#
# Dan Clewley (daniel.clewley@googlemail.com)
# 07/03/2014
#
# Based on TuiView example:
# https://bitbucket.org/chchrsc/tuiview/wiki/Saving%20Images%20From%20Python
#

import sys, os, argparse
from osgeo import gdal
from PyQt4.QtGui import QApplication
from tuiview import geolinkedviewers
from tuiview.viewerstretch import ViewerStretch

class ExportQuicklook(object):

    def __init__(self, inImage, width=500, height=None, inVector=None, keepwld=False):

        self.inimage = inImage
        self.invector = inVector
        self.keepwld = keepwld

        # have to create one of these before any windows to init the Qt toolkit
        self.app = QApplication(sys.argv)
        
        # create a container for geolinked viewers
        self.viewers = geolinkedviewers.GeolinkedViewers()
        
        # start a viewer 
        self.viewer = self.viewers.newViewer()

        self.dataset = gdal.Open(args.inimage, gdal.GA_ReadOnly)
        
        xSize = self.dataset.RasterXSize
        ySize = self.dataset.RasterYSize
        
        outWidth = width
        if height is None:
            outHeight = int(outWidth * (ySize / xSize))
        else:
            outHeight = args.height

        print("OutputImage size {0} x {1}".format(outWidth, outHeight))
        
        # Resize
        self.viewer.resizeForWidgetSize(outWidth, outHeight)

    def name2Path(self, inString):
        """
        Convert band name to valid file path
        """
        valid_char = '-_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        outString = ''
        for char in inString:
            if valid_char.find(char) > -1:
                outString += char
            elif char == '':
                outString += '_'
        return outString

    def runAllBands(self, outImage):
        """ Create a separate image for all bands
        """

        outimageBase = os.path.splitext(outImage)[0]
        outimageExt = os.path.splitext(outImage)[1]
        # Loop through number of bands in image
        nBands = self.dataset.RasterCount
                
        for i in range(nBands):
            band = i + 1
            
            if nBands == 1:
                outImage = self.outimage
            else:
                bandName = self.dataset.GetRasterBand(band).GetDescription()
                if bandName == "":
                    bandName = 'b' + str(band)
                else:
                    bandName = self.name2Path(bandName)
        
                outImage = outimageBase + '_' + bandName + outimageExt
        
            self.runSingleImage(outImage, stretchType='Greyscale', bands=(band,), stretchData=True)
    
    def runSingleImage(self, outImage, stretchType = None, bands=None, stretchData=True):
        """ Export single image using default or 
            specified stretchType:
            * RGB
            * ColourTable
            * Greyscape
        """
            
        if stretchType == None: # Set to default stretch
            self.app.setApplicationName('viewer')
            self.app.setOrganizationName('Viewer')
            self.viewer.addRasterInternal(self.inimage)

        elif stretchType.lower() == 'rgb':
            if bands == None:
                bands = (1,2,3)
            stretch = ViewerStretch()
            stretch.setBands(bands)
            stretch.setRGB()
            if stretchData:
                stretch.setStdDevStretch()
            else:
                stretch.setNoStretch()
            self.viewer.addRasterInternal(self.inimage, stretch)
        elif stretchType.lower() == 'greyscale':
            if bands == None:
                bands = (1,)
            stretch = ViewerStretch()
            stretch.setBands(bands)
            stretch.setGreyScale()
            if stretchData:
                stretch.setStdDevStretch()
            else:
                stretch.setNoStretch()
            self.viewer.addRasterInternal(self.inimage, stretch)
        elif stretchType.lower() == 'colortable' or stretchType.lower() == 'colourtable': 
            if bands == None:
                bands = (1,)
            stretch = ViewerStretch()
            stretch.setBands(bands)
            stretch.setColorTable()
            self.viewer.addRasterInternal(self.inimage, stretch)
       
        # Zoom to extent
        self.viewer.zoomFullExtent()
        
        if self.invector is not None:
            # add the vector
            self.viewer.addVectorInternal(self.invector)
            # now retrieve the 'layer' that represents the vector
            vecLayer = self.viewer.viewwidget.layers.getTopVectorLayer()
            # set any properties
            vecLayer.setLineWidth(1)
            vecLayer.setColor([255, 255, 0, 255]) # red, green, blue, alpha
            # lastly, do this to update window
            vecLayer.getImage()
            self.viewer.viewwidget.update()
        
        # save as .png, .jpg etc
        # also saves .wld file
        print('Saving to:',outImage)
        self.viewer.saveCurrentViewInternal(outImage)
        # Remove world image
        if not self.keepwld:
            os.remove(outImage + 'w')
        
        # Remove layer
        self.viewer.removeLayer()
        # Remove vector layer (if added)
        if args.invector is not None:
            self.viewer.removeLayer()
         
        
    def __del__(self):
        self.viewers.closeAll()
        self.dataset = None

if __name__ == "__main__":

    # Get input parameters
    parser = argparse.ArgumentParser(description="Export quicklooks from an image using TuiView")
    parser.add_argument("-i", "--inimage", type=str, help="Input image",required=True)
    parser.add_argument("-v", "--invector", type=str, default=None, help="Input vector (optional)",required=False)
    parser.add_argument("-o", "--outimage", type=str, help="Output image (s)", required=True)
    parser.add_argument("--width", type=int, default=500, help="Output width (default 500 pixels)", required=False)
    parser.add_argument("--height", type=int, default=None, help="Output height (default based on width to preserve ratio of original image)", required=False)
    parser.add_argument("--keepwld", default=False, action='store_true', help="Keep spatial information file (default is to remove)", required=False)
    parser.add_argument("--allbands", action='store_true', default=False, help="Run for all bands")
    parser.add_argument("--rgb", action='store_true', default=False, help="Export RGB image")
    parser.add_argument("--greyscale", action='store_true', default=False, help="Export Greyscale image")
    parser.add_argument("--colortable", action='store_true', default=False, help="Export colour table")
    parser.add_argument("--nostretch", action='store_true', default=False, help="Don't stretch data (use if data has already been stretched)")
    args = parser.parse_args()    

    ql = ExportQuicklook(args.inimage, args.width, args.height, args.invector, args.keepwld)

    stretchData = True
    if args.nostretch:
        stretchData = False

    if args.allbands:
        ql.runAllBands(args.outimage)
    else:
        stretchType = None
        if args.rgb:
            stretchType = 'RGB'
        elif args.greyscale:
            stretchType = 'Greyscale'
        elif args.colortable:
            stretchType = 'Colortable'
        ql.runSingleImage(args.outimage, stretchType, None, stretchData)

    ql = None
    
