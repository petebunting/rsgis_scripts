#! /usr/bin/env python

from CompareCtrlPts import CompareCtrlPts
import gc

referenceFiles = [\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_LiDAR_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_LiDAR_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_correct_LiDAR_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_correct_LiDAR_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_correct_LiDAR_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_correct_LiDAR_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_HyMap_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_correct_HyMap_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_correct_HyMap_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_correct_Landsat_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_LiDAR_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_LiDAR_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_correct_LiDAR_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_correct_LiDAR_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_correct_LiDAR_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_correct_LiDAR_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_HyMap_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_correct_HyMap_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_correct_HyMap_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_correct_Landsat_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_LiDAR_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_LiDAR_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_correct_LiDAR_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_correct_LiDAR_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_correct_LiDAR_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_correct_LiDAR_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_HyMap_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_correct_HyMap_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_correct_HyMap_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_correct_Landsat_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_sin10warpX_ctrlpts.pts'\
]

registeredFiles = [\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_LiDAR_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_LiDAR_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR_LiDAR_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR_LiDAR_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap_LiDAR_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap_LiDAR_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_HyMap_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_HyMap_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR_HyMap_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR_HyMap_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS_Landsat_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS_Landsat_XSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_LiDAR_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_LiDAR_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR_LiDAR_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR_LiDAR_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap_LiDAR_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap_LiDAR_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_HyMap_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_HyMap_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR_HyMap_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR_HyMap_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS_Landsat_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS_Landsat_YSin5Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_LiDAR_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_LiDAR_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR_LiDAR_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR_LiDAR_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap_LiDAR_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap_LiDAR_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_HyMap_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_HyMap_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR_HyMap_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR_HyMap_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS_Landsat_XSin10Warp_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS_Landsat_XSin10Warp_image2image.pts'\
]

outputPlots = [\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_LiDAR_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_LiDAR_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR_LiDAR_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR_LiDAR_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap_LiDAR_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap_LiDAR_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_HyMap_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_HyMap_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR_HyMap_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR_HyMap_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS_Landsat_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS_Landsat_XSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_LiDAR_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_LiDAR_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR_LiDAR_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR_LiDAR_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap_LiDAR_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap_LiDAR_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_HyMap_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_HyMap_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR_HyMap_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR_HyMap_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS_Landsat_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS_Landsat_YSin5Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_LiDAR_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_LiDAR_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR_LiDAR_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR_LiDAR_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap_LiDAR_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap_LiDAR_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_HyMap_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_HyMap_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR_HyMap_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR_HyMap_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS_Landsat_XSin10Warp',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS_Landsat_XSin10Warp'\
]

title= [\
'p142_CASI_LiDAR_XSin5Warp',\
'p138_CASI_LiDAR_XSin5Warp',\
'p142_AIRSAR_LiDAR_XSin5Warp',\
'p138_AIRSAR_LiDAR_XSin5Warp',\
'p142_HyMap_LiDAR_XSin5Warp',\
'p138_HyMap_LiDAR_XSin5Warp',\
'p142_CASI_HyMap_XSin5Warp',\
'p138_CASI_HyMap_XSin5Warp',\
'injune2_AIRSAR_HyMap_XSin5Warp',\
'injune8_AIRSAR_HyMap_XSin5Warp',\
'scene1_ALOS_Landsat_XSin5Warp',\
'scene2_ALOS_Landsat_XSin5Warp',\
'p142_CASI_LiDAR_YSin5Warp',\
'p138_CASI_LiDAR_YSin5Warp',\
'p142_AIRSAR_LiDAR_YSin5Warp',\
'p138_AIRSAR_LiDAR_YSin5Warp',\
'p142_HyMap_LiDAR_YSin5Warp',\
'p138_HyMap_LiDAR_YSin5Warp',\
'p142_CASI_HyMap_YSin5Warp',\
'p138_CASI_HyMap_YSin5Warp',\
'injune2_AIRSAR_HyMap_YSin5Warp',\
'injune8_AIRSAR_HyMap_YSin5Warp',\
'scene1_ALOS_Landsat_YSin5Warp',\
'scene2_ALOS_Landsat_YSin5Warp',\
'p142_CASI_LiDAR_XSin10Warp',\
'p138_CASI_LiDAR_XSin10Warp',\
'p142_AIRSAR_LiDAR_XSin10Warp',\
'p138_AIRSAR_LiDAR_XSin10Warp',\
'p142_HyMap_LiDAR_XSin10Warp',\
'p138_HyMap_LiDAR_XSin10Warp',\
'p142_CASI_HyMap_XSin10Warp',\
'p138_CASI_HyMap_XSin10Warp',\
'injune2_AIRSAR_HyMap_XSin10Warp',\
'injune8_AIRSAR_HyMap_XSin10Warp',\
'scene1_ALOS_Landsat_XSin10Warp',\
'scene2_ALOS_Landsat_XSin10Warp'\
]

summeries = []

compareCtrlPts = CompareCtrlPts()

for i in range(len(referenceFiles)):
    print title[i]
    compareCtrlPts = CompareCtrlPts()
    #print referenceFiles[i]
    #print registeredFiles[i]
    summery = compareCtrlPts.run(referenceFiles[i], registeredFiles[i], outputPlots[i], 'png', 50)
    summeries.append(summery)
    #print 'Min: ', summery[0], ' Mean: ', summery[1], ' Max: ', summery[2], ' Std Dev: ', summery[3]
    #print ''
    del compareCtrlPts
    gc.collect()
    
print 'title, \t min, \t mean, \t max, \t stddev'
for i in range(len(title)):
    print title[i], ',', summeries[i][0], ',', summeries[i][1], ',', summeries[i][2], ',', summeries[i][3]
