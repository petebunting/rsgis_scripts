#!/usr/bin/env python

import sys

# READ PARAMETER FILE #

parameter_file = open("/Users/heathercrump/Dropbox/Heather's PhD/Population_Model/Parameter_Files/Population_Model_GP_Parameter_File_34.txt", 'r')

i = -1

for line in parameter_file:
    #print "line = ", line
    line = line.strip()
    i = i + 1
    if i == 0:  
        numOfYears = int(line.replace('numOfYears=','').replace('/n','').replace(' ',''))
    if i == 1:
        initalAdultPairPop = int(line.replace('initalAdultPairPop=','').replace('/n','').replace(' ',''))
    if i == 2:
        winterSurvivalRate = float(line.replace('winterSurvivalRate=','').replace('/n','').replace(' ',''))
    if i == 3:
        averageEggsPerPair = float(line.replace('averageEggsPerPair=','').replace('/n','').replace(' ',''))
    if i == 4:
        averageFledgelingsPerPair = float(line.replace('averageFledgelingsPerPair=','').replace('/n','').replace(' ',''))
    if i == 5:
        preditorControl = line.replace('preditorControl=','').replace('/n','').replace(' ','')
    if i == 6:
        numOfFledgelings = float(line.replace('numOfFledgelings=','').replace('/n','').replace(' ',''))
    if i == 7:
        numOfFledgelingsYearOld = float(line.replace('numOfFledgelingsYearOld=','').replace('/n','').replace(' ',''))
        
# INTERNAL VARIABLES #

numOfAdultsPairs = initalAdultPairPop
numOfEggs = 0

TXT = open("/Users/heathercrump/Dropbox/Heather's PhD/Population_Model/Outputs/Population_Model_Output_GP_File_34.txt", 'w')

parametres = str("INPUT PARAMETERS" + "\n" + "\n" + "Number of years: " + str(numOfYears) + "\n" + "Initial number of adult pairs: " + str(initalAdultPairPop) + "\n" +  "Winter survival rate: " + str(winterSurvivalRate) + "\n" + "Average number of eggs per pair: " + str(averageEggsPerPair) + "\n" + "Average number of fledgelings per pair: " + str(averageFledgelingsPerPair) + "\n" + "Predator control: " + str(preditorControl) + "\n" +  "POPULATION ESTIMATES" + "\n" + "Initial number of fledgelings: " + str(numOfFledgelings)  + "\n" + "Initial number of fledgelings a year old: " + str(numOfFledgelingsYearOld) + "\n" + "\n" + "\n")

TXT.write(parametres)

# TIMING LOOP #

for year in range(numOfYears):
    numOfAdultsPairs += (numOfFledgelingsYearOld/2)
    numOfFledgelingsYearOld = numOfFledgelings
    
    # Winter Survival
    numOfAdultsPairs=numOfAdultsPairs*winterSurvivalRate
    numOfFledgelingsYearOld=numOfFledgelingsYearOld*winterSurvivalRate
    
    # Numbers of Eggs to hatch
    numOfEggs = numOfAdultsPairs * averageEggsPerPair
    
    # Number of Eggs to Fledgeling
    numOfFledgelings = numOfAdultsPairs * averageFledgelingsPerPair
    
    if preditorControl:
        numOfFledgelings=numOfFledgelings*0.75
    else:
        numOfFledgelings=numOfFledgelings*0.18

    #print "Year: ", year
    #print "Number of Adult Pairs: ", numOfAdultsPairs
    #print "Number of Fledgelings: ", numOfFledgelings
    #print "Number of Fledgelings a Year old: ", numOfFledgelingsYearOld, "\n"

# WRITE OUTPUT FILE #

    text = str("Year: " + str(year) + "\n" + "Number of Adult Pairs: " + str(numOfAdultsPairs) + "\n" +  "Number of Fledgelings: " + str(numOfFledgelings) + "\n" + "Number of Fledgelings a Year old: " + str(numOfFledgelingsYearOld) + "\n" + "\n")

    TXT.write(text)
    
TXT.close()
    
# CREATE R SCRIPT FOR OUTPUT FILE - SET UP FOR 20 YEARS OF DATA #

TXT = open("/Users/heathercrump/Dropbox/Heather's PhD/Population_Model/Outputs/Population_Model_Output_GP_File_34.txt", 'r')

i = -1

