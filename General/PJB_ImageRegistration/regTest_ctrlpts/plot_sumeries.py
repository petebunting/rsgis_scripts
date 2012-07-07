#! /usr/bin/env python

from pylab import *
from RegSummery import Summery

class SummeryPlots (object):
	'This is class to compare control point files'

	# Opens the two files and places references into attributes
	def openFile4Read(self, inputPath):
		return open(inputPath, 'r', -1)
	
	# Parse the Summery file into a List.
	def parseSummeryFile(self, summeryFile, summeryList):
		counter = 0
		for eachLine in summeryFile:
			if eachLine[0] != ';':
				tmpSummery = Summery()
				tmpSummery.createSummery(eachLine)
				summeryList.append(tmpSummery)		
				counter = counter + 1
	
	def plotSummeries(self, summeryList, plotTitles, plotCode, outFilepath, fileFormat, plotTitle):
	    ylabelTxt = 'Mean Distance'
	    if plotCode == 1:
	        ylabelTxt = 'Standard Deviation of Distance'
	    elif plotCode == 2:
	        ylabelCode = 'Minimum Distance'
	    elif plotCode == 3:
	        ylabelCode = 'Maxmimum Distance'
	    
	    x = list()
	    y = list()
	    counter = 0
	    
	    #Find summeries of interest
	    for i in range(len(plotTitles)):
	        for j in range(len(summeryList)):
	            #print list[j].title, ', ', list[j].mean, ', ', list[j].stddev, ', ', list[j].min, ', ', list[j].min
		
	            if summeryList[j].title == plotTitles[i]:
	                print summeryList[j].title
	                if plotCode == 0:
	                    y.append(summeryList[j].mean)
	                    x.append(counter)
	                    counter = counter + 1
	                elif plotCode == 1:
	                    y.append(summeryList[j].stddev)
	                    x.append(counter)
	                    counter = counter + 1
	                elif plotCode == 2:
	                    y.append(summeryList[j].min)
	                    x.append(counter)
	                    counter = counter + 1
	                elif plotCode == 3:
	                    y.append(summeryList[j].max)
	                    x.append(counter)
	                    counter = counter + 1
	    
	    #print 'x , y'
	    #for i in range(len(x)):
	    #    print x[i], ', ', y[i]
	        
	    
       
	    figure()               	    
	    ylabel(ylabelTxt)
	    plot(x,y)
	    title(plotTitle)
	    savefig(outFilepath, format=fileFormat)
	    #show()
	                    
	
	# Contains the main execution order of the class
	def run(self, summeryPath, plotTitles, plotcode, outFilepath, fileFormat, plotTitle):
		
		summeries = list()
		#print 'Created Lists'
		
		# Get file paths
		try:
			summeryFile = self.openFile4Read(summeryPath)	
		except IOError, e:
			print '\nCould not open file:\n', e
			return
		#print 'Read in images'
		
		# Parse the Sumery file
		self.parseSummeryFile(summeryFile, summeries)
		
		# Close Files
		try:
			summeryFile.close()
		except IOError, e:
			print '\nCould not close file.\n', e
			return
		
		#for i in range(len(summeries)):
		 #   print summeries[i].title, ', ', summeries[i].mean, ', ', summeries[i].stddev, ', ', summeries[i].min, ', ', summeries[i].min
		
		self.plotSummeries(summeries, plotTitles, plotcode, outFilepath, fileFormat, plotTitle)
		
		del summeries	

# If run for the command line create instance and run!
if __name__ == '__main__':
	summeryfilepath = '/Users/pete/Desktop/Registration_Tests/results/min_mean_max_stddev'
	
	plotTheseTitles = ['p142_CASI_base2LiDAR','p142_CASI2LiDAR_2X3Y','p142_CASI2LiDAR_4X6Y','p142_CASI2LiDAR_8X10Y','p142_CASI2LiDAR_16X18Y']
	
	plotcode = 0
	
	pTitle = 'P142 CASI-LiDAR Translations'
	
	obj = SummeryPlots()
	obj.run(summeryfilepath, plotTheseTitles, plotcode, '/Users/pete/Desktop/Registration_Tests/results/plots/plot_p142_CASI_LiDAR_translation.png', 'png', pTitle)
