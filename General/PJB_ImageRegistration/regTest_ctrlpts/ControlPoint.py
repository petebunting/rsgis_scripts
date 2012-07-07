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
                    #print 'REF X Point: ', self.refXPoint
                elif counter == 2:
                    self.refYPoint = float(str)
                    #print 'REF Y Point: ', self.refYPoint
                elif counter == 3:
                    self.floatXPoint = float(str)
                    #print 'FLOAT X Point: ', self.floatXPoint
                str = ''
                counter = counter + 1
            else:
                str = str +line[i]
        self.floatYPoint = float(str)
        #print 'FLOAT Y Point: ', self.floatYPoint
