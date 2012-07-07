#! /usr/bin/env python

import math

imageA = [\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,1526,2257],\
[0,0,1786,2462],\
[0,0,588,801],\
[0,0,451,801],\
[0,0,2218,1728],\
[0,0,1288,1832],\
[0,0,2218,1728],\
[0,0,1291,1832],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[251,526,959,1177],\
[336,891,1016,1500],\
[0,0,587,800],\
[0,0,450,800],\
[0,0,2218,1718],\
[0,0,1288,1832],\
[0,0,499,148],\
[0,0,497,145],\
[0,0,493,141],\
[0,0,485,133],\
[0,0,499,148],\
[0,0,497,145],\
[0,0,493,141],\
[0,0,485,133],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,145],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,497,150],\
[0,0,499,148],\
[0,0,497,145],\
[0,0,493,141],\
[0,0,485,133],\
[0,0,499,148],\
[0,0,497,145],\
[0,0,493,141],\
[0,0,485,133],\
[250,524,958,1175],\
[248,521,956,1172],\
[244,517,952,1168],\
[236,509,944,1160],\
[335,889,1015,1498],\
[333,886,1013,1495],\
[329,882,1009,1491],\
[321,874,1001,1483],\
[0,0,586,799],\
[0,0,584,796],\
[0,0,581,792],\
[0,0,572,784],\
[0,0,450,799],\
[0,0,447,796],\
[0,0,444,792],\
[0,0,436,784],\
[0,0,2217,1726],\
[0,0,2215,1723],\
[0,0,2211,1719],\
[0,0,2203,1711],\
[0,0,1288,1829],\
[0,0,1287,1826],\
[0,0,1283,1822],\
[0,0,1275,1814]\
]

imageB = [\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,1526,2257],\
[0,0,1786,2462],\
[0,0,588,801],\
[0,0,451,801],\
[0,0,2218,1728],\
[0,0,1288,1832],\
[0,0,2218,1728],\
[0,0,1291,1832],\
[0,0,500,150],\
[0,0,500,150],\
[9,38,508,187],\
[44,16,543,165],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,707,651],\
[0,0,679,109],\
[0,0,588,801],\
[0,0,450,801],\
[0,0,2218,1718],\
[0,0,1291,1832],\
[2,3,500,150],\
[4,6,500,150],\
[8,10,500,150],\
[16,18,500,150],\
[2,3,500,150],\
[4,6,500,150],\
[8,10,500,150],\
[16,18,500,150],\
[10,40,509,189],\
[12,43,511,192],\
[16,47,515,196],\
[42,55,523,199],\
[45,18,544,167],\
[47,21,546,170],\
[51,25,550,174],\
[59,33,555,182],\
[2,3,500,150],\
[4,6,500,150],\
[8,10,500,150],\
[16,18,500,150],\
[2,3,500,150],\
[4,6,500,150],\
[8,10,500,150],\
[16,18,500,150],\
[0,0,707,651],\
[0,0,707,651],\
[0,0,707,651],\
[0,0,707,651],\
[0,0,679,609],\
[0,0,679,609],\
[0,0,679,609],\
[0,0,679,609],\
[2,3,588,801],\
[5,6,588,801],\
[8,10,588,801],\
[16,18,588,801],\
[2,3,451,801],\
[5,6,451,801],\
[8,10,451,801],\
[16,18,451,801],\
[2,3,2218,1728],\
[4,6,2218,1728],\
[8,10,2218,1728],\
[16,18,2218,1728],\
[3,4,1290,1832],\
[5,7,1290,1832],\
[9,11,1290,1832],\
[17,19,1290,1832]\
]

transformation = [\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[0,0],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18],\
[-2,-3],\
[-4,-6],\
[-8,-10],\
[-16,-18]\
]

step = [ \
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[50,50],\
[50,50],\
[20,20],\
[20,20],\
[50,50],\
[50,50],\
[50,50],\
[50,50],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[50,50],\
[50,50],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[8,8],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[50,50],\
[50,50],\
[50,50],\
[50,50],\
[50,50],\
[50,50],\
[50,50],\
[50,50]\
]

