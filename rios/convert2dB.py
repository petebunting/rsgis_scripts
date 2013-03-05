# A script to convert to dB using the RIOS applier.
# Dan Clewley (daniel.clewley@gmail.com) - 05/02/2013

import sys
from rios import applier
from rios import cuiprogress
import numpy as np

def converttodB(info, inputs, outputs):
    """
    Converts to dB using:
    10*log10(b1)
    """
    outputs.outimage = 10 * np.log10(inputs.inimage)

if len(sys.argv) == 3:
    inImage = sys.argv[1]
    outImage = sys.argv[2] 
else:
    print '''Not enough parameters provided.
Usage:
   convert2dB.py inImage outImage
        '''
    exit()

infiles = applier.FilenameAssociations()
infiles.inimage = inImage

outfiles = applier.FilenameAssociations()
outfiles.outimage = outImage

controls = applier.ApplierControls()
controls.progress = cuiprogress.CUIProgressBar()
controls.setCalcStats(True)
applier.apply(converttodB, infiles, outfiles, controls=controls)
