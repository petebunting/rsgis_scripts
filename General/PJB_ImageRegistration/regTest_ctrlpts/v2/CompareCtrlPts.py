#! /usr/bin/env python

from matplotlib import rcParams
rcParams['interactive'] = False

from ControlPoint import ControlPoint
from math import sqrt
from pylab import *
import gc
import pdb

class CompareCtrlPts (object):
    'This is class to compare control point files'

    # Opens the two files and places references into attributes
    def openFile4Read(self, inputPath):
        return open(inputPath, 'r', -1)
    
    def checkforSemiColons(self, line):
        foundSemiColon = False
        for i in range(len(line)):
            #print  line[i],
            if line[i] == ';':
                foundSemiColon = True
        return foundSemiColon
    
    # Parse the Control points file into a List.
    def parseControlPointsFile(self, ctrlPtsFile, list, ref):
        counter = 0
        for eachLine in ctrlPtsFile:
            semiColon = self.checkforSemiColons(eachLine)
            if semiColon == False:
                tmpCtrlPt = ControlPoint()
                if ref:
                    tmpCtrlPt.createCtrlPt(counter, eachLine)
                else:
                    tmpCtrlPt.createCtrlPtTxt(counter, eachLine)
                #print "X: ", tmpCtrlPt.refXPoint, " Y: ", tmpCtrlPt.refYPoint,
                #print " X2: ", tmpCtrlPt.floatXPoint, " Y2: ", tmpCtrlPt.floatYPoint
                list.append(tmpCtrlPt)      
                counter = counter + 1
        #print 'Read in ', counter, ' points from with the file'
    
    # Summerize the comparison the control points
    def summerizeCtrlPts(self, refPoints, regPoints):
        
        #print 'refPoints: ', len(refPoints), ' regPoints: ', len(regPoints)
        sumDiff = 0
        max = 0
        min = 0
        first = True 
        if len(refPoints) != len(regPoints):
            print 'Lists are different lengths'
            print 'Reference Points: ', len(refPoints), ' Registration Points: ', len(regPoints)
            return [-1, -1 , -1, -1]
        else:
            for i in range(len(refPoints)):
                if refPoints[i].refXPoint != regPoints[i].refXPoint:
                    print 'Reference X points are different'
                elif refPoints[i].refYPoint != regPoints[i].refYPoint:
                    print 'Reference Y points are different'
                else:
                    xDiff = refPoints[i].floatXPoint - regPoints[i].floatXPoint
                    yDiff = refPoints[i].floatYPoint - regPoints[i].floatYPoint
                    
                    xDiffSqu = xDiff * xDiff
                    yDiffSqu = yDiff * yDiff
                    
                    if xDiffSqu == 0 and yDiffSqu == 0:
                        diffDist = 0
                        #print '0'
                    else:
                        diffDist = sqrt(xDiffSqu + yDiffSqu)
                        #print diffDist
                        if first:
                            max = diffDist
                            min = diffDist
                            first = False
                        else:
                            if max < diffDist:
                                max = diffDist
                            elif min > diffDist:
                                min = diffDist
                        sumDiff = sumDiff + diffDist
                        regPoints[i].distance = diffDist
            mean = sumDiff / len(refPoints)
            
            sumDeviations = 0
            for i in range(len(refPoints)):
                xDiff = refPoints[i].floatXPoint - regPoints[i].floatXPoint
                yDiff = refPoints[i].floatYPoint - regPoints[i].floatYPoint
                
                xDiffSqu = xDiff * xDiff
                yDiffSqu = yDiff * yDiff
                    
                if xDiffSqu == 0 and yDiffSqu == 0:
                    diffDist = 0
                    #print '0'
                else:
                    diffDist = sqrt(xDiffSqu + yDiffSqu)
                    #print diffDist
                deviation = mean - diffDist
                devSq = deviation * deviation
                sumDeviations = sumDeviations + devSq
                regPoints[i].deviation = sqrt(devSq)
                #print "regPoints[i].distance = ", regPoints[i].distance
                
            stddev = sqrt(sumDeviations/(len(refPoints)-1))
            
            #print 'Min: ', min, ' Mean: ', mean, ' Max: ', max, ' Std Dev: ', stddev
            
            return [min, mean, max, stddev]
    
    # create error plot
    def createDistancePlot(self, points, summery, spotSize):
        x = []
        y = []
        area = []
        colour = []
        axisRange = [0,0,0,0]
        first = True
        for i in range(len(points)):
            x.append(points[i].floatXPoint)
            y.append(points[i].floatYPoint)
            area.append(spotSize)
            colour.append(points[i].distance)
            if first:
                axisRange = [points[i].floatXPoint, points[i].floatXPoint,points[i].floatYPoint,points[i].floatYPoint]
                first = False
            else:
                if axisRange[0] > points[i].floatXPoint:
                    axisRange[0] = points[i].floatXPoint
                elif axisRange[1] < points[i].floatXPoint:
                    axisRange[1] = points[i].floatXPoint
                
                if axisRange[2] > points[i].floatYPoint:
                    axisRange[2] = points[i].floatYPoint
                elif axisRange[3] < points[i].floatYPoint:
                    axisRange[3] = points[i].floatYPoint
        
        
        # Flip Y Axis
        yOutput = []
        for i in range(len(y)):
            yOutput.append((axisRange[3]-y[i])+axisRange[2])
        
        print 'xMin = ', axisRange[0], ' xMax = ', axisRange[1], ' yMin = ', axisRange[2], ' yMax = ', axisRange[3],
        
        figure(num=None, dpi=200)
        scatter(x, yOutput, s=area, c=colour, marker='o', cmap=cm.jet, vmin=summery[0], vmax=summery[2], alpha=1.0)
        axis('equal')
        grid()
        colorbar()
        title('Distance')
        xlabel('X Axis')
        ylabel('Y Axis')
        show()
        
    # create error plot
    def createDeviationPlot(self, points, spotSize):
        x = []
        y = []
        area = []
        colour = []
        axisRange = [0,0,0,0]
        colourRange = [0,0]
        first = True
        for i in range(len(points)):
            x.append(points[i].floatXPoint)
            y.append(points[i].floatYPoint)
            area.append(spotSize)
            colour.append(points[i].deviation)
            if first:
                axisRange = [points[i].floatXPoint, points[i].floatXPoint,points[i].floatYPoint,points[i].floatYPoint]
                colourRange = [points[i].deviation, points[i].deviation]
                first = False
            else:
                if axisRange[0] > points[i].floatXPoint:
                    axisRange[0] = points[i].floatXPoint
                elif axisRange[1] < points[i].floatXPoint:
                    axisRange[1] = points[i].floatXPoint
                
                if axisRange[2] > points[i].floatYPoint:
                    axisRange[2] = points[i].floatYPoint
                elif axisRange[3] < points[i].floatYPoint:
                    axisRange[3] = points[i].floatYPoint
                    
                if colourRange[0] > points[i].deviation:
                    colourRange[0] = points[i].deviation
                elif colourRange[1] < points[i].deviation:
                    colourRange[1] = points[i].deviation
        
        
        # Flip Y Axis
        yOutput = []
        for i in range(len(y)):
            yOutput.append((axisRange[3]-y[i])+axisRange[2])
        
        figure(num=None, dpi=200)
        scatter(x, yOutput, s=area, c=colour, marker='o', cmap=cm.jet, vmin=colourRange[0], vmax=colourRange[1], alpha=1.0)
        axis('equal')
        grid()
        colorbar()
        title('Deviation')
        xlabel('X Axis')
        ylabel('Y Axis')
        show()
        
    def createPlot(self, points, summery, filepath, fileFormat, spotSize, plotsOutput):
        
        
        x = []
        y = []
        area = []
        colourDis = []
        colourDev = []
        colourMeasure = []
        colourWinSize = []
        axisRange = [0,0,0,0]
        colourRangeDis = [0,0]
        colourRangeDev = [0,0]
        colourRangeMeasure = [0,0]
        colourRangeWinSize = [0,0]
        first = True
        for i in range(len(points)):
            x.append(points[i].floatXPoint)
            y.append(points[i].floatYPoint)
            area.append(spotSize)
            colourDis.append(points[i].distance)
            colourDev.append(points[i].deviation)
            colourMeasure.append(points[i].measureValue)
            colourWinSize.append(points[i].winSize)
            if first:
                axisRange = [points[i].floatXPoint, points[i].floatXPoint,points[i].floatYPoint,points[i].floatYPoint]
                colourRangeDis = [points[i].distance, points[i].distance]
                colourRangeDev = [points[i].deviation, points[i].deviation]
                colourRangeMeasure = [points[i].measureValue, points[i].measureValue]
                colourRangeWinSize = [points[i].winSize, points[i].winSize]
                first = False
            else:
                if axisRange[0] > points[i].floatXPoint:
                    axisRange[0] = points[i].floatXPoint
                elif axisRange[1] < points[i].floatXPoint:
                    axisRange[1] = points[i].floatXPoint
                
                if axisRange[2] > points[i].floatYPoint:
                    axisRange[2] = points[i].floatYPoint
                elif axisRange[3] < points[i].floatYPoint:
                    axisRange[3] = points[i].floatYPoint
                
                if colourRangeDis[0] > points[i].distance:
                    colourRangeDis[0] = points[i].distance
                elif colourRangeDis[1] < points[i].distance:
                    colourRangeDis[1] = points[i].distance
                
                if colourRangeDev[0] > points[i].deviation:
                    colourRangeDev[0] = points[i].deviation
                elif colourRangeDev[1] < points[i].deviation:
                    colourRangeDev[1] = points[i].deviation
                    
                if colourRangeMeasure[0] > points[i].measureValue:
                    colourRangeMeasure[0] = points[i].measureValue
                elif colourRangeMeasure[1] < points[i].measureValue:
                    colourRangeMeasure[1] = points[i].measureValue
                
                if colourRangeWinSize[0] > points[i].winSize:
                    colourRangeWinSize[0] = points[i].winSize
                elif colourRangeWinSize[1] < points[i].winSize:
                    colourRangeWinSize[1] = points[i].winSize
        
        axisRange[0] = axisRange[0] - 10
        axisRange[1] = axisRange[1] + 10
        axisRange[2] = axisRange[2] - 10
        axisRange[3] = axisRange[3] + 10
        
        textSummery = 'Mean = ' + str(summery[1]) +' Standard Deviation = ' + str(summery[3])
        
        # Flip Y Axis
        yOutput = []
        for i in range(len(y)):
            yOutput.append((axisRange[3]-y[i])+axisRange[2])
        
        #pdb.set_trace()
        
        if plotsOutput[0] == 1:
            print 'Distance Range: [', colourRangeDis[0], ', ', colourRangeDis[1], ']'
            fig = figure(num=None, dpi=200)
            filepath_output = filepath + '_distance.png'
            if (colourRangeDis[0] - colourRangeDis[1]) == 0:
                scatter(x, yOutput, s=area, c='blue', marker='o', alpha=1.0)
            else:
                scatter(x, yOutput, s=area, c=colourDis, marker='o', cmap=cm.jet, vmin=colourRangeDis[0], vmax=colourRangeDis[1], alpha=1.0)
                colorbar()
            axis('scaled')
            axis(axisRange)
            title('Distance from Correct Position')
            xlabel(textSummery)
            savefig(filepath_output, format=fileFormat)
            close(fig)
            del fig, filepath_output, colourRangeDis, colourDis
        
        if plotsOutput[1] == 1:
            print 'Deviation Range: [', colourRangeDev[0], ', ', colourRangeDev[1], ']'
            fig = figure(num=None, dpi=200)
            filepath_output = filepath + '_deviation.png'
            if (colourRangeDev[0] - colourRangeDev[1]) == 0:
                scatter(x, yOutput, s=area, c='blue', marker='o', alpha=1.0)
            else:
                scatter(x, yOutput, s=area, c=colourDev, marker='o', cmap=cm.jet, vmin=colourRangeDev[0], vmax=colourRangeDev[1], alpha=1.0)
                colorbar()
            axis('scaled')
            axis(axisRange)
            title('Deviation from Mean')
            xlabel(textSummery)
            savefig(filepath_output, format=fileFormat)
            close(fig)
            del fig, filepath_output, colourRangeDev, colourDev
        
        if plotsOutput[2] == 1:
            print 'Measure Range: [', colourRangeMeasure[0], ', ', colourRangeMeasure[1], ']'
            fig = figure(num=None, dpi=200)
            filepath_output = filepath + '_measure.png'
            if (colourRangeMeasure[0] - colourRangeMeasure[1]) == 0:
                scatter(x, yOutput, s=area, c='blue', marker='o', alpha=1.0)
            else:
                scatter(x, yOutput, s=area, c=colourMeasure, marker='o', cmap=cm.jet, vmin=colourRangeMeasure[0], vmax=colourRangeMeasure[1], alpha=1.0)
                colorbar()
            axis('scaled')
            axis(axisRange)
            title('Similarity Measure Value')
            savefig(filepath_output, format=fileFormat)
            close(fig)
            del fig, filepath_output, colourRangeMeasure, colourMeasure
        
        if plotsOutput[3] == 1:
            print 'Window Size Range: [', colourRangeWinSize[0], ', ', colourRangeWinSize[1], ']'
            fig = figure(num=None, dpi=200)
            filepath_output = filepath + '_winsize.png'
            if (colourRangeWinSize[0] - colourRangeWinSize[1]) == 0:
                scatter(x, yOutput, s=area, c='blue', marker='o', alpha=1.0)
            else:
                scatter(x, yOutput, s=area, c=colourWinSize, marker='o', cmap=cm.jet, vmin=colourRangeWinSize[0], vmax=colourRangeWinSize[1], alpha=1.0)
                colorbar()
            axis('scaled')
            axis(axisRange)
            title('Window Size')
            savefig(filepath_output, format=fileFormat)
            close(fig)
            del fig, filepath_output, colourRangeWinSize, colourWinSize
        
        close('all')
        del x, y, yOutput, area
        gc.collect()
        
    
    # Contains the main execution order of the class
    def run(self, refPoints, regPoints, filepath, fileFormat, spotSize, plotsOutput):
        
        refCtrlPts = list()
        regCtrlPts = list()
        #print 'Created Lists'
        
        # Get file paths
        try:
            refFile = self.openFile4Read(refPoints) 
            regFile = self.openFile4Read(regPoints)
        except IOError, e:
            print '\nCould not open file:\n', e
            return
        #print 'Read in images'
        
        # Read and parse each file
        self.parseControlPointsFile(refFile, refCtrlPts, True)
        #print 'Parsed Reference File'
        self.parseControlPointsFile(regFile, regCtrlPts, False)
        #print 'Parsed Registration File'
        
        # Close Files
        try:
            refFile.close()
            regFile.close()
        except IOError, e:
            print '\nCould not close file.\n', e
            return
        #print 'Closed Files'
        
        # Summerize 
        summery = self.summerizeCtrlPts(refCtrlPts, regCtrlPts)
        #print 'Summerized Dataset'
        
        if summery[0] != -1:
            # Generate Error Plot
            self.createPlot(regCtrlPts, summery, filepath, fileFormat, spotSize, plotsOutput)
            #print 'Generated Plot'
        
        del refCtrlPts
        del regCtrlPts
        
        gc.collect()
        #print 'Del Lists'
        return summery
        

# If run for the command line create instance and run!
if __name__ == '__main__':
    refPointsIn = '/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_sin5warpX_ctrlpts.pts'
    regPointsIn = '/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_HyMap_XSin5Warp_image2image.pts'
    obj = CompareCtrlPts()
    obj.run(refPointsIn, regPointsIn, '/Users/pete/Desktop/plot_', 'png', 30)
