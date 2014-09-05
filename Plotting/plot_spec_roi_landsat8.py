#!/usr/bin/env python

"""
Plot spectral profile extracted using RSGISLib
"""

import numpy
from matplotlib import pylab as plt

roi_data = numpy.genfromtxt('roi_stats.csv', delimiter=',')

wavelengths = roi_data[0,1:]
radiance = roi_data[1,1:]

plt.plot(wavelengths, radiance, color='black')
plt.axvspan(433, 453, color='yellow')
plt.axvspan(450, 515, color='blue')
plt.axvspan(525, 600, color='green')
plt.axvspan(630, 680, color='red')
plt.axvspan(845, 885, color='0.5')
plt.axvspan(1560, 1660, color='0.5')
plt.axvspan(2100, 2300, color='0.5')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Radiance (nW/cm$2$/sr/nm)')
plt.xlim((400,2500))
plt.show()
plt.savefig('fenix_radiance_ls8.pdf')

