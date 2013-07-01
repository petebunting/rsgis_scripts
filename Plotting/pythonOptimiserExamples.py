# Script to produce plots showing path taken by various optimisers
# from:
#
# Clewley, D. 2012. Retreival of Forest Structure and Biomass From Radar Data using 
# Backscatter Modelling and Inversion. PhD Thesis. Aberystwyth University.
#
# Using the Rosenbrock function:
# http://en.wikipedia.org/wiki/Rosenbrock_function
#
# Plot based on code from wikipedia article.
# 
# Daniel Clewley (daniel.clewley@gmail.com)
#
from scipy.optimize import *
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

optimiserList  = ['neldermead', 'cg', 'bfgs', 'powell']

for optimiser in optimiserList:
    x0 = [-1, -1]
    if optimiser == 'neldermead':
        (xopt, fopt, iter, funcalls, warnflag, allvecs) = fmin(rosen, x0, xtol=1e-8, full_output=1, retall=1)
    elif optimiser == 'cg':
        (xopt, fopt, iter, funcalls, warnflag, allvecs) = fmin_cg(rosen, x0, fprime=rosen_der, full_output=1, retall=1)
    elif optimiser == 'bfgs':
        (xopt, fopt, gopt, Hopt, func_calls, grad_calls, warnflag, allvecs) = fmin_bfgs(rosen, x0, fprime=rosen_der, full_output=1, retall=1)
    elif (optimiser == 'powell'):
        (xopt, fopt, direc, iter, funcalls, warnflag, allvecs) = fmin_powell(rosen, x0, xtol=1e-8, full_output=1, retall=1)
    
    allvecs = np.array(allvecs)
    
    x0 = np.arange(-2.1,2.1,0.1)
    y0 = np.ones(x0.size)
    x = []
    y = []
    z = []
    
    for i in range(x0.size):
        x.append(x0)
    
    for j in range(x0.size):
        y.append(y0 * x0[j])
        
    x = np.array(x)
    y = np.array(y)
    
    path1 = []
    moveCmd = []
    
    first = True
    
    for val in allvecs:
        if first:
            moveCmd.append(Path.MOVETO)
            first = False
        else:
            moveCmd.append(Path.LINETO)
        path1.append((val[0], val[1]))
    
    for i in range (x0.size):
        z0 = []
        for j in range(y0.size):
            val = rosen([x0[j], x0[i]])
            z0.append(val)
        z.append(z0)
    
    z = np.array(z)
    contours = [0,1,2,3,4,5,10,20,30,40,50,100,500,1000,2000]
    contoursLine = [10,20,30,40,50,100,500,1000,2000]
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    CS = plt.contour(x0,x0,z,contoursLine,linewidths=0.5,colors='k')
    CS = plt.contourf(x0,x0,z,contours, norm=Normalize(vmin=0, vmax=100, clip=True), col=cm.jet)
    plt.colorbar() # draw colorbar
    # plot data points.
    plt.scatter(allvecs[:,0],allvecs[:,1],marker='o',c='black',s=10)
    
    path = Path(path1, moveCmd)
    patch = patches.PathPatch(path, facecolor='none', lw=2)
    ax.add_patch(patch)
    
    plt.xlim(-2,2)
    plt.ylim(-2,2)
#    if optimiser != 'anneal':
#        plt.annotate('Minima', xy=(1, 1))
    plt.xlabel("x")
    plt.ylabel("y")
    #plt.legend(('(1.5, 1.5)','(2, 2)','(-1.5, -1.5)'),loc='upper left')
    #plt.show()
    if optimiser == 'neldermead':
        plt.savefig('neldermead.pdf', format='pdf')
    elif optimiser == 'cg':
        plt.savefig('conjugategradient.pdf', format='pdf')
    elif optimiser == 'bfgs':
        plt.savefig('bfgs.pdf', format='pdf')
    elif (optimiser == 'powell'):
        plt.savefig('powell.pdf', format='pdf')
