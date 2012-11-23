#!/usr/bin/env python

import sys
from scipy import ndimage
from rios.imagereader import ImageReader
from rios.imagewriter import ImageWriter

inImage = sys.argv[1]
outImage = sys.argv[2]

reader = ImageReader(inImage)
writer = None
for (info, block) in reader:
    out = block * 2
    if writer is None:
        writer = ImageWriter(outImage, info=info, firstblock=out, drivername='HFA', creationoptions=['COMPRESSED=TRUE'])
    else:
        writer.write(out)

writer.close(calcStats=True)
