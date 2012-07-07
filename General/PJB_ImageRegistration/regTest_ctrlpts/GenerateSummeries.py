#! /usr/bin/env python

from CompareCtrlPts import CompareCtrlPts

referenceFiles = [\
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
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_16x18y_correct_Landsat_ctrlpts.pts',\
]

registeredFiles = [\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_base2LiDAR_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_base2LiDAR_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR_base2LiDAR_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR_base2LiDAR_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap_base2LiDAR_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap_base2LiDAR_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI_base2HyMap_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI_base2HyMap_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR_base2HyMap_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR_base2HyMap_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS_base2Landsat_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS_base2Landsat_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2LiDAR_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2LiDAR_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_AIRSAR2LiDAR_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_AIRSAR2LiDAR_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_HyMap2LiDAR_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_HyMap2LiDAR_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p142_CASI2HyMap_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/p138_CASI2HyMap_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune2_AIRSAR2HyMap_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/injune8_AIRSAR2HyMap_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene1_ALOS2Landsat_16X18Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_2X3Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_4X6Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_8X10Y_image2image.pts',\
'/Users/pete/Desktop/Registration_Tests/Reg_Ctrl_Pts/scene2_ALOS2Landsat_16X18Y_image2image.pts'\
]

outputPlots = [\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_base2LiDAR',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_base2LiDAR',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR_base2LiDAR',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR_base2LiDAR',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap_base2LiDAR',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap_base2LiDAR',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI_base2HyMap',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI_base2HyMap',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR_base2HyMap',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR_base2HyMap',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS_base2Landsat',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS_base2Landsat',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2LiDAR_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2LiDAR_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2LiDAR_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2LiDAR_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2LiDAR_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2LiDAR_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2LiDAR_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2LiDAR_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR2LiDAR_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR2LiDAR_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR2LiDAR_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_AIRSAR2LiDAR_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR2LiDAR_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR2LiDAR_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR2LiDAR_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_AIRSAR2LiDAR_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap2LiDAR_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap2LiDAR_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap2LiDAR_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_HyMap2LiDAR_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap2LiDAR_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap2LiDAR_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap2LiDAR_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_HyMap2LiDAR_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2HyMap_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2HyMap_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2HyMap_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p142_CASI2HyMap_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2HyMap_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2HyMap_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2HyMap_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/p138_CASI2HyMap_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR2HyMap_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR2HyMap_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR2HyMap_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune2_AIRSAR2HyMap_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR2HyMap_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR2HyMap_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR2HyMap_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/injune8_AIRSAR2HyMap_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS2Landsat_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS2Landsat_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS2Landsat_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene1_ALOS2Landsat_16X18Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS2Landsat_2X3Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS2Landsat_4X6Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS2Landsat_8X10Y',\
'/Users/pete/Desktop/Registration_Tests/plots/scene2_ALOS2Landsat_16X18Y'\
]

title= [\
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

summeries = []

compareCtrlPts = CompareCtrlPts()

for i in range(len(referenceFiles)):
    print title[i]
    #print referenceFiles[i]
    #print registeredFiles[i]
    summery = compareCtrlPts.run(referenceFiles[i], registeredFiles[i], outputPlots[i], 'png', 50)
    summeries.append(summery)
    #print 'Min: ', summery[0], ' Mean: ', summery[1], ' Max: ', summery[2], ' Std Dev: ', summery[3]
    #print ''

print 'title, \t min, \t mean, \t max, \t stddev'
for i in range(len(title)):
    print title[i], ',', summeries[i][0], ',', summeries[i][1], ',', summeries[i][2], ',', summeries[i][3]
