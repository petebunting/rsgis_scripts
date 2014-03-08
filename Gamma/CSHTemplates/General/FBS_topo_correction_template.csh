#! /bin/csh
#
# Created by Dan Clewley (IGES/AU).
# Copyright 2012 Dan Clewley. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# Script to process Topographically correct ALOS data
# using the method of Castel et al. 2001:
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

sigma2gamma SCENENAME_hh.utm SCENENAME.inc SCENENAME.gamma_hh.utm $width

product SCENENAME.gamma_hh.utm SCENENAME.pix SCENENAME_hh.utm.temp $width 1 1 0

lin_comb 1 SCENENAME_hh.utm.temp 0 0.777 SCENENAME.topo_hh.utm $width

# Remove temp files
rm *temp


