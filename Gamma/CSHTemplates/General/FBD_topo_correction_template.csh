#! /bin/csh
#
# Script to process Topographically correct ALOS data
# using the method of Castel et al. 2001:
#
# sigma_corrected = gamma_0 * PIX * sin(refAngle)
#
# Where the refference angle is set to 39 degrees (cos(39) = 0.777
#
# Castel et al. Sensitivity of space-borne SAR data to forest parameters over sloping terrain. 
#Theory and experiment. International journal of remote sensing(Print) (2001) vol. 22 (12) pp. 2351-2376
#
# Created by Dan Clewley 18/04/2010
#
# 
set width = `grep width gSCENENAME.dem.par | cut -d : -f 1 --complement`

sigma2gamma SCENENAME.hh.utm SCENENAME.inc SCENENAME.gamma.hh.utm $width
sigma2gamma SCENENAME.hv.utm SCENENAME.inc SCENENAME.gamma.hv.utm $width

product SCENENAME.gamma.hh.utm SCENENAME.pix SCENENAME.hh.utm.temp $width 1 1 0
product SCENENAME.gamma.hv.utm SCENENAME.pix SCENENAME.hv.utm.temp $width 1 1 0

lin_comb 1 SCENENAME.hh.utm.temp 0 0.777 SCENENAME.topo.hh.utm $width
lin_comb 1 SCENENAME.hv.utm.temp 0 0.777 SCENENAME.topo.hv.utm $width

# Remove temp files
rm *temp


