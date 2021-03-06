SPDPointsViewerColourTable* createColourTabWaves()
{
    float rgbVals[256][3] = {
        {124,121,131},
        {124,121,131},
        {121,141,134},
        {118,155,137},
        {115,160,140},
        {112,155,143},
        {109,141,146},
        {106,121,149},
        {103,97,152},
        {100,72,155},
        {97,52,158},
        {94,38,161},
        {91,34,164},
        {88,38,167},
        {85,52,170},
        {82,72,173},
        {79,96,176},
        {76,121,179},
        {73,141,182},
        {70,155,185},
        {68,160,187},
        {65,155,190},
        {62,141,193},
        {60,121,195},
        {57,97,198},
        {54,72,201},
        {52,52,203},
        {49,38,206},
        {47,34,208},
        {45,38,210},
        {42,52,213},
        {40,72,215},
        {38,96,217},
        {36,121,219},
        {33,141,222},
        {31,155,224},
        {29,160,226},
        {27,155,228},
        {25,141,230},
        {24,121,231},
        {22,97,233},
        {20,72,235},
        {19,52,236},
        {17,38,238},
        {15,34,240},
        {14,38,241},
        {13,52,242},
        {11,72,244},
        {13,96,245},
        {9,121,246},
        {8,141,247},
        {7,155,248},
        {6,160,249},
        {5,155,250},
        {4,141,251},
        {4,121,251},
        {3,97,252},
        {2,72,253},
        {2,52,253},
        {1,38,254},
        {1,34,254},
        {1,38,254},
        {1,52,254},
        {1,72,254},
        {1,96,255},
        {1,121,254},
        {1,141,254},
        {1,155,254},
        {1,160,254},
        {1,155,254},
        {2,141,253},
        {2,121,253},
        {3,97,252},
        {4,72,251},
        {4,52,251},
        {5,38,250},
        {6,34,249},
        {7,38,248},
        {8,52,247},
        {9,72,246},
        {13,96,245},
        {11,121,244},
        {13,141,242},
        {14,155,241},
        {15,160,240},
        {17,155,238},
        {19,141,236},
        {20,121,235},
        {22,97,233},
        {24,72,231},
        {25,52,230},
        {27,38,228},
        {29,34,226},
        {31,38,224},
        {33,52,222},
        {36,72,219},
        {38,96,217},
        {40,121,215},
        {42,141,213},
        {45,155,210},
        {47,160,208},
        {49,155,206},
        {52,141,203},
        {54,121,201},
        {57,97,198},
        {60,72,195},
        {62,52,193},
        {65,38,190},
        {68,34,187},
        {70,38,185},
        {73,52,182},
        {76,72,179},
        {79,96,176},
        {82,121,173},
        {85,141,170},
        {88,155,167},
        {91,160,164},
        {94,155,161},
        {97,141,158},
        {100,121,155},
        {103,96,152},
        {106,72,149},
        {109,52,146},
        {112,38,143},
        {115,34,140},
        {118,38,137},
        {121,52,134},
        {124,72,131},
        {128,97,127},
        {131,121,124},
        {134,141,121},
        {137,155,118},
        {140,160,115},
        {143,155,112},
        {146,141,109},
        {149,121,106},
        {152,96,103},
        {155,72,100},
        {158,52,97},
        {161,38,94},
        {164,34,91},
        {167,38,88},
        {170,52,85},
        {173,72,82},
        {176,97,79},
        {179,121,76},
        {182,141,73},
        {185,155,70},
        {187,160,68},
        {190,155,65},
        {193,141,62},
        {195,121,60},
        {198,96,57},
        {201,72,54},
        {203,52,52},
        {206,38,49},
        {208,34,47},
        {210,38,45},
        {213,52,42},
        {215,72,40},
        {217,97,38},
        {219,121,36},
        {222,141,33},
        {224,155,31},
        {226,160,29},
        {228,155,27},
        {230,141,25},
        {231,121,24},
        {233,96,22},
        {235,72,20},
        {236,52,19},
        {238,38,17},
        {240,34,15},
        {241,38,14},
        {242,52,13},
        {244,72,11},
        {245,97,13},
        {246,121,9},
        {247,141,8},
        {248,155,7},
        {249,160,6},
        {250,155,5},
        {251,141,4},
        {251,121,4},
        {252,96,3},
        {253,72,2},
        {253,52,2},
        {254,38,1},
        {254,34,1},
        {254,38,1},
        {254,52,1},
        {254,72,1},
        {255,97,1},
        {254,121,1},
        {254,141,1},
        {254,155,1},
        {254,160,1},
        {254,155,1},
        {253,141,2},
        {253,121,2},
        {252,96,3},
        {251,72,4},
        {251,52,4},
        {250,38,5},
        {249,34,6},
        {248,38,7},
        {247,52,8},
        {246,72,9},
        {245,97,13},
        {244,121,11},
        {242,141,13},
        {241,155,14},
        {240,160,15},
        {238,155,17},
        {236,141,19},
        {235,121,20},
        {233,96,22},
        {231,72,24},
        {230,52,25},
        {228,38,27},
        {226,34,29},
        {224,38,31},
        {222,52,33},
        {219,72,36},
        {217,97,38},
        {215,121,40},
        {213,141,42},
        {210,155,45},
        {208,160,47},
        {206,155,49},
        {203,141,52},
        {201,121,54},
        {198,96,57},
        {195,72,60},
        {193,52,62},
        {190,38,65},
        {187,34,68},
        {185,38,70},
        {182,52,73},
        {179,72,76},
        {176,97,79},
        {173,121,82},
        {170,141,85},
        {167,155,88},
        {164,160,91},
        {161,155,94},
        {158,141,97},
        {155,121,100},
        {152,96,103},
        {149,72,106},
        {146,52,109},
        {143,38,112},
        {140,34,115},
        {137,38,118},
        {134,52,121},
        {134,52,121}};

    SPDPointsViewerColourTable *colourTab = new SPDPointsViewerColourTable();
    colourTab->setName("Waves");
    for(unsigned int i = 0; i < 256; ++i)
    {
        ClrVals clrVal;
        clrVal.val = i;
        clrVal.red = rgbVals[i][0]/255;
        clrVal.green = rgbVals[i][1]/255;
        clrVal.blue = rgbVals[i][2]/255;
        colourTab->addColorValPair(clrVal);
    }
    return colourTab;
};
