import sys
import string
import re

inFileName = sys.argv[1].strip()
outFileName = sys.argv[2].strip()

parFile = open(inFileName, 'r') 
outFile = open(outFileName, 'w')

i = 0

for eachLine in parFile:
    if(i == 0):
        # write out header row
        header = 'region,family_n,latitude,longitud,latitudeDMS, longitudeDMS,houseid,location_id,village_code,hh_number,inter_date' + '\n'
        outFile.write(header)
    
    else:
        count = eachLine.count(',')
        elements = eachLine.split(',', count)
        
        elements[0] = elements[0].strip()
        elements[1] = elements[1].strip()
        elements[2] = elements[2].strip()
        elements[3] = elements[3].strip()
        elements[4] = elements[4].strip()
        elements[5] = elements[5].strip()
        elements[6] = elements[6].strip()
        elements[7] = elements[7].strip()
        elements[8] = elements[8].strip()
    
        region = elements[0]
        family_n = elements[1]
        latitude = elements[2] 
        longitude = elements[3]
        houseid = elements[4] 
        location_id = elements[5]
        village_code = elements[6] 
        hh_number = elements[7] 
        inter_date = elements[8]
        

        if(latitude == ''):
            latitudeDMS = ''
            longitudeDMS = ''  
            
        elif(longitude == ''):
            latitudeDMS = ''
            longitudeDMS = ''   
        
        else:
            # Split based on decimal point
            
            ### CONVERT LATITUDE ###
            # DEGREES
            latitudeElements = latitude.split('.', 1)
            degrees = latitudeElements[0]
            #latitudeAFloat = float(degrees)
            latitudeBFloat = float('.' + latitudeElements[1])
            
            # MINUTES
            latitudeBFloatA = latitudeBFloat * 60 # part after decimal * 60

            latitudeBFloatAString = str(latitudeBFloatA)
            latitudeElements2 = latitudeBFloatAString.split('.', 1)
            minutes = latitudeElements2[0]
            
            # SECONDS
            latitudeElements2 = latitudeBFloatAString.split('.', 1)
            latitudeAFloat2 = float(latitudeElements2[0])
            latitudeBFloat2 = float('.' + latitudeElements2[1])
            
            latitudeBFloatB = latitudeBFloat2 * 60
            seconds = str(latitudeBFloatB)
            
            latitudeDMS = degrees + '\'' + minutes + '\'' + seconds + '"'
           #print 'Lat DMS = ' + latidudeDMS
           
            ### CONVERT LONGDITUDE ###
            # DEGREES
            longitudeElements = longitude.split('.', 1)
            degrees = longitudeElements[0]
            #longitudeAFloat = float(degrees)
            longitudeBFloat = float('.' + longitudeElements[1])
            
            # MINUTES
            longitudeBFloatA = longitudeBFloat * 60 # part after decimal * 60

            longitudeBFloatAString = str(longitudeBFloatA)
            longitudeElements2 = longitudeBFloatAString.split('.', 1)
            minutes = longitudeElements2[0]
            
            # SECONDS
            longitudeElements2 = longitudeBFloatAString.split('.', 1)
            longitudeAFloat2 = float(longitudeElements2[0])
            longitudeBFloat2 = float('.' + longitudeElements2[1])
            
            longitudeBFloatB = longitudeBFloat2 * 60
            seconds = str(longitudeBFloatB)
            
            longitudeDMS = degrees + '\'' + minutes + '\'' + seconds + '"'
            
        # WRITE TO OUTPUT TEXT FILE
        outline = region + ',' + family_n + ',' +  latitude + ',' + longitude + ',' + latitudeDMS + ',' + longitudeDMS + ',' + houseid + ',' + location_id + ',' + village_code + ',' + hh_number + ',' + inter_date + '\n'
        #print outline
        outFile.write(outline)
             
    i = i + 1

parFile.close()
outFile.close()