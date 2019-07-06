import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
# IF basemap is not available run 'conda install -c conda-forge basemap'
from mpl_toolkits.basemap import Basemap
import numpy as np
import h5py

def run(FILE_NAME):

    # READ INPUT VARIABLES INTO MEMORY.
    with h5py.File(FILE_NAME, mode='r') as f:
        
        time = f['/Data_40HZ/Time/d_UTCTime_40'][:]
        
        latvar = f['/Data_40HZ/Geolocation/d_lat']
        latitude = latvar[:]
        lat_vr = [latvar.attrs['valid_min'], latvar.attrs['valid_max']]
        # apply valid max, min
        latitude[latitude < lat_vr[0]] = np.nan
        latitude[latitude > lat_vr[1]] = np.nan

        lonvar = f['/Data_40HZ/Geolocation/d_lon']
        longitude = lonvar[:]
        lon_vr = [lonvar.attrs['valid_min'], lonvar.attrs['valid_max']]
        # apply valid max, min
        longitude[longitude < lon_vr[0]] = np.nan
        longitude[longitude > lon_vr[1]] = np.nan
        
        """
        tempvar = f['/Data_1HZ/Atmosphere/d_Surface_temp']
        temp = tempvar[:]
        temp_vr = [tempvar.attrs['valid_min'], tempvar.attrs['valid_max']]
        units = tempvar.attrs['units']
        long_name = tempvar.attrs['long_name']
        # apply valid max, min
        temp[temp < temp_vr[0]] = np.nan
        temp[temp > temp_vr[1]] = np.nan
        """
        
        surfElevVar = f['/Data_40HZ/Elevation_Surfaces/d_elev']
        surfElev = surfElevVar[:]
        surfElev_vr = [surfElevVar.attrs['valid_min'], surfElevVar.attrs['valid_max']]
        units = surfElevVar.attrs['units']
        long_name = surfElevVar.attrs['long_name']
        # apply valid max, min
        surfElev[surfElev < surfElev_vr[0]] = np.nan
        surfElev[surfElev > surfElev_vr[1]] = np.nan
    
    # Create empty mskArr of same size as inputs
    mskArr = np.zeros_like(time, dtype=np.uint8)
    
    # Populate the mskArr with 1 if within Geographic bounds.
    roiMinLat = -45
    roiMaxLat = -9
    roiMinLon = 110
    roiMaxLon = 155
    mskArr = np.where((latitude > roiMinLat) & (latitude < roiMaxLat) & (longitude > roiMinLon) & (longitude < roiMaxLon) , 1, mskArr)
    ################################
    # UNCOMMENT TO GET WHOLE WORLD
    #mskArr[...] = 1
    ################################
    
    
    if np.sum(mskArr) == 0:
        print("No data in ROI")
        sys.exit()
    
    # Apply ROI mask to input data
    latitude = latitude[mskArr == 1]
    longitude = longitude[mskArr == 1]
    surfElev = surfElev[mskArr == 1]
    time = time[mskArr == 1]
    
    ########### CREATE CODE TO WRITE OUT TO CSV OR SOME OTHER FILE FORMAT ###########
    
    # TODO: MERGES INPUT ARRAYS INTO STRUCTURE... e.g., PANDAS DATATABLE...
       
    # TODO:
    
    #######################################
    
    
    ########### CREATES PLOT BUT YOU DON'T NEED THIS ########
    fig = plt.figure(figsize=(15, 6))
    ax1 =  plt.subplot(1, 2, 1)
    elapsed_time = (time - time[0])/60
    ax1.plot(elapsed_time, surfElev, 'b-')
    ax1.set_xlabel('Elapsed Time (minutes)')
    ax1.set_ylabel(units)

    # Plot surface temperature vs time.
    # plt.plot(time, temp)

    # Plot the trajectory
    plt.subplot(1, 2, 2)

    # Draw an equidistant cylindrical projection using the low resolution
    # coastline database.
    m = Basemap(projection='cyl', resolution='l', llcrnrlat=-90, urcrnrlat = 90, llcrnrlon=-180, urcrnrlon = 180)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90., 120., 30.))
    m.drawmeridians(np.arange(-180, 180., 45.))
    #m.pcolormesh(longitude, latitude, temp, latlon=True, vmin=0, vmax=1)
    m.scatter(longitude, latitude, c=surfElev, s=1, cmap=plt.cm.jet, edgecolors=None, linewidth=0)
    cb = m.colorbar()
    cb.set_label(units)

    basename = os.path.basename(FILE_NAME)
    plt.title('{0}\n{1}'.format(basename, long_name))
    fig = plt.gcf()
    # plt.show()
    pngfile = "{0}.py.png".format(basename)
    fig.savefig(pngfile)
    #######################################
    

if __name__ == "__main__":

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    hdffile = 'GLAH14_634_2131_002_0071_0_01_0001.H5'
    run(hdffile)
    


