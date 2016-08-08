#!/usr/bin/env python
"""
Extracts images from Sentinel 2 data using GDAL.

Requires GDAL > 2.1

Saves a single file for each resolution and UTM zone.

Author: Dan Clewley

Creation Date: 08/08/2015

"""
from __future__ import print_function
import argparse
import os
import sys
import glob
import subprocess
from distutils.version import LooseVersion
from osgeo import gdal
from osgeo import osr

# Try to import NERC-ARF 'get_gdal_drivers' library
# Available from https://github.com/pmlrsg/arsf_dem_scripts/blob/master/arsf_dem/get_gdal_drivers.py
HAVE_GET_GDAL_DRIVERS = False
try:
    import get_gdal_drivers
    HAVE_GET_GDAL_DRIVERS = True
except ImportError:
    pass

# Check GDAL version is above 2.1 (required for Sentienl 2 driver)
if gdal.__version__ < LooseVersion("2.1.0"):
    print("This script requires GDAL 2.1 or later", file=sys.stderr)
    sys.exit(1)

def get_subdataset_names(infile):
    """
    Get subdataset names from a Sentinel 2 file
    """
    # Check if a directory has been passed in (rather than xml)
    if os.path.isdir(infile):
        try:
            infile = glob.glob(os.path.join(infile, "S2*xml"))[0]
        except IndexError:
            raise IOError("Could not find required XML file for S2 data")

    out_names = []

    dataset = gdal.Open(infile, gdal.GA_ReadOnly)
    subdatasets = dataset.GetSubDatasets()

    # Last two subdatasets are preview images so ignore these.
    for sub_data in subdatasets[:-2]:
        out_names.append(sub_data[0])

    return out_names

def convert_epsg_utm(epsg_code):
    """
    Convert EPSG code into a string with UTM zone
    """
    spatial_ref = osr.SpatialReference()
    osr_out = spatial_ref.ImportFromEPSG(int(epsg_code))

    if osr_out != 0:
        raise Exception("Could not create projection. "
                        "Is {} a valid EPSG code".format(epsg_code))

    utm_zone = spatial_ref.GetUTMZone()

    if utm_zone != 0:
        # If positive North
        if utm_zone > 0:
            utm_zone_str = str(utm_zone).zfill(2)
            out_proj_str = "UTM%sN" % (utm_zone_str)
        # If negative South
        else:
            utm_zone = utm_zone * -1
            utm_zone_str = str(utm_zone).zfill(2)
            out_proj_str = "UTM%sS" % (utm_zone_str)
    else:
        raise Exception("EPSG code does not corespond to a UTM zone")

    return out_proj_str

def get_out_name(subdataset_name, out_ext=""):
    """
    Get output file name for sub dataset
    """
    outname = os.path.split(subdataset_name)[-1]

    outname = outname.replace(".xml","")
    outname = outname.replace(":","_")

    # Try to convert EPSG code into easier to read UTM zone
    epsg_code = outname.split("_")[-1]
    try:
        utm_str = convert_epsg_utm(epsg_code)
        outname = "_".join(outname.split("_")[:-2])
        outname = "{}_{}".format(outname, utm_str)
    # If this fails go with EPSG code
    except Exception as err:
        print(err, file=sys.stderr)
        pass

    outname = outname + out_ext

    return outname

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimise rasters for display "
                                                 "by calculating statistics and adding "
                                                 "overviews.")
    parser.add_argument("infiles",nargs="+",
                        help="Input file(s)")
    parser.add_argument("-o", "--outdir",
                        help="Output directory",
                        required=True)
    parser.add_argument("--of", default="KEA",
                        required=False,
                        help="Output format (GDAL name)")
    args = parser.parse_args()

    # Get extension and creation options
    if HAVE_GET_GDAL_DRIVERS:
        out_ext = get_gdal_drivers.GDALDrivers().get_ext_from_driver(args.of)
        out_creation_options = get_gdal_drivers.GDALDrivers().get_creation_options_from_ext(out_ext)
    # If get_gdal_drives is not available a couple of options are hardcoded
    else:
        if args.of == "KEA":
            out_ext = ".kea"
            out_creation_options = []
        elif args.of == "GTiff":
            out_ext = ".tif"
            out_creation_options = ["COMPRESS=LZW"]
        else:
            print("Could not import 'get_gdal_drivers' to determine correct "
                    "extension for {} format. Try using 'GTiff' or 'KEA' "
                    "instead".format(args.of))

    for dataset in args.infiles:
        print("\n** {} **\n".format(os.path.basename(dataset)))

        subdataset_names = get_subdataset_names(dataset)

        for num, subdataset in enumerate(subdataset_names):
            out_name = get_out_name(subdataset, out_ext)
            out_file = os.path.join(args.outdir, out_name)
            print(" [{0}/{1}] {2}".format(num+1, len(subdataset_names),
                                          out_name))

            gdal_translate_cmd = ["gdal_translate",
                                  "-of", args.of]
            # If there are creation options add these
            for creation_option in out_creation_options:
                gdal_translate_cmd.extend(["-co", creation_option])

            # NetCDF doesn't support uint16 so use int
            if args.of == "netCDF":
                gdal_translate_cmd.extend(["-ot", "Int16"])

            gdal_translate_cmd.extend([subdataset, out_file])
            print(" ".join(gdal_translate_cmd))
            subprocess.check_call(gdal_translate_cmd)

