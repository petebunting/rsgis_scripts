
import osgeo.gdal as gdal

outImg = "ModisImage.kea"
format = 'KEA'
sizeX = 2400
sizeY = 2400

driver = gdal.GetDriverByName( format )

metadata = driver.GetMetadata_Dict()    
if (gdal.DCAP_CREATE in metadata) and metadata[gdal.DCAP_CREATE] == 'YES':
	print('Driver ' + format + ' supports Create() method.')
else:
	print('Driver ' + format + ' not NOT support Create() method - choose another format.')

dst_ds = driver.Create( outImg, sizeX, sizeY, 7, gdal.GDT_Int16)


modisImage = "MODIS_MYD09A1/MYD09A1.A2014065.h17v03.005.2014083190707.hdf"
gdalImage = gdal.Open(modisImage)

metadata = gdalImage.GetMetadata_Dict()
#print(metadata)

gdalImageSubData = gdalImage.GetSubDatasets()

for subData in gdalImageSubData:
	#print(subData[0])
	if 'sur_refl_b01' in subData[0]:
		print('sur_refl_b01')
		dst_dsBand = dst_ds.GetRasterBand(1)
		data = gdal.Open(subData[0], gdal.GA_ReadOnly)
		dataBand = data.GetRasterBand(1)
		dst_dsBand.WriteArray(dataBand.ReadAsArray())
		#print(dataBand.ReadAsArray())
		data = None
	elif 'sur_refl_b02' in subData[0]:
		print('sur_refl_b02')
		dst_dsBand = dst_ds.GetRasterBand(2)
		data = gdal.Open(subData[0], gdal.GA_ReadOnly)
		dataBand = data.GetRasterBand(1)
		dst_dsBand.WriteArray(dataBand.ReadAsArray())
		data = None
	elif 'sur_refl_b03' in subData[0]:
		print('sur_refl_b03')
		dst_dsBand = dst_ds.GetRasterBand(3)
		data = gdal.Open(subData[0], gdal.GA_ReadOnly)
		dataBand = data.GetRasterBand(1)
		dst_dsBand.WriteArray(dataBand.ReadAsArray())
		data = None
	elif 'sur_refl_b04' in subData[0]:
		print('sur_refl_b04')
		dst_dsBand = dst_ds.GetRasterBand(4)
		data = gdal.Open(subData[0], gdal.GA_ReadOnly)
		dataBand = data.GetRasterBand(1)
		dst_dsBand.WriteArray(dataBand.ReadAsArray())
		data = None
	elif 'sur_refl_b05' in subData[0]:
		print('sur_refl_b05')
		dst_dsBand = dst_ds.GetRasterBand(5)
		data = gdal.Open(subData[0], gdal.GA_ReadOnly)
		dataBand = data.GetRasterBand(1)
		dst_dsBand.WriteArray(dataBand.ReadAsArray())
		data = None
	elif 'sur_refl_b06' in subData[0]:
		print('sur_refl_b06')
		dst_dsBand = dst_ds.GetRasterBand(6)
		data = gdal.Open(subData[0], gdal.GA_ReadOnly)
		dataBand = data.GetRasterBand(1)
		dst_dsBand.WriteArray(dataBand.ReadAsArray())
		data = None
	elif 'sur_refl_b07' in subData[0]:
		print('sur_refl_b07')
		dst_dsBand = dst_ds.GetRasterBand(7)
		data = gdal.Open(subData[0], gdal.GA_ReadOnly)
		dataBand = data.GetRasterBand(1)
		dst_dsBand.WriteArray(dataBand.ReadAsArray())
		data = None
	#else:
	#	print('Other')

