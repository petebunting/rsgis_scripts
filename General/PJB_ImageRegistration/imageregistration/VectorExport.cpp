/*
 *  VectorExport.cpp
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/03/2006.
 *  Copyright 2006 __MyCompanyName__. All rights reserved.
 *
 */

#include "VectorExport.h"

VectorExport::VectorExport()
{	
}

void VectorExport::outputVector()
{
	OGRSpatialReference oSRS;
	
	oSRS.SetProjCS( "UTM 55 (WGS84) in southern hemisphere." );
	oSRS.SetWellKnownGeogCS( "WGS84" );
	oSRS.SetUTM( 55, FALSE );
	
	
	
	const char *pszDriverName = "ESRI Shapefile";
    OGRSFDriver *poDriver;
	
	OGRRegisterAll();
	
	poDriver = OGRSFDriverRegistrar::GetRegistrar()->GetDriverByName(pszDriverName);
    if( poDriver == NULL )
    {
		std::cout << pszDriverName << " driver not available.\n";
		exit( 1 );
    }
	
	OGRDataSource *poDS;
	
    poDS = poDriver->CreateDataSource( "/Users/pete/point_out.shp", NULL );
    if( poDS == NULL )
    {
		std::cout << "Creation of output file failed.\n";
        exit( 1 );
    }
	
	OGRLayer *poLayer;
	
    poLayer = poDS->CreateLayer( "point_out", &oSRS, wkbPolygon, NULL );
    if( poLayer == NULL )
    {
		std::cout << "Layer creation failed.\n";
        exit( 1 );
    }
	
	OGRFieldDefn oFieldFID( "FID", OFTInteger );
	
    oFieldFID.SetWidth(32);
	
    if( poLayer->CreateField( &oFieldFID ) != OGRERR_NONE )
    {
		std::cout << "Creating FID field failed.\n";
        exit( 1 );
    }
	
	OGRFeature *poFeature;
	
	poFeature = new OGRFeature( poLayer->GetLayerDefn() );
	poFeature->SetField( "FID", 0 );
	
	OGRPolygon *poPolygon = new OGRPolygon();
	
	//poPolygon->setX( 5 );
	//poPolygon->setY( 8 );
	
	poFeature->SetGeometryDirectly( poPolygon ); 
	
	if( poLayer->CreateFeature( poFeature ) != OGRERR_NONE )
	{
		std::cout << "Failed to create feature in shapefile.\n";
		exit( 1 );
	}
	
	delete poFeature;
	OGRDataSource::DestroyDataSource( poDS );
}

VectorExport::~VectorExport()
{
}
