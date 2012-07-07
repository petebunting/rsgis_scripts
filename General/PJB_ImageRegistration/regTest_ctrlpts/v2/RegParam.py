#! /usr/bin/env python

comma = ','

class RegistrationParameter (object):
    "A Class Representing a registration summerize parameters"
    reference_file = ''
    registration_base = ''
    
    def createParamFromLine(self, line):
        strippedLine = line.strip()
        str = ''
        counter = 0;
        for i in range(len(line)):
            if line[i] == comma:
                if counter == 0:
                    self.reference_file = str.strip()
                str = ''
                counter = counter + 1
            else:
                str = str +line[i]
        self.registration_base = str.strip()
    
