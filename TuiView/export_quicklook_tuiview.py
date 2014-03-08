#!/usr/bin/env python
#
# A script to export quicklooks for 
# all bands in an image or an RGB image
# using TuiView
#
# Dan Clewley (daniel.clewley@googlemail.com)
# 07/03/2014
#

import sys, os, argparse
from osgeo import gdal
from PyQt4.QtGui import QApplication
from tuiview import geolinkedviewers
from tuiview.viewerstretch import ViewerStretch

class ExportQuicklook(object):

    def __init__(self, inImage, outImage, width=500, height=None, inVector=None, keepwld=False):

        self.inimage = inImage
        self.outimage = outImage
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
            outHeight = outWidth * int(ySize / xSize)
        else:
            outHeight = args.height
        
        # Resize
        self.viewer.resizeForWidgetSize(outWidth, outHeight)


    def runAllBands(self):
        """ Create a separate image for all bands
        """

        outimageBase = os.path.splitext(self.outimage)[0]
        outimageExt = os.path.splitext(self.outimage)[1]
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
                    bandName = bandName.replace(' ','_')
        
                outImage = outimageBase + '_' + bandName + outimageExt
        
            stretch = ViewerStretch()
            stretch.setBands((band,))
            stretch.setGreyScale()
            stretch.setStdDevStretch()
            
            # Add the file
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
            self.viewer.saveCurrentViewInternal(outImage)
            # Remove world image
            if not self.keepwld:
                os.remove(outImage + 'w')
            
            # Remove layer
            self.viewer.removeLayer()
            # Remove vector layer (if added)
            if args.invector is not None:
                self.viewer.removeLayer()
    
    def runRGB(self):
        """ Export RGB image. Assumes image has already been stretched
            and RGB mapped to bands 1,2,3.
        """
            
        outImage = self.outimage

        stretch = ViewerStretch()
        stretch.setBands((1,2,3))
        stretch.setRGB()
        stretch.setNoStretch()
        
        # Add the file
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
    parser.add_argument("--height", type=int, default=None, help="Output height (default based on width to preserve ratio of origional image)", required=False)
    parser.add_argument("--keepwld", default=False, action='store_true', help="Keep spatial information file (default is to remove)", required=False)
    parser.add_argument("--allbands", action='store_true', default=False, help="Run for all bands")
    parser.add_argument("--rgb", action='store_true', default=False, help="Export RGB image (assumes already stretched)")
    args = parser.parse_args()    

    ql = ExportQuicklook(args.inimage, args.outimage, args.width, args.height, args.invector, args.keepwld)

    if args.allbands:
        ql.runAllBands()
    elif args.rgb:
        ql.runRGB()

    ql = None
    
