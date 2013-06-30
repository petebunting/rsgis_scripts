# genPolSignature.py
# A python script to geneate polarimetric signatures from an input Stokes Matrix
#
# Dan Clewley
# 12/03/11
#
  
from math import sin, cos
import numpy as np
import matplotlib.pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
import csv


pi = np.pi 
piDiv2 = pi / 2 # 90 degrees
degScale = pi / 180

class genPolSignature (object):

    def getSignatureClassic(self):
        # Output files for co-pol and cross pol
        outFileNameCoPol = 'copol_out.csv'
        outFileNameCrossPol = 'cross_out.csv'

        stokesM = np.genfromtxt("dihedral.txt")
        
        psiDeg = 0
        psiDegStep = 10
        chiDeg = 0
        chiDegStep = 10
        
        coPolData = []
        crossPolData = []
        
        for psiDeg in range(0,190,5): # Loop through orientation angle
            for chiDeg in range(-45,55,5): # Loop through elipticity
        
                psi = psiDeg * degScale
                chi = chiDeg * degScale
        
                stokest = np.matrix([1,cos(2*psi)*cos(2*chi),sin(2*psi)*cos(2*chi),sin(2*chi)])
                stokesr = np.matrix([1,cos(2*(psi))*cos(2*(chi-piDiv2)),sin(2*(psi))*cos(2*(chi-piDiv2)),sin(2*(chi-piDiv2))])
                coPolPower = float((stokest*stokesM)*stokest.transpose())
                crossPolPower = float((stokesr*stokesM)*stokest.transpose())
                coPolData.append([psiDeg,chiDeg,coPolPower]) 
                crossPolData.append([psiDeg,chiDeg,crossPolPower])        
        
        coPolData = np.array(coPolData) # Convert to numpy array
        crossPolData = np.array(crossPolData) # Convert to numpy array
        
        # Normalise co-pol power
        maxPower = coPolData.max(axis=0)[2] # Calculate maximum power
        normPower = coPolData[:,2]/maxPower # Divide power values by maximum power
        coPolData[:,2] = normPower.copy() # Copy back to plot data
        # Normalise cross-pol power
        maxPower = crossPolData.max(axis=0)[2] # Calculate maximum power
        normPower = crossPolData[:,2]/maxPower # Divide power values by maximum power
        crossPolData[:,2] = normPower.copy() # Copy back to plot data
        
        np.savetxt(outFileNameCoPol, coPolData, delimiter=',') # Write to text file
        np.savetxt(outFileNameCrossPol, crossPolData, delimiter=',') # Write to text file
        
        #self.colourPlot(coPolData, 38, 20, 'copol_colour.pdf')
        #self.colourPlot(crossPolData, 38, 20, 'crosspol_colour.pdf')
        self.wirePlot(coPolData, 38, 20, 'copol_wireframe.pdf')
        self.wirePlot(crossPolData, 38, 20, 'crosspol_wireframe.pdf')
          

    def wirePlot(self, inData, numX, numY, outFileName):
        ''' Create wireframe plot of data '''
        x=np.reshape(inData[:,0],(numX, numY))
        y=np.reshape(inData[:,1],(numX, numY))
        z=np.reshape(inData[:,2],(numX, numY))
        fig=p.figure()
        ax = p3.Axes3D(fig)
        ax.plot_wireframe(x,y,z)
        p.savefig(outFileName, format='pdf')
        #p.show()
        
    def colourPlot(self, inData, numX, numY, outFileName):
        ''' Create colour map plot of data,
        expexts array with 3 columns (x, y, z) '''
        z = np.reshape(inData[:,2],(numX, numY))
        p.imshow(z, cmap=p.cm.jet)
        p.savefig(outFileName, format='pdf')
        #p.show()
        
if '__main__':
    obj = genPolSignature()
    obj.getSignatureClassic()
