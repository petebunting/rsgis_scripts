#####################################################
## NAME: segment
## Source Name: segment.py
## Author: Peter Bunting
## Email: pjb00@aber.ac.uk
## Usage: 
## Description:  
## Date: 21 June 2007
## Updated: 21 June 2007
#####################################################

import sys
import os
import string
import imghdr
import Image

class segment (object):

    def performSegmentation(self, segmentLocation, sigma, k, min, inputDIR, outputDIR, tmpDIR, filename, printOut):
        filenameSplit = filename.split('.', 2)
        printOut.printMessage('filenameSplit: '+str(filenameSplit))
        if len(filenameSplit) == 2:
            if filenameSplit[1] == 'jpg':
                printOut.printMessage('SEGMENT!')
                imageType = imghdr.what(inputDIR+'\\'+filename)
                printOut.printMessage('Image Type: '+str(imageType))
                imageFile = inputDIR+filename
                if not imageType == 'ppm':
                    printOut.printMessage('Image needs conversion!')
                    im = Image.open(inputDIR+'\\'+filename)
                    im.save(tmpDIR+'\\tmp.ppm', 'ppm')
                    imageFile = tmpDIR + '\\tmp.ppm'
                command = segmentLocation + '\\segment ' + str(sigma) + ' ' + str(k) + ' ' + str(min) + ' ' + imageFile + ' ' + tmpDIR+'\\tmp_output.ppm'
                printOut.printMessage('Running: ' + command)
                os.system(command)
                printOut.printMessage('Finished Segmentation..')
                outFileName = outputDIR + '\\' + filenameSplit[0] + '_segment.png'
                printOut.printMessage('Output File Name: ' + outFileName)
                im = Image.open(tmpDIR+'\\tmp_output.ppm')
                im.save(outFileName)
                os.remove(tmpDIR+'\\tmp_output.ppm')
                os.remove(tmpDIR+'\\tmp.ppm')

        
    def segmentDir(self, segmentLocation, sigma, k, min, inputDIR, outputDIR, tmpDIR):
        print 'Working directory: '+inputDIR
        fileList = os.listdir(inputDIR)
        print fileList
        for filename in fileList:
            print 'filename: '+filename
            self.performSegmentation(segmentLocation, sigma, k, min, inputDIR, outputDIR, tmpDIR, filename, self)
    
    def printMessage(self, outText):
    	print outText
    	
    def run(self):
        usrSegmentDIR = "D:\\segmentation\\segment\\segment"
        usrSigma = "0.5"
        usrK = "500"
        usrMin = "20"
        usrInputDIR = "D:\\segmentation\\images"
        usrOutputDIR = "D:\\segmentation\\images\\output"
        tmpOutputDIR = "D:\\segmentation\\images\\tmp"
        
        numArgs = len(sys.argv)
        
        if numArgs == 1:
            print 'Using DEFAULT parameters'
            obj.segmentDir(usrSegmentDIR, 
                           usrSigma, 
                           usrK,
                           usrMin, 
                           usrInputDIR,
                           usrOutputDIR,
                           tmpOutputDIR)
        elif numArgs == 8:
            usrSegmentDIR = sys.argv[1]
            usrSigma = sys.argv[2]
            usrK = sys.argv[3]
            usrMin = sys.argv[4]
            usrInputDIR = sys.argv[5]
            usrOutputDIR = sys.argv[6]
            tmpOutputDIR = sys.argv[7]
            obj.segmentDir(usrSegmentDIR, 
                           usrSigma, 
                           usrK,
                           usrMin, 
                           usrInputDIR,
                           usrOutputDIR,
                           tmpOutputDIR)
        else:
            self.help()
            
    def help(self):
        print 'Help for segment command'
        print 'python segment.py <segmentDIR> <sigma> <k> <min> <inputDIR> <outputDIR> <tmpDIR>'
        print 'segmentDIR - Directory containing the segment command'
        print 'sigma - parameter for segmentation'
        print 'k - parameter for segmentation'
        print 'min - parameter for segmentation'
        print 'inputDIR - Directory containing the input images in JPG format'
        print 'outputDIR - Directory where the outputted segmented images will be place in PNG format'
        print 'tmpDIR - Directory used during processing to temporally store intermediate results'
        
            
if __name__ == '__main__':         
    obj = segment()
    obj.run()

               