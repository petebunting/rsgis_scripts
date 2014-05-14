#!/usr/bin/env python

import argparse
from rios import ratapplier
import numpy

def classifyRAT(info, inputs, outputs):

    outClass = numpy.zeros_like(inputs.inrat.b1Mean, dtype=numpy.int16)

    # Check for loss of water bodies (1)
    outClass = numpy.where(inputs.inrat.b1Mean < 1000, 1, outClass)

    # Save output column to RAT
    outputs.outrat.outClass = outClass

# Set up options
parser = argparse.ArgumentParser()
parser.add_argument("inclumps", nargs=1,type=str, help="Input clumps file")
args = parser.parse_args() 

inRats = ratapplier.RatAssociations()
outRats = ratapplier.RatAssociations()
            
inRats.inrat = ratapplier.RatHandle(args.inclumps[0])
outRats.outrat = ratapplier.RatHandle(args.inclumps[0])
            
ratapplier.apply(classifyRAT, inRats, outRats)
