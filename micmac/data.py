#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 11:48:13 2018

@author: ciaranrobb

Edit and output a C-Astral 'corrected' array for use with MicMac 

The error GNSS is normally so miniscule that arguably it doesn't matter a huge amount
but for the sake of completness...

C-Astral are dependent on commercial software for the above which is annoying,
plus there own program only works in Windows (lame)

This is a bit of kludge at the moment to be refined...
"""

import numpy as np
import pandas as pd
import os
from glob2 import glob

import piexif
import glob2
from os import path

from PIL import Image
from joblib import Parallel, delayed


def convert_c3p(lognm):
    
    """
    Edit csv file for c3p to work with MicMac.
    
    This assumes the column order is name, x, y, z, yaw, pitch, roll
    
    Parameters
    ----------  
    
    lognm : string
            path to c3p derived csv file
    
                           
    """

    # must be read as an object as we are dealing with strings and numbers
    npCsv = np.loadtxt(lognm, dtype='object')
    
    
    # get rid of the first columns consisting number 1
    npCsv = npCsv[:,1:len(npCsv)]
    
    # so columns are now image, x,y,z,error, time,date, yaw,pitch,roll,ypr
    # only need index 0:4 and 
    
    npCsv = np.hstack((npCsv[:,0:4], npCsv[:, 7:10]))
    
    # header for MicMac     
    hdr = ["#F=N", "X", "Y", "Z", "K", "W", "P"]
    
    dF = pd.DataFrame(npCsv)
    
    edNm = lognm[:-4]+'_edited.csv'
    
    dF.to_csv(edNm, sep=' ', index=False, header=hdr)       
       
def remove_prefix(folder, prefix):
    
    """
    Remove pointless file prefix on C3p jpgs. 
    
    Parameters
    ----------  
    
    folder : string
             path to folder containing jpgs
             
    prefix : string
             prefix to remove from jpg files
                           
    """
    
    fileList = glob(os.path.join(folder,'*.JPG'))
    
    for file in fileList:
        new = file.replace(prefix, '', 1)
        os.rename(file, new)
        



def focalen_exif(folder):
    
    """
    Add focal info to exif for MicMac.
    MicMac also has a tool for this - just in case it doesnt work
    
    Parameters
    ----------  
    
    folder : string
             path to folder containing jpgs
             
                           
    """
    
    fileList = glob2.glob(path.join(folder, '*.JPG'))
    
    def _ed_ppx_exif(fle):
        
        img = Image.open(fle)
        
       # w, h = img.size
        
        exif_dict = piexif.load(img.info['exif'])
    #    
    #    exif_dict['Exif'][piexif.ImageIFD.XResolution] = (w, 1)
    #    exif_dict['Exif'][piexif.ImageIFD.YResolution] = (h, 1)
        
        # multiply by 1.5 to get 35mm equiv apparently (based on googling)
        exif_dict['Exif'][piexif.ExifIFD.FocalLength]=(16, 30)
        
        
        exif_dict['Exif'][piexif.ExifIFD.FocalLengthIn35mmFilm]=(24,45)
        # if it was 30 as matej said
    #    exif_dict['Exif'][piexif.ExifIFD.FocalLengthIn35mmFilm]=(24,45)
        
    #    exif_dict["1st"][piexif.ImageIFD.XResolution] = (w, 1)
    #    exif_dict["1st"][piexif.ImageIFD.YResolution] = (h, 1)
    #
    #    exif_dict["1st"][piexif.ExifIFD.FocalLength]=(50, 5)
    #    
    #    exif_dict["1st"][piexif.ExifIFD.FocalLengthIn35mmFilm]=(75,10)
        
        exif_bytes = piexif.dump(exif_dict)
        
        piexif.insert(exif_bytes, fle)

    Parallel(n_jobs=-1,verbose=5)(delayed(_ed_ppx_exif)(file) for file in fileList)