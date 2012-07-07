#! /usr/bin/env python

import os

shpFilePath = "/Users/pete/Desktop/shps/"
shploadappend = '/usr/local/pgsql/bin/shp2pgsql -a'
shploadcreate = '/usr/local/pgsql/bin/shp2pgsql -cI'
schema = 'ccwschema.basicsegmentation'
pipe2psql = ' | /usr/local/pgsql/bin/psql -d ccwdb'

if not os.path.exists(shpFilePath):
    print 'Filepath does not exist'
else:
    print shpFilePath, ' is OK.'

if not os.path.isdir(shpFilePath):
    print 'Filepath is not a directory!'
else:
    print shpFilePath, ' is a directory.'
    
shpList = os.listdir(shpFilePath)
first = True

for i in range(len(shpList)):
    
    #print '0: ', os.path.splitext(shpList[i])[0], ' 1: ', os.path.splitext(shpList[i])[1]
    if os.path.splitext(shpList[i])[1] == '.shp':
        #print shpList[i]
        if first:
            command = shploadcreate + ' "' + shpFilePath + shpList[i] + '" ' + schema + pipe2psql
            first = False
        else:
            command = shploadappend + ' "' + shpFilePath + shpList[i] + '" ' + schema + pipe2psql
        
        #os.system(command)
        print command
        

    