outputFile = [ \
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_LiDAR2LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_LiDAR2LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI2CASI_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI2CASI_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap2HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap2HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR2AIRSAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR2AIRSAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_landsat2landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_landsat2landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS2ALOS_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS2ALOS_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_2x3y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_4x6y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_8x10y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_16x18y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_2x3y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_4x6y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_8x10y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_16x18y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_2x3y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_4x6y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_8x10y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_16x18y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_2x3y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_4x6y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_8x10y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_16x18y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_2x3y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_4x6y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_8x10y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_16x18y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_2x3y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_4x6y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_8x10y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_16x18y_correct_LiDAR_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_2x3y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_4x6y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_8x10y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_16x18y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_2x3y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_4x6y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_8x10y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_16x18y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_2x3y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_4x6y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_8x10y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_16x18y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_2x3y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_4x6y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_8x10y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_16x18y_correct_HyMap_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_2x3y_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_4x6y_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_8x10y_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_16x18y_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_2x3y_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_4x6y_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_8x10y_correct_Landsat_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_16x18y_correct_Landsat_ctrlpts.pts'\
]

title= [\
'p142_LiDAR2LiDAR',\
'p138_LiDAR2LiDAR',\
'p142_CASI2CASI',\
'p138_CASI2CASI',\
'p142_HyMap2HyMap',\
'p138_HyMap2HyMap',\
'injune2_AIRSAR2AIRSAR',\
'injune8_AIRSAR2AIRSAR',\
'scene1_landsat2landsat',\
'scene2_landsat2landsat',\
'scene1_ALOS2ALOS',\
'scene2_ALOS2ALOS',\
'p142_CASI_base2LiDAR',\
'p138_CASI_base2LiDAR',\
'p142_AIRSAR_base2LiDAR',\
'p138_AIRSAR_base2LiDAR',\
'p142_HyMap_base2LiDAR',\
'p138_HyMap_base2LiDAR',\
'p142_CASI_base2HyMap',\
'p138_CASI_base2HyMap',\
'injune2_AIRSAR_base2HyMap',\
'injune8_AIRSAR_base2HyMap',\
'scene1_ALOS_base2Landsat',\
'scene2_ALOS_base2Landsat',\
'p142_CASI2LiDAR_2X3Y',\
'p142_CASI2LiDAR_4X6Y',\
'p142_CASI2LiDAR_8X10Y',\
'p142_CASI2LiDAR_16X18Y',\
'p138_CASI2LiDAR_2X3Y',\
'p138_CASI2LiDAR_4X6Y',\
'p138_CASI2LiDAR_8X10Y',\
'p138_CASI2LiDAR_16X18Y',\
'p142_AIRSAR2LiDAR_2X3Y',\
'p142_AIRSAR2LiDAR_4X6Y',\
'p142_AIRSAR2LiDAR_8X10Y',\
'p142_AIRSAR2LiDAR_16X18Y',\
'p138_AIRSAR2LiDAR_2X3Y',\
'p138_AIRSAR2LiDAR_4X6Y',\
'p138_AIRSAR2LiDAR_8X10Y',\
'p138_AIRSAR2LiDAR_16X18Y',\
'p142_HyMap2LiDAR_2X3Y',\
'p142_HyMap2LiDAR_4X6Y',\
'p142_HyMap2LiDAR_8X10Y',\
'p142_HyMap2LiDAR_16X18Y',\
'p138_HyMap2LiDAR_2X3Y',\
'p138_HyMap2LiDAR_4X6Y',\
'p138_HyMap2LiDAR_8X10Y',\
'p138_HyMap2LiDAR_16X18Y',\
'p142_CASI2HyMap_2X3Y',\
'p142_CASI2HyMap_4X6Y',\
'p142_CASI2HyMap_8X10Y',\
'p142_CASI2HyMap_16X18Y',\
'p138_CASI2HyMap_2X3Y',\
'p138_CASI2HyMap_4X6Y',\
'p138_CASI2HyMap_8X10Y',\
'p138_CASI2HyMap_16X18Y',\
'injune2_AIRSAR2HyMap_2X3Y',\
'injune2_AIRSAR2HyMap_4X6Y',\
'injune2_AIRSAR2HyMap_8X10Y',\
'injune2_AIRSAR2HyMap_16X18Y',\
'injune8_AIRSAR2HyMap_2X3Y',\
'injune8_AIRSAR2HyMap_4X6Y',\
'injune8_AIRSAR2HyMap_8X10Y',\
'injune8_AIRSAR2HyMap_16X18Y',\
'scene1_ALOS2Landsat_2X3Y',\
'scene1_ALOS2Landsat_4X6Y',\
'scene1_ALOS2Landsat_8X10Y',\
'scene1_ALOS2Landsat_16X18Y',\
'scene2_ALOS2Landsat_2X3Y',\
'scene2_ALOS2Landsat_4X6Y',\
'scene2_ALOS2Landsat_8X10Y',\
'scene2_ALOS2Landsat_16X18Y'\
]

newline = str('\n')
tab = str('\t')
comment = '; Correct control points for testing the control point identification algorithm'

for i in range(len(outputFile)):

	outFile = open(outputFile[i], 'w')

	outFile.write(str(comment))
	outFile.write(newline)
	outFile.write(('; ' + title[i]))
	outFile.write(newline)
	
	imageACurrentX = imageA[i][0] + step[i][0]
	imageACurrentY = imageA[i][1] + step[i][1]
	imageBCurrentX = imageB[i][0] + step[i][0]
	imageBCurrentY = imageB[i][1] + step[i][1]
	
	while imageACurrentY < imageA[i][3]:
	
		while imageACurrentX < imageA[i][2]:
			outStr = tab
			outStr = outStr + str(imageACurrentX)
			outStr = outStr + tab
			outStr = outStr + str(imageACurrentY)
			outStr = outStr + tab
			outStr = outStr + str((imageBCurrentX + transformation[i][0]))
			outStr = outStr + tab
			outStr = outStr + str((imageBCurrentY + transformation[i][1]))
		
			outFile.write(outStr)
			outFile.write(newline)
			imageACurrentX = imageACurrentX + step[i][0] + 1
			imageBCurrentX = imageBCurrentX + step[i][1] + 1
		
		imageACurrentY = imageACurrentY + step[i][1] + 1
		imageBCurrentY = imageBCurrentY + step[i][1] + 1
		imageACurrentX = imageA[i][0] + step[i][0]
		imageBCurrentX = imageB[i][0] + step[i][0]
		
	outFile.close()
	
