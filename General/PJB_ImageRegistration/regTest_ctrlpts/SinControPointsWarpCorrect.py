#! /usr/bin/env python

import math

imageA = [\
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
[0,0,1288,1832]\
]

imageB = [\
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
[0,0,1291,1832]\
]

imageACorr = [\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[250,520,957,1181],\
[335,885,1014,1504],\
[0,0,587,800],\
[0,0,450,800],\
[0,0,2218,1728],\
[0,0,1288,1832],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[245,525,961,1176],\
[335,890,1014,1499],\
[0,0,587,800],\
[0,0,450,800],\
[0,0,2218,1728],\
[0,0,1288,1831],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[250,515,957,1186],\
[0,0,634,595],\
[0,0,587,800],\
[0,0,450,800],\
[0,0,2218,1728],\
[0,0,1288,1832],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[240,525,966,1176],\
[335,890,1014,1499],\
[0,0,587,800],\
[0,0,450,800],\
[0,0,2218,1728],\
[0,0,1288,1831],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[250,510,957,1191],\
[335,875,1014,1513],\
[0,0,587,800],\
[0,0,450,800],\
[0,0,2218,1728],\
[0,0,1288,1832],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[0,0,500,150],\
[236,525,971,1176],\
[335,890,1013,1499],\
[0,0,587,800],\
[0,0,450,800],\
[0,0,2218,1728],\
[0,0,1288,1831]\
]

imageBCorr = [\
[0,5,500,155],\
[0,5,500,155],\
[10,44,510,194],\
[45,22,545,172],\
[0,5,500,155],\
[0,5,500,155],\
[0,0,707,661],\
[0,0,679,619],\
[1,5,588,805],\
[0,5,450,805],\
[0,5,2218,1733],\
[1,6,1289,1838],\
[5,0,505,150],\
[5,0,505,150],\
[10,39,510,189],\
[50,17,550,167],\
[5,0,505,150],\
[5,0,505,150],\
[0,0,716,651],\
[0,0,679,609],\
[6,0,593,800],\
[5,0,455,800],\
[5,0,2223,1728],\
[6,1,1294,1832],\
[0,9,500,159],\
[0,9,500,159],\
[10,48,510,198],\
[54,17,554,167],\
[0,9,500,159],\
[0,9,500,159],\
[0,0,707,671],\
[45,25,679,620],\
[1,10,588,810],\
[0,10,450,810],\
[0,10,2218,1738],\
[1,11,1289,1843],\
[11,0,511,150],\
[11,0,511,150],\
[10,39,510,189],\
[54,17,554,167],\
[11,0,511,150],\
[5,0,505,150],\
[0,0,726,651],\
[0,0,679,609],\
[11,0,598,800],\
[10,0,460,800],\
[10,0,2228,1728],\
[11,1,1299,1832],\
[0,13,500,163],\
[0,13,500,163],\
[10,51,510,201],\
[1,14,501,164],\
[0,13,500,163],\
[0,13,500,163],\
[0,0,707,681],\
[0,0,679,638],\
[1,16,588,816],\
[0,15,450,815],\
[0,15,2218,1743],\
[1,16,1289,1848],\
[16,0,516,150],\
[16,0,516,150],\
[9,39,509,189],\
[58,17,558,167],\
[16,0,516,150],\
[16,0,516,150],\
[0,0,735,651],\
[0,0,678,609],\
[15,0,602,800],\
[14,0,464,800],\
[15,0,2233,1728],\
[16,1,1304,1832]\
]


step = [ \
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
[20,20],\
[20,20],\
[20,20],\
[20,20],\
[50,50],\
[50,50]\
]

# 0 == X and 1 == Y
warpAxis = [ \
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
0,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1,\
1\
]

