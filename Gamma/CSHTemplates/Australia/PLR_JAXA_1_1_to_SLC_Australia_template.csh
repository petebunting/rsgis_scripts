#! /bin/csh
#
# Script to convert JAXA 1.1 data to GAMMA SLC
# Created by Joao Carreiras
#
# Modified by Dan Clewley 05/01/11 as template for BatchGamma.py
#

# Create the SLC and ISP parameter file in MSP format.
par_EORC_PALSAR LEDFILENAME temp.hh.slc.par HHFILENAME temp.hh.slc
par_EORC_PALSAR LEDFILENAME temp.hv.slc.par HVFILENAME temp.hv.slc
par_EORC_PALSAR LEDFILENAME temp.vv.slc.par VVFILENAME temp.vv.slc
par_EORC_PALSAR LEDFILENAME temp.vh.slc.par VVFILENAME temp.vh.slc
#
# Calibrate the SLCs. Since the SLCs are already corrected for antenna pattern, we only need to correct for
# the absolute calibration factor. For level 1.1 data processed by JAXA after January 9, 2009, the absolute 
# calibration factor is -115.0 dB.
radcal_SLC temp.hh.slc temp.hh.slc.par SCENENAME.hh.slc SCENENAME.hh.slc.par 1 - 0 0 1 0 -115.0
radcal_SLC temp.hv.slc temp.hv.slc.par SCENENAME.hv.slc SCENENAME.hv.slc.par 1 - 0 0 1 0 -115.0
radcal_SLC temp.vv.slc temp.vv.slc.par SCENENAME.vv.slc SCENENAME.vv.slc.par 1 - 0 0 1 0 -115.0
radcal_SLC temp.vh.slc temp.vh.slc.par SCENENAME.vh.slc SCENENAME.vh.slc.par 1 - 0 0 1 0 -115.0

# Generate a file with the SLC extents.
SLC_corners SCENENAME.hh.slc.par > SCENENAME.hh.slc.corners
SLC_corners SCENENAME.hv.slc.par > SCENENAME.hv.slc.corners
SLC_corners SCENENAME.vv.slc.par > SCENENAME.vv.slc.corners
SLC_corners SCENENAME.vh.slc.par > SCENENAME.vh.slc.corners