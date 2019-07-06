#!/bin/bash

# A script for creating a DEM and ortho from micmac
# The setting -1 means it will detect points at max resoltuiom - this is lengthy.
# Change to something like 2000 or lower tpo resize smaller and thus quicker 


# Creatw an image pair list based on gps coordinates
# The .csv file is a list of containing image name GNSS coords yaw pitch roll
# A func exists (data.py) to reformat the bramour data - for other platforms
# Not eesential but speeds up matching a lot - if not should read from exif
# if all data avalable
mm3d OriConvert OriTxtInFile llanbedr_pic_name_MM.csv Nav-Brut-RTL ChSys=DegreeWGS84@WGS84 MTD1=1 NameCple=FileImagesNeighbour.xml CalcV=1

# Tie point detection - BE WARNED! This is atfull resolutiom (-1) and will take a
# LONG time 

mm3d Tapioca File FileImagesNeighbour.xml -1;

# 1. Alternatively replace -1 with image resizing option eg 1000

# 2. Alternatively use mulscale to try at a reduced resolution, then only the images
# with no of tie points over a certain threshold are used on final tie point
# detection with full res imagery

# mm3d Tapioca MulScale File FileImagesNeighbour.xml lowressize hiressize NbMinPt nofofpoints
# mm3d Tapioca MulScale File FileImagesNeighbour.xml 1000 4000 NbMinPt 10



# Compute orientations
mm3d Tapas Fraser ".*JPG" Out=All-Rel;


# Next calculate the movement during camera execution to edit the cloud in next command
# this is for lever arm compensation

mm3d CenterBascule .*JPG All-Rel Nav-Brut-RTL tmp CalcV=1;

# Calculate the adjustment for the images based on the last figure returned above in
# cmd output
# Delay = ......

# Convert coords
mm3d OriConvert OriTxtInFile boats.csv Nav-adjusted-RTL  MTD1=1 Delay=0.0380975;

# Execute the adjustment
mm3d CenterBascule .*JPG All-Rel Nav-adjusted-RTL All-RTL;


# Ortho and dem production----------------------------------------------------------------------------
# The old way - not recommended

#mm3d Malt Ortho ".*JPG" All-RTL DirMEC=MEC;

# There is a bug with Tawny!!!!
#mm3d Tawny MEC;

# RECOMMENDED
# Use the newer MicMac functions PIMs and Pims2MNT----------------------------------------------
# Check out the micmac site for mandatory and named args

mm3d Pims MicMac ".*JPG" All-RTL;

# DEM (PIMs-Merged_Prof.tif) is produced in the  PIMS-Tmp-Basc folder 
mm3d Pims2MNT MicMac DoOrtho=1;

# MICMAC - based mosaicing 
# RadiomEgal=1 means match the image hists or whatever

Tawny PIMs-ORTHO/ RadiomEgal=1 Out=Orthophotomosaic.tif

# VODKA cmd get rid of vignetting TODO

#-----------------------------------------------------------------------------------------------------

# Create a dense coloured point cloud
mm3d Nuage2Ply PIMs-TmpBasc/PIMs-Merged.xml Attr=PIMs-ORTHO/Orthophotomosaic.tif Out=pointcloud.ply;



# OSSIM - BASED MOSAICING ----------------------------------------------------------------------------
# Just here as an alternative for putting together tiles 
# Create some image histograms for ossim
#ossim-create-histo -i *Ort**.tif;

# Basic ortho with ossim is:
#ossim-orthoigen *Ort**.tif mosaic.tif;

# Or more options
# Here am feathering edges and matching histogram to specific image - produced most pleasing result
# See https://trac.osgeo.org/ossim/wiki/orthoigen for really detailed cmd help
#ossim-orthoigen --combiner-type ossimFeatherMosaic --hist-match Ort_DSC00698.tif *Ort**.tif mosaic.tif;

# ----------------------------------------------------------------------------------------------------