outputWarpFiles = [ \
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_LiDAR_sin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_LiDARsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_AIRSAR_LiDARsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_AIRSAR_LiDARsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_HyMap_LiDARsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_HyMap_LiDARsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_HyMapsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_HyMapsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune2_AIRSAR_HyMapsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune8_AIRSAR_HyMapsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene1_ALOS_Landsatsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene2_ALOS_Landsatsin5warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_LiDAR_sin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_LiDARsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_AIRSAR_LiDARsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_AIRSAR_LiDARsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_HyMap_LiDARsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_HyMap_LiDARsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_HyMapsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_HyMapsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune2_AIRSAR_HyMapsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune8_AIRSAR_HyMapsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene1_ALOS_Landsatsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene2_ALOS_Landsatsin5warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_LiDAR_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_LiDARsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_AIRSAR_LiDARsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_AIRSAR_LiDARsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_HyMap_LiDARsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_HyMap_LiDARsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_HyMapsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_HyMapsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune2_AIRSAR_HyMapsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune8_AIRSAR_HyMapsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene1_ALOS_Landsatsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene2_ALOS_Landsatsin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_LiDAR_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_LiDARsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_AIRSAR_LiDARsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_AIRSAR_LiDARsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_HyMap_LiDARsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_HyMap_LiDARsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_HyMapsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_HyMapsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune2_AIRSAR_HyMapsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune8_AIRSAR_HyMapsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene1_ALOS_Landsatsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene2_ALOS_Landsatsin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_LiDAR_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_LiDARsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_AIRSAR_LiDARsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_AIRSAR_LiDARsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_HyMap_LiDARsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_HyMap_LiDARsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_HyMapsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_HyMapsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune2_AIRSAR_HyMapsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune8_AIRSAR_HyMapsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene1_ALOS_Landsatsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene2_ALOS_Landsatsin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_LiDAR_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_LiDARsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_AIRSAR_LiDARsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_AIRSAR_LiDARsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_HyMap_LiDARsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_HyMap_LiDARsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p142_CASI_HyMapsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/p138_CASI_HyMapsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune2_AIRSAR_HyMapsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/injune8_AIRSAR_HyMapsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene1_ALOS_Landsatsin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/WarppedImages4Tests/ctrl_pts/scene2_ALOS_Landsatsin15warpY_ctrlpts.pts'\
]

outputCorrectFiles = [ \
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
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_sin10warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_LiDAR_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_LiDAR_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_correct_LiDAR_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_correct_LiDAR_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_correct_LiDAR_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_correct_LiDAR_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_HyMap_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_correct_HyMap_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_correct_HyMap_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_correct_Landsat_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_sin10warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_LiDAR_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_LiDAR_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_correct_LiDAR_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_correct_LiDAR_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_correct_LiDAR_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_correct_LiDAR_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_HyMap_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_correct_HyMap_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_correct_HyMap_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_correct_Landsat_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_sin15warpX_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_LiDAR_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_LiDAR_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_AIRSAR_correct_LiDAR_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_AIRSAR_correct_LiDAR_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_HyMap_correct_LiDAR_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_HyMap_correct_LiDAR_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p142_CASI_correct_HyMap_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/p138_CASI_correct_HyMap_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune2_AIRSAR_correct_HyMap_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/injune8_AIRSAR_correct_HyMap_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene1_ALOS_correct_Landsat_sin15warpY_ctrlpts.pts',\
'/Users/pete/Desktop/Registration_Tests/CorrectProducedCtrlPts/scene2_ALOS_correct_Landsat_sin15warpY_ctrlpts.pts'\
]

amplitude = [ \
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
5,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
10,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15,\
15\
]

frequency = 0
newline = str('\n')
tab = str('\t')
warpComment = '; Output control points for warping the image with a sin function'
correctComment = '; Output control points to correct the sin warp'

for i in range(len(imageA)):
	print outputWarpFiles[i]
	print outputCorrectFiles[i]
	
	outWarpFile = open(outputWarpFiles[i], 'w')
	outCorrectFile = open(outputCorrectFiles[i], 'w')

	outWarpFile.write(warpComment)
	outWarpFile.write(newline)
	outWarpFile.write(('; ' + outputWarpFiles[i]))
	outWarpFile.write(newline)

	outCorrectFile.write(correctComment)
	outCorrectFile.write(newline)
	outCorrectFile.write(('; ' + outputCorrectFiles[i]))
	outCorrectFile.write(newline)
	
	if warpAxis[i] == 0:
		frequency = (math.pi / (imageB[i][2]-imageB[i][0]))*2
	else:
		frequency = (math.pi / (imageB[i][3]-imageB[i][1]))*2
	
	halfBXDist = (imageB[i][2]-imageB[i][0])/2
	halfBYDist = (imageB[i][1]-imageB[i][3])/2
	
	imageACurrentX = imageA[i][0] + step[i][0]
	imageACurrentY = imageA[i][1] + step[i][1]
	imageBCurrentX = imageB[i][0] + step[i][0]
	imageBCurrentY = imageB[i][1] + step[i][1]
	imageBOutputY = 0.0
	imageBOutputX = 0.0
	
	while imageACurrentY < imageA[i][3]:
		
		while imageACurrentX < imageA[i][2]:
		
			# Output Warp contrl Points:
			if warpAxis[i] == 0:
				imageBOutputX = imageBCurrentX
				imageBOutputY = imageBCurrentY + (amplitude[i] * math.sin((imageBCurrentX*frequency)))
			else:
				imageBOutputX = imageBCurrentX + (amplitude[i] * math.sin((imageBCurrentY*frequency)))
				imageBOutputY = imageBCurrentY 
		
			outStr = tab
			outStr = outStr + str(imageACurrentX)
			outStr = outStr + tab
			outStr = outStr + str(imageACurrentY)
			outStr = outStr + tab
			outStr = outStr + str(imageBOutputX)
			outStr = outStr + tab
			outStr = outStr + str(imageBOutputY)
		
			outWarpFile.write(outStr)
			outWarpFile.write(newline)
			
			imageACurrentX = imageACurrentX + step[i][0] + 1
			imageBCurrentX = imageBCurrentX + step[i][0] + 1
		
		imageACurrentY = imageACurrentY + step[i][1] + 1
		imageBCurrentY = imageBCurrentY + step[i][1] + 1
		imageACurrentX = imageA[i][0] + step[i][0]
		imageBCurrentX = imageB[i][0] + step[i][0]
		
		
		
	imageACurrentCorrX = imageACorr[i][0] + step[i][0]
	imageACurrentCorrY = imageACorr[i][1] + step[i][1]
	imageBCurrentCorrX = imageBCorr[i][0] + step[i][0]
	imageBCurrentCorrY = imageBCorr[i][1] + step[i][1]
	imageBOutputCorrX = 0.0
	imageBOutputCorrY = 0.0
	
	while imageACurrentCorrY < imageACorr[i][3]:
		
		while imageACurrentCorrX < imageACorr[i][2]:
			
			# Output Correct control Points:
			if warpAxis[i] == 0:
				imageBOutputCorrX = imageBCurrentCorrX
				imageBOutputCorrY = imageBCurrentCorrY + (amplitude[i] * math.sin(((imageBCurrentCorrX+halfBXDist)*frequency)))
			else:
				imageBOutputCorrX = imageBCurrentCorrX + (amplitude[i] * math.sin(((imageBCurrentCorrY+halfBYDist)*frequency)))
				imageBOutputCorrY = imageBCurrentCorrY 
				
			if imageBOutputCorrX < imageBCorr[2] and imageBOutputCorrY < imageBCorr[3]:
				outStr = tab
				outStr = outStr + str(imageACurrentCorrX)
				outStr = outStr + tab
				outStr = outStr + str(imageACurrentCorrY)
				outStr = outStr + tab
				outStr = outStr + str(imageBOutputCorrX)
				outStr = outStr + tab
				outStr = outStr + str(imageBOutputCorrY)
		
				outCorrectFile.write(outStr)
				outCorrectFile.write(newline)
			
			# Update the position variables
			imageACurrentCorrX = imageACurrentCorrX + step[i][0] + 1
			imageBCurrentCorrX = imageBCurrentCorrX + step[i][0] + 1
		
		imageACurrentCorrY = imageACurrentCorrY + step[i][1] + 1
		imageBCurrentCorrY = imageBCurrentCorrY + step[i][1] + 1
		imageACurrentCorrX = imageACorr[i][0] + step[i][0]
		imageBCurrentCorrX = imageBCorr[i][0] + step[i][0]
	
	outCorrectFile.close()
	outWarpFile.close()
