#! /usr/bin/env python

#######################################
# Class for storing the parameters
# associated with an ALOS scene for
# constucting the standard file name.
#
# Author: Pete Bunting
# Email: pete.bunting@aber.ac.uk
# Date: 07/04/2008
# Version: 1.0
#######################################

comma = ','

class ALOSParams (object):
    scnid = 'ALPSRP000000000'
    prod_ID = 'A0000000-000'
    opemd = 'XXX'
    scn_cdate = 'YYYYMMDD'
    scn_clat = -1
    scn_clon = -1
    offnadir = -1
    level = -1
    
    def __init__(self):
        self.scnid = 'ALPSRP000000000'
        self.prod_ID = 'A0000000-000'
        self.opemd = 'XXX'
        self.scn_cdate = 'YYYYMMDD'
        self.scn_clat = -1
        self.scn_clon = -1
        self.offnadir = -1
        self.level = -1
        
    def getScnID(self):
        return self.scnid
        
    def getProdID(self):
        return self.prod_ID
    
    def getOpeMD(self):
        return self.opemd
        
    def getScnCDate(self):
        return self.scn_cdate
    
    def getScnCLat(self):
        return self.scn_clat
        
    def getScnCLon(self):
        return self.scn_clon
        
    def getOffNadir(self):
        return self.offnadir
    
    def getLevel(self):
        return self.level
        
    def getStrLat(self):
        dec = False
        neg = False
        count = 0
        countdec = 0
        strLat = str(self.scn_clat)
        outstr = ''
        for i in range(len(strLat)):
            #print 'strLat[' + str(i) + ']: ' + strLat[i] + ' - Count: ' + str(count) + ' - outstr: ' + outstr
            if strLat[i] == '-':
                neg = True
                #do nothing
            elif strLat[i] == '.':
                dec = True
                #do nothing
            else:
                outstr = outstr + strLat[i]
                count = count + 1
                if dec:
                    countdec = countdec + 1
                if count > 3 or countdec > 0:
                    break
        return outstr
        
    def getStrLong(self):
        dec = False
        neg = False
        count = 0
        countdec = 0
        strLon = str(self.scn_clon)
        outstr = ''
        for i in range(len(strLon)):
            #print 'strLat[' + str(i) + ']: ' + strLon[i] + ' - Count: ' + str(count) + ' - outstr: ' + outstr
            if strLon[i] == '-':
                neg = True
                #do nothing
            elif strLon[i] == '.':
                dec = True
                #do nothing
            else:
                outstr = outstr + strLon[i]
                count = count + 1
                if dec:
                    countdec = countdec + 1
                if count > 3 or countdec > 0:
                    break
        return outstr
    
    def getDateStr(self):
        year = ''
        month = ''
        day = ''
        counter = 0
        str = ''
        for i in range(len(self.scn_cdate)):
            if self.scn_cdate[i] == '/':
                if counter == 0:
                    day = str.strip()
                elif counter == 1:
                    month = str.strip()
                str = ''
                counter = counter + 1
            else:
                str = str +self.scn_cdate[i]
        year = str.strip()
        
        if len(day) == 1:
            day = '0' + day
        if len(month) == 1:
            month = '0' + month
        if len(year) == 2:
            year = '20' + year
        return year+month+day
    
    def getOffNadirStr(self):
        return str(int(self.offnadir))
    
    def sameScnID(self, sceneID):
        count = self.scnid.count(sceneID)
        #print 'self.scnid: ' + self.scnid 
        #print 'sceneID: ' + sceneID
        #print 'count: ' + str(count)
        if count > 0:
            return True
        return False
        
        
    def sameProdID(self, productID):
        count = self.prod_ID.count(productID)
        #print 'self.scnid: ' + self.scnid 
        #print 'productID: ' + productID
        #print 'count: ' + str(count)
        if count > 0:
            return True
        return False
    
    def createData(self, line):
        strVar = ''
        counter = 0;
        for i in range(len(line)):
            if line[i] == comma:
                if counter == 0:
                    self.scnid = strVar.strip()
                elif counter == 1:
                    self.prod_ID = strVar.strip()
                elif counter == 2:
                    self.opemd = strVar.strip()
                elif counter == 3:
                    self.scn_cdate = strVar.strip()
                elif counter == 4:
                    self.scn_clat = float(strVar.strip())
                elif counter == 5:
                    self.scn_clon = float(strVar.strip())
                elif counter == 6:
                    self.offnadir = float(strVar.strip())
                strVar = ''
                counter = counter + 1
            else:
                strVar = strVar +line[i]
        self.level = float(strVar.strip())
    
    def toString(self):
        outStr = self.scnid + ', ' + self.prod_ID + ', ' + self.opemd + ', ' + self.scn_cdate + ', ' + str(self.scn_clat) + ', ' + str(self.scn_clon) + ', ' + str(self.offnadir) + ', ' + str(self.level)
        return outStr
    