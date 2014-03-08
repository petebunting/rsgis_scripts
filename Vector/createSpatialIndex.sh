#!/bin/bash

# Create spatial index 

name=`basename $1 .shp`

ogrinfo $1 -sql "CREATE SPATIAL INDEX ON ${name}"