for line in TXT:
    line = line.strip()
    i = i + 1
    # Adults
    if i == 13:
        Year_0_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_0_AdultPairs = str(Year_0_AdultPairs)
    if i == 18:
        Year_1_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_1_AdultPairs = str(Year_1_AdultPairs)
    if i == 23:
        Year_2_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_2_AdultPairs = str(Year_2_AdultPairs)
    if i == 28:
        Year_3_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_3_AdultPairs = str(Year_3_AdultPairs)
    if i == 33:
        Year_4_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_4_AdultPairs = str(Year_4_AdultPairs)
    if i == 38:
        Year_5_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_5_AdultPairs = str(Year_5_AdultPairs)
    if i == 43:
        Year_6_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_6_AdultPairs = str(Year_6_AdultPairs)
    if i == 48:
        Year_7_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_7_AdultPairs = str(Year_7_AdultPairs)
    if i == 53:
        Year_8_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_8_AdultPairs = str(Year_8_AdultPairs)
    if i == 58:
        Year_9_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_9_AdultPairs = str(Year_9_AdultPairs)
    if i == 63:
        Year_10_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_10_AdultPairs = str(Year_10_AdultPairs)
    if i == 68:
        Year_11_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_11_AdultPairs = str(Year_11_AdultPairs)
    if i == 73:
        Year_12_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_12_AdultPairs = str(Year_12_AdultPairs)
    if i == 78:
        Year_13_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_13_AdultPairs = str(Year_13_AdultPairs)
    if i == 83:
        Year_14_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_14_AdultPairs = str(Year_14_AdultPairs)
    if i == 88:
        Year_15_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_15_AdultPairs = str(Year_15_AdultPairs)
    if i == 93:
        Year_16_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_16_AdultPairs = str(Year_16_AdultPairs)
    if i == 98:
        Year_17_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_17_AdultPairs = str(Year_17_AdultPairs)
    if i == 103:
        Year_18_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_18_AdultPairs = str(Year_18_AdultPairs)
    if i == 108:
        Year_19_AdultPairs = float(line.replace('Number of Adult Pairs: ','').replace('/n','').replace(' ',''))
        Year_19_AdultPairs = str(Year_19_AdultPairs)      
        Adult_Pairs_Values = str(Year_0_AdultPairs + ", " + Year_1_AdultPairs + ", " + Year_2_AdultPairs + ", " + Year_3_AdultPairs + ", " + Year_4_AdultPairs + ", " + Year_5_AdultPairs + ", " + Year_6_AdultPairs + ", " + Year_7_AdultPairs + ", " + Year_8_AdultPairs + ", " + Year_9_AdultPairs + ", " + Year_10_AdultPairs + ", " + Year_11_AdultPairs + ", " + Year_12_AdultPairs + ", " + Year_13_AdultPairs + ", " + Year_14_AdultPairs + ", " + Year_15_AdultPairs + ", " + Year_16_AdultPairs + ", " + Year_17_AdultPairs + ", " + Year_18_AdultPairs + ", " + Year_19_AdultPairs)
        # Fledgelings
    if i == 14:
        Year_0_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_0_Fledgelings = str(Year_0_Fledgelings)
    if i == 19:
        Year_1_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_1_Fledgelings = str(Year_1_Fledgelings)
    if i == 24:
        Year_2_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_2_Fledgelings = str(Year_2_Fledgelings)
    if i == 29:
        Year_3_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_3_Fledgelings = str(Year_3_Fledgelings)
    if i == 34:
        Year_4_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_4_Fledgelings = str(Year_4_Fledgelings)
    if i == 39:
        Year_5_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_5_Fledgelings = str(Year_5_Fledgelings)
    if i == 44:
        Year_6_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_6_Fledgelings = str(Year_6_Fledgelings)
    if i == 49:
        Year_7_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_7_Fledgelings = str(Year_7_Fledgelings)
    if i == 54:
        Year_8_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_8_Fledgelings = str(Year_8_Fledgelings)
    if i == 59:
        Year_9_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_9_Fledgelings = str(Year_9_Fledgelings)
    if i == 64:
        Year_10_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_10_Fledgelings = str(Year_10_Fledgelings)
    if i == 69:
        Year_11_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_11_Fledgelings = str(Year_11_Fledgelings)
    if i == 74:
        Year_12_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_12_Fledgelings = str(Year_12_Fledgelings)
    if i == 79:
        Year_13_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_13_Fledgelings = str(Year_13_Fledgelings)
    if i == 84:
        Year_14_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_14_Fledgelings = str(Year_14_Fledgelings)
    if i == 89:
        Year_15_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_15_Fledgelings = str(Year_15_Fledgelings)
    if i == 94:
        Year_16_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_16_Fledgelings = str(Year_16_Fledgelings)
    if i == 99:
        Year_17_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_17_Fledgelings = str(Year_17_Fledgelings)
    if i == 104:
        Year_18_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_18_Fledgelings = str(Year_18_Fledgelings)
    if i == 109:
        Year_19_Fledgelings = float(line.replace('Number of Fledgelings: ','').replace('/n','').replace(' ',''))
        Year_19_Fledgelings = str(Year_19_Fledgelings)      
        Fledgelings_Values = str(Year_0_Fledgelings + ", " + Year_1_Fledgelings + ", " + Year_2_Fledgelings + ", " + Year_3_Fledgelings + ", " + Year_4_Fledgelings + ", " + Year_5_Fledgelings + ", " + Year_6_Fledgelings + ", " + Year_7_Fledgelings + ", " + Year_8_Fledgelings + ", " + Year_9_Fledgelings + ", " + Year_10_Fledgelings + ", " + Year_11_Fledgelings + ", " + Year_12_Fledgelings + ", " + Year_13_Fledgelings + ", " + Year_14_Fledgelings + ", " + Year_15_Fledgelings + ", " + Year_16_Fledgelings + ", " + Year_17_Fledgelings + ", " + Year_18_Fledgelings + ", " + Year_19_Fledgelings)
    # Fledgelings a year old
    if i == 15:
        Year_0_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_0_Fledgelings_YearOld = str(Year_0_Fledgelings_YearOld)
    if i == 20:
        Year_1_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_1_Fledgelings_YearOld = str(Year_1_Fledgelings_YearOld)
    if i == 25:
        Year_2_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_2_Fledgelings_YearOld = str(Year_2_Fledgelings_YearOld)
    if i == 30:
        Year_3_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_3_Fledgelings_YearOld = str(Year_3_Fledgelings_YearOld)
    if i == 35:
        Year_4_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_4_Fledgelings_YearOld = str(Year_4_Fledgelings_YearOld)
    if i == 40:
        Year_5_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_5_Fledgelings_YearOld = str(Year_5_Fledgelings_YearOld)
    if i == 45:
        Year_6_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_6_Fledgelings_YearOld = str(Year_6_Fledgelings_YearOld)
    if i == 50:
        Year_7_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_7_Fledgelings_YearOld = str(Year_7_Fledgelings_YearOld)
    if i == 55:
        Year_8_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_8_Fledgelings_YearOld = str(Year_8_Fledgelings_YearOld)
    if i == 60:
        Year_9_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_9_Fledgelings_YearOld = str(Year_9_Fledgelings_YearOld)
    if i == 65:
        Year_10_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_10_Fledgelings_YearOld = str(Year_10_Fledgelings_YearOld)
    if i == 70:
        Year_11_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_11_Fledgelings_YearOld = str(Year_11_Fledgelings_YearOld)
    if i == 75:
        Year_12_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_12_Fledgelings_YearOld = str(Year_12_Fledgelings_YearOld)
    if i == 80:
        Year_13_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_13_Fledgelings_YearOld = str(Year_13_Fledgelings_YearOld)
    if i == 85:
        Year_14_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_14_Fledgelings_YearOld = str(Year_14_Fledgelings_YearOld)
    if i == 90:
        Year_15_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_15_Fledgelings_YearOld = str(Year_15_Fledgelings_YearOld)
    if i == 95:
        Year_16_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_16_Fledgelings_YearOld = str(Year_16_Fledgelings_YearOld)
    if i == 100:
        Year_17_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_17_Fledgelings_YearOld = str(Year_17_Fledgelings_YearOld)
    if i == 105:
        Year_18_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_18_Fledgelings_YearOld = str(Year_18_Fledgelings_YearOld)
    if i == 110:
        Year_19_Fledgelings_YearOld = float(line.replace('Number of Fledgelings a Year old: ','').replace('/n','').replace(' ',''))
        Year_19_Fledgelings_YearOld = str(Year_19_Fledgelings_YearOld)      
        Fledgelings_YearOld_Values = str(Year_0_Fledgelings_YearOld + ", " + Year_1_Fledgelings_YearOld + ", " + Year_2_Fledgelings_YearOld + ", " + Year_3_Fledgelings_YearOld + ", " + Year_4_Fledgelings_YearOld + ", " + Year_5_Fledgelings_YearOld + ", " + Year_6_Fledgelings_YearOld + ", " + Year_7_Fledgelings_YearOld + ", " + Year_8_Fledgelings_YearOld + ", " + Year_9_Fledgelings_YearOld + ", " + Year_10_Fledgelings_YearOld + ", " + Year_11_Fledgelings_YearOld + ", " + Year_12_Fledgelings_YearOld + ", " + Year_13_Fledgelings_YearOld + ", " + Year_14_Fledgelings_YearOld + ", " + Year_15_Fledgelings_YearOld + ", " + Year_16_Fledgelings_YearOld + ", " + Year_17_Fledgelings_YearOld + ", " + Year_18_Fledgelings_YearOld + ", " + Year_19_Fledgelings_YearOld)

