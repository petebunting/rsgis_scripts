import numpy as np
import argparse

def getPixelSize(lat, latsize, lonsize):
    """ Get the pixel size (in m) based on latitude and
        pixel size in degrees
    """

    # Set up parameters for elipse
    # Semi-major and semi-minor for WGS-84 ellipse
    ellipse = [6378137.0, 6356752.314245]
    
    radlat = np.deg2rad(lat)
    
    Rsq = (ellipse[0]*np.cos(radlat))**2+(ellipse[1]*np.sin(radlat))**2
    Mlat = (ellipse[0]*ellipse[1])**2/(Rsq**1.5)
    Nlon = ellipse[0]**2/np.sqrt(Rsq)
    xsize = np.pi/180*np.cos(radlat)*Nlon*lonsize
    ysize = np.pi/180*Mlat*latsize

    return xsize, ysize

# Set up options
parser = argparse.ArgumentParser()
parser.add_argument("lat", nargs=1,type=str, help="Latitude")
parser.add_argument("latsize", nargs=1,type=str, help="Pixel sixe (y)")
parser.add_argument("lonsize", nargs=1,type=str, help="Pixel size (x)")
args = parser.parse_args() 

xsize, ysize = getPixelSize(float(args.lat[0]),float(args.latsize[0]),float(args.lonsize[0]))

print('xsize = {} m, ysize = {} m'.format(xsize,ysize))



