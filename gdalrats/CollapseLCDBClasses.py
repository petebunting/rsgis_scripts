#!/usr/bin/env python

import sys
from rios import rat
import numpy as np
import osgeo.gdal as gdal
import optparse

def collapseClasses(inputFile, lcdbColName, outputColName):
    ratDataset = gdal.Open(inputFile, gdal.GA_Update)
    lcdbCol = rat.readColumn(ratDataset, lcdbColName)
    
    outClassesCol = np.zeros_like(lcdbCol)
    
    # 0 Undefined
    UNDEFINED = 0
    # 1 High Producing Exotic Herbaceous
    HIGH_PRODUCING_EXOTIC_HERBACEOUS = 1
    # 2 Tall Tussock Grassland
    TALL_TUSSOCK_GRASSLAND = 2
    # 3 Other Herbaceous
    OTHER_HERBACEOUS = 3
    # 4 Scrub
    SCRUB = 4
    # 5 Indigenous Forest
    INDIGENOUS_FOREST = 5
    # 6 Exotic Forest
    EXOTIC_FOREST = 6
    # 7 Other Woody
    OTHER_WOODY = 7
    # 8 Sub Alpine Scrubland
    SUB_ALPINE_SCRUBLAND = 8
    # 9 Built Up
    BUILT_UP = 9
    # 10 Bare Ground
    BARE_GROUND = 10
    # 11 Water
    WATER = 11
    # 12 Perminant Snow and Ice
    PERMINANT_SNOW_ICE = 12

    # Undefined -> UNDEFINED
    outClassesCol = np.where(lcdbCol==0,UNDEFINED,outClassesCol)
    # Built-up Area (settlement) -> BUILT_UP
    outClassesCol = np.where(lcdbCol==1,BUILT_UP,outClassesCol)
    # Urban Parkland/Open Space -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==2,OTHER_HERBACEOUS,outClassesCol)
    # Transport Infrastructure -> BUILT_UP
    outClassesCol = np.where(lcdbCol==5,BUILT_UP,outClassesCol)
    # Surface Mines and Dumps -> BARE_GROUND
    outClassesCol = np.where(lcdbCol==6,BARE_GROUND,outClassesCol)
    # Coastal Sand and Gravel -> BARE_GROUND
    outClassesCol = np.where(lcdbCol==10,BARE_GROUND,outClassesCol)
    # River and Lakeshore Gravel and Rock -> BARE_GROUND
    outClassesCol = np.where(lcdbCol==11,BARE_GROUND,outClassesCol)
    # Landslide -> BARE_GROUND
    outClassesCol = np.where(lcdbCol==12,BARE_GROUND,outClassesCol)
    # Alpine Gravel and Rock -> BARE_GROUND
    outClassesCol = np.where(lcdbCol==13,BARE_GROUND,outClassesCol)
    # Permanent Snow and Ice -> PERMINANT_SNOW_ICE
    outClassesCol = np.where(lcdbCol==14,PERMINANT_SNOW_ICE,outClassesCol)
    # Alpine Grass/Herbfield -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==15,OTHER_HERBACEOUS,outClassesCol)
    # Lake and Pond -> WATER
    outClassesCol = np.where(lcdbCol==20,WATER,outClassesCol)
    # River -> WATER
    outClassesCol = np.where(lcdbCol==21,WATER,outClassesCol)
    # Estuarine Open Water -> WATER
    outClassesCol = np.where(lcdbCol==22,WATER,outClassesCol)
    # Short-rotation Cropland -> HIGH_PRODUCING_EXOTIC_HERBACEOUS
    outClassesCol = np.where(lcdbCol==30,HIGH_PRODUCING_EXOTIC_HERBACEOUS,outClassesCol)
    # Cultivation -> BARE_GROUND
    outClassesCol = np.where(lcdbCol==31,BARE_GROUND,outClassesCol)
    # Orchard Vineyard & Other Perennial Crops -> HIGH_PRODUCING_EXOTIC_HERBACEOUS
    outClassesCol = np.where(lcdbCol==33,HIGH_PRODUCING_EXOTIC_HERBACEOUS,outClassesCol)
    # High Producing Exotic Grassland -> HIGH_PRODUCING_EXOTIC_HERBACEOUS
    outClassesCol = np.where(lcdbCol==40,HIGH_PRODUCING_EXOTIC_HERBACEOUS,outClassesCol)
    # Low Producing Grassland -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==41,OTHER_HERBACEOUS,outClassesCol)
    # Tall Tussock Grassland -> TALL_TUSSOCK_GRASSLAND
    outClassesCol = np.where(lcdbCol==43,TALL_TUSSOCK_GRASSLAND,outClassesCol)
    # Depleted Grassland -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==44,OTHER_HERBACEOUS,outClassesCol)
    # Herbaceous Freshwater Vegetation -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==45,OTHER_HERBACEOUS,outClassesCol)
    # Herbaceous Saline Vegetation -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==46,OTHER_HERBACEOUS,outClassesCol)
    # Flaxland -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==47,OTHER_HERBACEOUS,outClassesCol)
    # Fernland -> OTHER_HERBACEOUS
    outClassesCol = np.where(lcdbCol==50,OTHER_HERBACEOUS,outClassesCol)
    # Gorse and/or Broom -> SCRUB
    outClassesCol = np.where(lcdbCol==51,SCRUB,outClassesCol)
    # Manuka and/or Kanuka -> SCRUB
    outClassesCol = np.where(lcdbCol==52,SCRUB,outClassesCol)
    # Broadleaved Indigenous Hardwoods -> INDIGENOUS_FOREST
    outClassesCol = np.where(lcdbCol==54,INDIGENOUS_FOREST,outClassesCol)
    # Sub Alpine Shrubland -> SUB_ALPINE_SCRUBLAND
    outClassesCol = np.where(lcdbCol==55,SUB_ALPINE_SCRUBLAND,outClassesCol)
    # Mixed Exotic Shrubland -> SCRUB
    outClassesCol = np.where(lcdbCol==56,SCRUB,outClassesCol)
    # Matagouri or Grey Scrub -> SCRUB
    outClassesCol = np.where(lcdbCol==58,SCRUB,outClassesCol)
    # Forest - Harvested -> BARE_GROUND
    outClassesCol = np.where(lcdbCol==64,BARE_GROUND,outClassesCol)
    # Deciduous Hardwoods -> OTHER_WOODY
    outClassesCol = np.where(lcdbCol==68,OTHER_WOODY,outClassesCol)
    # Indigenous Forest -> INDIGENOUS_FOREST
    outClassesCol = np.where(lcdbCol==69,INDIGENOUS_FOREST,outClassesCol)
    # Mangroves -> OTHER_WOODY
    outClassesCol = np.where(lcdbCol==70,OTHER_WOODY,outClassesCol)
    # Exotic Forest -> EXOTIC_FOREST
    outClassesCol = np.where(lcdbCol==71,EXOTIC_FOREST,outClassesCol)
    
    rat.writeColumn(ratDataset, outputColName, outClassesCol)


# Command arguments
class CmdArgs:
  def __init__(self):
    p = optparse.OptionParser()
    p.add_option("-i","--input", dest="inputFile", default=None, help="Input file.")
    p.add_option("-c","--classes", dest="classesCol", default=None, help="The column with the LCDB classes.")
    p.add_option("-o","--output", dest="outputCol", default=None, help="The column where the collapsed classes will be written.")
    (options, args) = p.parse_args()
    self.__dict__.update(options.__dict__)

    if self.inputFile is None:
        p.print_help()
        print "Input filename must be set."
        sys.exit()


if __name__ == '__main__':
    cmdargs = CmdArgs()
    collapseClasses(cmdargs.inputFile, cmdargs.classesCol, cmdargs.outputCol)