TXT.close()

# ADD R SCRIPT TO OUTPUT FILE #

TXT = open("/Users/heathercrump/Dropbox/Heather's PhD/Population_Model/Outputs/Population_Model_Output_GP_File_34.txt", 'a')

year_number = str("0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19")

# Adults plot

R_script_PART1 = str("\n" + "R SCRIPT FOR PLOTTING NUMBERS OF ADULTS" + "\n" + "\n" + "Adult_Pairs_Values = c(" + Adult_Pairs_Values + ")" + "\n" + "year_number = c(" + year_number + ")" + "\n" + "\n")

TXT.write(R_script_PART1)

R_script_PART2 = str("par(mfrow=c(1,1))" + "\n" + "\n" + 'plot.ts(Adult_Pairs_Values, ylab = "Number of Adult Birds", xaxt = "n", xlab = "Year Number", col = "black", main = "Population Model Output - Number of Adult Pairs")' + "\n" + "axis(1, at=1:20, labels= year_number)" + "\n" + "dev.copy2pdf(file=\"/Users/heathercrump/Dropbox/Heather's PhD/Population_Model/Figures/Number_of_adult_pairs.png\")" + "\n")

TXT.write(R_script_PART2)

# Fledgelings plot

R_script_PART1 = str("\n" + "R SCRIPT FOR PLOTTING NUMBERS OF FLEDGELINGS" + "\n" + "\n" + "Fledgelings_Values = c(" + Fledgelings_Values + ")" + "\n" + "year_number = c(" + year_number + ")" + "\n" + "\n")

