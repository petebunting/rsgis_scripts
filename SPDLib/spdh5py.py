import h5py
import numpy as np
from xml.dom.minidom import parseString


class SPDReader:
    """
    Some methods to read SPD files
    """

    def __init__(self,infile):
        self.f = h5py.File(infile, 'r')   


    def closeSPDFile(self):
        """
        Close the SPD header
        """
        self.f.close()
        

    def readSPDHeader(self):
        """
        Read the SPD header
        """
        dictn = {}
        for name,obj in self.f['HEADER'].items():
            if obj[()].size == 1:
                dictn[name] = obj[0]
            else:
                dictn[name] = obj[()]
        return dictn


    def readSPDPulsesRow(self,row,fieldName=None):
        """
        Read a row of pulse data
        """
        cnt = self.f['INDEX']['PLS_PER_BIN'][row]
        if cnt.any():
            idx = self.f['INDEX']['BIN_OFFSETS'][row]
            if fieldName is None:
                pData = self.f['DATA']['PULSES'][idx[0]:idx[-1]+cnt[-1]]
            else:
                pData = self.f['DATA']['PULSES'][idx[0]:idx[-1]+cnt[-1],fieldName]
            return pData.view(np.recarray)
        else:
            return None


    def readSPDPointsRow(self,row,fieldName=None):
        """
        Read a row of point data
        """
        cnt = self.f['INDEX']['PLS_PER_BIN'][row]
        if cnt.any():
            idx = self.f['INDEX']['BIN_OFFSETS'][row]       
            pData = self.f['DATA']['PULSES'][idx[0]:idx[-1]+cnt[-1],'PTS_START_IDX','NUMBER_OF_RETURNS']
            start = pData['PTS_START_IDX'][0]
            finish = pData['PTS_START_IDX'][-1] + pData['NUMBER_OF_RETURNS'][-1]
            if fieldName is None:
                points = self.f['DATA']['POINTS'][start:finish]
            else:
                points = self.f['DATA']['POINTS'][start:finish,fieldName]
            return points.view(np.recarray)
        else:
            return None


    def readSPDOriginRow(self,row):
        """
        Read a row of point data
        """
        cnt = self.f['INDEX']['PLS_PER_BIN'][row]
        if cnt.any():
            idx = self.f['INDEX']['BIN_OFFSETS'][row]       
            pData = self.f['DATA']['PULSES'][idx[0]:idx[-1]+cnt[-1],'X_ORIGIN','Y_ORIGIN','Z_ORIGIN','NUMBER_OF_RETURNS']
            return pData.view(np.recarray)
        else:
            return None


    def readSPDXYZRow(self,row,returnType=None):
        """
        Read a row of XYZ point data
        ReturnType:
            1 = first returns
            2 = middle returns
            3 = last returns
            otherwise all returns
        """
        cnt = self.f['INDEX']['PLS_PER_BIN'][row]
        if cnt.any():
            idx = self.f['INDEX']['BIN_OFFSETS'][row]       
            pData = self.f['DATA']['PULSES'][idx[0]:idx[-1]+cnt[-1],'PTS_START_IDX','NUMBER_OF_RETURNS']
            start = pData['PTS_START_IDX'][0]
            finish = pData['PTS_START_IDX'][-1] + pData['NUMBER_OF_RETURNS'][-1]
            points = self.f['DATA']['POINTS'][start:finish,'X','Y','Z']
            if returnType == 1:
                idx = pData['PTS_START_IDX'] - pData['PTS_START_IDX'][0]
                mask = pData['NUMBER_OF_RETURNS'] > 0
                points = points[idx[mask]]
            elif returnType == 2:
                idx = np.ones(points.size)
                mask = pData['NUMBER_OF_RETURNS'] > 0
                idx[pData['PTS_START_IDX'][mask] - pData['PTS_START_IDX'][mask][0]] = 0
                idx[pData['PTS_START_IDX'][mask] - pData['PTS_START_IDX'][mask][0] + pData['NUMBER_OF_RETURNS'] - 1] = 0
                points = points[idx > 0]
            elif returnType == 3:
                idx = pData['PTS_START_IDX'] - pData['PTS_START_IDX'][0] + pData['NUMBER_OF_RETURNS'] - 1
                mask = pData['NUMBER_OF_RETURNS'] > 0
                points = points[idx[mask]]
            return points.view(np.recarray)
        else:
            return None



class SPDWriter:
    """
    Some methods to write SPD files
    """

    def __init__(self,infile):
        self.f = h5py.File(infile, 'a')


    def closeSPDFile(self):
        """
        Close the SPD header
        """
        self.f.close()


#    def writeHeightFromPlane(self,p):
#        """
#        Calculate and write point heights above a user defined plane        
#        p is an array of three plane coefficients
#        """
#        for row in range(self.f['HEADER']['NUMBER_BINS_Y'][0]):
#            cnt = self.f['INDEX']['PLS_PER_BIN'][row]
#            if cnt.any():
#                idx = self.f['INDEX']['BIN_OFFSETS'][row]
#                pData = self.f['DATA']['PULSES'][idx[0]:idx[-1]+cnt[-1],'PTS_START_IDX','NUMBER_OF_RETURNS','X_ORIGIN','Y_ORIGIN','Z_ORIGIN']
#                start = pData['PTS_START_IDX'][0]
#                finish = pData['PTS_START_IDX'][-1] + pData['NUMBER_OF_RETURNS'][-1]
#                if start < finish:
#                    points = self.f['DATA']['POINTS'][start:finish]
#                    points['HEIGHT'] = (points['Z']-pData['Z_ORIGIN'][pData['NUMBER_OF_RETURNS']>0]) - p[0] * (points['X']-pData['X_ORIGIN'][pData['NUMBER_OF_RETURNS']>0]) + p[1] * (points['Y']-pData['Y_ORIGIN'][pData['NUMBER_OF_RETURNS']>0]) - p[2]
#                    self.f['DATA']['POINTS'][start:finish] = points
        

    def writeHeightFromPlane(self,p):
        """
        Calculate and write point heights above a user defined plane        
        p is an array of three plane coefficients
        """
        for row in range(self.f['HEADER']['NUMBER_BINS_Y'][0]):
            cnt = self.f['INDEX']['PLS_PER_BIN'][row]
            if cnt.any():
                idx = self.f['INDEX']['BIN_OFFSETS'][row]
                pData = self.f['DATA']['PULSES'][idx[0]:idx[-1]+cnt[-1],'PTS_START_IDX','NUMBER_OF_RETURNS']
                start = pData['PTS_START_IDX'][0]
                finish = pData['PTS_START_IDX'][-1] + pData['NUMBER_OF_RETURNS'][-1]
                points = self.f['DATA']['POINTS'][start:finish]
                points['HEIGHT'] = points['Z'] - (p[0] * points['X'] + p[1] * points['Y'] + p[2])
                self.f['DATA']['POINTS'][start:finish] = points

    
    def writeSPDHeaderField(self,field,value):
        """
        Write an SPD header field
        """
        self.f['HEADER'][field][()] = value
        
