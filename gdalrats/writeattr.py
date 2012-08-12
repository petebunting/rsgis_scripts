#!/usr/bin/env python

import sys
from rios import rat
import numpy

fname = sys.argv[1]

floatdata = numpy.arange(0, 100, dtype=numpy.float)
intdata = numpy.arange(100, 200, dtype=numpy.integer)

rat.writeColumn(fname, "floatstuff", floatdata)
rat.writeColumn(fname, "intstuff", intdata)