TXT.write(R_script_PART1)

R_script_PART2 = str("par(mfrow=c(1,1))" + "\n" + "\n" + 'plot.ts(Fledgelings_Values, ylab = "Number of Fledgelings", xaxt = "n", xlab = "Year Number", col = "black", main = "Population Model Output - Number of Fledgelings")' + "\n" + "axis(1, at=1:20, labels= year_number)" + "\n" + "dev.copy2pdf(file=\"/Users/heathercrump/Dropbox/Heather's PhD/Population_Model/Figures/Number_of_fledgelings.png\")" + "\n")

TXT.write(R_script_PART2)

# Fledgelings a year old

R_script_PART1 = str("\n" + "R SCRIPT FOR PLOTTING NUMBERS OF FLEDGELINGS WHICH ARE A YEAR OLD" + "\n" + "\n" + "Fledgelings_YearOld_Values = c(" + Fledgelings_YearOld_Values + ")" + "\n" + "year_number = c(" + year_number + ")" + "\n" + "\n")

TXT.write(R_script_PART1)

R_script_PART2 = str("par(mfrow=c(1,1))" + "\n" + "\n" + 'plot.ts(Fledgelings_YearOld_Values, ylab = "Number of Fledgelings a Year Old", xaxt = "n", xlab = "Year Number", col = "black", main = "Population Model Output - Number of Fledgelings a Year Old")' + "\n" + "axis(1, at=1:20, labels= year_number)" + "\n" + "dev.copy2pdf(file=\"/Users/heathercrump/Dropbox/Heather's PhD/Population_Model/Figures/Number_of_Fledgelings_YearOld.png\")" + "\n")

TXT.write(R_script_PART2)

TXT.close()