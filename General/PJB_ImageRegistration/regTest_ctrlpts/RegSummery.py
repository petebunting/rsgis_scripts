#! /usr/bin/env python

class Summery (object):
    'Represents the summery of the registration tests'
    title = 'hello'
    min = 0
    max = 0
    mean = 0
    stddev = 0
    
    def createSummery(self, line):
    
        line.lstrip()
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
