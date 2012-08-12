#!/usr/bin/env python

import sys
from rios import rat
fname = sys.argv[1]

print rat.readColumn(fname, "floatstuff")
