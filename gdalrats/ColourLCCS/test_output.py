#!/usr/bin/env python

import sys
from rios import rat
import numpy as np
import osgeo.gdal as gdal

def colourLevel4(LCCSs):
    # Create Output Arrays
    redColours = np.empty_like(LCCSs, dtype=np.int)
    redColours[...] = 0
    greenColours = np.empty_like(LCCSs, dtype=np.int)
    greenColours[...] = 0
    blueColours = np.empty_like(LCCSs, dtype=np.int)
    blueColours[...] = 0
    alphaColours = np.empty_like(LCCSs, dtype=np.int)
    alphaColours[...] = 255

    # NA
    redColours = np.where(LCCSs == "NA", 0, redColours)
    greenColours = np.where(LCCSs == "NA", 0, greenColours)
    blueColours = np.where(LCCSs == "NA", 0, blueColours)
    alphaColours = np.where(LCCSs == "NA", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B2_A7.A10", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B2_A7.A10", 220, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B2_A7.A10", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B2_A7.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B2_A7.A9", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B2_A7.A9", 210, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B2_A7.A9", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B2_A7.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B2_A8.A10", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B2_A8.A10", 200, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B2_A8.A10", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B2_A8.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B2_A8.A9", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B2_A8.A9", 190, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B2_A8.A9", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B2_A8.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B3_A7.A10", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B3_A7.A10", 180, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B3_A7.A10", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B3_A7.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B3_A7.A9", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B3_A7.A9", 170, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B3_A7.A9", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B3_A7.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B3_A8.A10", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B3_A8.A10", 160, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B3_A8.A10", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B3_A8.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B3_A8.A9", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B3_A8.A9", 150, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B3_A8.A9", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B3_A8.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1.B4_A7.A10", 200, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1.B4_A7.A10", 140, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1.B4_A7.A10", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1.B4_A7.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1_A7.A10", 220, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1_A7.A10", 140, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1_A7.A10", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1_A7.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1_A7.A9", 240, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1_A7.A9", 140, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1_A7.A9", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1_A7.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1_A8.A10", 250, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1_A8.A10", 140, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1_A8.A10", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1_A8.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A1_A8.A9", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A1_A8.A9", 160, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A1_A8.A9", 10, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A1_A8.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2.B2_A7.A10", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2.B2_A7.A10", 200, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2.B2_A7.A10", 255, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2.B2_A7.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2.B2_A7.A9", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2.B2_A7.A9", 190, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2.B2_A7.A9", 245, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2.B2_A7.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2.B2_A8.A10", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2.B2_A8.A10", 180, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2.B2_A8.A10", 235, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2.B2_A8.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2.B2_A8.A9", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2.B2_A8.A9", 170, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2.B2_A8.A9", 225, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2.B2_A8.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2.B3_A7.A10", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2.B3_A7.A10", 160, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2.B3_A7.A10", 215, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2.B3_A7.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2.B3_A7.A9", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2.B3_A7.A9", 150, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2.B3_A7.A9", 205, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2.B3_A7.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2.B3_A8.A10", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2.B3_A8.A10", 140, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2.B3_A8.A10", 195, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2.B3_A8.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2_A7.A10", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2_A7.A10", 130, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2_A7.A10", 185, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2_A7.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2_A7.A9", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2_A7.A9", 120, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2_A7.A9", 175, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2_A7.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2_A8.A10", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2_A8.A10", 120, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2_A8.A10", 165, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2_A8.A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A2_A8.A9", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A2_A8.A9", 120, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A2_A8.A9", 155, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A2_A8.A9", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A4", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A4", 140, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A4", 145, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A4", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A4.B2", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A4.B2", 150, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A4.B2", 135, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A4.B2", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A4.B3", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A4.B3", 160, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A4.B3", 125, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A4.B3", 255, alphaColours)

    redColours = np.where(LCCSs == "A11.A11A4.B4", 255, redColours)
    greenColours = np.where(LCCSs == "A11.A11A4.B4", 170, greenColours)
    blueColours = np.where(LCCSs == "A11.A11A4.B4", 115, blueColours)
    alphaColours = np.where(LCCSs == "A11.A11A4.B4", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A12A", 175, redColours)
    greenColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A12A", 255, greenColours)
    blueColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A12A", 100, blueColours)
    alphaColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A12A", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A13", 155, redColours)
    greenColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A13", 245, greenColours)
    blueColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A13", 100, blueColours)
    alphaColours = np.where(LCCSs == "A12.A1.A11.D1.E2_A13", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A1.A11.D2.E2_A12A", 135, redColours)
    greenColours = np.where(LCCSs == "A12.A1.A11.D2.E2_A12A", 235, greenColours)
    blueColours = np.where(LCCSs == "A12.A1.A11.D2.E2_A12A", 100, blueColours)
    alphaColours = np.where(LCCSs == "A12.A1.A11.D2.E2_A12A", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A1.D1.E2", 115, redColours)
    greenColours = np.where(LCCSs == "A12.A1.D1.E2", 225, greenColours)
    blueColours = np.where(LCCSs == "A12.A1.D1.E2", 100, blueColours)
    alphaColours = np.where(LCCSs == "A12.A1.D1.E2", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A1.D1.E2_A10", 95, redColours)
    greenColours = np.where(LCCSs == "A12.A1.D1.E2_A10", 215, greenColours)
    blueColours = np.where(LCCSs == "A12.A1.D1.E2_A10", 100, blueColours)
    alphaColours = np.where(LCCSs == "A12.A1.D1.E2_A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A1.D2.E2", 75, redColours)
    greenColours = np.where(LCCSs == "A12.A1.D2.E2", 205, greenColours)
    blueColours = np.where(LCCSs == "A12.A1.D2.E2", 100, blueColours)
    alphaColours = np.where(LCCSs == "A12.A1.D2.E2", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A1.D2.E2_A10", 55, redColours)
    greenColours = np.where(LCCSs == "A12.A1.D2.E2_A10", 195, greenColours)
    blueColours = np.where(LCCSs == "A12.A1.D2.E2_A10", 100, blueColours)
    alphaColours = np.where(LCCSs == "A12.A1.D2.E2_A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A12A.B7", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A12A.B7", 150, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A12A.B7", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A12A.B7", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A13.B7", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A13.B7", 140, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A13.B7", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.A11.B3.D1.E2_A13.B7", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.A11.B3.D2.E2_A12A.B7", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.A11.B3.D2.E2_A12A.B7", 130, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.A11.B3.D2.E2_A12A.B7", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.A11.B3.D2.E2_A12A.B7", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B6", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B6", 120, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B6", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B6", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B7", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B7", 110, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B7", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.B3.D1.E2_A10.B7", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B6", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B6", 100, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B6", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B6", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B7", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B7", 90, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B7", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.B3.D1.E2_B7", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B6", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B6", 80, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B6", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B6", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B7", 10, redColours)
    greenColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B7", 70, greenColours)
    blueColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B7", 10, blueColours)
    alphaColours = np.where(LCCSs == "A12.A3.B3.D2.E2_A10.B7", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.A11.D1.E2", 255, redColours)
    greenColours = np.where(LCCSs == "A12.A4.A11.D1.E2", 150, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.A11.D1.E2", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.A11.D1.E2", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A", 245, redColours)
    greenColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A", 140, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A.B9", 235, redColours)
    greenColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A.B9", 130, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A.B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A12A.B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A13.B9", 225, redColours)
    greenColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A13.B9", 120, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A13.B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.A11.D1.E2_A13.B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.A11.D1.E2_B9", 215, redColours)
    greenColours = np.where(LCCSs == "A12.A4.A11.D1.E2_B9", 110, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.A11.D1.E2_B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.A11.D1.E2_B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.A11.D2.E2_A12A.B9", 205, redColours)
    greenColours = np.where(LCCSs == "A12.A4.A11.D2.E2_A12A.B9", 100, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.A11.D2.E2_A12A.B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.A11.D2.E2_A12A.B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.A14.D1.E2_A12A.B9", 195, redColours)
    greenColours = np.where(LCCSs == "A12.A4.A14.D1.E2_A12A.B9", 90, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.A14.D1.E2_A12A.B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.A14.D1.E2_A12A.B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.D1.E2", 185, redColours)
    greenColours = np.where(LCCSs == "A12.A4.D1.E2", 80, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.D1.E2", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.D1.E2", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.D1.E2_A10", 175, redColours)
    greenColours = np.where(LCCSs == "A12.A4.D1.E2_A10", 70, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.D1.E2_A10", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.D1.E2_A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.D1.E2_A10.B9", 165, redColours)
    greenColours = np.where(LCCSs == "A12.A4.D1.E2_A10.B9", 60, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.D1.E2_A10.B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.D1.E2_A10.B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.D1.E2_B9", 155, redColours)
    greenColours = np.where(LCCSs == "A12.A4.D1.E2_B9", 50, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.D1.E2_B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.D1.E2_B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.D2.E2_A10", 145, redColours)
    greenColours = np.where(LCCSs == "A12.A4.D2.E2_A10", 40, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.D2.E2_A10", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.D2.E2_A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A4.D2.E2_A10.B9", 135, redColours)
    greenColours = np.where(LCCSs == "A12.A4.D2.E2_A10.B9", 30, greenColours)
    blueColours = np.where(LCCSs == "A12.A4.D2.E2_A10.B9", 50, blueColours)
    alphaColours = np.where(LCCSs == "A12.A4.D2.E2_A10.B9", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A5", 100, redColours)
    greenColours = np.where(LCCSs == "A12.A5", 255, greenColours)
    blueColours = np.where(LCCSs == "A12.A5", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A5", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A12A.B13", 95, redColours)
    greenColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A12A.B13", 235, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A12A.B13", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A12A.B13", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A13.B13", 90, redColours)
    greenColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A13.B13", 215, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A13.B13", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.A11.B4.E5_A13.B13", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.A11.E5", 85, redColours)
    greenColours = np.where(LCCSs == "A12.A6.A11.E5", 195, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.A11.E5", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.A11.E5", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.A11.E5_A12A", 80, redColours)
    greenColours = np.where(LCCSs == "A12.A6.A11.E5_A12A", 175, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.A11.E5_A12A", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.A11.E5_A12A", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.A11.E5_A13", 120, redColours)
    greenColours = np.where(LCCSs == "A12.A6.A11.E5_A13", 155, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.A11.E5_A13", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.A11.E5_A13", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.A14.E5_A12A", 140, redColours)
    greenColours = np.where(LCCSs == "A12.A6.A14.E5_A12A", 155, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.A14.E5_A12A", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.A14.E5_A12A", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.A14.E5_A16", 160, redColours)
    greenColours = np.where(LCCSs == "A12.A6.A14.E5_A16", 155, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.A14.E5_A16", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.A14.E5_A16", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.B4.E5_A10.B13", 180, redColours)
    greenColours = np.where(LCCSs == "A12.A6.B4.E5_A10.B13", 155, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.B4.E5_A10.B13", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.B4.E5_A10.B13", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.B4.E5_B13", 200, redColours)
    greenColours = np.where(LCCSs == "A12.A6.B4.E5_B13", 155, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.B4.E5_B13", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.B4.E5_B13", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.E5", 220, redColours)
    greenColours = np.where(LCCSs == "A12.A6.E5", 155, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.E5", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.E5", 255, alphaColours)

    redColours = np.where(LCCSs == "A12.A6.E5_A10", 240, redColours)
    greenColours = np.where(LCCSs == "A12.A6.E5_A10", 155, greenColours)
    blueColours = np.where(LCCSs == "A12.A6.E5_A10", 255, blueColours)
    alphaColours = np.where(LCCSs == "A12.A6.E5_A10", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A1.B2.XX.XX_XX", 50, redColours)
    greenColours = np.where(LCCSs == "A23.A23A1.B2.XX.XX_XX", 200, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A1.B2.XX.XX_XX", 200, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A1.B2.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A1.B3.XX.XX_XX", 75, redColours)
    greenColours = np.where(LCCSs == "A23.A23A1.B3.XX.XX_XX", 175, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A1.B3.XX.XX_XX", 190, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A1.B3.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A1.B4.XX.XX_XX", 75, redColours)
    greenColours = np.where(LCCSs == "A23.A23A1.B4.XX.XX_XX", 150, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A1.B4.XX.XX_XX", 180, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A1.B4.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A1.XX.XX_XX", 75, redColours)
    greenColours = np.where(LCCSs == "A23.A23A1.XX.XX_XX", 125, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A1.XX.XX_XX", 170, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A1.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A2.B2.XX.XX_XX", 100, redColours)
    greenColours = np.where(LCCSs == "A23.A23A2.B2.XX.XX_XX", 100, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A2.B2.XX.XX_XX", 160, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A2.B2.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A2.B3.XX.XX_XX", 125, redColours)
    greenColours = np.where(LCCSs == "A23.A23A2.B3.XX.XX_XX", 75, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A2.B3.XX.XX_XX", 150, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A2.B3.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A2.B4.XX.XX_XX", 150, redColours)
    greenColours = np.where(LCCSs == "A23.A23A2.B4.XX.XX_XX", 50, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A2.B4.XX.XX_XX", 140, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A2.B4.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A23.A23A2.XX.XX_XX", 175, redColours)
    greenColours = np.where(LCCSs == "A23.A23A2.XX.XX_XX", 25, greenColours)
    blueColours = np.where(LCCSs == "A23.A23A2.XX.XX_XX", 130, blueColours)
    alphaColours = np.where(LCCSs == "A23.A23A2.XX.XX_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A14.XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A14.XX", 80, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A14.XX", 270, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A14.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A15.XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A15.XX", 70, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A15.XX", 260, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.A13.XX.D1.E2_A15.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A14.XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A14.XX", 60, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A14.XX", 250, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A14.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A15.XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A15.XX", 50, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A15.XX", 240, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.A13.XX.D2.E2_A15.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.XX.D1.E2_A12.XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.XX.D1.E2_A12.XX", 40, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.XX.D1.E2_A12.XX", 230, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.XX.D1.E2_A12.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.XX.D1.E2_XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.XX.D1.E2_XX", 30, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.XX.D1.E2_XX", 220, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.XX.D1.E2_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.XX.D2.E2_A12.XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.XX.D2.E2_A12.XX", 20, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.XX.D2.E2_A12.XX", 210, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.XX.D2.E2_A12.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A1.XX.D2.E2_XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A1.XX.D2.E2_XX", 10, greenColours)
    blueColours = np.where(LCCSs == "A24.A1.XX.D2.E2_XX", 200, blueColours)
    alphaColours = np.where(LCCSs == "A24.A1.XX.D2.E2_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A14.B7.XX", 200, redColours)
    greenColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A14.B7.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A14.B7.XX", 190, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A14.B7.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A15.B7.XX", 190, redColours)
    greenColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A15.B7.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A15.B7.XX", 190, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D1.E2_A15.B7.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B6.XX", 180, redColours)
    greenColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B6.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B6.XX", 190, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B6.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B7.XX", 170, redColours)
    greenColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B7.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B7.XX", 190, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.A13.B3.XX.D2.E2_A14.B7.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B6.XX", 160, redColours)
    greenColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B6.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B6.XX", 190, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B6.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B7.XX", 150, redColours)
    greenColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B7.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B7.XX", 190, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_A12.B7.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B6.XX", 140, redColours)
    greenColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B6.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B6.XX", 170, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B6.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B7.XX", 130, redColours)
    greenColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B7.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B7.XX", 150, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.B3.XX.D1.E2_B7.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A3.B3.XX.D2.E2_A12.B7.XX", 120, redColours)
    greenColours = np.where(LCCSs == "A24.A3.B3.XX.D2.E2_A12.B7.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A3.B3.XX.D2.E2_A12.B7.XX", 130, blueColours)
    alphaColours = np.where(LCCSs == "A24.A3.B3.XX.D2.E2_A12.B7.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.B9.XX", 110, redColours)
    greenColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.B9.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.B9.XX", 110, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.B9.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.XX", 100, redColours)
    greenColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.XX", 90, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A14.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.B9.XX", 90, redColours)
    greenColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.B9.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.B9.XX", 70, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.B9.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.XX", 80, redColours)
    greenColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.XX", 50, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_A15.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_B9.XX", 70, redColours)
    greenColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_B9.XX", 0, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_B9.XX", 30, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.A13.XX.D1.E2_B9.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.B9.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.B9.XX", 200, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.B9.XX", 100, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.B9.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.XX", 245, redColours)
    greenColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.XX", 200, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.XX", 90, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.XX.D1.E2_A12.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.XX.D1.E2_B9.XX", 235, redColours)
    greenColours = np.where(LCCSs == "A24.A4.XX.D1.E2_B9.XX", 200, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.XX.D1.E2_B9.XX", 80, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.XX.D1.E2_B9.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.XX.D1.E2_XX", 225, redColours)
    greenColours = np.where(LCCSs == "A24.A4.XX.D1.E2_XX", 200, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.XX.D1.E2_XX", 70, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.XX.D1.E2_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.B9.XX", 215, redColours)
    greenColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.B9.XX", 200, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.B9.XX", 60, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.B9.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.XX", 205, redColours)
    greenColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.XX", 200, greenColours)
    blueColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.XX", 50, blueColours)
    alphaColours = np.where(LCCSs == "A24.A4.XX.D2.E2_A12.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A14.B13.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A14.B13.XX", 255, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A14.B13.XX", 200, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A14.B13.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A15.B13.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A15.B13.XX", 250, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A15.B13.XX", 170, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.A13.B4.XX.E5_A15.B13.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A14.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A14.XX", 245, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A14.XX", 140, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A14.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A15.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A15.XX", 240, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A15.XX", 110, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.A13.XX.E5_A15.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.A13.XX.E5_XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.A13.XX.E5_XX", 235, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.A13.XX.E5_XX", 80, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.A13.XX.E5_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A17.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A17.XX", 230, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A17.XX", 50, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A17.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A18.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A18.XX", 225, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A18.XX", 20, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.A16.XX.E5_A18.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.B4.XX.E5_A12.B13.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.B4.XX.E5_A12.B13.XX", 220, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.B4.XX.E5_A12.B13.XX", 20, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.B4.XX.E5_A12.B13.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.B4.XX.E5_B13.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.B4.XX.E5_B13.XX", 215, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.B4.XX.E5_B13.XX", 20, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.B4.XX.E5_B13.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.XX.E5_A12.XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.XX.E5_A12.XX", 210, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.XX.E5_A12.XX", 20, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.XX.E5_A12.XX", 255, alphaColours)

    redColours = np.where(LCCSs == "A24.A6.XX.E5_XX", 255, redColours)
    greenColours = np.where(LCCSs == "A24.A6.XX.E5_XX", 205, greenColours)
    blueColours = np.where(LCCSs == "A24.A6.XX.E5_XX", 20, blueColours)
    alphaColours = np.where(LCCSs == "A24.A6.XX.E5_XX", 255, alphaColours)

    redColours = np.where(LCCSs == "B16.A3_A8", 255, redColours)
    greenColours = np.where(LCCSs == "B16.A3_A8", 0, greenColours)
    blueColours = np.where(LCCSs == "B16.A3_A8", 255, blueColours)
    alphaColours = np.where(LCCSs == "B16.A3_A8", 255, alphaColours)

    redColours = np.where(LCCSs == "B27.A1.B1.C2.D2_XX.B6", 10, redColours)
    greenColours = np.where(LCCSs == "B27.A1.B1.C2.D2_XX.B6", 200, greenColours)
    blueColours = np.where(LCCSs == "B27.A1.B1.C2.D2_XX.B6", 255, blueColours)
    alphaColours = np.where(LCCSs == "B27.A1.B1.C2.D2_XX.B6", 255, alphaColours)

    redColours = np.where(LCCSs == "B27.A1.B2.C2.D2_XX.B6", 0, redColours)
    greenColours = np.where(LCCSs == "B27.A1.B2.C2.D2_XX.B6", 150, greenColours)
    blueColours = np.where(LCCSs == "B27.A1.B2.C2.D2_XX.B6", 255, blueColours)
    alphaColours = np.where(LCCSs == "B27.A1.B2.C2.D2_XX.B6", 255, alphaColours)

    redColours = np.where(LCCSs == "B27.A2.B1.C2.D2_XX.B6", 0, redColours)
    greenColours = np.where(LCCSs == "B27.A2.B1.C2.D2_XX.B6", 100, greenColours)
    blueColours = np.where(LCCSs == "B27.A2.B1.C2.D2_XX.B6", 255, blueColours)
    alphaColours = np.where(LCCSs == "B27.A2.B1.C2.D2_XX.B6", 255, alphaColours)

    redColours = np.where(LCCSs == "B27.A2.B2.C2.D2_XX.B6", 0, redColours)
    greenColours = np.where(LCCSs == "B27.A2.B2.C2.D2_XX.B6", 60, greenColours)
    blueColours = np.where(LCCSs == "B27.A2.B2.C2.D2_XX.B6", 250, blueColours)
    alphaColours = np.where(LCCSs == "B27.A2.B2.C2.D2_XX.B6", 255, alphaColours)

    redColours = np.where(LCCSs == "B27.B2.C2.D2_XX.B6", 0, redColours)
    greenColours = np.where(LCCSs == "B27.B2.C2.D2_XX.B6", 10, greenColours)
    blueColours = np.where(LCCSs == "B27.B2.C2.D2_XX.B6", 150, blueColours)
    alphaColours = np.where(LCCSs == "B27.B2.C2.D2_XX.B6", 255, alphaColours)
    return redColours, greenColours, blueColours, alphaColours

# Input file.
fname = "/some/random/file.kea"
ratDataset = gdal.Open( fname, gdal.GA_Update )

print "Import Columns."
LCCSs = rat.readColumn(ratDataset, "LCCS")

print "Classifying Level 4"
red, green, blue, alpha = colourLevel4(LCCSs)
rat.writeColumn(ratDataset, "Red", red)
rat.writeColumn(ratDataset, "Green", green)
rat.writeColumn(ratDataset, "Blue", blue)
rat.writeColumn(ratDataset, "Alpha", alpha)
