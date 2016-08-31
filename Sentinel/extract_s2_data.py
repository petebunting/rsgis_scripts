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

VALID_RESOLUTIONS = [10, 20, 60]

# QI dataset names
QI_ALL_BANDS = ["CLOUDS"]
QI_INDIVIDUAL_BANDS = ["DEFECT", "DETFOO", "NODATA", "SATURA", "TECQUA"]

def get_subdataset_names(infile, resolution=None):
    """
    Get subdataset names from a Sentinel 2 file

    Excludes preview images (last two subdatasets)

    If 'resolution' is passed in will only return subdatasets matching this

    Returns tuple from GDAL with:
        (Name, Description)

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
        if resolution is not None:
            if resolution not in VALID_RESOLUTIONS:
                raise Exception("Resolution {} is not valid. Available options "
                                "are 10, 20 and 60".format(resolution))
            # Get resolution
            subdata_res = sub_data[0].split(":")[2].rstrip("m")
            if int(subdata_res) == int(resolution):
                out_names.append(sub_data)
        else:
            out_names.append(sub_data)

    return out_names

def get_out_name(subdataset_name_tuple, out_ext=""):
    """
    Get output file name for sub dataset

    Takes tuple with (subdataset name, description)
    """
    subdataset_name = subdataset_name_tuple[0]
    outname = os.path.split(subdataset_name)[-1]

    outname = outname.replace(".xml","")
    outname = outname.replace(":","_")

    # Get UTM string from description.
    utm_str = subdataset_name_tuple[1].split(",")[-1].replace(" ","")
    outname = "_".join(outname.split("_")[:-2])
    outname = "{}_{}".format(outname, utm_str)

    outname = outname + out_ext

    return outname

def check_num_vector_layers(input_vector):
    """
    Gets the number of layers within a vector
    """

    ds = gdal.OpenEx(input_vector, gdal.OF_VECTOR)
    num_layers = ds.GetLayerCount()
    ds = None

    return num_layers


def merge_gml_to_sqlite(input_vector_files, output_vector, layer_name=None):
    """
    Merge multiple GML files to a single SQLite vector file.

    Will remove output file if it already exists.
    """
    output_format = "SQLite"
    if layer_name is None:
        output_layer_name = os.path.splitext(os.path.basename(output_vector))[0]
    else:
        output_layer_name = layer_name
    first_file = True
    if os.path.isfile(output_vector):
        os.remove(output_vector)

    for i, input_vector in enumerate(input_vector_files):

        if first_file:
            # For first file need to create new output (will fail if already exists)
            first_file = False
            convert_cmd = ["ogr2ogr",
                           "-f", output_format,
                           "-nln", output_layer_name,
                           output_vector, input_vector]
            subprocess.check_call(convert_cmd)
        else:
            convert_cmd = ["ogr2ogr",
                           "-update", "-append",
                           "-nln", output_layer_name,
                           output_vector, input_vector]
            subprocess.check_call(convert_cmd)


def merge_qi_vectors(input_dir, output_dir):
    """
    Merge all QI vectors from GML format for individual granules to a single
    SQLite file
    """

    if os.path.splitext(input_dir)[0] == '.zip':
        raise IOError("Need to unzip directory to extract QI data")

    input_basename = os.path.basename(input_dir)
    input_basename = input_basename.replace(".SAFE","")

    for flag in QI_ALL_BANDS:
        gml_files_list = glob.glob(os.path.join(input_dir, "GRANULE", "*", "QI_DATA",
                                                "*MSK_{}*_B00*.gml".format(flag)))
        output_file = os.path.join(output_dir,
                                   "{}_{}_B00.sqlite".format(input_basename, flag))
        if len(gml_files_list) == 0:
            print("Could not find any files for '{}' flag".format(flag),
                  file=sys.stderr)
        else:
            merge_gml_to_sqlite(gml_files_list, output_file, flag)
            if check_num_vector_layers(output_file) == 0:
                os.remove(output_file)
            else:
                print(" " + os.path.basename(output_file))

    # Set up list of bands
    bands_list = [str(i).zfill(2) for i in range(1,13)]
    bands_list.append('8A')

    for flag in QI_INDIVIDUAL_BANDS:
        for band in bands_list:
            gml_files_list = glob.glob(os.path.join(input_dir, "GRANULE",
                                                     "*", "QI_DATA",
                                                     "*MSK_{}*_B{}*.gml".format(flag, band)))
            output_file = os.path.join(output_dir,
                                "{}_{}_B{}.sqlite".format(input_basename, flag, band))
            if len(gml_files_list) == 0:
                print("Could not find any files for '{}' flag"
                      "(band {})".format(flag, band),
                      file=sys.stderr)
            else:
                merge_gml_to_sqlite(gml_files_list, output_file, flag)
                if check_num_vector_layers(output_file) == 0:
                    os.remove(output_file)
                else:
                    print(" " + os.path.basename(output_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Sentinel-2 data to"
                                                 " indivitual files using GDAL")
    parser.add_argument("infiles",nargs="+",
                              help="Input file(s)")
    parser.add_argument("-o", "--outdir",
                              help="Output directory",
                              required=True)
    parser.add_argument("--of", default="ENVI",
                              required=False,
                              help="Output format (GDAL name)")
    parser.add_argument("--resolution", default=None,
                              required=False,
                              type=int,
                              help="Resolution to extract. Options are 10, 20 and 60")
    parser.add_argument("--extract_qi", default=False,
                              required=False,
                              action='store_true',
                              help="Also extract QI masks to SQLite database")
    args = parser.parse_args()

    # Get extension and creation options
    if HAVE_GET_GDAL_DRIVERS:
        out_ext = get_gdal_drivers.GDALDrivers().get_ext_from_driver(args.of)
        out_creation_options = get_gdal_drivers.GDALDrivers().get_creation_options_from_ext(out_ext)
    # If get_gdal_drives is not available a couple of options are hardcoded
    else:
        if args.of == "ENVI":
            out_ext = ".bsq"
            out_creation_options = []
        elif args.of == "netCDF":
            out_ext = "nc"
            out_creation_options = ['FORMAT=NC4C', 'COMPRESS=DEFLATE']
        else:
            print("Could not import 'get_gdal_drivers' to determine correct "
                    "extension for {} format. Try using 'ENVI' or 'netCDF' "
                    "instead".format(args.of))

    for dataset in args.infiles:
        print("\n** {} **\n".format(os.path.basename(dataset)))

        subdataset_names = get_subdataset_names(dataset,
                                                resolution=args.resolution)

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

            gdal_translate_cmd.extend([subdataset[0], out_file])
            print(" ".join(gdal_translate_cmd))
            subprocess.check_call(gdal_translate_cmd)

        # Merge QI layers for each granule (GDAL doesn't do this).
        if args.extract_qi:
            print(" Extracting QI layers")
            input_basename = os.path.split(dataset)[1]
            input_basename = input_basename.replace(".SAFE","")
            out_qi_dir = os.path.join(args.outdir, input_basename + "_qi")
            try:
                os.makedirs(out_qi_dir)
            except OSError:
                # Assume already exists and continue
                pass

            merge_qi_vectors(dataset, out_qi_dir)

