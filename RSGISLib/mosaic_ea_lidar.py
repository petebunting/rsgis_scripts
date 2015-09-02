#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mosaic files within a zip archive using RSGISLib

Author: Dan Clewley
Creation Date: 02/09/2015

Designed to mosaic Environemnt Agency LiDAR-derived DTM and DSM files
downloaded in ASCII format from http://environment.data.gov.uk/ds/survey

zip_to_gdal_path function adapted from TuiView (http://tuiview.org/)
Function author Terry Cain

Made available under GPLv3 License

"""

import argparse
import rsgislib
from rsgislib import imageutils
import zipfile

SOURCE_NODATA = -9999.0
OUT_NODATA = 0 

OSGB_WKT_STRING = '''PROJCS["OSGB 1936 / British National Grid",
    GEOGCS["OSGB 1936",
        DATUM["OSGB_1936",
            SPHEROID["Airy 1830",6377563.396,299.3249646,
                AUTHORITY["EPSG","7001"]],
            AUTHORITY["EPSG","6277"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4277"]],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    PROJECTION["Transverse_Mercator"],
    PARAMETER["latitude_of_origin",49],
    PARAMETER["central_meridian",-2],
    PARAMETER["scale_factor",0.9996012717],
    PARAMETER["false_easting",400000],
    PARAMETER["false_northing",-100000],
    AUTHORITY["EPSG","27700"],
    AXIS["Easting",EAST],
    AXIS["Northing",NORTH]]
'''

def zip_to_gdal_path(filepath):
    """
    Takes in a zip filepath and if the zip contains files
    ascii files, prepend '/viszip' to the path 
    so that they can be opened using GDAL without extraction.
    
    """
    zip_file_list = []
    
    if zipfile.is_zipfile(filepath):
        try:
            zip_file = zipfile.ZipFile(filepath)
            zip_file_contents = ['/vsizip/{0}/{1}'.format(filepath, zip_info_object.filename) for zip_info_object in zip_file.filelist if           zip_info_object.filename.endswith('.asc')]
            zip_file_list.extend(zip_file_contents)
            zip_file.close()
        except zipfile.BadZipfile:
            pass

    return zip_file_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfiles', nargs='*',type=str, help='Input zip file(s)')
    parser.add_argument('-o','--outmosaic',type=str, required=True, help='Output mosaic')
    parser.add_argument("--nostats", action='store_true',default=False, help="Don't calculate statistics and pyramids for mosaic (default is to calculate)")
    args=parser.parse_args()

    file_list = [] 
    
    for zip_file in args.inputfiles:
        file_list.extend(zip_to_gdal_path(zip_file))

    if len(file_list) == 0:
        print('No ".asc" found within zip file(s) provided as input', file=sys.stderr)

    print('\nCreating mosaic...')
    imageutils.createImageMosaic(file_list,args.outmosaic, 
                                OUT_NODATA, SOURCE_NODATA,
                                1,0,
                                rsgislib.RSGISPyUtils().getGDALFormatFromExt(args.outmosaic),
                                rsgislib.TYPE_32FLOAT) 

    # Assign Projection
    print('\nAssigning projection')
    imageutils.assignProj(args.outmosaic, wktString=OSGB_WKT_STRING)

    if not args.nostats:
        # Create pyramids
        print('\nCalculating stats and pyramids...')
        imageutils.popImageStats(args.outmosaic,True,0.,True)
        print('Finished')
