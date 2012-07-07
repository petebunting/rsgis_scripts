#! /usr/bin/env python

class Summery (object):
    'Represents the summery of the registration tests'
    title = 'hello'
    min = 0
    max = 0
    mean = 0
    stddev = 0
    
    def createSummery(self, line):
        #print 'Line = ', line
        #print 'line[0]', line[0]
        line.strip()
        str = ''
        counter = 0;
        for i in range(len(line)):
            if line[i] == ',':
                if counter == 0:
                    self.title = str.strip()
                elif counter == 1:
                    self.min = float(str.strip())
                elif counter == 2:
                    self.mean = float(str.strip())
                elif counter == 3:
                    self.max = float(str.strip())
                str = ''
                counter = counter + 1
            else:
                str = str +line[i]
        self.stddev = float(str.strip())
    
    
    def createSummery(self, summeryArray, summeryTitle):
        self.title = summeryTitle
        self.min = summeryArray[0]
        self.mean = summeryArray[1]
        self.max = summeryArray[2]
        self.stddev = summeryArray[3]
    
    def toString(self):
        strOut = '' + self.title + ',' + str(self.min) + ',' + str(self.mean) + ',' + str(self.max) + ',' + str(self.stddev) + '\n'
        return strOut
        
