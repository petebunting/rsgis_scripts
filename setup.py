#!/usr/bin/env python
"""
Setup script for RSGISScripts

Based on setup from gdalutils.
"""
import glob
from distutils.core import setup

scriptsList = [
'Vector/OGR2OGR/CreateCSVfromSHP.py',
'Text/FindReplaceTextDIR.py',
'Text/JoinTablesCSV.py',
'gdalrats/setthematic.py',
'File/Rename/reFindandReplaceFileName.py',
'GDAL/setbandname.py',
'GDAL/subsetImage2Image.py',
'TuiView/export_quicklook_tuiview.py',
'classification/GenerateClassLegend.py',
'Plotting/two_band_scatter_plot.py']

setup(name='rsgis_scripts',
      scripts=scriptsList)
