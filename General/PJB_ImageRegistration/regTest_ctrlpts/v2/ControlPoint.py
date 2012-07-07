#! /usr/bin/env python

id = 0

tab = '\t'

class ControlPoint (object):
    "A Class Representing a Control Point"
    refXPoint = 0
    refYPoint = 0
    floatXPoint = 0
    floatYPoint = 0
    deviation = 0
    distance = 0
    winSize = 0
    pxlRes = 0
    perRange = 0
    measureValue = 0
    
    def setID(self, newID):
        id = newID
    
    def setRefXPoint(self, point):
        self.refXPoint = point
    
    def setRefYPoint(self, point):
        self.refYPoint = point
        
    def setfFoatXPoint(self, point):
        self.FloatXPoint = point
        
    def setfFoatYPoint(self, point):
        self.FloatYPoint = point
        
    def setDeviation(self, num):
        self.deviation = num
        
    def getID(self):
        return id
    
    def getRefXPoint(self):
        return refXPoint
    
    def getRefYPoint(self):
        return refYPoint
    
    def getFloatXPoint(self):
        return floatXPoint
    
    def getFloatYPoint(self):
        return floatYPoint
     
    def getDeviation(self):
        return deviation
    
    def printControlPoint(self):
        print 'Control Point: '
        
    def createCtrlPtTxt(self, pointID, line):
        #print pointID, ': ', line
        id = pointID
        line.lstrip()
        str = ''
        counter = 0;
        for i in range(len(line)):
            if line[i] == tab:
                if counter == 1:
                    self.refXPoint = float(str)
                elif counter == 2:
                    self.refYPoint = float(str)
                elif counter == 3:
                    self.floatXPoint = float(str)
                elif counter == 4:
                    self.floatYPoint = float(str)
                elif counter == 5:
                    self.winSize = float(str)
                elif counter == 6:
                    self.pxlSize = float(str)
                elif counter == 7:
                    self.perRange = float(str)
                str = ''
                counter = counter + 1
            else:
                str = str +line[i]
        if str != '':
            #print '\'', str.strip(), '\''
            self.measureValue = float(str)
            
    def createCtrlPt(self, pointID, line):
        #print pointID, ': ', line
        id = pointID
        line.lstrip()
        str = ''
        counter = 0;
        for i in range(len(line)):
            if line[i] == tab:
                if counter == 1:
                    self.refXPoint = float(str)
                elif counter == 2:
                    self.refYPoint = float(str)
                elif counter == 3:
                    self.floatXPoint = float(str)
                str = ''
                counter = counter + 1
            else:
                str = str +line[i]
        self.floatYPoint = float(str)
    


