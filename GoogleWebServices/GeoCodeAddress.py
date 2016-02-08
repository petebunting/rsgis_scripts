import urllib
import urllib.request
import json
from io import StringIO

urlBase = 'https://maps.googleapis.com/maps/api/geocode/json?address='
urlKey = '&key=AIzaSyC636iQ3STxH2zEGIu5M4b-pOhe5J3z5d0'

inFile = '2016_students_with_term_add.csv'
outFile = '2016_students_with_term_add_locs.csv'
outErrFile = '2016_students_with_term_add_locsErrs.txt'

outCSV = open(outFile, 'w')
outErr = open(outErrFile, 'w')
inCSV = open(inFile)
counter = 0
for line in inCSV:
    if counter == 0:
        outline = line.strip()
        outline = outline + ',Lat,Lon\n'
        outCSV.write(outline)
                
    elif counter > 0:
        vars = line.split(',')
        #print(vars[0].strip() + ":\t" + vars[14].strip() + "; " + vars[15].strip() + "; " + vars[16].strip()+ "; " + vars[17].strip() + "; " + vars[18].strip())
        
        idxs = [14,15,16,17,18]
        address = ""
        first = True
        for i in idxs:
            val = vars[i].strip()
            if not val is "":
                if first:
                    address = val
                    first = False
                else:
                    address = address + " " + val
        try:
            lat = 52.4209036
            lon = -4.0640616
            if address.count('Cwrt Mawr') > 0:
                address = 'Cwrt Mawr Aberystwyth'
            elif address.count('Fferm Penglais') > 0:
                address = 'Fferm Penglais Aberystwyth'
            elif address.count('Gwalia Residences') > 0:
                 address = 'Gwalia Residences Aberystwyth'
            elif address.count('Trefloyne') > 0:
                 address = 'Trefloyne Aberystwyth'
            elif address.count('Pentre Jane Morgan') > 0:
                 address = 'Pentre Jane Morgan Aberystwyth'
            else:       
                addressURL = address.replace(' ', '+')
                print(vars[0].strip() + ": " + addressURL)
                
                url = urlBase + addressURL + urlKey
                print(url)
                req = urllib.request.Request(url)
                resp = urllib.request.urlopen(req)
                io = StringIO(resp.read().decode("utf-8"))
                jsonData = json.load(io)
                #print(json.dumps(jsonData))
                status = json.dumps(jsonData['status'])
    
                if status == '"OK"':
                    print(json.dumps(jsonData['results'][0]['geometry']['location'], sort_keys=True, indent=1))
        
                    lat = jsonData['results'][0]['geometry']['location']['lat']
                    lon = jsonData['results'][0]['geometry']['location']['lng']
                else:
                    print("ERROR")
                    outErr.write(vars[0].strip()+'\n')
            
            outline = line.strip()
            outline = outline + ',' + str(lat) + ',' + str(lon) + '\n'
            outCSV.write(outline)
        except:
            outErr.write(vars[0].strip()+'\n')   
        #if counter > 10:
        #    break
    counter = counter + 1
        
outCSV.flush()
outCSV.close()

outErr.flush()
outErr.close()
    


